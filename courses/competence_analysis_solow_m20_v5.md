# Cognitive Task Analysis (CTA): Solow M20 V5

- **Course ID:** `solow_m20_v5`
- **Macro-Competency:** Dominio y aplicación analítica integral de Solow M20 V5
- **Structure:** 19 total competencies (2 Facts, 9 Concepts, 8 Skills) with 85 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `H-01` | Hipótesis del Modelo de Solow | Fact | Understand | Unidad 2: Hipótesis del Modelo de Solow | - | 3 |
| `C-03` | Modelo Neoclásico de Acumulación | Concept | Evaluate | Unidad 3: Modelo Neoclásico de Acumulación | - | 3 |
| `Hab-01` | Ecuación Fundamental de Solow | Skill | Evaluate | Unidad 3: Ecuación Fundamental de Solow | H-01, C-03 | 10 |
| `C-01` | Línea de Fase y Estabilidad | Concept | Evaluate | Unidad 3: Línea de Fase y Estabilidad | Hab-01 | 3 |
| `C-02` | Progreso Tecnológico y Estado Uniforme | Concept | Analyze | Unidad 4: Progreso Tecnológico y Estado Uniforme | C-01 | 3 |
| `Hab-02` | Solución Cuantitativa Cobb-Douglas | Skill | Evaluate | Unidad 5: Solución Cuantitativa Cobb-Douglas | Hab-01, C-01 | 6 |
| `C-04` | Estabilidad y Crecimiento Balanceado | Concept | Evaluate | Unidad 7: Estabilidad y Crecimiento Balanceado | Hab-01 | 3 |
| `Hab-04` | Dinámica Harrod-Domar en Solow | Skill | Analyze | Unidad 11: Dinámica Harrod-Domar en Solow | C-03, Hab-01 | 6 |
| `Hab-05` | Solución Explícita Cobb-Douglas | Skill | Evaluate | Unidad 13: Solución Explícita Cobb-Douglas | Hab-01, C-04 | 6 |
| `Hab-06` | Modelo CES con Sustitución Extrema | Skill | Analyze | Unidad 14: Modelo CES con Sustitución Extrema | Hab-01, C-04 | 6 |
| `H-02` | Precios y Productividad Marginal | Fact | Understand | Unidad 16: Precios y Productividad Marginal | C-03 | 3 |
| `C-05` | Precios Competitivos y Arbitraje | Concept | Evaluate | Unidad 16: Precios Competitivos y Arbitraje | H-02 | 3 |
| `C-06` | Isocuantas y Participación Factorial | Concept | Evaluate | Unidad 19: Isocuantas y Participación Factorial | C-05 | 3 |
| `Hab-07` | Cambio Tecnológico Neutral | Skill | Evaluate | Unidad 22: Cambio Tecnológico Neutral | C-05, C-06 | 6 |
| `C-07` | Oferta Elástica de Trabajo | Concept | Analyze | Unidad 24: Oferta Elástica de Trabajo | C-05 | 3 |
| `Hab-08` | Tasa de Ahorro Variable e Impuestos | Skill | Evaluate | Unidad 26: Tasa de Ahorro Variable e Impuestos | C-05 | 6 |
| `C-08` | Crecimiento Poblacional Endógeno | Concept | Evaluate | Unidad 27: Crecimiento Poblacional Endógeno | Hab-08 | 3 |
| `Hab-09` | Salarios Rígidos y Desempleo | Skill | Evaluate | Unidad 29: Salarios Rígidos y Desempleo | C-05 | 6 |
| `C-09` | Preferencia por la Liquidez y Trampa | Concept | Evaluate | Unidad 30: Preferencia por la Liquidez y Trampa | C-05, Hab-09 | 3 |

---

## Detailed Competency Specifications

### [H-01] Hipótesis del Modelo de Solow (Fact)

- **Bloom Level:** Understand
- **Session:** Unidad 2: Hipótesis del Modelo de Solow
- **Prerequisites:** None
- **Recommended Modalities:** multiple_select, fill_in_the_blank, concept_matching
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
Función de producción $Q=f(K,L)$ linealmente homogénea con proporciones variables, productos marginales positivos y decrecientes, ahorro $\dot{K}=sQ$ y crecimiento laboral $\dot{L}/L=\lambda$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Proporciones fijas | conceptual_swap | high | $Q=\rho K$ | Distinga el modelo de Domar de proporciones fijas del de Solow, donde capital y mano de obra se combinan en proporciones variables. |
| `D-H01-02` | Retornos crecientes | conceptual_swap | high | $f_{KK}>0$ | Recuerde que Solow supone productos marginales positivos pero decrecientes para cada insumo, es decir $f_{KK}<0$ y $f_{LL}<0$. |
| `D-H01-03` | Ahorro sobre capital | conceptual_swap | high | $\dot{K}=sK$ | Aplique la propensión marginal al ahorro $s$ sobre el flujo de producto neto $Q$ y no sobre el acervo de capital $K$. |

---

### [C-03] Modelo Neoclásico de Acumulación (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Modelo Neoclásico de Acumulación
- **Prerequisites:** None
- **Recommended Modalities:** adversarial_break, unstructured_model, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 3)

#### Description & Cognitive Model
Sustitución de proporciones fijas por $Y=F(K,L)$ con rendimientos constantes a escala, $\dot{K}=sF(K,L)$ y $L(t)=L_0 e^{nt}$ en pleno empleo.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Proporciones fijas | conceptual_swap | high | La relación capital-producto es rígida y no sustituible | Distinga el supuesto de proporciones variables neoclásico de la rigidez Harrod-Domar que genera el filo de la navaja. |
| `D-C03-02` | Rendimientos decrecientes globales | conceptual_swap | high | $F(\lambda K,\lambda L)<\lambda F(K,L)$ | Recuerde que sin recurso escaso como la tierra, la función $F(K,L)$ es homogénea de primer grado con rendimientos constantes. |
| `D-C03-03` | Desempleo estructural | conceptual_swap | high | El empleo difiere de $L(t)=L_0 e^{nt}$ | Verifique que el salario real se ajusta instantáneamente para mantener pleno empleo continuo de la fuerza laboral creciente. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | Homogeneidad de grado 1 $F(\lambda K,\lambda L)=\lambda F(K,L)$ | Sin rendimientos constantes a escala no puede reducirse el sistema a la razón capital-trabajo. | - |
| `A-C03-02` | - | Pleno empleo continuo con oferta inelástica $L(t)=L_0 e^{nt}$ | Si el salario real es rígido, aparece desempleo y falla la trayectoria de acumulación. | - |

---

### [Hab-01] Ecuación Fundamental de Solow (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Ecuación Fundamental de Solow
- **Prerequisites:** H-01, C-03
- **Recommended Modalities:** proof_dag, open_symbolic, adversarial_break, fill_in_the_blank
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3), `solow1956.pdf` (page 6)

#### Description & Cognitive Model
Derivación de la ecuación diferencial fundamental $\dot{k}=s\phi(k)-\lambda k$ (o $\dot{r}=sF(r,1)-nr$ para $r=K/L$) a partir de rendimientos constantes a escala, $\dot{K}=sF(K,L)$ y la diferenciación de $K=kL$.

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Omite regla producto | skipped_step | high | $\dot{k}=s\phi(k)$ | Aplique la regla del producto al diferenciar $K=kL$: $\dot{K}=L\dot{k}+k\dot{L}$, lo cual introduce la dilución $-\lambda k$ al despejar $\dot{k}$. |
| `D-Hab01-07` | Omite dilución laboral | skipped_step | high | $\dot{r}=sF(r,1)$ | Al diferenciar $r=K/L$ respecto al tiempo, reste la tasa de crecimiento laboral $nr$ que diluye el capital por trabajador. |
| `D-Hab01-02` | Signo positivo en dilución | skipped_step | high | $\dot{k}=s\phi(k)+\lambda k$ | Al igualar $L\dot{k}+k\lambda L=sL\phi(k)$ y despejar $\dot{k}$, pase el término $\lambda k$ restando al miembro derecho. |
| `D-Hab01-08` | Invierte signo de dilución | skipped_step | high | $\dot{r}=sF(r,1)+nr$ | Recuerde que $\dot{r}/r = \dot{K}/K - \dot{L}/L$, por lo que el crecimiento poblacional $n$ reduce la razón capital-trabajo. |
| `D-Hab01-03` | Divide mal por L | conceptual_swap | high | $\dot{k}=sL\phi(k)-\lambda k$ | Elimine el factor común $L>0$ de todos los términos al igualar $L\dot{k}+\lambda kL=sL\phi(k)$ para obtener la ecuación en $k$. |
| `D-Hab01-09` | No divide por L | conceptual_swap | high | $\dot{r}=sF(K,L)-nr$ | Use la homogeneidad de grado uno para factorizar $L=L_0 e^{nt}$ y expresar el producto por trabajador como $F(r,1)$. |
| `D-Hab01-04` | Ahorro en k lineal | conceptual_swap | high | $\dot{k}=sk-\lambda k$ | Mantenga la función intensiva $\phi(k)=f(k,1)$ que representa el producto medio del trabajo y no la sustituya por $k$. |
| `D-Hab01-05` | Confunde L punto | conceptual_swap | high | $\dot{k}=s\phi(k)-\lambda$ | Recuerde que $\dot{L}/L=\lambda$ implica $\dot{L}=\lambda L$, por lo que $k\dot{L}/L=\lambda k$ y el término de dilución conserva el factor $k$. |
| `D-Hab01-10` | Multiplica por r el ahorro | conceptual_swap | high | $\dot{r}=srF(r,1)-nr$ | Verifique que al sustituir $L/K = 1/r$ en $r \cdot sF(K,L)/K$, el factor $r$ se cancela y queda $sF(r,1)$. |
| `D-Hab01-06` | Invierte parámetros | conceptual_swap | high | $\dot{k}=\lambda\phi(k)-sk$ | Asocie $s$ a la inversión bruta por trabajador $s\phi(k)$ y $\lambda$ al crecimiento exponencial de la fuerza laboral que diluye $k$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Homogeneidad lineal de $f(K,L)$ con $L>0$ | Sin retornos constantes a escala no es posible reducir $Q/L$ a una función $\phi(k)$ de una sola variable. | - |
| `A-Hab01-02` | - | Tasa de ahorro $s\in(0,1)$ constante y crecimiento laboral $n>0$ | Si $s$ o $n$ varían endógenamente, la ecuación autónoma unidimensional deja de ser válida. | - |

---

### [C-01] Línea de Fase y Estabilidad (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Línea de Fase y Estabilidad
- **Prerequisites:** Hab-01
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
Análisis cualitativo-gráfico de $\dot{k}=s\phi(k)-\lambda k$: intersección de $s\phi(k)$ con el rayo $\lambda k$ en $\bar{k}>0$, pendiente negativa de la línea de fase y convergencia global hacia el estado uniforme

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Equilibrio inestable | conceptual_swap | high | La línea de fase cruza $\bar{k}$ con pendiente positiva. | Observe que para $k<\bar{k}$ se cumple $s\phi(k)>\lambda k$ ($\dot{k}>0$) y para $k>\bar{k}$ se cumple $\dot{k}<0$, generando convergencia estable. |
| `D-C01-02` | Crecimiento nulo en estado uniforme | conceptual_swap | high | En $\bar{k}$, las variables $K$, $L$ y $Q$ permanecen constantes. | Distinga el estado estacionario de crecimiento cero del estado uniforme de Solow, donde $K$, $L$ y $Q$ crecen todos a la tasa $\lambda$. |
| `D-C01-03` | No pasa por el origen | conceptual_swap | high | La curva $s\phi(k)$ tiene ordenada positiva en $k=0$. | Como el capital es un factor indispensable, cuando $K=0$ ($k=0$) el producto $Q=0$ y la curva $s\phi(k)$ debe partir del origen. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Existe un intervalo positivo donde $s\phi(k)>\lambda k$ con $\phi'(k)>0$ y $\phi''(k)<0$ | Sin este cruce inicial por encima del rayo $\lambda k$ no existe un equilibrio positivo estable $\bar{k}>0$. | - |

---

### [C-02] Progreso Tecnológico y Estado Uniforme (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 4: Progreso Tecnológico y Estado Uniforme
- **Prerequisites:** C-01
- **Recommended Modalities:** invariant_canvas, adversarial_break, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
Efecto del mejoramiento tecnológico $Q=T(t)f(K,L)$ con $dT/dt>0$ sobre el diagrama de fase: desplazamiento secular hacia arriba de $s\phi(k)$ que eleva sucesivamente el capital por trabajador $\bar{k}$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Desplazamiento del rayo | conceptual_swap | high | El progreso tecnológico aumenta la pendiente del rayo $\lambda k$. | Recuerde que $T(t)$ multiplica la función de producción y desplaza hacia arriba la curva $s\phi(k)$, sin alterar la tasa laboral $\lambda$. |
| `D-C02-02` | Reducción del equilibrio | conceptual_swap | high | Al aumentar $T(t)$, la relación capital-trabajo de equilibrio $\bar{k}$ disminuye. | Un desplazamiento hacia arriba de $s\phi(k)$ produce intersecciones sucesivamente más altas con el rayo $\lambda k$, aumentando $\bar{k}$. |
| `D-C02-03` | Desplazamiento hacia abajo | conceptual_swap | high | El término $T(t)$ con $dT/dt>0$ desplaza la curva $s\phi(k)$ hacia abajo. | Dado que $T(t)$ es creciente en el tiempo, una cantidad fija de $K$ y $L$ genera mayor producto futuro, elevando la curva $s\phi(k)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | El índice tecnológico $T(t)$ satisface $dT/dt>0$ multiplicando a $f(K,L)$ | Si la tecnología fuera constante en el tiempo, $\bar{k}$ y la productividad por trabajador permanecerían fijos en un único estado uniforme. | - |

---

### [Hab-02] Solución Cuantitativa Cobb-Douglas (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Solución Cuantitativa Cobb-Douglas
- **Prerequisites:** Hab-01, C-01
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 5)

#### Description & Cognitive Model
Resolución de la ecuación de Bernoulli $\dot{k}+\lambda k=sk^\alpha$ mediante el cambio de variable $z=k^{1-\alpha}$ para hallar la trayectoria $k(t)$ y el límite de estado uniforme $\bar{k}=(s/\lambda)^{\frac{1}{1-\alpha}}$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Exponente directo | skipped_step | high | $\bar{k}=(s/\lambda)^{1-\alpha}$ | Al tener $k^{1-\alpha}\to s/\lambda$ cuando $t\to\infty$, eleve ambos lados al exponente recíproco $\frac{1}{1-\alpha}$ para despejar $k$. |
| `D-Hab02-02` | Omite factor 1-alpha en ODE | skipped_step | high | $\frac{dz}{dt}+\lambda z=s$ | Al diferenciar $z=k^{1-\alpha}$ respecto al tiempo resulta $\dot{z}=(1-\alpha)k^{-\alpha}\dot{k}$, por lo que ambos términos quedan multiplicados por $(1-\alpha)$. |
| `D-Hab02-03` | Invierte razón s/lambda | conceptual_swap | high | $\bar{k}=(\lambda/s)^{\frac{1}{1-\alpha}}$ | Verifique que en estado uniforme $sk^\alpha=\lambda k$ implica $k^{1-\alpha}=s/\lambda$, de modo que $\bar{k}$ varía directamente con $s$ e inversamente con $\lambda$. |
| `D-Hab02-04` | Exponente positivo en tiempo | conceptual_swap | high | $e^{+(1-\alpha)\lambda t}$ | En $\dot{z}+az=b$ con $a=(1-\alpha)\lambda>0$, el factor integrante produce $e^{-at}$, garantizando que el término transitorio decaiga a cero. |
| `D-Hab02-05` | Sustitución incorrecta de z | conceptual_swap | high | $z=k^\alpha$ | Para linealizar una ecuación de Bernoulli $\dot{k}+\lambda k=sk^m$ con $m=\alpha$, la sustitución estándar requerida es $z=k^{1-m}=k^{1-\alpha}$. |
| `D-Hab02-06` | Confunde condición inicial | conceptual_swap | high | $z(0)=k(0)$ | Al regresar de $z(t)$ a la variable original $k(t)$ mediante $z=k^{1-\alpha}$, el valor inicial debe transformarse como $z(0)=k(0)^{1-\alpha}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Parámetro Cobb-Douglas $\alpha\in(0,1)$ y tasa laboral $\lambda>0$ | Como $(1-\alpha)\lambda>0$, el término exponencial $e^{-(1-\alpha)\lambda t}$ tiende a cero cuando $t\to\infty$. | - |

---

### [C-04] Estabilidad y Crecimiento Balanceado (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 7: Estabilidad y Crecimiento Balanceado
- **Prerequisites:** Hab-01
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 7)

#### Description & Cognitive Model
Análisis cualitativo de $\dot{r}=sF(r,1)-nr$: equilibrio estable $r^*$, equilibrios múltiples ($r_1,r_3$ estables y $r_2$ inestable) o inexistencia.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Confunde estabilidad | conceptual_swap | high | Si $nr>sF(r,1)$ para $r>r^*$, entonces $r$ diverge | Observe que cuando $nr>sF(r,1)$ se tiene $\dot{r}<0$, por lo que $r$ decrece hacia $r^*$ garantizando convergencia estable. |
| `D-C04-02` | Todo cruce es estable | conceptual_swap | high | En la Figura II, $r_2$ también es equilibrio estable | Verifique la pendiente en $r_2$: allí $sF(r,1)$ cruza a $nr$ desde abajo, por lo que cualquier perturbación amplifica la desviación. |
| `D-C04-03` | Equilibrio siempre existe | conceptual_swap | high | Toda función $F(r,1)$ tiene un cruce con $nr$ | Considere que si $sF(r,1)$ yace enteramente por encima o por debajo de $nr$, no existe equilibrio de crecimiento balanceado. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | Productividad marginal decreciente del capital y $F(0,1)=0$ en el caso estándar | Si la producción es posible sin capital o con productividad creciente, surgen múltiples equilibrios o divergencia. | - |

---

### [Hab-04] Dinámica Harrod-Domar en Solow (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 11: Dinámica Harrod-Domar en Solow
- **Prerequisites:** C-03, Hab-01
- **Recommended Modalities:** open_symbolic, unstructured_model, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 11)

#### Description & Cognitive Model
Resolución de $\dot{r}=s\min(r/a, 1/b)-nr$ bajo proporciones fijas $Y=\min(K/a, L/b)$ comparando la tasa natural $n$ y garantizada $s/a$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Confunde cuellos de botella | skipped_step | high | Para $r<a/b$, el factor limitante es el trabajo $1/b$ | Compare $r/a$ y $1/b$: si $r<a/b$, entonces $r/a < 1/b$ y el capital es el cuello de botella, rigiendo $\dot{r}=(s/a-n)r$. |
| `D-Hab04-02` | Equilibrio cuando n>s/a | skipped_step | high | Si $n_1>s/a$, $r$ converge a $s/(n_1 b)$ | Note que $s/(n_1 b) < a/b$ cuando $n_1>s/a$; al cruzar $a/b$ cambia el régimen a $\dot{r}=(s/a-n_1)r<0$ y $r$ tiende a cero. |
| `D-Hab04-03` | Invierte tasa garantizada | conceptual_swap | high | La tasa garantizada de Harrod es $a/s$ | Recuerde que $a$ es el coeficiente de aceleración capital-producto, por lo que la tasa garantizada de crecimiento es $s/a$. |
| `D-Hab04-04` | Desempleo cuando n<s/a | conceptual_swap | high | Si $n_3<s/a$, el factor redundante es el trabajo | Cuando $n_3<s/a$, $r$ converge a $s/(n_3 b) > a/b$, donde sobra capital con productividad marginal nula y empleo pleno. |
| `D-Hab04-05` | Proporción de capital empleada | conceptual_swap | high | La fracción de capital empleada es $s/(an_3)$ | Calcule la razón entre el capital requerido $(a/b)L$ y el capital existente $rL = (s/(n_3 b))L$, lo que da $an_3/s$. |
| `D-Hab04-06` | Solución exponencial errónea | conceptual_swap | high | $r(t) = (r_0 - \frac{s}{n_1 b})e^{n_1 t} + \frac{s}{n_1 b}$ | Al integrar $\dot{r}=s/b - n_1 r$, el factor integrante exige exponente negativo $-n_1 t$ para que el transitorio decaiga. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Coeficientes técnicos fijos $a>0$ (capital) y $b>0$ (trabajo) sin sustitución | Cualquier sustitución marginal entre factores elimina la redundancia persistente y crea una zona estable. | - |

---

### [Hab-05] Solución Explícita Cobb-Douglas (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 13: Solución Explícita Cobb-Douglas
- **Prerequisites:** Hab-01, C-04
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 13)

#### Description & Cognitive Model
Integración directa de $\dot{K}=sK^a(L_0 e^{nt})^{1-a}$ con $b=1-a$ para hallar $K(t)$, el equilibrio $r^*=(s/n)^{1/(1-a)}$ y el coeficiente $C=s/n$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Exponente invertido en r* | skipped_step | high | $r^*=(s/n)^{1-a}$ | Al igualar $sr^a = nr$, resulta $r^{1-a}=s/n$, por lo que debe elevar ambos miembros al recíproco $1/(1-a)$. |
| `D-Hab05-02` | Invierte razón s/n | skipped_step | high | $r^*=(n/s)^{\frac{1}{1-a}}$ | Verifique la intuición económica: mayor ahorro $s$ y menor crecimiento laboral $n$ elevan la razón capital-trabajo $r^*$. |
| `D-Hab05-03` | Error en ingreso per cápita | conceptual_swap | high | $Y/L \Rightarrow (s/n)^{1/b}$ | Sustituya $r^*=(s/n)^{1/b}$ en la función por trabajador $Y/L = r^a$ para obtener $(s/n)^{a/b}$. |
| `D-Hab05-04` | Error en coeficiente C | conceptual_swap | high | $C = K/Y = n/s$ | Use $Y/L = r^a$ y $K/L = r$: entonces $C = K/Y = r^{1-a} = r^b = s/n$, cumpliendo la relación $n = s/C$. |
| `D-Hab05-05` | Omite condición inicial K0 | conceptual_swap | high | $K(t) = [(s/n)L_0^b e^{nbt}]^{1/b}$ | Al integrar $\dot{K}=sK^a L_0^b e^{nbt}$ como ecuación de Bernoulli, incluya la constante de integración fijada por $K(0)=K_0$. |
| `D-Hab05-06` | Exponente erróneo en e | conceptual_swap | high | El término asintótico crece como $e^{nbt}$ dentro de la raíz | Al aplicar la potencia exterior $1/b$ sobre $e^{nbt}$, los exponentes se multiplican y $K(t)$ crece asintóticamente a tasa $n$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | Elasticidad del capital $a\in(0,1)$ en $Y=K^a L^{1-a}$ | Si $a\ge 1$, desaparece el rendimiento marginal decreciente y no existe equilibrio estacionario único. | - |

---

### [Hab-06] Modelo CES con Sustitución Extrema (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 14: Modelo CES con Sustitución Extrema
- **Prerequisites:** Hab-01, C-04
- **Recommended Modalities:** open_symbolic, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 14)

#### Description & Cognitive Model
Análisis de $Y=(aK^p+L^p)^{1/p}$ ($0<p<1$) y del caso $p=1/2$ con $\dot{r}=s(a\sqrt{r}+1)^2-nr$: divergencia si $sa^2>n$ y $r^*=(1/(\sqrt{n/s}-a))^2$ si $sa^2<n$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Invierte condición umbral | skipped_step | high | Existe equilibrio estable cuando $sa^2 > n$ | Compare las pendientes asintóticas: si $sa^2>n$, la curva $s(a\sqrt{r}+1)^2$ crece más rápido que $nr$ y no hay intersección. |
| `D-Hab06-02` | Olvida elevar al cuadrado r* | skipped_step | high | $r^* = \frac{1}{\sqrt{n/s}-a}$ | Tras resolver $\sqrt{s}(a\sqrt{r}+1)=\sqrt{nr}$ para $\sqrt{r}$, eleve ambos lados al cuadrado para obtener $r^*$. |
| `D-Hab06-03` | Error en ordenada al origen | conceptual_swap | high | La curva $sF(r,1)$ parte de $0$ cuando $r=0$ | En esta familia es posible producir solo con trabajo; evaluando en $r=0$ se obtiene $sF(0,1)=s>0$. |
| `D-Hab06-04` | Signo erróneo en denominador | conceptual_swap | high | $r^* = (1/(\sqrt{n/s}+a))^2$ | Al agrupar $\sqrt{r}(\sqrt{n/s}-a)=1$ desde $a\sqrt{r}+1=\sqrt{nr/s}$, el término $a$ pasa restando al lado derecho. |
| `D-Hab06-05` | Convexidad errónea p>1 | conceptual_swap | high | El caso $p>1$ garantiza rendimientos marginales decrecientes | Recuerde que para $p>1$ las isocuantas tienen la convexidad incorrecta; se requiere $0<p<1$ para rendimientos decrecientes. |
| `D-Hab06-06` | Error en ingreso límite | conceptual_swap | high | El ingreso per cápita límite es $1/(1-a\sqrt{n/s})^2$ | Evalúe $F(r^*,1)=(a\sqrt{r^*}+1)^2$ sustituyendo $\sqrt{r^*}=1/(\sqrt{n/s}-a)$, lo que simplifica a $1/(1-a\sqrt{s/n})^2$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Parámetro de sustitución $0<p<1$ con producción viable sin capital | Si $p\ge 1$, las isocuantas pierden convexidad estricta y no es sensato exigir pleno empleo de ambos factores. | - |

---

### [H-02] Precios y Productividad Marginal (Fact)

- **Bloom Level:** Understand
- **Session:** Unidad 16: Precios y Productividad Marginal
- **Prerequisites:** C-03
- **Recommended Modalities:** fill_in_the_blank, multiple_select, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 16)

#### Description & Cognitive Model
Sistema de cuatro precios ($p, w, q, i$) con $p(t)$ dado y ecuaciones competitivas $\partial F/\partial L = w/p$ y $\partial F/\partial K = q/p$ dependientes solo de $r$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H02-01` | Nivel de precios endógeno | conceptual_swap | high | El modelo real determina el nivel absoluto $p(t)$ | Recuerde que en el sistema real nada determina el nivel absoluto de precios, por lo que $p(t)$ se toma como dato exógeno. |
| `D-H02-02` | Productividad depende de escala | conceptual_swap | high | $\partial F/\partial K$ depende de $K$ y $L$ por separado | Por homogeneidad de grado uno de $F(K,L)$, sus derivadas parciales son homogéneas de grado cero y solo dependen de $r=K/L$. |
| `D-H02-03` | Iguala renta al salario | conceptual_swap | high | $\partial F/\partial K = w/p$ | Distinga la retribución real del trabajo $w/p=\partial F/\partial L$ de la renta real del capital $q/p=\partial F/\partial K$. |

---

### [C-05] Precios Competitivos y Arbitraje (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 16: Precios Competitivos y Arbitraje
- **Prerequisites:** H-02
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 16)

#### Description & Cognitive Model
Determinación competitiva del salario real $\frac{\partial F}{\partial L}=\frac{w}{p}$ y renta real $\frac{\partial F}{\partial K}=\frac{q}{p}$, junto con la condición de arbitraje $i(t)=\frac{q(t)}{p(t)}+\frac{\dot{p}(t)}{p(t)}$ bajo rendimientos constantes a escala

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Iguala tasa nominal y real | conceptual_swap | high | $i(t)=q(t)/p(t)$ siempre | Sume la tasa de variación del precio del bien de capital $\dot{p}/p$ al rendimiento propio $q/p$ para igualar el retorno monetario $i(t)$. |
| `D-C05-02` | Signo invertido en inflación | conceptual_swap | high | $i(t)=q(t)/p(t)-\dot{p}(t)/p(t)$ | Recuerde que si el precio del capital cae ($\dot{p}<0$), la renta propia $q/p$ debe superar a $i(t)$ para compensar la pérdida de capital. |
| `D-C05-03` | Productividad depende de escala | conceptual_swap | high | $\partial F/\partial K$ depende de $K$ y $L$ por separado | Aplique la homogeneidad de grado uno de $F(K,L)$: las productividades marginales dependen únicamente de la razón capital-trabajo $r=K/L$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Competencia perfecta, rendimientos constantes a escala y previsión perfecta sin riesgo | Sin competencia o arbitraje perfecto fallan las igualdades marginales y la relación entre $i(t)$ y $q(t)/p(t)$. | - |
| `A-C05-02` | - | Nivel absoluto de precios $p(t)$ dado exógenamente en el sistema real | Sin $p(t)$ exógeno quedan indeterminados los precios nominales $w(t)$ y $q(t)$. | - |

---

### [C-06] Isocuantas y Participación Factorial (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 19: Isocuantas y Participación Factorial
- **Prerequisites:** C-05
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 19)

#### Description & Cognitive Model
Relación entre pendiente de isocuantas y razón de precios $w/q$ a lo largo de rayos desde el origen, contrastando proporciones fijas de Harrod-Domar, Cobb-Douglas $Y=K^aL^{1-a}$ y $Y=(a\sqrt{K}+\sqrt{L})^2$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Participación siempre constante | conceptual_swap | high | La participación laboral es independiente de $s$ y $n$ en todo modelo | Distinga la función Cobb-Douglas (participación fija $1-a$) de casos como $Y=(a\sqrt{K}+\sqrt{L})^2$, donde la participación laboral $1-a\sqrt{s/n}$ depende de $s$ y $n$. |
| `D-C06-02` | Precio positivo en factor redundante | conceptual_swap | high | En Harrod-Domar con $r>a/b$ ambos factores cobran renta positiva | Evalúe la productividad marginal en proporciones fijas: si $r>a/b$, el capital es redundante ($q=0$) y todo el producto se imputa al trabajo ($w=p/b$). |
| `D-C06-03` | Indeterminación fuera de equilibrio | conceptual_swap | high | Los precios $w$ y $q$ son indeterminados para cualquier $r$ | Limite la indeterminación de precios en Harrod-Domar exclusivamente al vértice exacto $r=a/b$, donde solo se cumple $aq+bw=p$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Rendimientos constantes a escala y convexidad normal de las isocuantas | Si no hay rendimientos constantes, la pendiente de la isocuanta varía a lo largo de un mismo rayo desde el origen. | - |

---

### [Hab-07] Cambio Tecnológico Neutral (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 22: Cambio Tecnológico Neutral
- **Prerequisites:** C-05, C-06
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 22)

#### Description & Cognitive Model
Resolución de la trayectoria asintótica bajo cambio tecnológico neutral $Y=A(t)F(K,L)$ con $A(t)=e^{gt}$ y función Cobb-Douglas $Y=e^{gt}K^a(L_0e^{nt})^{1-a}$, obteniendo tasas límite de $K$, $Y$, $K/L$ y $K/Y$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Suma simple de tasas | skipped_step | high | El producto crece a $n+g$ y el capital a $n+g$ | Considere el efecto compuesto del mayor ahorro sobre el capital: en la solución con $b=1-a$, el capital crece a $n+g/b$ y el producto a $n+ag/b$. |
| `D-Hab07-02` | Razón K/L estacionaria | skipped_step | high | $K/L$ converge a un valor constante $r^*$ | Verifique que al crecer $K$ a tasa $n+g/b$ y $L$ a tasa $n$, la razón capital-trabajo $K/L$ crece indefinidamente a tasa $g/b>0$ sin alcanzar estado estacionario. |
| `D-Hab07-03` | Tasa errónea de K/Y | conceptual_swap | high | El coeficiente $K/Y$ permanece constante en el largo plazo | Calcule la diferencia de tasas entre capital y producto: $(n+g/b)-(n+ag/b)=(1-a)g/b=g$, por lo que $K/Y$ crece a tasa $g$. |
| `D-Hab07-04` | Confunde tasas de K y Y | conceptual_swap | high | $Y$ crece más rápido que $K$ a tasa $n+g/b$ | Recuerde que en $Y=e^{gt}K^a L^{1-a}$ la tasa de $Y$ es $g+a(n+g/b)+(1-a)n=n+ag/b$, estrictamente menor que la tasa $n+g/b$ del capital. |
| `D-Hab07-05` | Participación laboral creciente | conceptual_swap | high | Al subir $K/L$ indefinidamente, cae la participación laboral | Aplique la propiedad de Cobb-Douglas con cambio neutral: aunque el salario real sube sin límite, la participación relativa del trabajo permanece constante en $1-a$. |
| `D-Hab07-06` | Olvida condición a>1/2 | conceptual_swap | high | $Y$ siempre crece más rápido que $n+g$ | Compare $a/(1-a)$ con $1$: el crecimiento del producto $n+ag/b$ supera a $n+g$ únicamente cuando $a>1/2$ debido a la acumulación inducida. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Progreso técnico neutral multiplicativo $A(t)=e^{gt}$ con $g>0$ y $b=1-a\in(0,1)$ | Si el cambio técnico no es neutral o $a\ge 1$, la solución cerrada de Bernoulli y las tasas asintóticas cambian. | - |

---

### [C-07] Oferta Elástica de Trabajo (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 24: Oferta Elástica de Trabajo
- **Prerequisites:** C-05
- **Recommended Modalities:** adversarial_break, proof_dag, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 24)

#### Description & Cognitive Model
Extensión del mercado laboral con oferta elástica $L=L_0e^{nt}(w/p)^h$ y ecuación $\dot{r}=(sF(r,1)-nr)(1+ah/r)^{-1}$, comparada con la forma general $L=G(t,w/p)$ sobre el equilibrio $r^*$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Elasticidad siempre altera r* | conceptual_swap | high | Cualquier oferta elástica cambia la razón de equilibrio $r^*$ | Observe que bajo la especificación multiplicativa $L=L_0e^{nt}(w/p)^h$, el factor $(1+ah/r)^{-1}$ no anula ni desplaza las raíces de $sF(r,1)-nr=0$, manteniendo $r^*$ intacto. |
| `D-C07-02` | Equilibrio general independiente de G | conceptual_swap | high | En $L=G(t,w/p)$ el equilibrio siempre cumple $sF(r,1)=nr$ | Sustituya $\dot{r}=0$ y $\dot{w}=0$ en la ecuación general: la condición estacionaria es $sF(r,1)=\frac{r}{G}\frac{\partial G}{\partial t}$, que coincide con $nr$ solo si $\frac{1}{G}\frac{\partial G}{\partial t}=n$. |
| `D-C07-03` | Límite infinito de oferta | conceptual_swap | high | La curva $L=L_0e^{nt}(w/p)^h$ captura el tope máximo de población activa | Tenga presente la advertencia del modelo: la forma de elasticidad constante crece sin límite ante salarios reales muy altos y debe modificarse cerca del pleno empleo poblacional. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Nivel de precios constante $p$ y función de producción Cobb-Douglas para la reducción explícita | Si $p$ varía o $F$ no es Cobb-Douglas, $\dot{w}/w$ no se reduce simplemente a $a\dot{r}/r$. | - |

---

### [Hab-08] Tasa de Ahorro Variable e Impuestos (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 26: Tasa de Ahorro Variable e Impuestos
- **Prerequisites:** C-05
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 26)

#### Description & Cognitive Model
Análisis de estabilidad con tasa de ahorro endógena decreciente $s(r)$ en $\dot{r}=s(r)F(r,1)-nr$ y cálculo de la tasa efectiva de ahorro $s+(v-s)t$ bajo impuesto proporcional $t$ con fracción invertida $v$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | Ahorro inverso al rendimiento | skipped_step | high | Al subir $r$ aumenta $q/p$ y por tanto aumenta $s(r)$ | Recuerde que un mayor $r$ reduce el rendimiento real del capital $q/p$; como el ahorro depende positivamente del rendimiento, $s(r)$ es una función decreciente de $r$. |
| `D-Hab08-02` | Estado estacionario clásico | skipped_step | high | Si $s(r)=0$ para $r$ grande se detiene el crecimiento en estado estacionario | Verifique que aunque $s(r)$ anule la inversión neta para $r$ muy alto, el crecimiento continuo de la fuerza laboral $n>0$ reduce $r$ de vuelta hacia el equilibrio estable. |
| `D-Hab08-03` | Impuesto siempre reduce ahorro | conceptual_swap | high | Todo impuesto sobre la renta $t$ reduce el ahorro efectivo a $s(1-t)$ | Sume la fracción $v$ de la recaudación $tY$ invertida por el Estado al ahorro privado $s(1-t)Y$, obteniendo la tasa efectiva $s+(v-s)t$. |
| `D-Hab08-04` | Suma directa sin restar st | conceptual_swap | high | La tasa efectiva con gasto público invertido es $s+vt$ | Aplique el ahorro privado sobre el ingreso disponible $(1-t)Y$ antes de sumar $vtY$: $s(1-t)+vt=s+(v-s)t$. |
| `D-Hab08-05` | Umbral equivocado de v | conceptual_swap | high | El impuesto aumenta el ahorro efectivo si $v>0$ | Compare la propensión a invertir estatal $v$ con la privada $s$: el ahorro efectivo $s+(v-s)t$ sube respecto a $s$ solo si $v>s$. |
| `D-Hab08-06` | Crecimiento explosivo inevitable | conceptual_swap | high | Aunque $s(r)$ caiga a cero, $r$ puede divergir a infinito | Note que si $s(r)$ se anula para $r$ suficientemente grande, la curva $s(r)F(r,1)$ cae por debajo de $nr$ y garantiza que la última intersección sea estable. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab08-01` | - | Tasa de ahorro $s(r)$ decreciente en $r$ e impuesto proporcional $t\in(0,1)$ sobre la renta | Si el impuesto es no proporcional o $s(r)$ crece con $r$, se alteran las curvas y pueden surgir equilibrios inestables. | - |

---

### [C-08] Crecimiento Poblacional Endógeno (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 27: Crecimiento Poblacional Endógeno
- **Prerequisites:** Hab-08
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 27)

#### Description & Cognitive Model
Dinámica $\dot{r}=sF(r,1)-n(r)r$ cuando la tasa poblacional $n(r)$ depende del ingreso per cápita: aparición de equilibrio estable de estancamiento $r_1$ y umbral inestable $r_2$ sin rendimientos crecientes

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Requiere rendimientos crecientes | conceptual_swap | high | Las trampas de pobreza exigen rendimientos crecientes a escala | Distinga el origen del umbral $r_2$: la trampa de estancamiento $r_1$ surge aquí bajo rendimientos constantes a escala puramente por la respuesta endógena $n(r)$. |
| `D-C08-02` | Estabilidad invertida en r1 y r2 | conceptual_swap | high | $r_1$ es inestable y cualquier perturbación lleva a $r_2$ | Analice el signo de $\dot{r}=sF(r,1)-n(r)r$ en la Figura IX: por debajo de $r_2$ el sistema retorna al equilibrio estable $r_1$; solo superando $r_2$ se sostiene la expansión. |
| `D-C08-03` | Rayo lineal de dilución | conceptual_swap | high | La curva de dilución $n(r)r$ sigue siendo una recta desde el origen | Reemplace la recta $nr$ por la curva no lineal $n(r)r$, cuya curvatura refleja cómo varía la natalidad y mortalidad al aumentar el ingreso por habitante. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C08-01` | - | Crecimiento laboral $n(r)$ negativo o bajo en ingresos mínimos, creciente en medios y decreciente en altos | Si $n(r)$ es constante o monótona sin cruce múltiple, desaparece la bifurcación entre trampa $r_1$ y despegue sobre $r_2$. | - |

---

### [Hab-09] Salarios Rígidos y Desempleo (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 29: Salarios Rígidos y Desempleo
- **Prerequisites:** C-05
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 29)

#### Description & Cognitive Model
Análisis del modelo neoclásico con salario real rígido $\bar{w}/p$, que fija la razón capital-trabajo en $\bar{r}$ y determina el crecimiento del empleo $\frac{\dot{L}}{L}=\frac{s}{\bar{r}}F(\bar{r},1)$ frente a la tasa laboral $n$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab09-01` | r sigue ajustándose libremente | skipped_step | high | Con salario rígido $\bar{w}/p$, la razón $r$ sigue convergiendo a $r^*$ | Recuerde que la productividad marginal del trabajo depende solo de $r$: fijar el salario real en $\bar{w}/p$ fija automáticamente la razón capital-trabajo en $K/L=\bar{r}$. |
| `D-Hab09-02` | Invierte condición de desempleo | skipped_step | high | Si $\frac{s}{\bar{r}}F(\bar{r},1)>n$ se desarrolla desempleo creciente | Compare la tasa de crecimiento del empleo $\frac{s}{\bar{r}}F(\bar{r},1)$ con la de la fuerza laboral $n$: el desempleo crece cuando el empleo crece más lento ($<n$). |
| `D-Hab09-03` | Fórmula errónea de L punto sobre L | conceptual_swap | high | El empleo crece a tasa $\frac{\dot{L}}{L}=sF(\bar{r},1)$ | Sustituya $K=\bar{r}L$ en la ecuación de acumulación $\dot{K}=sF(K,L)$: $\bar{r}\dot{L}=sF(\bar{r}L,L)$, por lo que al dividir por $\bar{r}L$ queda $\frac{\dot{L}}{L}=\frac{s}{\bar{r}}F(\bar{r},1)$. |
| `D-Hab09-04` | Signo de r punto mal interpretado | conceptual_swap | high | El desempleo ocurre cuando $\bar{w}/p$ corresponde a un $\dot{r}>0$ normal | Relacione la pendiente del rayo con $\dot{r}$: un salario rígido demasiado alto fija $\bar{r}$ donde $\frac{s}{\bar{r}}F(\bar{r},1)<n$, equivalente a $\dot{r}<0$ en el modelo flexible. |
| `D-Hab09-05` | Empleo igual a oferta laboral | conceptual_swap | high | Aun con salario rígido se mantiene $L=L_0e^{nt}$ por pleno empleo | Distinga el empleo efectivo $L(t)$ de la oferta laboral exógena $L_0e^{nt}$: bajo salario rígido, $L(t)$ queda determinado por la acumulación de capital y puede rezagarse. |
| `D-Hab09-06` | Salario alto implica escasez | conceptual_swap | high | Un salario rígido por encima del equilibrio genera escasez de trabajo | Verifique que un salario real alto eleva la razón $\bar{r}$ requerida, reduce la tasa de acumulación de empleo por debajo de $n$ y genera desempleo creciente. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab09-01` | - | Salario real exógenamente rígido en $\bar{w}/p$ y ajuste del empleo para igualar productividad marginal | Si el salario se vuelve flexible al alza ante escasez o a la baja ante desempleo, el sistema retoma la dinámica de $r$. | - |

---

### [C-09] Preferencia por la Liquidez y Trampa (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 30: Preferencia por la Liquidez y Trampa
- **Prerequisites:** C-05, Hab-09
- **Recommended Modalities:** adversarial_break, unstructured_model, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 30)

#### Description & Cognitive Model
Equilibrio monetario $\bar{M}=Q(Y,q/p)=Q(F(K,L),F_K(K,L))$ que determina el capital en uso $K(t)$, mostrando cómo la trampa de liquidez induce subutilización de capital y exige dinámica monetaria

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | K(t) igual al stock disponible | conceptual_swap | high | El capital en uso $K(t)$ siempre coincide con el stock acumulado | Distinga el stock físico disponible (dado por la historia de inversión) del capital empleado $K(t)$ determinado por $\bar{M}=Q(Y,q/p)$; su diferencia mide exceso de oferta o demanda. |
| `D-C09-02` | Trampa de liquidez inocua | conceptual_swap | high | Una tasa de interés rígida en la trampa no afecta la utilización del capital | Compare la trampa de liquidez con el salario rígido: una tasa de interés rígida por encima del nivel de equilibrio genera subutilización persistente del capital. |
| `D-C09-03` | Modelo real suficiente | conceptual_swap | high | El modelo real neoclásico basta para analizar la asignación entre efectivo y capital | Reconozca el límite señalado por Solow: cuando la decisión involucra efectivo frente a capital, el precio de la mercancía compuesta importa y se requiere dinámica monetaria. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | Nivel general de precios constante y demanda de dinero dependiente de $Y$ y $q/p$ con oferta $\bar{M}$ dada | Sin precios flexibles o dinámica monetaria explícita, el modelo real no captura las presiones sobre $p(t)$ en la trampa de liquidez. | - |

---
