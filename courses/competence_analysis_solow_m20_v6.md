# Cognitive Task Analysis (CTA): Solow M20 V6

- **Course ID:** `solow_m20_v6`
- **Macro-Competency:** Dominio y aplicación analítica integral de Solow M20 V6
- **Structure:** 19 total competencies (1 Facts, 12 Concepts, 6 Skills) with 81 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `PRE-01` | Hipótesis de Solow y Acumulación | Fact | Understand | Unidad 3: Acumulación y Escala Constante | - | 5 |
| `C-01` | Ecuación Fundamental de Solow | Concept | Analyze | Unidad 2: Ecuación Fundamental de Solow | PRE-01 | 3 |
| `C-02` | Línea de Fase y Estabilidad | Concept | Evaluate | Unidad 3: Línea de Fase y Estabilidad | C-01 | 3 |
| `C-03` | Estado Uniforme y Tecnología | Concept | Analyze | Unidad 4: Estado Uniforme y Tecnología | C-02 | 3 |
| `Hab-02` | Derivación de la Ecuación Fundamental | Skill | Evaluate | Unidad 6: Ecuación Fundamental de Solow | PRE-01 | 6 |
| `C-04` | Estabilidad del Equilibrio Estacionario | Concept | Evaluate | Unidad 7: Estabilidad del Equilibrio Estacionario | Hab-02 | 3 |
| `Hab-01` | Solución Cuantitativa y Explícita Cobb-Douglas | Skill | Evaluate | Unidad 5: Solución Cuantitativa Cobb-Douglas | C-01, C-02, Hab-02, C-04 | 10 |
| `C-05` | Equilibrios Múltiples y No Existencia | Concept | Analyze | Unidad 8: Equilibrios Múltiples y No Existencia | C-04 | 3 |
| `C-06` | Caso Proporciones Fijas (Harrod-Domar) | Concept | Evaluate | Unidad 11: Caso Proporciones Fijas (Harrod-Domar) | Hab-02, C-04 | 3 |
| `Hab-04` | Familia CES y Caso p=1/2 | Skill | Evaluate | Unidad 14: Familia CES y Caso p=1/2 | Hab-02, C-05 | 6 |
| `C-07` | Precios Competitivos y Productividad Marginal | Concept | Analyze | Unidad 16: Precios Competitivos y Productividad Marginal | PRE-01, C-04 | 3 |
| `C-08` | Arbitraje de Activos y Tasa Propia | Concept | Evaluate | Unidad 17: Arbitraje de Activos y Tasa Propia | C-07 | 3 |
| `C-09` | Precios Factoriales en Isocuantas | Concept | Evaluate | Unidad 20: Precios Factoriales en Isocuantas | C-08 | 3 |
| `Hab-05` | Crecimiento con Cambio Tecnológico Neutral | Skill | Evaluate | Unidad 22: Crecimiento con Cambio Tecnológico Neutral | C-08 | 6 |
| `C-10` | Oferta Elástica de Trabajo | Concept | Analyze | Unidad 24: Oferta Elástica de Trabajo | C-09 | 3 |
| `Hab-06` | Ahorro Variable e Impuesto Proporcional | Skill | Evaluate | Unidad 26: Ahorro Variable e Impuesto Proporcional | C-09 | 6 |
| `C-11` | Población Endógena y Trampa de Estancamiento | Concept | Evaluate | Unidad 28: Población Endógena y Trampa de Estancamiento | Hab-06 | 3 |
| `Hab-07` | Salarios Rígidos y Brecha de Empleo | Skill | Analyze | Unidad 29: Salarios Rígidos y Brecha de Empleo | C-10 | 6 |
| `C-12` | Preferencia por Liquidez y Trampa Monetaria | Concept | Evaluate | Unidad 30: Preferencia por Liquidez y Trampa Monetaria | C-08, Hab-07 | 3 |

---

## Detailed Competency Specifications

### [PRE-01] Hipótesis de Solow y Acumulación (Fact)

- **Bloom Level:** Understand
- **Session:** Unidad 3: Acumulación y Escala Constante
- **Prerequisites:** None
- **Recommended Modalities:** fill_in_the_blank, multiple_select, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 3), `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
Función de producción $Y=F(K,L)$ ($K,L>0$) con rendimientos constantes a escala y productos marginales decrecientes, acumulación neta $\dot{K}=sY$ y crecimiento laboral exógeno $L(t)=L_0 e^{nt}$.

#### Fused Distractor Models (5)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-PRE01-01` | Ahorro sobre capital | conceptual_swap | high | $\dot{K}=sK$ | Distinga el flujo de ingreso neto $Y$ del acervo $K$; la inversión neta es una fracción constante $s$ del producto $Y$. |
| `D-PRE01-04` | Proporción fija Domar | conceptual_swap | high | $Q=\rho K$ sin mano de obra | Distinga el modelo de Solow, donde $K$ y $L$ se combinan en proporciones variables, del caso fijo de Domar. |
| `D-PRE01-02` | Rendimientos decrecientes globales | conceptual_swap | high | $F(\lambda K,\lambda L)<\lambda Y$ | Recuerde que sin recurso fijo como la tierra, $F(K,L)$ es homogénea de primer grado con rendimientos constantes a escala. |
| `D-PRE01-05` | Retornos crecientes | conceptual_swap | high | $f_{KK}>0$ y $f_{LL}>0$ | Recuerde que los productos marginales son positivos ($f_K,f_L>0$) pero decrecientes ($f_{KK},f_{LL}<0$). |
| `D-PRE01-03` | Crecimiento lineal del trabajo | conceptual_swap | high | $L(t)=L_0(1+nt)$ | Aplique el crecimiento exponencial continuo $L(t)=L_0 e^{nt}$ para una tasa relativa constante $\dot{L}/L=n$ de fuerza laboral. |

---

### [C-01] Ecuación Fundamental de Solow (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 2: Ecuación Fundamental de Solow
- **Prerequisites:** PRE-01
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
Reducción de $Q=L\phi(k)$ con $k\equiv K/L$ y diferenciación de $K=kL$ para derivar la ecuación diferencial fundamental $\dot{k}=s\phi(k)-\lambda k$ del modelo de Solow.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Omite regla del producto | conceptual_swap | high | $\dot{K}=L\dot{k}$ | Aplique la regla del producto al diferenciar $K=kL$: $\dot{K}=L\dot{k}+k\dot{L}=L\dot{k}+k\lambda L$. |
| `D-C01-02` | Signo invertido en dilución | conceptual_swap | high | $\dot{k}=s\phi(k)+\lambda k$ | Reste $\lambda k$ porque el crecimiento de la fuerza laboral diluye la relación capital-mano de obra $k=K/L$. |
| `D-C01-03` | Conserva factor L | conceptual_swap | high | $\dot{k}=sL\phi(k)-\lambda k$ | Divida toda la igualdad $L\dot{k}+k\lambda L=sL\phi(k)$ entre el factor común $L>0$ para obtener $\dot{k}$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Homogeneidad lineal $f(K,L)=Lf(K/L,1)=L\phi(k)$ con $L>0$ | Sin homogeneidad de grado 1 no puede eliminarse $L$ en la ecuación diferencial. | - |
| `A-C01-02` | - | Concavidad de $\phi(k)$ con $\phi'(k)=f_K>0$ y $\phi''(k)=Lf_{KK}<0$ | Sin concavidad estricta no se garantiza una única intersección estable. | - |

---

### [C-02] Línea de Fase y Estabilidad (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Línea de Fase y Estabilidad
- **Prerequisites:** C-01
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
Análisis cualitativo-gráfico de $\dot{k}=s\phi(k)-\lambda k$ mediante las curvas $s\phi(k)$ y $\lambda k$, intersección en $\bar{k}$ y estabilidad dinámica por pendiente negativa de la línea de fase.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Inestabilidad en cruce negativo | conceptual_swap | high | Pendiente negativa implica divergencia | Observe en la línea de fase que si $k<\bar{k}$ entonces $\dot{k}>0$ y si $k>\bar{k}$ entonces $\dot{k}<0$, convergiendo a $\bar{k}$. |
| `D-C02-02` | Distancia horizontal | conceptual_swap | high | $\dot{k}$ es distancia horizontal entre curvas | Mida $\dot{k}=s\phi(k)-\lambda k$ como la distancia vertical entre la curva cóncava $s\phi(k)$ y el rayo $\lambda k$. |
| `D-C02-03` | Equilibrio en origen | conceptual_swap | high | $\bar{k}=0$ es el equilibrio estable | Recuerde que para todo $k>0$ inicial el sistema converge a la intersección positiva $\bar{k}$ donde $s\phi(\bar{k})=\lambda\bar{k}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | Capital indispensable $\phi(0)=0$ y existencia de $k>0$ con $s\phi(k)>\lambda k$ | Si $s\phi(k)\le\lambda k$ para todo $k>0$, no existe intersección positiva $\bar{k}$. | - |

---

### [C-03] Estado Uniforme y Tecnología (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 4: Estado Uniforme y Tecnología
- **Prerequisites:** C-02
- **Recommended Modalities:** adversarial_break, unstructured_model, multiple_select
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
Estado uniforme en $\bar{k}$ donde $K$, $L$, inversión neta $\dot{K}$ y producto $Q$ crecen a tasa idéntica $\lambda$, y efecto de $Q=T(t)f(K,L)$ con $dT/dt>0$ que eleva sucesivamente $\bar{k}$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Confunde estacionario y uniforme | conceptual_swap | high | En estado uniforme $K$ y $Q$ no crecen | Distinga estado estacionario (tasa cero) de estado uniforme, donde $K$, $L$, $\dot{K}$ y $Q$ crecen juntos a tasa $\lambda$. |
| `D-C03-02` | Desplazamiento hacia abajo | conceptual_swap | high | $T'(t)>0$ reduce $\bar{k}$ | Note que $T(t)$ creciente multiplica el producto y desplaza $s\phi(k)$ hacia arriba, generando valores mayores de $\bar{k}$. |
| `D-C03-03` | Requiere ajuste exógeno | conceptual_swap | high | Solo se alcanza $\bar{k}$ con delicado balance | En Solow la convergencia a la tasa $\lambda$ ocurre automáticamente por la dinámica de $k$, sin el filo de la navaja de Domar. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | Tecnología $T(t)$ es función creciente del tiempo con $dT/dt>0$ | Si $T$ fuera constante, $\bar{k}$ permanecería fijo en un único nivel. | - |

---

### [Hab-02] Derivación de la Ecuación Fundamental (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 6: Ecuación Fundamental de Solow
- **Prerequisites:** PRE-01
- **Recommended Modalities:** proof_dag, open_symbolic, fill_in_the_blank
- **Evidence Citations:** `solow1956.pdf` (page 6)

#### Description & Cognitive Model
Derivación de la ecuación diferencial $\dot{r}=sF(r,1)-nr$ para la razón capital-trabajo $r=K/L$ usando homogeneidad de primer grado de $F(K,L)$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Omite dilución laboral | skipped_step | high | $\dot{r}=sF(r,1)$ | Al diferenciar $K=rL_0 e^{nt}$ respecto al tiempo, conserve el término $nr$ que refleja la dilución del capital por nuevo trabajador. |
| `D-Hab02-02` | Signo invertido en dilución | skipped_step | high | $\dot{r}=sF(r,1)+nr$ | Verifique que $\dot{r}/r=\dot{K}/K-\dot{L}/L$: el crecimiento laboral $n$ reduce la razón capital-trabajo y entra con signo negativo. |
| `D-Hab02-03` | Divide mal por L | conceptual_swap | high | $\dot{r}=sF(r,0)-nr$ | Al factorizar $L$ en $F(K,L)=L\cdot F(K/L,1)$, el segundo argumento se convierte en $L/L=1$, nunca en cero. |
| `D-Hab02-04` | Falta tasa de ahorro | conceptual_swap | high | $\dot{r}=F(r,1)-nr$ | Multiplique el producto por trabajador $F(r,1)$ por la propensión a ahorrar $s$ antes de restar la dilución $nr$. |
| `D-Hab02-05` | Tasa relativa sin r | conceptual_swap | high | $\dot{r}=\frac{sF(r,1)}{r}-n$ | Multiplique ambos lados de $\dot{r}/r=sF(r,1)/r-n$ por $r$ para obtener la tasa absoluta de cambio $\dot{r}$. |
| `D-Hab02-06` | Escala cuadrática | conceptual_swap | high | $\dot{r}=sLF(r,1)-nr$ | Cancele el factor común $L=L_0 e^{nt}$ en ambos miembros tras aplicar homogeneidad de grado uno en $F(K,L)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Homogeneidad de primer grado $F(K,L)=L\cdot F(K/L,1)$ y pleno empleo continuo | Sin escala constante la dinámica de $r$ dependería explícitamente del tamaño absoluto $L(t)$. | - |

---

### [C-04] Estabilidad del Equilibrio Estacionario (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 7: Estabilidad del Equilibrio Estacionario
- **Prerequisites:** Hab-02
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 7)

#### Description & Cognitive Model
Análisis cualitativo del equilibrio estacionario $sF(r^*,1)=nr^*$ ($\dot{r}=0$) y convergencia asintótica hacia el crecimiento balanceado a tasa natural $n$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Inestabilidad en Cobb-Douglas | conceptual_swap | high | $r>r^* \Rightarrow \dot{r}>0$ | Observe en la Figura I que para $r>r^*$ el rayo $nr$ supera a $sF(r,1)$, por lo que $\dot{r}<0$ y $r$ decrece hacia $r^*$. |
| `D-C04-02` | Crecimiento más lento bajo r* | conceptual_swap | high | $r<r^* \Rightarrow \dot{K}/K < n$ | Cuando $r<r^*$, se cumple $\dot{r}>0$, lo que implica que capital y producto crecen más rápido que la fuerza laboral hasta alcanzar $r^*$. |
| `D-C04-03` | Ignora trampa en origen | conceptual_swap | high | $K=0 \Rightarrow r \to r^*$ | Note la excepción del origen: si $K=0$ entonces $r=0$, no hay producto ni acumulación y la economía no puede despegar. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | Curva $sF(r,1)$ pasa por el origen, es cóncava hacia abajo y cruza $nr$ desde arriba | Si $sF(r,1)$ no cruza $nr$ desde arriba, el equilibrio único estable desaparece. | - |

---

### [Hab-01] Solución Cuantitativa y Explícita Cobb-Douglas (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Solución Cuantitativa Cobb-Douglas
- **Prerequisites:** C-01, C-02, Hab-02, C-04
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 5), `solow1956.pdf` (page 13)

#### Description & Cognitive Model
Resolución explícita del modelo Cobb-Douglas mediante linealización de Bernoulli $z=k^{1-\alpha}$ e integración directa de $\dot{K}=sK^a(L_0 e^{nt})^{1-a}$ para obtener $k(t)$, equilibrio $r^*=(s/n)^{1/(1-a)}$, ingreso per cápita y coeficiente $C=K/Y=s/n$.

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Sustitución incorrecta de z | skipped_step | high | $z=k^\alpha$ linealiza la ecuación | Aplique el cambio de variable estándar de Bernoulli $z=k^{1-m}$ con $m=\alpha$, es decir $z=k^{1-\alpha}$. |
| `D-Hab01-07` | Exponente sin invertir | skipped_step | high | $r^*=(s/n)^{1-a}$ | Al resolver $sr^a=nr$, se obtiene $r^{1-a}=s/n$; eleve ambos miembros al recíproco $1/(1-a)$ para despejar $r^*$. |
| `D-Hab01-02` | Omite factor (1-alpha) | skipped_step | high | $\dot{z}+\lambda z=s$ | Multiplique ambos términos por $(1-\alpha)$ al aplicar la regla de la cadena: $\dot{z}=(1-\alpha)k^{-\alpha}\dot{k}$. |
| `D-Hab01-08` | Razón n/s invertida | skipped_step | high | $r^*=(n/s)^{\frac{1}{1-a}}$ | Verifique la estática comparativa: mayor tasa de ahorro $s$ y menor crecimiento $n$ elevan el capital por trabajador de equilibrio $r^*$. |
| `D-Hab01-03` | Exponente directo en equilibrio | conceptual_swap | high | $k^*=(s/\lambda)^{1-\alpha}$ | Como $k^{1-\alpha}\to s/\lambda$ cuando $t\to\infty$, eleve al exponente recíproco $1/(1-\alpha)$ para despejar $k^*$. |
| `D-Hab01-09` | Omite condición inicial K0 | conceptual_swap | high | $K(t)=[(s/n)L_0^b e^{nbt}]^{1/b}$ | Incluya la constante de integración evaluada en $t=0$ para capturar la trayectoria transitoria desde el capital inicial $K_0$. |
| `D-Hab01-04` | Invierte razón s y lambda | conceptual_swap | high | $k^*=(\lambda/s)^{1/(1-\alpha)}$ | Verifique que $k^*$ varía directamente con el ahorro $s$ e inversamente con el crecimiento laboral $\lambda$. |
| `D-Hab01-10` | Ingreso per cápita erróneo | conceptual_swap | high | $Y/L \to (s/n)^{1/b}$ | Sustituya $r^*$ en $Y/L=r^a$ para obtener el exponente correcto $a/(1-a)$, no $1/(1-a)$. |
| `D-Hab01-05` | Signo positivo en exponencial | conceptual_swap | high | $e^{+(1-\alpha)\lambda t}$ | La solución homogénea de $\dot{z}+az=b$ con $a=(1-\alpha)\lambda>0$ decae con exponente negativo $e^{-(1-\alpha)\lambda t}$. |
| `D-Hab01-11` | Coeficiente de capital invertido | conceptual_swap | high | $C=K/Y=n/s$ | Recuerde que en crecimiento equilibrado $\dot{K}/K=sY/K=n$, de modo que el coeficiente de capital $C=K/Y$ converge a $s/n$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Parámetro Cobb-Douglas $\alpha\in(0,1)$ y tasa laboral $\lambda>0$ | Si $\alpha\ge 1$ o $\lambda\le 0$, el término exponencial no converge a cero. | - |
| `A-Hab01-02` | - | Participación del capital $a\in(0,1)$ en la función Cobb-Douglas $Y=K^a L^{1-a}$ | Si $a\ge 1$, desaparece el rendimiento marginal decreciente y el equilibrio único. | - |

---

### [C-05] Equilibrios Múltiples y No Existencia (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 8: Equilibrios Múltiples y No Existencia
- **Prerequisites:** C-04
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 8)

#### Description & Cognitive Model
Configuraciones alternativas de $sF(r,1)$ frente a $nr$: equilibrios múltiples con umbral inestable $r_2$ (Fig. II) y trayectorias sin equilibrio estacionario (Fig. III)

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Umbral r2 estable | conceptual_swap | high | $r_2$ atrae trayectorias cercanas | Verifique en la Figura II que $sF(r,1)$ cruza $nr$ desde abajo en $r_2$; cualquier perturbación aleja al sistema hacia $r_1$ o $r_3$. |
| `D-C05-02` | Origen como equilibrio | conceptual_swap | high | $r=0$ es equilibrio si $F(0,1)>0$ | Cuando la producción es posible sin capital ($F(0,1)>0$), $sF(0,1)>0$ genera acumulación positiva y el origen no es equilibrio. |
| `D-C05-03` | Cae ingreso agregado en Fig. III | conceptual_swap | high | $s_2 F^2(r,1)<nr \Rightarrow \dot{Y}<0$ | Distinga las variables: aunque $r$ y el ingreso per cápita caigan continuamente, la inversión neta positiva y $L$ creciente hacen subir $Y$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | La función $F(r,1)$ es no decreciente pero puede presentar tramos convexos o asíntotas extremas | Permite violar la unicidad o existencia de intersecciones con el rayo $nr$. | - |

---

### [C-06] Caso Proporciones Fijas (Harrod-Domar) (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 11: Caso Proporciones Fijas (Harrod-Domar)
- **Prerequisites:** Hab-02, C-04
- **Recommended Modalities:** adversarial_break, multiple_select, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 11)

#### Description & Cognitive Model
Análisis del caso $Y=\min(K/a,L/b)$ donde $\dot{r}=s\min(r/a,1/b)-nr$ produce redundancia laboral si $n>s/a$, equilibrio neutro si $n=s/a$ o exceso de capital si $n<s/a$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Ajuste salarial elimina exceso | conceptual_swap | high | $n_3 < s/a$ con pleno uso de $K$ | Con proporciones fijas, la productividad marginal del capital cae a cero para $r>a/b$; la fracción empleada de capital es solo $an_3/s$. |
| `D-C06-02` | Equilibrio en n1 > s/a | conceptual_swap | high | $r \to s/(n_1 b)$ es estable | Observe que $s/(n_1 b)<a/b$; al cruzar $a/b$ la ecuación cambia a $\dot{r}=(s/a-n_1)r<0$ y $r$ cae hacia cero con desempleo creciente. |
| `D-C06-03` | Tasa garantizada errónea | conceptual_swap | high | Tasa garantizada igual a $s/b$ | Distinga los coeficientes: $s/b$ es la altura de la meseta horizontal, mientras que $s/a$ es la pendiente inicial o tasa garantizada. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Isoquantas en ángulo recto $Y=\min(K/a,L/b)$ sin sustitución entre factores | Introduce el filo de la navaja de Harrod-Domar y rigidez independiente de los precios. | - |

---

### [Hab-04] Familia CES y Caso p=1/2 (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 14: Familia CES y Caso p=1/2
- **Prerequisites:** Hab-02, C-05
- **Recommended Modalities:** open_symbolic, adversarial_break, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 14)

#### Description & Cognitive Model
Resolución de $\dot{r}=s(a\sqrt{r}+1)^2-nr$ para $Y=(a\sqrt{K}+\sqrt{L})^2$, factorización con $A=a-\sqrt{n/s}$ y condición de bifurcación entre divergencia ($sa^2>n$) y equilibrio ($sa^2<n$)

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Desigualdad de equilibrio invertida | skipped_step | high | $sa^2>n$ implica equilibrio estable | Si $sa^2>n$, la pendiente asintótica de $s(a\sqrt{r}+1)^2$ supera a $nr$, por lo que $sF(r,1)>nr$ siempre y no existe equilibrio. |
| `D-Hab04-02` | Raíz de r* sin cuadrado | skipped_step | high | $r^*=1/(\sqrt{n/s}-a)$ | Al resolver $s(a\sqrt{r}+1)^2=nr$ se despeja primero $\sqrt{r^*}=1/(\sqrt{n/s}-a)$ y luego se eleva al cuadrado para hallar $r^*$. |
| `D-Hab04-03` | Error en desarrollo binomial | conceptual_swap | high | $Y=a^2K+L$ | Desarrolle completamente el cuadrado $(a\sqrt{K}+\sqrt{L})^2=a^2K+L+2a\sqrt{KL}$ para no perder la complementariedad entre factores. |
| `D-Hab04-04` | Altura inicial en cero | conceptual_swap | high | $sF(0,1)=0$ | Con $p=1/2$ es posible producir solo con trabajo; en $r=0$ la curva $sF(r,1)$ arranca en una altura positiva igual a $s$. |
| `D-Hab04-05` | Signo en factorización A | conceptual_swap | high | $A=a+\sqrt{n/s}$ y $B=a+\sqrt{n/s}$ | Factorice la diferencia de cuadrados $(a^2-n/s)r+2a\sqrt{r}+1$ usando signos opuestos: $A=a-\sqrt{n/s}$ y $B=a+\sqrt{n/s}$. |
| `D-Hab04-06` | Convexo para p>1 | conceptual_swap | high | Isoquantas válidas con $p>1$ | Restrinja $0<p<1$; si $p>1$, las isocuantas tienen convexidad errónea y no rigen rendimientos marginales decrecientes. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Parámetro de sustitución $0<p<1$ (específicamente $p=1/2$) y $a>0$ | Fuera de $0<p<1$ se pierde la convexidad estándar de isocuantas y el pleno empleo conjunto. | - |

---

### [C-07] Precios Competitivos y Productividad Marginal (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 16: Precios Competitivos y Productividad Marginal
- **Prerequisites:** PRE-01, C-04
- **Recommended Modalities:** proof_dag, multiple_select, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 16)

#### Description & Cognitive Model
Determinación del salario real $w/p=\partial F/\partial L$ y renta real del capital $q/p=\partial F/\partial K$ en competencia perfecta, con $p(t)$ dado e independencia de escala bajo rendimientos constantes

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Nivel absoluto determinado | conceptual_swap | high | El modelo real fija $p(t)$ | En una economía real sin dinero, nada determina el nivel absoluto de precios; por ello $p(t)$ se toma como dado. |
| `D-C07-02` | Productividad depende de escala | conceptual_swap | high | $\partial F/\partial L$ depende de $L$ y $r$ | Por el teorema de Euler para funciones homogéneas de grado uno, las derivadas parciales son homogéneas de grado cero y solo dependen de $r$. |
| `D-C07-03` | Precios rígidos con pleno empleo | conceptual_swap | high | $w/p$ fijo asegura $L$ pleno | Dado que trabajo y capital se ofrecen inelásticamente en cada instante, $w/p$ y $q/p$ deben ajustarse instantáneamente para vaciar los mercados. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Competencia pura con ajuste instantáneo de precios de factores y oferta inelástica en cada instante | Bajo competencia monopolística o rigidez salarial falla la función agregada neoclásica y el pleno empleo. | - |

---

### [C-08] Arbitraje de Activos y Tasa Propia (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 17: Arbitraje de Activos y Tasa Propia
- **Prerequisites:** C-07
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 17)

#### Description & Cognitive Model
Relación de arbitraje perfecto entre la tasa de interés monetaria $i(t)$, el alquiler real $q(t)/p(t)$ y la variación de precios $\dot{p}(t)/p(t)$: $i(t)=\frac{q(t)}{p(t)}+\frac{\dot{p}(t)}{p(t)}$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Iguala tasa monetaria y real | conceptual_swap | high | $i(t)=q(t)/p(t)$ siempre | Incluya la ganancia o pérdida de capital $\dot{p}(t)/p(t)$ al comparar el rendimiento de prestar dinero con el de mantener stock físico de capital. |
| `D-C08-02` | Resta variación de precios | conceptual_swap | high | $i(t)=q(t)/p(t)-\dot{p}(t)/p(t)$ | Sume la inflación esperada $\dot{p}/p$ al alquiler real $q/p$: si el precio del bien cae, la tasa propia $q/p$ debe superar a $i(t)$ para sostener activos. |
| `D-C08-03` | Confunde alquiler nominal y real | conceptual_swap | high | $i(t)=q(t)+\dot{p}(t)/p(t)$ | Divida el alquiler monetario $q(t)$ entre el precio de transferencia $p(t)$ para obtener la tasa propia de interés en unidades de capital. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C08-01` | - | Arbitraje perfecto sin riesgo ni preferencia por liquidez | Si hay incertidumbre o aversión al riesgo, falla la igualdad exacta entre tasas. | - |
| `A-C08-02` | - | Previsión perfecta de alquileres futuros $q(u)$ e intereses $i(z)$ | Sin previsión perfecta el precio $p(t)$ no iguala el valor presente integral. | - |

---

### [C-09] Precios Factoriales en Isocuantas (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 20: Precios Factoriales en Isocuantas
- **Prerequisites:** C-08
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 20)

#### Description & Cognitive Model
Determinación de la razón de precios factoriales $w/q$ mediante la pendiente de las isocuantas de $F(K,L)$ y comportamiento de participaciones relativas en Harrod-Domar y CES

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Participación laboral siempre constante | conceptual_swap | high | La participación del trabajo es independiente de $s$ y $n$ | Verifique la forma funcional: en $Y=(a\sqrt{K}+\sqrt{L})^2$ la participación laboral $1-a\sqrt{s/n}$ sí depende de $n$ y de $s$, a diferencia de Cobb-Douglas. |
| `D-C09-02` | Determinación única en proporciones fijas | conceptual_swap | high | En $r=a/b$ los precios $w$ y $q$ son únicos | Recuerde que en la esquina de Harrod-Domar $r=a/b$ ambos factores son escasos en dosis compuesta y solo se determina la suma $aq/p+bw/p=1$. |
| `D-C09-03` | Invierte factor redundante en Harrod | conceptual_swap | high | Si $r>a/b$, el trabajo es redundante y $w=0$ | Identifique el factor abundante: cuando $r>a/b$ sobra capital respecto al trabajo, por lo que $q=0$ y todo el producto se imputa al trabajo ($w=p/b$). |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | Rendimientos constantes a escala y competencia perfecta en factores | Sin competencia perfecta la pendiente de la isocuanta no iguala la razón $w/q$. | - |

---

### [Hab-05] Crecimiento con Cambio Tecnológico Neutral (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 22: Crecimiento con Cambio Tecnológico Neutral
- **Prerequisites:** C-08
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 22)

#### Description & Cognitive Model
Cálculo de tasas asintóticas de crecimiento del capital $K$, producto $Y$, razón $K/L$ y coeficiente $K/Y$ bajo progreso neutral $Y=e^{gt}K^aL^{1-a}$ con $b=1-a$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Omite efecto compuesto del ahorro | skipped_step | high | $K$ crece a tasa $n+g$ | Divida la tasa de cambio técnico $g$ entre $b=1-a$: el mayor producto genera ahorro adicional que eleva el crecimiento de $K$ a $n+g/b$. |
| `D-Hab05-02` | Iguala tasa de Y y de K | skipped_step | high | $Y$ crece a tasa $n+g/b$ | Pondera el crecimiento de $K$ por su elasticidad $a$: $Y=e^{gt}K^aL^{1-a}$ crece a tasa $g+a(n+g/b)+(1-a)n=n+ag/b$. |
| `D-Hab05-03` | Supone K/L estacionario | conceptual_swap | high | $K/L$ converge a un valor finito $r^*$ | Observe que con $A(t)=e^{gt}$ la relación $K/L$ crece indefinidamente a tasa $g/b$ porque el ahorro compuesto supera el crecimiento laboral $n$. |
| `D-Hab05-04` | Anula crecimiento de K/Y | conceptual_swap | high | El coeficiente $K/Y$ es constante | Reste las tasas asintóticas de $K$ y $Y$: $(n+g/b)-(n+ag/b)=(1-a)g/b=g$, por lo que el coeficiente $K/Y$ crece a tasa $g$. |
| `D-Hab05-05` | Usa factor b en lugar de 1/b | conceptual_swap | high | $K/L$ crece a tasa $bg$ | Al elevar la solución exponencial de $K(t)^b$ a la potencia $1/b$, el exponente $(nb+g)t$ se divide por $b$, dando $n+g/b$. |
| `D-Hab05-06` | Cambia participación laboral | conceptual_swap | high | La participación laboral sube con $t$ | Recuerde que en Cobb-Douglas la participación relativa del trabajo permanece constante en $1-a$ aun cuando $w/p$ y $K/L$ crezcan sin límite. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | Progreso técnico neutral de Hicks-Solow $A(t)=e^{gt}$ con $b=1-a>0$ | Si $b\le 0$, desaparecen los rendimientos decrecientes del capital. | - |

---

### [C-10] Oferta Elástica de Trabajo (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 24: Oferta Elástica de Trabajo
- **Prerequisites:** C-09
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 24)

#### Description & Cognitive Model
Efecto de una oferta laboral sensible al salario real $L=L_0 e^{nt}(w/p)^h$ frente al caso general $L=G(t,w/p)$ sobre la ecuación dinámica (6a)-(6b) y el equilibrio $r^*$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C10-01` | Cree que elasticidad h siempre cambia r* | conceptual_swap | high | Con $h>0$ en (14), $r^*$ necesariamente cambia | Factorice $(sF(r,1)-nr)(1+ah/r)^{-1}$ en la ecuación (6a): $\dot{r}=0$ ocurre exactamente en el mismo punto donde $sF(r,1)=nr$. |
| `D-C10-02` | Generaliza invarianza a cualquier G | conceptual_swap | high | Toda función $L=G(t,w/p)$ deja $r^*$ intacto | Compare con la condición general $sF(r,1)=\frac{r}{G}\frac{\partial G}{\partial t}$: solo si $\frac{1}{G}\frac{\partial G}{\partial t}=n$ el equilibrio permanece inalterado. |
| `D-C10-03` | Omite término salarial en dinámica | conceptual_swap | high | La ecuación (6a) es $\dot{r}=sF(r,1)-nr$ | Diferencie $L=L_0 e^{nt}(w/p)^h$ respecto al tiempo para incluir la respuesta $-h\dot{w}/w$ dentro de la tasa de variación de $r=K/L$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C10-01` | - | Salarios reales por debajo del límite físico de la fuerza laboral | A salarios muy altos la oferta (14) viola el tope máximo de población activa. | - |

---

### [Hab-06] Ahorro Variable e Impuesto Proporcional (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 26: Ahorro Variable e Impuesto Proporcional
- **Prerequisites:** C-09
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 26)

#### Description & Cognitive Model
Análisis de estabilidad con tasa de ahorro dependiente del rendimiento $s(r)$ en $\dot{r}=s(r)F(r,1)-nr$ y cálculo de la tasa efectiva $s+(v-s)t$ bajo impuesto proporcional $t$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Invierte dirección del ahorro con r | skipped_step | high | $s(r)$ crece al aumentar $r$ | Relacione ahorro con rendimiento: si el ahorro depende positivamente de $q/p$ y el producto marginal cae con $r$, entonces $s(r)$ es decreciente en $r$. |
| `D-Hab06-02` | Predice estado estacionario con s(r)=0 | conceptual_swap | high | Si $s(r)=0$ para $r$ grande, $r$ queda estacionario | Recuerde que la fuerza laboral sigue creciendo a tasa $n$; si la inversión cae a cero, $r=K/L$ disminuye inevitablemente hacia $r^*$. |
| `D-Hab06-03` | Omite ahorro privado gravado | skipped_step | high | $s_{eff}=s+vt$ | Aplique la tasa $s$ sobre el ingreso disponible $(1-t)Y$: $\dot{K}=s(1-t)Y+vtY=(s+(v-s)t)Y$, restando el ahorro privado desplazado. |
| `D-Hab06-04` | Supone impuesto siempre eleva ahorro | conceptual_swap | high | Todo impuesto $t>0$ aumenta $s_{eff}$ | Compare la propensión pública a invertir $v$ con la privada $s$: el ahorro efectivo solo aumenta si $v>s$ y disminuye si $v<s$. |
| `D-Hab06-05` | Confunde consumo fiscal con inversión | conceptual_swap | high | Si $v=0$, entonces $s_{eff}=s$ | Sustituya $v=0$ en $s+(v-s)t$: si toda la recaudación se consume, la tasa efectiva de ahorro cae de $s$ a $s(1-t)$. |
| `D-Hab06-06` | Mantiene r* constante con impuesto | conceptual_swap | high | El impuesto proporcional no desplaza $r^*$ | Observe que $s_{eff}F(r,1)$ expande o contrae verticalmente la curva de ahorro, desplazando la intersección con $nr$ hacia un nuevo $r^*$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Impuesto proporcional a la renta con fracción constante $v\in[0,1]$ invertida | Impuestos no proporcionales distorsionan la curva $sF(r,1)$ de manera no uniforme. | - |

---

### [C-11] Población Endógena y Trampa de Estancamiento (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 28: Población Endógena y Trampa de Estancamiento
- **Prerequisites:** Hab-06
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 28)

#### Description & Cognitive Model
Equilibrios múltiples en $\dot{r}=sF(r,1)-n(r)r$ cuando la tasa demográfica $n(r)$ responde al ingreso per cápita: estabilidad local en $r_1$ y umbral crítico inestable $r_2$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C11-01` | Invierte estabilidad de r1 y r2 | conceptual_swap | high | $r_1$ es inestable y $r_2$ es estable | Verifique el signo de $\dot{r}=sF(r,1)-n(r)r$: debajo de $r_2$ la curva $n(r)r$ supera a $sF(r,1)$ ($\dot{r}<0$), devolviendo al sistema hacia $r_1$. |
| `D-C11-02` | Requiere rendimientos crecientes para trampa | conceptual_swap | high | Sin rendimientos crecientes no existe trampa | Note que aquí la función de producción mantiene rendimientos constantes a escala; la trampa surge únicamente de la no linealidad demográfica $n(r)$. |
| `D-C11-03` | Descarta crecimiento sostenido sobre r2 | conceptual_swap | high | Si $r_0>r_2$, la economía regresa a $r_1$ | Analice la región $r>r_2$: allí $sF(r,1)>n(r)r$, por lo que $\dot{r}>0$ y un gran impulso inicial de inversión desencadena expansión autosostenida. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C11-01` | - | Tasa demográfica $n(r)$ depende solo del ingreso per cápita $F(r,1)$ | Si $n$ es exógeno constante, el rayo $nr$ es lineal y desaparece el umbral $r_2$. | - |

---

### [Hab-07] Salarios Rígidos y Brecha de Empleo (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 29: Salarios Rígidos y Brecha de Empleo
- **Prerequisites:** C-10
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 29)

#### Description & Cognitive Model
Determinación de la tasa de crecimiento del empleo $\frac{\dot{L}}{L}=\frac{s}{\bar{r}}F(\bar{r},1)$ ante un salario real rígido $\bar{w}/p$ y diagnóstico de desempleo o escasez frente a $n$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Desempleo cuando pendiente supera n | skipped_step | high | Si $(s/\bar{r})F(\bar{r},1)>n$, surge desempleo | Compare el crecimiento del empleo con el de la población activa $n$: si el empleo crece más rápido que $n$, se produce escasez laboral, no desempleo. |
| `D-Hab07-02` | Permite variar r con salario rígido | skipped_step | high | Aunque $\bar{w}/p$ sea fijo, $r$ varía libremente | Use la condición marginal $\partial F/\partial L=\bar{w}/p$: como el producto marginal depende solo de $r$, fijar $\bar{w}/p$ fija necesariamente $r=\bar{r}$. |
| `D-Hab07-03` | Invierte relación con r punto | conceptual_swap | high | Si $\bar{r}$ corresponde a $\dot{r}>0$, hay desempleo | Observe en el diagrama que $\dot{r}<0$ equivale a $sF(\bar{r},1)<n\bar{r}$, es decir, $(s/\bar{r})F(\bar{r},1)<n$, lo cual genera desempleo creciente. |
| `D-Hab07-04` | Omite divisor r barra en tasa | conceptual_swap | high | El empleo crece a tasa $sF(\bar{r},1)$ | Sustituya $K=\bar{r}L$ en $\dot{K}=sF(K,L)$ para obtener $\bar{r}\dot{L}=sF(\bar{r}L,L)$ y divida entre $\bar{r}L$ para hallar $\dot{L}/L$. |
| `D-Hab07-05` | Supone empleo fijo en nivel inicial | conceptual_swap | high | Con salario rígido, $\dot{L}=0$ | Recuerde que la acumulación de capital $sY$ permite expandir el empleo exponencialmente a tasa $(s/\bar{r})F(\bar{r},1)$ manteniendo constante la razón $\bar{r}$. |
| `D-Hab07-06` | Ignora flexibilidad al alza | conceptual_swap | high | La escasez laboral mantiene $\bar{w}/p$ fijo | Distinga que cuando $(s/\bar{r})F(\bar{r},1)>n$ la escasez de mano de obra presionará eventualmente al salario real para volverse flexible al alza. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Salario real fijado exógenamente en $\bar{w}/p$ por rigidez a la baja | Si el salario fuera flexible, el mercado laboral se vaciaría con $L=L_0 e^{nt}$. | - |

---

### [C-12] Preferencia por Liquidez y Trampa Monetaria (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 30: Preferencia por Liquidez y Trampa Monetaria
- **Prerequisites:** C-08, Hab-07
- **Recommended Modalities:** adversarial_break, unstructured_model, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 30)

#### Description & Cognitive Model
Interacción entre demanda de dinero $\bar{M}=Q(F(K,L),F_K(K,L))$ y capital en uso $K(t)$, subutilización en trampa de liquidez y límite del modelo neoclásico puramente real

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C12-01` | Mantiene K siempre plenamente empleado | conceptual_swap | high | Todo el capital acumulado se utiliza en (15) | Distinga el stock disponible acumulado del capital en uso $K(t)$ resuelto por $\bar{M}=Q(Y,q/p)$: la diferencia mide exceso de oferta o demanda de capital. |
| `D-C12-02` | Trampa eleva utilización de capital | conceptual_swap | high | En la trampa de liquidez se sobreutiliza el capital | Analogamente al salario rígido, si la tasa de interés queda rígida por encima del nivel de equilibrio, el resultado es la subutilización del stock de capital. |
| `D-C12-03` | Prescinde de dinámica monetaria | conceptual_swap | high | El modelo real basta aun con preferencia por liquidez | Reconozca que cuando los agentes eligen entre efectivo y capital físico, el precio $p$ y los factores monetarios inciden directamente en inversión y consumo. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C12-01` | - | Cantidad nominal de dinero $\bar{M}$ dada y demanda de saldos dependiente de $Y$ y $q/p$ | Si la demanda de dinero fuera independiente de $q/p$, se desconectaría del alquiler real. | - |

---
