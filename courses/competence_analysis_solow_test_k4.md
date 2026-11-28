# Cognitive Task Analysis (CTA): Solow Test K4

- **Course ID:** `solow_test_k4`
- **Macro-Competency:** Dominio y aplicación analítica integral de Solow Test K4
- **Structure:** 19 total competencies (1 Facts, 11 Concepts, 7 Skills) with 82 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `H-01` | Hipótesis Neoclásicas de Ahorro y Trabajo Exógeno | Fact | Understand | Unidad 2: Hipótesis Dinámicas de Ahorro y Fuerza Laboral | - | 5 |
| `C-01` | Forma Per Cápita y Ecuación Fundamental | Concept | Analyze | Unidad 2: Forma Per Cápita y Ecuación Fundamental | H-01 | 3 |
| `C-02` | Análisis de Fase y Estabilidad Local Cóncava | Concept | Evaluate | Unidad 3: Análisis de Fase y Estabilidad del Equilibrio | C-01 | 3 |
| `C-03` | Estado Uniforme y Progreso Tecnológico | Concept | Evaluate | Unidad 4: Estado Uniforme y Progreso Tecnológico | C-02 | 3 |
| `Hab-01` | Linealización de Bernoulli Per Cápita (Cobb-Douglas) | Skill | Evaluate | Unidad 4: Solución Cuantitativa Cobb-Douglas vía Bernoulli | C-01, C-02 | 6 |
| `Hab-02` | Ecuación Fundamental de Solow | Skill | Evaluate | Unidad 6: Ecuación Fundamental de Solow | H-01 | 6 |
| `C-04` | Multiplicidad de Equilibrios y Umbral Inestable en Fase | Concept | Evaluate | Unidad 7: Estabilidad y Multiplicidad en Diagrama de Fase | Hab-02 | 3 |
| `C-05` | Regímenes de Proporciones Fijas Harrod-Domar | Concept | Analyze | Unidad 10: Regímenes de Proporciones Fijas Harrod-Domar | Hab-02 | 3 |
| `Hab-03` | Integración Directa de Trayectoria Agregada K(t) | Skill | Evaluate | Unidad 13: Solución Explícita en Cobb-Douglas | Hab-02, C-04 | 6 |
| `C-06` | Ajuste Endógeno del Coeficiente Capital-Producto | Concept | Evaluate | Unidad 14: Ajuste Endógeno del Coeficiente Capital-Producto | Hab-03 | 3 |
| `Hab-04` | Equilibrio y Umbral en Función Radical | Skill | Evaluate | Unidad 14: Equilibrio y Umbral en Función Radical | Hab-02, C-04 | 6 |
| `C-07` | Precios Factoriales, Productividad Marginal y Arbitraje | Concept | Analyze | Unidad 16: Precios Competitivos y Productividad Marginal | H-01, C-04 | 5 |
| `Hab-05` | Participación Factorial y Salario Real | Skill | Evaluate | Unidad 21: Participación Factorial y Salario Real | C-07 | 6 |
| `Hab-06` | Crecimiento con Cambio Tecnológico Neutral | Skill | Evaluate | Unidad 22: Crecimiento con Cambio Tecnológico Neutral | C-07 | 6 |
| `C-09` | Oferta Laboral Elástica al Salario | Concept | Evaluate | Unidad 24: Oferta Laboral Elástica al Salario | C-07 | 3 |
| `C-10` | Tasa de Ahorro Variable Endógena | Concept | Analyze | Unidad 25: Tasa de Ahorro Variable Endógena | C-07 | 3 |
| `Hab-07` | Tasa de Ahorro Efectiva con Impuestos | Skill | Evaluate | Unidad 26: Tasa de Ahorro Efectiva con Impuestos | C-10 | 6 |
| `C-11` | Crecimiento Poblacional Endógeno y Trampas | Concept | Evaluate | Unidad 27: Crecimiento Poblacional Endógeno y Trampas | C-07 | 3 |
| `C-12` | Rigidez Salarial y Preferencia por Liquidez | Concept | Evaluate | Unidad 29: Rigidez Salarial y Preferencia por Liquidez | C-07 | 3 |

---

## Detailed Competency Specifications

### [H-01] Hipótesis Neoclásicas de Ahorro y Trabajo Exógeno (Fact)

- **Bloom Level:** Understand
- **Session:** Unidad 2: Hipótesis Dinámicas de Ahorro y Fuerza Laboral
- **Prerequisites:** None
- **Recommended Modalities:** fill_in_the_blank, multiple_select, concept_matching
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2), `solow1956.pdf` (page 3)

#### Description & Cognitive Model
En el modelo neoclásico de Solow, el capital y el trabajo se combinan con rendimientos constantes a escala y proporciones variables, acumulación $\dot{K}=sY$ y oferta laboral exógena exponencial $\dot{L}/L=n$ bajo pleno empleo.

#### Fused Distractor Models (5)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Proporción fija Domar | conceptual_swap | high | $Q=\rho K$ sin insumo laboral | Distinga el modelo de Domar de proporciones fijas del marco de Solow donde capital y trabajo varían libremente. |
| `D-H01-04` | Ahorro sobre capital | conceptual_swap | high | $\dot{K}=sK$ | Aplique la propensión al ahorro $s$ sobre el flujo de producto neto $Y$, nunca sobre el stock de capital $K$. |
| `D-H01-05` | Crecimiento lineal laboral | conceptual_swap | high | $L(t)=L_0(1+nt)$ | Modele el crecimiento continuo a tasa proporcional constante $n$ mediante la función exponencial $L_0 e^{nt}$. |
| `D-H01-03` | Trabajo constante | conceptual_swap | high | $\dot{L}=\lambda$ en nivel | Recuerde que $\lambda>0$ representa la tasa proporcional de crecimiento $\dot{L}/L$, generando crecimiento exponencial laboral. |
| `D-H01-06` | Rendimientos decrecientes globales | conceptual_swap | high | $F(\lambda K,\lambda L)<\lambda Y$ | Recuerde que la ausencia de un factor fijo como la tierra implica homogeneidad de grado uno en capital y trabajo. |

---

### [C-01] Forma Per Cápita y Ecuación Fundamental (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 2: Forma Per Cápita y Ecuación Fundamental
- **Prerequisites:** H-01
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
La homogeneidad lineal $Q=f(K,L)=L\phi(k)$ con $k=K/L$, $\phi'(k)>0$ y $\phi''(k)<0$ permite condensar la dinámica en $\dot{k}=s\phi(k)-\lambda k$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Omite término de dilución | conceptual_swap | high | $\dot{k}=s\phi(k)$ | Al diferenciar $k=K/L$ por regla del producto aparece el término de dilución $-\lambda k$ debido al crecimiento laboral. |
| `D-C01-02` | Concavidad invertida | conceptual_swap | high | $\phi''(k)>0$ | Verifique que $f_{KK}<0$ implica $\phi''(k)=Lf_{KK}<0$, por lo que $\phi(k)$ crece a tasa decreciente. |
| `D-C01-03` | Signo positivo en dilución | conceptual_swap | high | $\dot{k}=s\phi(k)+\lambda k$ | Al sustituir $\dot{K}=L\dot{k}+\lambda kL$ en $\dot{K}=sL\phi(k)$, reste $\lambda k$ al despejar $\dot{k}$ en equilibrio dinámico. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Función de producción linealmente homogénea $Q=f(K,L)$ con $K,L>0$ | Sin rendimientos constantes a escala no existe reducción a $\phi(k)$. | - |
| `A-C01-02` | - | Productividades marginales positivas $f_K,f_L>0$ y decrecientes $f_{KK},f_{LL}<0$ | Sin concavidad estricta $\phi''(k)<0$ no se garantiza unicidad ni estabilidad. | - |

---

### [C-02] Análisis de Fase y Estabilidad Local Cóncava (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Análisis de Fase y Estabilidad del Equilibrio
- **Prerequisites:** C-01
- **Recommended Modalities:** open_symbolic, adversarial_break, multiple_select
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
En el diagrama de fase de $\dot{k}=s\phi(k)-\lambda k$, la intersección $\bar{k}$ entre la curva cóncava $s\phi(k)$ y el rayo $\lambda k$ define un equilibrio estable si $\frac{d\dot{k}}{dk}\big|_{\bar{k}}<0$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Equilibrio con pendiente positiva | conceptual_swap | high | $\frac{d\dot{k}}{dk}\big|_{\bar{k}}>0$ implica estabilidad | Una línea de fase con pendiente positiva en $\bar{k}$ aleja cualquier $k(0)\ne\bar{k}$; la estabilidad exige pendiente negativa. |
| `D-C02-02` | Ordenada no nula en origen | conceptual_swap | high | $s\phi(0)>0$ en la gráfica | Como el capital $K$ es un insumo indispensable, si $k=0$ entonces $Q=0$ y la curva $s\phi(k)$ parte del origen. |
| `D-C02-03` | Confunde ejes de fase | conceptual_swap | high | Grafica $k$ vertical contra $\dot{k}$ horizontal | Ubique $\dot{k}$ en el eje vertical y $k$ en el eje horizontal para leer el signo de $\dot{k}$ como distancia vertical. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | El capital es indispensable ($k=0 \Rightarrow \phi(0)=0$) y existe $k>0$ con $s\phi(k)>\lambda k$ | Sin intersección positiva $\bar{k}$ no habría equilibrio intertemporal interior. | - |

---

### [C-03] Estado Uniforme y Progreso Tecnológico (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Estado Uniforme y Progreso Tecnológico
- **Prerequisites:** C-02
- **Recommended Modalities:** unstructured_model, adversarial_break, multiple_select
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
En el equilibrio $\bar{k}$ se alcanza un estado uniforme donde $K$, $L$, $\dot{K}$ y $Q$ crecen todos a tasa $\lambda$; si la tecnología $T(t)$ crece ($dT/dt>0$), $s\phi(k)$ se desplaza hacia arriba elevando $\bar{k}$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Confunde estado uniforme y estacionario | conceptual_swap | high | En $\bar{k}$ todas las variables tienen tasa cero | Distinga estado estacionario de estado uniforme: en $\bar{k}$ la razón $k$ es constante, pero $K,L,\dot{K},Q$ crecen a tasa $\lambda$. |
| `D-C03-02` | Desplazamiento descendente por tecnología | conceptual_swap | high | $dT/dt>0$ reduce el capital $\bar{k}$ | Un incremento de $T(t)$ en $Q=T(t)f(K,L)$ eleva el producto por trabajador y desplaza $s\phi(k)$ hacia arriba, aumentando $\bar{k}$. |
| `D-C03-03` | Inversión crece distinto a capital | conceptual_swap | high | $\dot{K}$ crece a tasa $s\lambda$ en estado uniforme | Si $K=Ae^{\lambda t}$, su derivada $\dot{K}=\lambda Ae^{\lambda t}$ crece exactamente a la misma tasa exponencial $\lambda$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | Tecnología exógena multiplicativa $Q=T(t)f(K,L)$ con $dT/dt>0$ | Sin progreso tecnológico, el producto per cápita converge a un nivel fijo. | - |

---

### [Hab-01] Linealización de Bernoulli Per Cápita (Cobb-Douglas) (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Solución Cuantitativa Cobb-Douglas vía Bernoulli
- **Prerequisites:** C-01, C-02
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
Con producción Cobb-Douglas $Q=K^\alpha L^{1-\alpha}$ ($\phi(k)=k^\alpha$), la ecuación de Bernoulli $\dot{k}+\lambda k=sk^\alpha$ se linealiza con $z=k^{1-\alpha}$ para obtener $k^{1-\alpha}(t)$ y el límite $k^*=(s/\lambda)^{\frac{1}{1-\alpha}}$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Sustitución de Bernoulli incorrecta | skipped_step | high | $z=k^{\alpha}$ en lugar de $z=k^{1-\alpha}$ | Para una ecuación de Bernoulli $\dot{k}+\lambda k=sk^\alpha$, sustituya $z=k^{1-\alpha}$ de modo que $\dot{z}=(1-\alpha)k^{-\alpha}\dot{k}$. |
| `D-Hab01-02` | Omite factor 1-alpha en ODE lineal | skipped_step | high | $\frac{dz}{dt}+\lambda z=s$ | Al aplicar la regla de la cadena en $z=k^{1-\alpha}$, multiplique toda la ecuación por $(1-\alpha)$ antes de integrar. |
| `D-Hab01-03` | Exponente sin invertir en límite | conceptual_swap | high | $k^*=\left(\frac{s}{\lambda}\right)^{1-\alpha}$ | Como $k^{1-\alpha}\to s/\lambda$ cuando $t\to\infty$, eleve ambos lados al recíproco $1/(1-\alpha)$ para despejar $k^*$. |
| `D-Hab01-04` | Invierte razón s y lambda | conceptual_swap | high | $k^*=\left(\frac{\lambda}{s}\right)^{\frac{1}{1-\alpha}}$ | Verifique que el término constante de la ODE lineal es $b/a=(1-\alpha)s/((1-\alpha)\lambda)=s/\lambda$, directo en $s$ e inverso en $\lambda$. |
| `D-Hab01-05` | Signo positivo en exponencial | conceptual_swap | high | $e^{+(1-\alpha)\lambda t}$ | El factor integrante de $\dot{z}+az=b$ produce $e^{-at}=e^{-(1-\alpha)\lambda t}$, garantizando convergencia cuando $t\to\infty$. |
| `D-Hab01-06` | Omite condición inicial en z | conceptual_swap | high | $k(t)=k(0)e^{-(1-\alpha)\lambda t}+\frac{s}{\lambda}$ | Evalue la condición inicial en la variable transformada $z(0)=k(0)^{1-\alpha}$ antes de revertir el cambio de variable. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Participación del capital $\alpha\in(0,1)$ y crecimiento laboral $\lambda>0$ | Si $\alpha\ge 1$ o $\lambda\le 0$, el término exponencial no converge a cero. | - |

---

### [Hab-02] Ecuación Fundamental de Solow (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 6: Ecuación Fundamental de Solow
- **Prerequisites:** H-01
- **Recommended Modalities:** proof_dag, open_symbolic, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 6)

#### Description & Cognitive Model
Derivación de la ecuación diferencial $\dot{r}=sF(r,1)-nr$ para la razón capital-trabajo $r=K/L$ aplicando homogeneidad de grado uno de $F(K,L)$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Omite dilución laboral | skipped_step | high | $\dot{r}=sF(r,1)$ | Reste la tasa de crecimiento laboral $n$ multiplicada por $r$ al diferenciar el cociente $r=K/L$ respecto al tiempo. |
| `D-Hab02-02` | Signo invertido en dilución | skipped_step | high | $\dot{r}=sF(r,1)+nr$ | Verifique que el crecimiento de la fuerza laboral $L$ en el denominador reduce la razón $r=K/L$ con signo negativo. |
| `D-Hab02-03` | Falta factor r al despejar | conceptual_swap | high | $\dot{r}=sF(r,1)-n$ | Multiplique ambos lados de $\dot{r}/r=\dot{K}/K-\dot{L}/L$ por $r$ para obtener el término completo $-nr$. |
| `D-Hab02-04` | No divide F por L | conceptual_swap | high | $\dot{r}=sF(K,L)-nr$ | Factorice $L$ fuera de $F(K,L)$ usando rendimientos constantes a escala para expresar el producto por trabajador $F(r,1)$. |
| `D-Hab02-05` | Confunde razón con tasa | conceptual_swap | high | $\dot{r}/r=sF(r,1)-nr$ | Distinga entre la derivada absoluta $\dot{r}$ y la tasa proporcional $\dot{r}/r$ al despejar la ecuación diferencial. |
| `D-Hab02-06` | Omite ahorro s | conceptual_swap | high | $\dot{r}=F(r,1)-nr$ | Conserve la fracción ahorrada $s$ del producto por trabajador $F(r,1)$, pues solo la parte no consumida acumula capital. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Homogeneidad de primer grado $F(K,L)=L F(K/L,1)$ | Sin rendimientos constantes a escala $\dot{r}$ dependería de $L(t)$ y no sería autónoma. | - |
| `A-Hab02-02` | - | Pleno empleo continuo de capital $K$ y trabajo $L=L_0 e^{nt}$ | Si existe desempleo persistente, $\dot{L}/L$ deja de coincidir con la tasa natural $n$. | - |

---

### [C-04] Multiplicidad de Equilibrios y Umbral Inestable en Fase (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 7: Estabilidad y Multiplicidad en Diagrama de Fase
- **Prerequisites:** Hab-02
- **Recommended Modalities:** adversarial_break, unstructured_model, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 7)

#### Description & Cognitive Model
Análisis cualitativo de $\dot{r}=sF(r,1)-nr$: equilibrio único estable, equilibrios múltiples con umbral inestable o ausencia total de equilibrio.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Cruce inverso estable | conceptual_swap | high | $sF'(r^*,1)>n \Rightarrow r^*$ estable | Evalúe el signo de $\dot{r}$ a ambos lados: la estabilidad exige que $sF(r,1)$ corte a $nr$ desde arriba hacia abajo. |
| `D-C04-02` | Convergencia siempre garantizada | conceptual_swap | high | $\forall F,\ \exists r^*>0$ estable | Recuerde que si $sF(r,1)$ permanece siempre por encima o por debajo de $nr$, no existe equilibrio de crecimiento balanceado. |
| `D-C04-03` | Origen siempre equilibrio | conceptual_swap | high | $F(0,1)>0 \Rightarrow r=0$ es equilibrio | Verifique si la producción es posible sin capital: cuando $F(0,1)>0$, $\dot{r}>0$ en el origen y $r=0$ no es equilibrio. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | Función $F(r,1)$ no decreciente y continua en $r\ge 0$ | Discontinuidades o pendientes negativas impedirían aplicar el análisis estándar de cruces con el rayo $nr$. | - |

---

### [C-05] Regímenes de Proporciones Fijas Harrod-Domar (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 10: Regímenes de Proporciones Fijas Harrod-Domar
- **Prerequisites:** Hab-02
- **Recommended Modalities:** adversarial_break, unstructured_model, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 10)

#### Description & Cognitive Model
Dinámica con $Y=\min(K/a,L/b)$ y $\dot{r}=s\min(r/a,1/b)-nr$, comparando la tasa natural $n$ frente a la tasa garantizada $s/a$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Ajuste suave con Leontief | conceptual_swap | high | $n \ne s/a \Rightarrow r \to a/b$ estable | Distinga las proporciones fijas de las neoclásicas: si $n>s/a$ crece el desempleo, y si $n<s/a$ crece el exceso de capital. |
| `D-C05-02` | Invierte tasa garantizada | conceptual_swap | high | Tasa garantizada $=a/s$ | Divida la propensión al ahorro $s$ entre el coeficiente de aceleración capital-producto $a$ para obtener la tasa garantizada $s/a$. |
| `D-C05-03` | Uso pleno con exceso de capital | conceptual_swap | high | $n_3 < s/a \Rightarrow$ empleo de capital $=1$ | Calcule la fracción efectivamente empleada del capital en equilibrio cuando $n_3<s/a$, dada por la razón $an_3/s<1$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Coeficientes técnicos fijos $a>0$ y $b>0$ sin sustitución factorial | Si se permite sustitución continua entre $K$ y $L$, desaparecen la rigidez y el filo de navaja. | - |

---

### [Hab-03] Integración Directa de Trayectoria Agregada K(t) (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 13: Solución Explícita en Cobb-Douglas
- **Prerequisites:** Hab-02, C-04
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 13)

#### Description & Cognitive Model
Integración directa de $\dot{K}=sK^a(L_0 e^{nt})^{1-a}$ con $b=1-a$ para hallar la trayectoria $K(t)$ y el equilibrio estacionario $r^*=(s/n)^{1/(1-a)}$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Exponente sin invertir | skipped_step | high | $r^*=(s/n)^{1-a}$ | Al despejar $r^{1-a}=s/n$, eleve ambos miembros al recíproco $1/(1-a)$ del exponente original. |
| `D-Hab03-02` | Invierte razón s/n | skipped_step | high | $r^*=(n/s)^{1/(1-a)}$ | Verifique que mayor ahorro $s$ y menor crecimiento laboral $n$ elevan la razón capital-trabajo de equilibrio $r^*$. |
| `D-Hab03-03` | Omite término inicial en K(t) | conceptual_swap | high | $K(t)=\left[\frac{s}{n}L_0^b e^{nbt}\right]^{1/b}$ | Incluya la constante de integración evaluada en el instante inicial para satisfacer la condición de borde $K(0)=K_0$. |
| `D-Hab03-04` | Olvida exponente b en L0 | conceptual_swap | high | $K(t)=\left[K_0^b-\frac{s}{n}L_0+\frac{s}{n}L_0 e^{nbt}\right]^{1/b}$ | Conserve el exponente $b=1-a$ sobre $L_0$ proveniente de $(L_0 e^{nt})^{1-a}$ antes de integrar la ecuación lineal en $K^b$. |
| `D-Hab03-05` | Falta factor 1/n al integrar | conceptual_swap | high | $K(t)=\left[K_0^b-sL_0^b+sL_0^b e^{nbt}\right]^{1/b}$ | Recuerde dividir por $nb$ al integrar $e^{nbt}$ y luego cancelar el factor $b$ proveniente de la derivada de $K^b$. |
| `D-Hab03-06` | Potencia errónea en r* | conceptual_swap | high | $r^*=(s/n)^a$ | Iguale $sr^a=nr$ y reste exponentes para obtener $r^{1-a}=s/n$ antes de elevar a la potencia $1/(1-a)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | Elasticidad del producto respecto al capital $a\in(0,1)$ | Si $a\ge 1$, los rendimientos marginales del capital no decrecen y desaparece la convergencia a $r^*$ finito. | - |

---

### [C-06] Ajuste Endógeno del Coeficiente Capital-Producto (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 14: Ajuste Endógeno del Coeficiente Capital-Producto
- **Prerequisites:** Hab-03
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 14)

#### Description & Cognitive Model
Convergencia asintótica en Cobb-Douglas hacia $Y/L=(s/n)^{a/(1-a)}$ y $C=K/Y=s/n$, mostrando que $n=s/C$ emerge por ajuste de oferta y demanda.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Coeficiente C exógeno | conceptual_swap | high | $C=K/Y$ es parámetro fijo | Observe que bajo sustitución factorial $C=K/Y=r^{1-a}$ varía con $r$ hasta igualar endógenamente $s/n$ en equilibrio. |
| `D-C06-02` | Exponente incorrecto en Y/L | conceptual_swap | high | $\lim_{t\to\infty} Y/L=(s/n)^{1/(1-a)}$ | Sustituya el equilibrio $r^*=(s/n)^{1/(1-a)}$ dentro de $Y/L=r^a$ para obtener el exponente correcto $a/(1-a)$. |
| `D-C06-03` | Invierte relación n=s/C | conceptual_swap | high | $n=C/s$ | Despeje la tasa natural $n$ de $C=s/n$ para verificar que iguala la tasa garantizada $s/C$ de Harrod-Domar. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Tasa de ahorro $s>0$ y tasa natural $n>0$ constantes | Si $n=0$ o $s=0$, el cociente $s/n$ queda indefinido o colapsa a cero. | - |

---

### [Hab-04] Equilibrio y Umbral en Función Radical (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 14: Equilibrio y Umbral en Función Radical
- **Prerequisites:** Hab-02, C-04
- **Recommended Modalities:** open_symbolic, adversarial_break, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 14)

#### Description & Cognitive Model
Resolución de $\dot{r}=s(a\sqrt{r}+1)^2-nr$ para $Y=(a\sqrt{K}+\sqrt{L})^2$: régimen explosivo si $sa^2>n$ y equilibrio $r^*=\left(\frac{1}{\sqrt{n/s}-a}\right)^2$ si $sa^2<n$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Condición de equilibrio invertida | skipped_step | high | $sa^2>n \Rightarrow \exists r^*>0$ estable | Compare las pendientes asintóticas: si $sa^2>n$, la curva $sF(r,1)$ crece más rápido que $nr$ y $r$ diverge sin límite. |
| `D-Hab04-02` | Olvida elevar al cuadrado r* | skipped_step | high | $r^*=\frac{1}{\sqrt{n/s}-a}$ | Eleve al cuadrado la expresión despejada para $\sqrt{r^*}$ al resolver $\sqrt{s}(a\sqrt{r}+1)=\sqrt{n}\sqrt{r}$. |
| `D-Hab04-03` | Signo positivo en denominador | conceptual_swap | high | $r^*=\left(\frac{1}{\sqrt{n/s}+a}\right)^2$ | Agrupe correctamente los términos con $\sqrt{r^*}$ al pasar $a\sqrt{s}\sqrt{r^*}$ restando al miembro de $\sqrt{n}\sqrt{r^*}$. |
| `D-Hab04-04` | Omite raíz en n/s | conceptual_swap | high | $r^*=\left(\frac{1}{n/s-a}\right)^2$ | Tome raíz cuadrada en ambos lados de $s(a\sqrt{r}+1)^2=nr$ antes de despejar $\sqrt{r^*}$. |
| `D-Hab04-05` | Confunde r* con ingreso límite | conceptual_swap | high | $\lim Y/L=\left(\frac{1}{\sqrt{n/s}-a}\right)^2$ | Evalúe $(a\sqrt{r^*}+1)^2$ en el equilibrio para hallar el ingreso límite $1/(1-a\sqrt{s/n})^2$. |
| `D-Hab04-06` | Origen es equilibrio con p=1/2 | conceptual_swap | high | $r=0 \Rightarrow \dot{r}=0$ | Note que con $Y=(a\sqrt{K}+\sqrt{L})^2$ el producto sin capital es positivo y $sF(0,1)=s>0$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Parámetro $p\in(0,1)$ en la familia $(aK^p+L^p)^{1/p}$ | Si $p\ge 1$, las isocuantas pierden convexidad estricta o son lineales, invalidando la productividad marginal decreciente. | - |

---

### [C-07] Precios Factoriales, Productividad Marginal y Arbitraje (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 16: Precios Competitivos y Productividad Marginal
- **Prerequisites:** H-01, C-04
- **Recommended Modalities:** unstructured_model, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 16)

#### Description & Cognitive Model
Determinación competitiva del salario real $\frac{\partial F}{\partial L}=\frac{w}{p}$ y la renta real del capital $\frac{\partial F}{\partial K}=\frac{q}{p}$ como funciones exclusivas de $r$, junto con la condición de arbitraje $i(t)=q/p+\dot{p}/p$.

#### Fused Distractor Models (5)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Dependencia de escala absoluta | conceptual_swap | high | $\frac{\partial F}{\partial K}$ depende de $K$ y $L$ por separado | Aplique el teorema de Euler para funciones homogéneas de grado uno: las derivadas parciales son homogéneas de grado cero y solo dependen de $r=K/L$. |
| `D-C07-04` | Iguala i con q/p | conceptual_swap | high | $i(t)=\frac{q(t)}{p(t)}$ siempre | Incluya la ganancia o pérdida de capital $\dot{p}/p$ en la condición de arbitraje cuando el nivel de precios varía. |
| `D-C07-02` | Iguala productividad a precio nominal | conceptual_swap | high | $\frac{\partial F}{\partial L}=w$ | Deflacte las remuneraciones nominales $w$ y $q$ por el nivel de precios $p(t)$ para igualarlas a las productividades marginales físicas. |
| `D-C07-05` | Signo invertido en p | conceptual_swap | high | $i(t)=\frac{q(t)}{p(t)}-\frac{\dot{p}(t)}{p(t)}$ | Sume la tasa de inflación $\dot{p}/p$ al rendimiento propio $q/p$: si el precio cae, $q/p$ debe superar a $i(t)$. |
| `D-C07-03` | Determinación del nivel de precios | conceptual_swap | high | El sistema real determina $p(t)$ | Recuerde que en un sistema puramente real solo se determinan precios relativos reales $w/p$ y $q/p$, tomando $p(t)$ como dado. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Competencia pura y ajuste instantáneo de $w/p$ y $q/p$ | Con rigideces nominales o competencia monopolística falla la igualación directa a la productividad marginal agregada. | - |
| `A-C07-02` | - | Competencia perfecta y rendimientos constantes a escala en $F(K,L)$ | Sin competencia ni homogeneidad de grado uno, los productos marginales no determinan $w/p$ y $q/p$ en función única de $r$. | - |
| `A-C07-03` | - | Previsión perfecta, ausencia de riesgo y arbitraje sin fricciones entre capital y bonos | Con incertidumbre o preferencia por liquidez, $i(t)$ y $q/p+\dot{p}/p$ divergen. | - |

---

### [Hab-05] Participación Factorial y Salario Real (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 21: Participación Factorial y Salario Real
- **Prerequisites:** C-07
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 21)

#### Description & Cognitive Model
Cálculo de $w/p$, $q/p$ y participación laboral $(w/p)(L/Y)$ en Cobb-Douglas, $Y=(a\sqrt{K}+\sqrt{L})^2$ y proporciones fijas

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Participación constante general | skipped_step | high | $\frac{wL}{pY}$ siempre independiente de $s,n$ | Verifique si la función de producción es Cobb-Douglas; en $Y=(a\sqrt{K}+\sqrt{L})^2$, la participación laboral depende de $s$ y $n$. |
| `D-Hab05-02` | Invierte razón en Y | skipped_step | high | $\frac{\partial Y}{\partial L}=a\sqrt{\frac{L}{K}}+1$ | Derive $(a\sqrt{K}+\sqrt{L})^2$ respecto a $L$ aplicando la regla de la cadena para obtener $a\sqrt{K/L}+1=a\sqrt{r}+1$. |
| `D-Hab05-03` | Exponente erróneo en w/p | conceptual_swap | high | $w/p=(1-a)(s/n)^{1/(1-a)}$ | Sustituya $r^*=(s/n)^{1/(1-a)}$ dentro de $w/p=(1-a)r^a$ para obtener el exponente correcto $a/(1-a)$. |
| `D-Hab05-04` | Renta positiva si sobra K | conceptual_swap | high | $q>0$ cuando $r>a/b$ en Leontief | Recuerde que con proporciones fijas, si $r>a/b$ el capital es redundante, su producto marginal es nulo y $q=0$. |
| `D-Hab05-05` | Asigna exceso al trabajo | conceptual_swap | high | $w/p=p/b$ cuando $r<a/b$ | Distinga el factor abundante del escaso: si $r<a/b$ sobra trabajo, por lo que $w=0$ y todo el producto va al capital ($q=p/a$). |
| `D-Hab05-06` | Signo erróneo en participación | conceptual_swap | high | $\frac{wL}{pY}=1+a\sqrt{s/n}$ | Multiplique $w/p=(1-a\sqrt{s/n})^{-1}$ por $L/Y=(1-a\sqrt{s/n})^2$ para obtener $1-a\sqrt{s/n}<1$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | Existencia de equilibrio balanceado con $\sqrt{n/s}>a$ en $Y=(a\sqrt{K}+\sqrt{L})^2$ | Si $\sqrt{n/s}\le a$, no existe razón capital-trabajo estacionaria finita. | - |

---

### [Hab-06] Crecimiento con Cambio Tecnológico Neutral (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 22: Crecimiento con Cambio Tecnológico Neutral
- **Prerequisites:** C-07
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 22)

#### Description & Cognitive Model
Tasas asintóticas de $K$, $Y$, $K/L$ y $K/Y$ bajo cambio tecnológico neutral $Y=e^{gt}K^aL^{1-a}$ con $b=1-a$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Ignora efecto compuesto | skipped_step | high | $\frac{\dot{Y}}{Y}\to n+g$ | Considere que mayor producto eleva el ahorro y la acumulación de capital, llevando la tasa de $Y$ a $n+ag/b$. |
| `D-Hab06-02` | Capital iguala a producto | skipped_step | high | $\frac{\dot{K}}{K}\to n+g$ | Divida la tasa tecnológica $g$ por $b=1-a$ al integrar $\dot{K}$: el capital crece asintóticamente a tasa $n+g/b$. |
| `D-Hab06-03` | Razón K/L estacionaria | conceptual_swap | high | $\frac{\dot{r}}{r}\to 0$ asintóticamente | Reste la tasa laboral $n$ de la tasa del capital $n+g/b$: la razón capital-trabajo $r=K/L$ crece sin límite a tasa $g/b$. |
| `D-Hab06-04` | Razón K/Y constante | conceptual_swap | high | $\frac{K}{Y}$ tiende a constante | Reste la tasa de $Y$ ($n+ag/b$) de la tasa de $K$ ($n+g/b$) para verificar que el coeficiente de capital $K/Y$ crece a tasa $g$. |
| `D-Hab06-05` | Participación laboral crece | conceptual_swap | high | $\frac{wL}{pY}$ aumenta con $t$ | Distinga el salario real $w/p$ (que sí crece indefinidamente) de la participación laboral en Cobb-Douglas (constante en $1-a$). |
| `D-Hab06-06` | Invierte a y b | conceptual_swap | high | $\frac{\dot{Y}}{Y}\to n+\frac{bg}{a}$ | Pondere la tasa de crecimiento del capital ($n+g/b$) por su elasticidad $a$ y sume $g+b n$ para obtener $n+ag/b$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Progreso tecnológico exógeno neutral de Hicks $A(t)=e^{gt}$ multiplicando $F(K,L)$ con $a\in(0,1)$ | Si $a\ge 1$ o $A(t)$ no es exponencial, las tasas asintóticas lineales dejan de cumplirse. | - |

---

### [C-09] Oferta Laboral Elástica al Salario (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 24: Oferta Laboral Elástica al Salario
- **Prerequisites:** C-07
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 24)

#### Description & Cognitive Model
Efecto de la oferta laboral $L=L_0e^{nt}(w/p)^h$ y la forma general $L=G(t,w/p)$ sobre la ecuación dinámica de $r$ y su equilibrio

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Cambia r* siempre | conceptual_swap | high | La elasticidad $h>0$ altera $r^*$ en (14) | Observe que en $\dot{r}=(sF(r,1)-nr)(1+ah/r)^{-1}$ el término $(1+ah/r)^{-1}>0$ no cambia el cero de $\dot{r}=0$. |
| `D-C09-02` | Omite término salarial | conceptual_swap | high | $\dot{r}=sF(r,1)-nr$ con $h>0$ | Incluya la respuesta de la oferta laboral al crecimiento salarial $-h(\dot{w}/w)$ al diferenciar $r=K/L$ respecto al tiempo. |
| `D-C09-03` | Conserva nr general | conceptual_swap | high | $sF(r,1)=nr$ para todo $G(t,w/p)$ | Sustituya $n$ por $\frac{1}{G}\frac{\partial G}{\partial t}$ en la condición estacionaria general; $r^*$ solo coincide si esa razón vale $n$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | Nivel de precios constante $p$ y elasticidad salarial finita $h>0$ por debajo del límite físico laboral | A salarios muy altos la oferta laboral enfrenta un techo demográfico y la elasticidad constante deja de ser válida. | - |

---

### [C-10] Tasa de Ahorro Variable Endógena (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 25: Tasa de Ahorro Variable Endógena
- **Prerequisites:** C-07
- **Recommended Modalities:** unstructured_model, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 25)

#### Description & Cognitive Model
Dinámica $\dot{r}=s(r)F(r,1)-nr$ cuando la tasa de ahorro responde positivamente al rendimiento del capital $q/p$ e inversamente a $r$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C10-01` | Relación directa con r | conceptual_swap | high | $s(r)$ es función creciente de $r$ | Relacione rendimiento y escasez: mayor $r$ reduce el producto marginal $q/p$, por lo que una respuesta positiva a $q/p$ hace decrecer $s(r)$. |
| `D-C10-02` | Permite estado estacionario | conceptual_swap | high | Si $s(r)=0$, cesa $n$ y hay estado estacionario total | Note que aunque $s(r)=0$ detenga la acumulación de capital, el crecimiento exógeno laboral $n>0$ sigue reduciendo $r$ posteriormente. |
| `D-C10-03` | Desestabiliza equilibrio | conceptual_swap | high | $s(r)$ decreciente genera escape $r\to\infty$ | Evalúe el efecto estabilizador: al subir $r$ cae $s(r)$ y frena el ahorro; si $s(r)$ se anula para $r$ grande, el último cruce con $nr$ es estable. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C10-01` | - | Tasa de ahorro $s(r)$ decreciente en $r$ con crecimiento poblacional exógeno $n>0$ | Si $s(r)$ fuese creciente en $r$, podrían amplificarse las desviaciones y perderse la estabilidad. | - |

---

### [Hab-07] Tasa de Ahorro Efectiva con Impuestos (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 26: Tasa de Ahorro Efectiva con Impuestos
- **Prerequisites:** C-10
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 26)

#### Description & Cognitive Model
Cálculo de la tasa de ahorro efectiva $s_{\mathrm{ef}}=s+(v-s)t$ bajo impuesto proporcional $t$ con fracción invertida $v$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Grava sin reducir privado | skipped_step | high | $s_{\mathrm{ef}}=s+vt$ | Aplique el ahorro privado $s$ sobre el ingreso disponible $(1-t)Y$ antes de sumar la inversión pública $vtY$. |
| `D-Hab07-02` | Siempre eleva ahorro | skipped_step | high | $s_{\mathrm{ef}}>s$ para cualquier $v>0$ | Compare la propensión a invertir estatal $v$ con la privada $s$: el ahorro efectivo sube solo si $v>s$ y cae si $v<s$. |
| `D-Hab07-03` | Consumo total sin efecto | conceptual_swap | high | Si $v=0$, $s_{\mathrm{ef}}=s$ | Sustituya $v=0$ en $s(1-t)+vt$: si todo el impuesto se consume, la tasa de ahorro efectiva cae a $s(1-t)$. |
| `D-Hab07-04` | Inversión total ignora s | conceptual_swap | high | Si $v=1$, $s_{\mathrm{ef}}=s+t$ | Simplifique $s(1-t)+t=s+t(1-s)$: parte de la recaudación sustituye ahorro privado que habría ocurrido sin impuesto. |
| `D-Hab07-05` | Cambia pendiente nr | conceptual_swap | high | El impuesto rota la recta $nr$ | Aplique el cambio de $s$ a $s_{\mathrm{ef}}$ sobre la curva $sF(r,1)$, dejando inalterada la recta de dilución laboral $nr$. |
| `D-Hab07-06` | Invierte signo v-s | conceptual_swap | high | $s_{\mathrm{ef}}=s+(s-v)t$ | Factorice $s(1-t)+vt=s+(v-s)t$ verificando que aumentar $v$ eleva la formación neta de capital. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Impuesto proporcional a la renta $t\in(0,1)$ con fracción constante $v\in[0,1]$ destinada a inversión | Impuestos no proporcionales distorsionan la forma de $sF(r,1)$ de manera no uniforme. | - |

---

### [C-11] Crecimiento Poblacional Endógeno y Trampas (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 27: Crecimiento Poblacional Endógeno y Trampas
- **Prerequisites:** C-07
- **Recommended Modalities:** unstructured_model, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 27)

#### Description & Cognitive Model
Equilibrios múltiples en $\dot{r}=sF(r,1)-n(r)r$ con $n(r)$ endógeno: trampa estable $r_1$ y umbral crítico inestable $r_2$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C11-01` | Requiere rendimientos crecientes | conceptual_swap | high | Las trampas exigen rendimientos crecientes | Note que la no linealidad de $n(r)r$ genera equilibrios múltiples y trampa en $r_1$ aun bajo rendimientos constantes a escala. |
| `D-C11-02` | r2 es equilibrio estable | conceptual_swap | high | Desde $r<r_2$ converge a $r_2$ | Analice el signo de $\dot{r}=sF(r,1)-n(r)r$: debajo de $r_2$ es negativo y cae hacia $r_1$; encima de $r_2$ es positivo y despega. |
| `D-C11-03` | Recta nr invariante | conceptual_swap | high | $n(r)r$ sigue siendo un rayo lineal | Distinga el caso $n$ constante del endógeno $n(r)$: al depender $n$ del ingreso per cápita $F(r,1)$, $n(r)r$ se curva. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C11-01` | - | Tasa de crecimiento poblacional $n(r)=\dot{L}/L$ dependiente del ingreso per cápita $F(r,1)$ o del salario real | Si la demografía es puramente exógena, la curva $n(r)r$ colapsa al rayo lineal $nr$. | - |

---

### [C-12] Rigidez Salarial y Preferencia por Liquidez (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 29: Rigidez Salarial y Preferencia por Liquidez
- **Prerequisites:** C-07
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 29)

#### Description & Cognitive Model
Desempleo por salario real rígido $\bar{w}/p$ con $\frac{\dot{L}}{L}=\frac{s}{\bar{r}}F(\bar{r},1)<n$ y subutilización de capital por liquidez $\bar{M}=Q(Y,q/p)$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C12-01` | Empleo crece a tasa n | conceptual_swap | high | Con $\bar{w}/p$ fijo, $\dot{L}/L=n$ | Distinga el crecimiento de la fuerza laboral $n$ de la tasa de absorción de empleo $(s/\bar{r})F(\bar{r},1)$ fijada por $\bar{r}$. |
| `D-C12-02` | Desempleo si pendiente mayor | conceptual_swap | high | $\frac{s}{\bar{r}}F(\bar{r},1)>n \Rightarrow$ desempleo | Compare la pendiente del rayo $(s/\bar{r})F(\bar{r},1)$ con $n$: si es menor que $n$ surge desempleo; si es mayor, escasez laboral. |
| `D-C12-03` | Neutralidad monetaria en trampa | conceptual_swap | high | El modelo real basta en trampa de liquidez | Reconozca que en la trampa de liquidez la tasa de interés rígida subutiliza capital y exige una dinámica monetaria explícita. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C12-01` | - | Rigidez a la baja del salario real $\bar{w}/p$ o demanda de saldos ociosos infinitamente elástica en trampa de liquidez | Con precios y salarios flexibles sin preferencia por liquidez, los mercados se vacían con pleno empleo. | - |

---
