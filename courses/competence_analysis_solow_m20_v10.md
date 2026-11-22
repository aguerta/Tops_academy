# Cognitive Task Analysis (CTA): Solow M20 V10

- **Course ID:** `solow_m20_v10`
- **Macro-Competency:** Dominio y aplicación analítica integral de Solow M20 V10
- **Structure:** 17 total competencies (1 Facts, 10 Concepts, 6 Skills) with 80 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `H-01` | Función de Producción Per Cápita | Fact | Understand | Unidad 2: Función de Producción Per Cápita | - | 3 |
| `C-03` | Supuestos Base del Modelo Neoclásico | Concept | Evaluate | Unidad 4: Supuestos Base del Modelo Neoclásico | - | 3 |
| `Hab-01` | Ecuación Fundamental de Solow | Skill | Evaluate | Unidad 3: Ecuación Fundamental de Solow | H-01, C-03 | 10 |
| `C-01` | Análisis Cualitativo y Estado Uniforme | Concept | Evaluate | Unidad 4: Análisis Cualitativo y Estado Uniforme | Hab-01 | 3 |
| `C-02` | Cambio Tecnológico Secular | Concept | Analyze | Unidad 4: Cambio Tecnológico Secular | C-01 | 3 |
| `C-04` | Estabilidad y Equilibrios Múltiples | Concept | Evaluate | Unidad 7: Estabilidad y Equilibrios Múltiples | Hab-01 | 3 |
| `Hab-02` | Solución Explícita Cobb-Douglas | Skill | Evaluate | Unidad 5: Solución Cuantitativa Cobb-Douglas | Hab-01, C-01, C-04 | 10 |
| `C-05` | Caso Proporciones Fijas (Harrod-Domar) | Concept | Analyze | Unidad 11: Caso Proporciones Fijas (Harrod-Domar) | C-04 | 3 |
| `Hab-05` | Análisis Modelo CES Cuadrático | Skill | Evaluate | Unidad 14: Análisis Modelo CES Cuadrático | Hab-01, C-04 | 6 |
| `C-06` | Precios Competitivos y Arbitraje | Concept | Analyze | Unidad 16: Precios Competitivos de Factores | C-03, Hab-01 | 6 |
| `C-08` | Isocuantas y Precios de Factores | Concept | Analyze | Unidad 19: Isocuantas y Precios de Factores | C-06 | 3 |
| `Hab-06` | Participación Relativa del Trabajo | Skill | Evaluate | Unidad 21: Participación Relativa del Trabajo | C-06, C-08 | 6 |
| `Hab-07` | Cambio Tecnológico Neutral | Skill | Evaluate | Unidad 22: Cambio Tecnológico Neutral | C-06 | 6 |
| `C-09` | Oferta Laboral Elástica | Concept | Evaluate | Unidad 23: Oferta Laboral Elástica | C-06 | 3 |
| `C-10` | Ahorro Variable e Impuestos | Concept | Evaluate | Unidad 25: Ahorro Variable e Impuestos | C-06 | 3 |
| `C-11` | Población Endógena y Trampa | Concept | Evaluate | Unidad 27: Población Endógena y Trampa | C-08 | 3 |
| `Hab-08` | Rigidez Salarial y Liquidez | Skill | Evaluate | Unidad 29: Rigidez Salarial y Liquidez | C-06, C-08 | 6 |

---

## Detailed Competency Specifications

### [H-01] Función de Producción Per Cápita (Fact)

- **Bloom Level:** Understand
- **Session:** Unidad 2: Función de Producción Per Cápita
- **Prerequisites:** None
- **Recommended Modalities:** fill_in_the_blank, multiple_select, concept_matching
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
La función neoclásica linealmente homogénea $Q=f(K,L)$ se expresa en forma intensiva como $Q=L\phi(k)$ con $k\equiv K/L$, $\phi'(k)>0$ y $\phi''(k)<0$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Invierte relación capital-trabajo | conceptual_swap | high | Define $k \equiv L/K$ | Recuerde que $k\equiv K/L$ mide el capital disponible por trabajador; al factorizar $L$ por homogeneidad lineal resulta $Q=Lf(K/L,1)=L\phi(k)$. |
| `D-H01-02` | Segunda derivada positiva | conceptual_swap | high | Asume $\phi''(k) > 0$ | Dado que $f_{KK}=\phi''(k)/L<0$ por rendimientos decrecientes del capital, la función intensiva $\phi(k)$ es estrictamente cóncava con $\phi''(k)<0$. |
| `D-H01-03` | Proporción fija Domar | conceptual_swap | high | Supone $Q=\rho K$ sin mano de obra $L$ | A diferencia del modelo de Domar con proporciones fijas, Solow permite combinar $K$ y $L$ en proporciones variables mediante $Q=f(K,L)$. |

---

### [C-03] Supuestos Base del Modelo Neoclásico (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Supuestos Base del Modelo Neoclásico
- **Prerequisites:** None
- **Recommended Modalities:** multiple_select, adversarial_break, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 4)

#### Description & Cognitive Model
Estructura del modelo neoclásico de crecimiento con un bien compuesto $Y=F(K,L)$ de rendimientos constantes a escala, ahorro $sY$, crecimiento laboral $L(t)=L_0 e^{nt}$ y pleno empleo.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Proporciones fijas | conceptual_swap | high | $Y=\min(K/a,L/b)$ | Distinga el modelo neoclásico de Solow, que permite sustitución continua entre $K$ y $L$, del caso Harrod-Domar de proporciones fijas. |
| `D-C03-02` | Rendimientos decrecientes globales | conceptual_swap | high | $F(\lambda K,\lambda L)<\lambda Y$ | Recuerde que Solow supone ausencia de recursos no aumentables como la tierra, garantizando homogeneidad de grado uno en capital y trabajo. |
| `D-C03-03` | Ahorro sobre capital | conceptual_swap | high | $\dot{K}=sK$ | La inversión neta $\dot{K}$ proviene de ahorrar una fracción constante $s$ del producto neto $Y=F(K,L)$, nunca del stock de capital existente. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | Homogeneidad de primer grado $F(\lambda K,\lambda L)=\lambda F(K,L)$ | Sin rendimientos constantes a escala no puede reducirse el sistema a la razón $r=K/L$. | - |
| `A-C03-02` | - | Pleno empleo continuo de trabajo $L(t)=L_0 e^{nt}$ y capital $K(t)$ | Si los factores no se emplean plenamente, la identidad $\dot{K}=sF(K,L_0 e^{nt})$ deja de cumplirse. | - |

---

### [Hab-01] Ecuación Fundamental de Solow (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Ecuación Fundamental de Solow
- **Prerequisites:** H-01, C-03
- **Recommended Modalities:** proof_dag, open_symbolic, adversarial_break, fill_in_the_blank
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3), `solow1956.pdf` (page 6)

#### Description & Cognitive Model
Derivación de la ecuación diferencial fundamental del modelo de Solow ($\dot{k}=s\phi(k)-\lambda k$ o $\dot{r}=sF(r,1)-nr$) para la razón capital-trabajo $k=r=K/L$ mediante diferenciación del producto y homogeneidad de grado uno.

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Omite regla del producto | skipped_step | high | Usa $\dot{K}=L\dot{k}$ ignorando $\dot{L}$ | Al diferenciar $K=kL$ respecto al tiempo debe aplicar la regla del producto completa $\dot{K}=L\dot{k}+k\dot{L}$ antes de sustituir $\dot{L}=\lambda L$. |
| `D-Hab01-07` | Signo positivo en nr | skipped_step | high | $\dot{r}=sF(r,1)+nr$ | Al diferenciar $r=K/L$ resulta $\dot{r}/r=\dot{K}/K-\dot{L}/L$; como el trabajo diluye el capital por trabajador, el término $nr$ entra restando. |
| `D-Hab01-02` | Signo positivo en dilución | skipped_step | high | Escribe $\dot{k}=s\phi(k)+\lambda k$ | Al despejar $\dot{k}$ de $L\dot{k}+k\lambda L=sL\phi(k)$, el término de crecimiento laboral $\lambda k$ pasa restando pues diluye el capital por trabajador. |
| `D-Hab01-08` | Omite factor r en dilución | skipped_step | high | $\dot{r}=sF(r,1)-n$ | Multiplique ambos lados de $\dot{r}/r=sF(r,1)/r-n$ por $r$ para obtener correctamente la dilución $nr$ en unidades de capital por trabajador. |
| `D-Hab01-03` | Olvida dividir por L | conceptual_swap | high | Deja $L$ multiplicando en $\dot{k}=sL\phi(k)-\lambda k$ | Divida ambos miembros de $L\dot{k}+k\lambda L=sL\phi(k)$ entre el factor común positivo $L$ para obtener la ecuación en términos exclusivamente de $k$. |
| `D-Hab01-09` | Falla en homogeneidad | conceptual_swap | high | $\dot{r}=sF(K,1)-nr$ | Use la homogeneidad de grado uno de $F(K,L)$ dividiendo ambos argumentos por $L$ para expresar la función como $L F(r,1)$ antes de simplificar. |
| `D-Hab01-04` | Aplica ahorro solo a k | conceptual_swap | high | Escribe $\dot{k}=sk-\lambda k$ | La inversión neta $\dot{K}=sQ$ es una fracción del producto $Q=L\phi(k)$, no del stock de capital $K$; por ello el primer término es $s\phi(k)$. |
| `D-Hab01-10` | Confunde L con L0 | conceptual_swap | high | $\dot{r}=sL_0 F(r,1)-nr$ | Divida ambos miembros de $(\dot{r}+nr)L_0 e^{nt}=s L_0 e^{nt}F(r,1)$ por el factor común completo $L_0 e^{nt}$ para eliminar toda escala inicial. |
| `D-Hab01-05` | Confunde tasa lambda con nivel L | conceptual_swap | high | Escribe $\dot{k}=s\phi(k)-Lk$ | Sustituya $\dot{L}=\lambda L$ usando la tasa exponencial constante $\lambda>0$, de modo que tras dividir por $L$ quede el parámetro $\lambda$ y no la variable $L$. |
| `D-Hab01-06` | Invierte signo de la ecuación | conceptual_swap | high | Escribe $\dot{k}=\lambda k - s\phi(k)$ | La acumulación de capital por trabajador aumenta con el ahorro $s\phi(k)$ y disminuye con el crecimiento laboral $\lambda k$, resultando $s\phi(k)-\lambda k$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Tasa de ahorro marginal $s$ constante y crecimiento exponencial de la fuerza laboral $\dot{L}/L=\lambda>0$ | Si $s$ o $\lambda$ varían con $t$, la ecuación diferencial deja de ser autónoma en $k$. | - |
| `A-Hab01-02` | - | La fuerza laboral es estrictamente positiva $L(t)=L_0 e^{nt}>0$ | Si $L(t)=0$, la razón $r=K/L$ y la división por $L$ quedan indefinidas. | - |

---

### [C-01] Análisis Cualitativo y Estado Uniforme (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Análisis Cualitativo y Estado Uniforme
- **Prerequisites:** Hab-01
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
Análisis de la línea de fase $\dot{k}=s\phi(k)-\lambda k$: intersección de $s\phi(k)$ y $\lambda k$ en $\bar{k}>0$ con pendiente negativa estable y crecimiento uniforme a tasa $\lambda$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Equilibrio con pendiente positiva | conceptual_swap | high | Afirma que $\bar{k}$ es estable si $d\dot{k}/dk > 0$ | Cuando la línea de fase tiene pendiente negativa en $\bar{k}$, $\dot{k}>0$ para $k<\bar{k}$ y $\dot{k}<0$ para $k>\bar{k}$, garantizando convergencia hacia $\bar{k}$. |
| `D-C01-02` | Confunde estado uniforme con estacionario | conceptual_swap | high | Sostiene que $K$, $Q$ e inversión dejan de crecer en $\bar{k}$ | En el estado uniforme la razón $k=K/L$ permanece constante en $\bar{k}$, pero $K$, $L$, $Q$ y la inversión neta crecen todos a la tasa idéntica $\lambda>0$. |
| `D-C01-03` | Curva s*phi(k) no parte del origen | conceptual_swap | high | Dibuja $s\phi(k)>0$ cuando $k=0$ | Como el capital $K$ es un factor indispensable de producción, si $K=0$ entonces $k=0$ y $Q=0$, por lo que $\phi(0)=0$ y $s\phi(k)$ parte del origen. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | El capital $K$ es indispensable ($\phi(0)=0$) y existe $k>0$ tal que $s\phi(k)>\lambda k$ | Sin esta condición las curvas $s\phi(k)$ y $\lambda k$ no se intersecan en un equilibrio positivo $\bar{k}>0$. | - |

---

### [C-02] Cambio Tecnológico Secular (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 4: Cambio Tecnológico Secular
- **Prerequisites:** C-01
- **Recommended Modalities:** adversarial_break, multiple_select, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
Con progreso tecnológico $Q=T(t)f(K,L)$ donde $dT/dt>0$, la curva $s\phi(k)$ se desplaza hacia arriba generando valores crecientes de $\bar{k}$ y productividad.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Desplazamiento hacia abajo | conceptual_swap | high | Afirma que $dT/dt>0$ desplaza $s\phi(k)$ hacia abajo | El término multiplicativo creciente $T(t)$ aumenta el producto para cada $K$ y $L$, desplazando $s\phi(k)$ hacia arriba y elevando la intersección $\bar{k}$ con $\lambda k$. |
| `D-C02-02` | Rota el rayo de dilución | conceptual_swap | high | Cambia la pendiente del rayo $\lambda k$ al variar $T(t)$ | El progreso tecnológico $T(t)$ multiplica la función de producción $f(K,L)$ afectando la curva $s\phi(k)$, mientras el rayo laboral $\lambda k$ depende solo de $\lambda$. |
| `D-C02-03` | Mantiene k constante en el tiempo | conceptual_swap | high | Supone que $\bar{k}$ no cambia con $T(t)$ creciente | Con mejoramiento tecnológico continuo se produce una sucesión de estados uniformes con intersecciones más altas, aumentando el capital por trabajador $\bar{k}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | La tecnología $T(t)$ es una función creciente del tiempo ($dT/dt>0$) multiplicativa en $Q=T(t)f(K,L)$ | Si $dT/dt=0$, la función de producción es invariante en el tiempo y $\bar{k}$ permanece fijo. | - |

---

### [C-04] Estabilidad y Equilibrios Múltiples (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 7: Estabilidad y Equilibrios Múltiples
- **Prerequisites:** Hab-01
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 7)

#### Description & Cognitive Model
Análisis gráfico de $\dot{r}=sF(r,1)-nr$: equilibrio único estable $r^*$, equilibrios múltiples con umbral inestable $r_2$ y ausencia de estado estacionario.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Invierte signo de ajuste | conceptual_swap | high | Si $r>r^*$ entonces $\dot{r}>0$ | Observe en la Figura I que a la derecha de $r^*$ el rayo $nr$ supera a $sF(r,1)$, por lo que $\dot{r}=sF(r,1)-nr<0$ y $r$ decrece hacia $r^*$. |
| `D-C04-02` | Estabilidad universal | conceptual_swap | high | Todo equilibrio $r_i$ en Figura II es estable | Compare las pendientes en cada cruce de la Figura II: en $r_2$ la curva $sF(r,1)$ corta desde abajo a $nr$, haciendo $r_2$ inestable ante perturbaciones. |
| `D-C04-03` | Cruce garantizado | conceptual_swap | high | Siempre existe $r^*>0$ con $sF(r^*,1)=nr^*$ | Considere la Figura III: si $s_1 F^1(r,1)>nr$ para todo $r$, $r$ crece sin límite; si $s_2 F^2(r,1)<nr$, el ingreso por trabajador cae continuamente. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | Capital inicial positivo $K_0>0$ cuando $F(0,1)=0$ | Si $K_0=0$ y $F(0,1)=0$, la economía permanece atrapada en $r=0$ sin producción ni acumulación. | - |

---

### [Hab-02] Solución Explícita Cobb-Douglas (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Solución Cuantitativa Cobb-Douglas
- **Prerequisites:** Hab-01, C-01, C-04
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 5), `solow1956.pdf` (page 13)

#### Description & Cognitive Model
Integración explícita de la dinámica de Solow con función Cobb-Douglas ($\dot{k}+\lambda k=sk^\alpha$ vía Bernoulli $z=k^{1-\alpha}$ o $\dot{K}=sK^a(L_0 e^{nt})^{1-a}$) para obtener la trayectoria temporal, el estado estacionario $r^*=(s/n)^{1/(1-a)}$ y la razón $K/Y=s/n$.

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Cambio de variable incorrecto | skipped_step | high | Usa $z=k^\alpha$ para linealizar $\dot{k}+\lambda k=sk^\alpha$ | Para una ecuación de Bernoulli $\dot{k}+Rk=Tk^m$ con $m=\alpha$, la sustitución linealizante correcta es $z=k^{1-m}=k^{1-\alpha}$, no $k^\alpha$. |
| `D-Hab02-07` | Exponente sin invertir | skipped_step | high | $r^*=(s/n)^{1-a}$ | Al igualar $sr^a=nr$ se obtiene $r^{1-a}=s/n$; debe elevar ambos miembros al recíproco $1/(1-a)$ para despejar $r^*$ correctamente. |
| `D-Hab02-02` | Omite factor (1-alpha) al linealizar | skipped_step | high | Escribe $\frac{dz}{dt}+\lambda z = s$ | Al diferenciar $z=k^{1-\alpha}$ surge $\dot{z}=(1-\alpha)k^{-\alpha}\dot{k}$, por lo que tanto $\lambda z$ como el término constante $s$ quedan multiplicados por $(1-\alpha)$. |
| `D-Hab02-08` | Invierte razón s/n | skipped_step | high | $r^*=(n/s)^{1/(1-a)}$ | Verifique el signo económico: una mayor tasa de ahorro $s$ y menor crecimiento poblacional $n$ elevan el capital por trabajador $r^*=(s/n)^{1/(1-a)}$. |
| `D-Hab02-03` | Invierte razón en el límite | conceptual_swap | high | Concluye $\bar{k}=(\lambda/s)^{\frac{1}{1-\alpha}}$ | Cuando $t\to\infty$, $k^{1-\alpha}\to b/a = (1-\alpha)s / [(1-\alpha)\lambda] = s/\lambda$; mayor tasa de ahorro $s$ eleva $\bar{k}$ y mayor $\lambda$ lo reduce. |
| `D-Hab02-09` | Error en Y/L límite | conceptual_swap | high | $Y/L \to (s/n)^{1/(1-a)}$ | Recuerde que $Y/L=r^a$ en Cobb-Douglas; al sustituir $r^*=(s/n)^{1/(1-a)}$ se obtiene el producto por trabajador límite $(s/n)^{a/(1-a)}$. |
| `D-Hab02-04` | Exponente directo en lugar de recíproco | conceptual_swap | high | Despeja $\bar{k}=(s/\lambda)^{1-\alpha}$ | Para despejar $k$ de $k^{1-\alpha}=s/\lambda$, debe elevar ambos miembros al exponente recíproco $1/(1-\alpha)$ obteniendo $(s/\lambda)^{1/(1-\alpha)}$. |
| `D-Hab02-10` | Exponente erróneo en K(t) | conceptual_swap | high | $K(t)=[K_0^b+\frac{s}{n}L_0^b(e^{nbt}-1)]^b$ | Al integrar $\dot{K}K^{-a}=sL_0^b e^{nbt}$ se obtiene $K^b$, por lo que para recuperar $K(t)$ debe elevarse la expresión resultante a $1/b$. |
| `D-Hab02-05` | Signo positivo en la exponencial | conceptual_swap | high | Usa $e^{+(1-\alpha)\lambda t}$ en la solución $z(t)$ | En $\dot{z}+az=b$ con $a=(1-\alpha)\lambda>0$, la parte transitoria decae como $e^{-at}=e^{-(1-\alpha)\lambda t}\to 0$ cuando $t\to\infty$. |
| `D-Hab02-06` | Omite condición inicial k(0) | conceptual_swap | high | Escribe $k(t)^{1-\alpha}=\frac{s}{\lambda}e^{-(1-\alpha)\lambda t}+\frac{s}{\lambda}$ | La constante arbitraria de la solución lineal se determina evaluando en $t=0$: $z(0)-s/\lambda = k(0)^{1-\alpha}-s/\lambda$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Función Cobb-Douglas $Q=K^\alpha L^{1-\alpha}$ con $\alpha\in(0,1)$ y $\lambda>0$ | Si $\alpha\ge 1$ o $\lambda\le 0$, $(1-\alpha)\lambda\le 0$ y la trayectoria no converge a un estado uniforme finito. | - |
| `A-Hab02-02` | - | Participación del capital $a\in(0,1)$ con $b=1-a>0$ | Si $a\ge 1$, desaparecen los rendimientos marginales decrecientes y el equilibrio estacionario único. | - |

---

### [C-05] Caso Proporciones Fijas (Harrod-Domar) (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 11: Caso Proporciones Fijas (Harrod-Domar)
- **Prerequisites:** C-04
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 11)

#### Description & Cognitive Model
Dinámica con función Leontief $Y=\min(K/a,L/b)$: tasa garantizada $s/a$ frente a tasa natural $n$, redundancia laboral o de capital y zona intermedia de equilibrio.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Invierte redundancia | conceptual_swap | high | Si $n>s/a$ sobra capital | Cuando la tasa natural $n$ supera a la garantizada $s/a$, $r$ cae por debajo de $a/b$, el capital es el cuello de botella y aparece desempleo laboral. |
| `D-C05-02` | Tasa garantizada errónea | conceptual_swap | high | La tasa garantizada es $s/b$ | La tasa garantizada de Harrod depende del coeficiente de aceleración del capital $a$, siendo $s/a$ la pendiente inicial de $s\min(r/a,1/b)$. |
| `D-C05-03` | Proporción empleada inversa | conceptual_swap | high | Fracción de capital empleada $s/(an_3)$ | En equilibrio con exceso de capital ($r^*=s/(n_3 b)>a/b$), la fracción empleada es $(a/b)/r^*=an_3/s<1$, mientras crece la capacidad ociosa. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Coeficientes técnicos fijos $a>0$ y $b>0$ sin sustitución | Si se permite sustitución factorial en $[r_{\min},r_{\max}]$, desaparece el filo de navaja en esa zona. | - |

---

### [Hab-05] Análisis Modelo CES Cuadrático (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 14: Análisis Modelo CES Cuadrático
- **Prerequisites:** Hab-01, C-04
- **Recommended Modalities:** open_symbolic, unstructured_model, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 14)

#### Description & Cognitive Model
Resolución del caso $Y=(a\sqrt{K}+\sqrt{L})^2$ con $\dot{r}=s(a\sqrt{r}+1)^2-nr$: condición de estabilidad $sa^2<n$, equilibrio $r^*$ e ingreso límite por trabajador.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Desigualdad de equilibrio inversa | skipped_step | high | Existe equilibrio si $sa^2>n$ | Cuando $sa^2>n$, la curva $s(a\sqrt{r}+1)^2$ crece más rápido que $nr$ y nunca lo corta, generando crecimiento ilimitado de $r$ sin estado estacionario. |
| `D-Hab05-02` | Signo erróneo en r* | skipped_step | high | $r^*=(1/(\sqrt{n/s}+a))^2$ | Al resolver $\sqrt{s}(a\sqrt{r}+1)=\sqrt{nr}$ despejando $\sqrt{r}$ resulta $\sqrt{r}(\sqrt{n/s}-a)=1$, con signo negativo antes de $a$. |
| `D-Hab05-03` | Omite elevar al cuadrado | conceptual_swap | high | $r^*=1/(\sqrt{n/s}-a)$ | Recuerde que la ecuación linealizada resuelve $\sqrt{r^*}=1/(\sqrt{n/s}-a)$; debe elevar al cuadrado para obtener la razón capital-trabajo $r^*$. |
| `D-Hab05-04` | Confunde ingreso límite | conceptual_swap | high | $Y/L \to (1-a\sqrt{s/n})^2$ | Sustituya $\sqrt{r^*}=1/(\sqrt{n/s}-a)$ en $Y/L=(a\sqrt{r^*}+1)^2$ para verificar que el ingreso límite por trabajador es $1/(1-a\sqrt{s/n})^2$. |
| `D-Hab05-05` | Raíz negativa en solución | conceptual_swap | high | $A=a+\sqrt{n/s}$ y $B=a-\sqrt{n/s}$ | En la ecuación (8), el factor que se anula cuando $sa^2<n$ es $A=a-\sqrt{n/s}<0$, mientras $B=a+\sqrt{n/s}>0$ permanece positivo. |
| `D-Hab05-06` | Origen como equilibrio | conceptual_swap | high | $sF(0,1)=0$ | En $Y=(a\sqrt{K}+\sqrt{L})^2$ es posible producir solo con trabajo, por lo que $sF(r,1)$ inicia en altura $s>0$ cuando $r=0$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | Parámetro de sustitución $0<p<1$ (específicamente $p=1/2$) y $sa^2<n$ | Si $p\ge 1$, las isocuantas pierden convexidad estricta; si $sa^2>n$, no existe equilibrio estacionario. | - |

---

### [C-06] Precios Competitivos y Arbitraje (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 16: Precios Competitivos de Factores
- **Prerequisites:** C-03, Hab-01
- **Recommended Modalities:** proof_dag, multiple_select, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 16)

#### Description & Cognitive Model
Determinación competitiva del salario real $w/p=\partial F/\partial L$ y renta real $q/p=\partial F/\partial K$ que vacían los mercados factoriales dependiendo solo de $r$, junto con la condición de arbitraje perfecto $i(t)=q(t)/p(t)+\dot{p}(t)/p(t)$ y valor presente del capital.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Dependencia de escala | conceptual_swap | high | $w/p$ depende de $K$ y $L$ por separado | Por homogeneidad de grado uno de $F(K,L)$, sus derivadas parciales son homogéneas de grado cero y dependen únicamente de la razón $r=K/L$. |
| `D-C06-04` | Iguala i con q/p | conceptual_swap | high | $i(t)=q(t)/p(t)$ siempre | Sume la tasa de variación del precio $\dot{p}(t)/p(t)$ a la renta real $q(t)/p(t)$ cuando el nivel de precios no es constante. |
| `D-C06-02` | Nivel de precios endógeno | conceptual_swap | high | El modelo real determina $p(t)$ | En este sistema real no hay ecuación monetaria para determinar el nivel absoluto de precios $p(t)$, por lo que $p(t)$ se toma como dado. |
| `D-C06-05` | Resta variación de precios | conceptual_swap | high | $i(t)=q(t)/p(t)-\dot{p}(t)/p(t)$ | Recuerde que si los precios caen ($\dot{p}<0$), la renta real debe superar a $i$ para compensar la pérdida de valor del capital. |
| `D-C06-03` | Rigidez de salarios reales | conceptual_swap | high | $w/p$ es constante e independiente de $r$ | Los precios factoriales $w/p$ y $q/p$ se ajustan instantáneamente según la productividad marginal para mantener el pleno empleo de ambos factores. |
| `D-C06-06` | Salarios nominales marginales | conceptual_swap | high | $\partial F/\partial L=w$ | Divida el salario nominal $w(t)$ por el precio del producto real $p(t)$ para igualar la productividad marginal física al salario real. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Mercados competitivos con ajuste instantáneo de precios factoriales | Si existen rigideces nominales o competencia monopolística, la productividad marginal deja de igualar los retornos reales. | - |
| `A-C06-02` | - | Competencia perfecta y rendimientos constantes a escala en $F(K,L)$ | Sin competencia ni homogeneidad de grado 1, las productividades marginales no igualan precios reales ni dependen solo de $r$. | - |
| `A-C06-03` | - | Previsión perfecta, ausencia de riesgo y de preferencias por activos | Con incertidumbre o preferencia por liquidez, la condición de arbitraje sin riesgo deja de determinar la tenencia de capital. | - |

---

### [C-08] Isocuantas y Precios de Factores (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 19: Isocuantas y Precios de Factores
- **Prerequisites:** C-06
- **Recommended Modalities:** invariant_canvas, multiple_select, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 19)

#### Description & Cognitive Model
Relación entre la pendiente constante de las isocuantas a lo largo de rayos $K=rL$ y la razón de precios $w/q$, en contraste con la indeterminación y saltos discontinuos del caso de proporciones fijas Harrod-Domar.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Caída indefinida de renta | conceptual_swap | high | Ajuste hacia $r^*$ exige caída perpetua de $q/p$ | Distinga el resultado neoclásico del de Harrod: si existe un equilibrio estable $r^*$, la razón $w/q$ converge a un límite finito. |
| `D-C08-02` | Harrod siempre proporcional | conceptual_swap | high | En proporciones fijas $w=p/b$ y $q=p/a$ siempre | Verifique que fuera de $r=a/b$ uno de los factores es redundante y su producto marginal y precio real se anulan por completo. |
| `D-C08-03` | Precio único en balance | conceptual_swap | high | En $r=a/b$ los precios $w$ y $q$ son únicos | Note que en la esquina $r=a/b$ solo se cumple $aq+bw=p$, por lo que los precios individuales de ambos factores quedan indeterminados. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C08-01` | - | Isocuantas diferenciables con convexidad normal frente a ángulos rectos | Si las isocuantas forman ángulos rectos como en Harrod-Domar, desaparece la sustituibilidad y los precios sufren saltos extremos. | - |

---

### [Hab-06] Participación Relativa del Trabajo (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 21: Participación Relativa del Trabajo
- **Prerequisites:** C-06, C-08
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 21)

#### Description & Cognitive Model
Cálculo de la participación relativa del trabajo $(w/p)(L/Y)$ en crecimiento balanceado: constancia $1-a$ en Cobb-Douglas frente a $1-a\sqrt{s/n}$ en la función $Y=(a\sqrt{K}+\sqrt{L})^2$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Participación constante universal | skipped_step | high | $\theta_L$ es independiente de $s$ y $n$ siempre | Calcule $(w/p)(L/Y)$ explícitamente para $Y=(a\sqrt{K}+\sqrt{L})^2$; verá que depende de $s$ y $n$ mediante $1-a\sqrt{s/n}$. |
| `D-Hab06-02` | Invierte razón s/n | skipped_step | high | $\theta_L=1-a\sqrt{n/s}$ | Sustituya $r^*=(\sqrt{n/s}-a)^{-2}$ en $w/p=1/(1-a\sqrt{s/n})$ y en $Y/L$; mayor $n$ reduce $w/p$ pero eleva la participación laboral. |
| `D-Hab06-03` | Omite raíz cuadrada | conceptual_swap | high | $\theta_L=1-a(s/n)$ | Conserve el exponente $1/2$ proveniente de $\sqrt{K}$ y $\sqrt{L}$ al despejar la razón de equilibrio $r^*$ y evaluar $\partial Y/\partial L$. |
| `D-Hab06-04` | Confunde salario con participación | conceptual_swap | high | Mayor $n$ reduce tanto $w/p$ como $\theta_L$ | Diferencie el salario real unitario $w/p$ de la fracción del ingreso $(w/p)(L/Y)$: en este ejemplo un $n$ mayor eleva $\theta_L$. |
| `D-Hab06-05` | Asigna parámetro a al trabajo | conceptual_swap | high | $\theta_L=a$ en Cobb-Douglas | Derive $Y=K^a L^{1-a}$ respecto a $L$: el exponente de $L$ es $1-a$, por lo que la participación del trabajo es $1-a$. |
| `D-Hab06-06` | Omite producto por trabajador | conceptual_swap | high | $\theta_L=1/(1-a\sqrt{s/n})$ | Divida el salario real $w/p=(1-a\sqrt{s/n})^{-1}$ entre el producto por trabajador $Y/L=(1-a\sqrt{s/n})^{-2}$ para hallar la participación. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Existencia de equilibrio balanceado con $\sqrt{n/s}>a$ en $Y=(a\sqrt{K}+\sqrt{L})^2$ | Si $\sqrt{n/s}\le a$, no existe razón positiva $r^*$ de crecimiento balanceado. | - |

---

### [Hab-07] Cambio Tecnológico Neutral (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 22: Cambio Tecnológico Neutral
- **Prerequisites:** C-06
- **Recommended Modalities:** open_symbolic, proof_dag, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 22)

#### Description & Cognitive Model
Análisis asintótico del modelo Cobb-Douglas con progreso técnico neutral $Y=e^{gt}K^a L^{1-a}$ ($b=1-a$): tasas de crecimiento de $K$ ($n+g/b$), $Y$ ($n+ag/b$), $K/L$ ($g/b$) y $K/Y$ ($g$).

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Tasa de K igual a n+g | skipped_step | high | $\dot{K}/K=n+g$ | Resuelva la ecuación diferencial de $K(t)$ con $b=1-a$: el término exponencial dominante $e^{(nb+g)t/b}$ da tasa $n+g/b$. |
| `D-Hab07-02` | Equilibrio finito de r | skipped_step | high | $K/L$ converge a un $r^*$ constante | Compare las tasas de $K$ ($n+g/b$) y de $L$ ($n$): como $g/b>0$, la razón capital-trabajo $K/L$ crece sin límite a tasa $g/b$. |
| `D-Hab07-03` | Tasa de Y igual a n+g | conceptual_swap | high | $\dot{Y}/Y=n+g$ siempre | Calcule $\dot{Y}/Y=g+a(\dot{K}/K)+(1-a)n=n+ag/b$; note que si $a>1/2$ el producto crece incluso más rápido que $n+g$. |
| `D-Hab07-04` | K/Y constante | conceptual_swap | high | La razón $K/Y$ permanece constante | Reste ambas tasas asintóticas: $(n+g/b)-(n+ag/b)=g(1-a)/b=g>0$, de modo que el coeficiente de capital $K/Y$ crece a tasa $g$. |
| `D-Hab07-05` | Salario real constante | conceptual_swap | high | $w/p$ se estabiliza en el largo plazo | Observe que $K/L$ crece indefinidamente a tasa $g/b$, por lo que la productividad marginal del trabajo y el salario real suben sin límite. |
| `D-Hab07-06` | Participación laboral crece | conceptual_swap | high | $\theta_L$ aumenta con el progreso técnico | Recuerde que en la función Cobb-Douglas con cambio neutral la participación relativa del trabajo permanece constante en $1-a$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Cambio tecnológico neutral multiplicativo $A(t)=e^{gt}$ con $a\in(0,1)$ | Si $A(t)$ altera las pendientes de las isocuantas o $a\ge 1$, las tasas asintóticas y la constancia de $\theta_L$ dejan de cumplirse. | - |

---

### [C-09] Oferta Laboral Elástica (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 23: Oferta Laboral Elástica
- **Prerequisites:** C-06
- **Recommended Modalities:** adversarial_break, proof_dag, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 23)

#### Description & Cognitive Model
Generalización con oferta de trabajo dependiente del salario real $L=L_0 e^{nt}(w/p)^h$ y $L=G(t,w/p)$: ecuación dinámica $\dot{r}=(sF(r,1)-nr)(1+ah/r)^{-1}$ e invariancia o desplazamiento de $r^*$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Cambia r* con elasticidad constante | conceptual_swap | high | Un $h>0$ altera siempre el valor de $r^*$ | Iguale a cero $\dot{r}=(sF(r,1)-nr)(1+ah/r)^{-1}$: el factor $(1+ah/r)^{-1}$ es positivo, luego $r^*$ satisface la misma ecuación $sF(r,1)=nr$. |
| `D-C09-02` | Omite término salarial en r punto | conceptual_swap | high | $\dot{r}=sF(r,1)-nr$ también con $L=G(t,w/p)$ | Incluya el término $-h(\dot{w}/w)$ o la derivada parcial respecto a $w/p$ al diferenciar $K/L$ cuando la oferta laboral responde al salario. |
| `D-C09-03` | Invariancia universal en G(t,w/p) | conceptual_swap | high | Toda función $G(t,w/p)$ preserva el $r^*$ base | Verifique en (6b) que $r^*$ solo coincide con el caso inelástico si $(1/G)(\partial G/\partial t)=n$; en general la elasticidad desplaza $r^*$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | Función de oferta $L=L_0e^{nt}(w/p)^h$ sin cota máxima física de trabajo | A salarios reales muy altos, la oferta laboral debe acotarse por el tamaño efectivo de la fuerza laboral. | - |

---

### [C-10] Ahorro Variable e Impuestos (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 25: Ahorro Variable e Impuestos
- **Prerequisites:** C-06
- **Recommended Modalities:** invariant_canvas, adversarial_break, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 25)

#### Description & Cognitive Model
Efecto estabilizador de una tasa de ahorro decreciente con la razón capital-trabajo $\dot{r}=s(r)F(r,1)-nr$ y desplazamiento de la tasa efectiva a $s+(v-s)t$ bajo un impuesto proporcional sobre la renta.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C10-01` | Ahorro variable crea estado estacionario | conceptual_swap | high | Si $s(r)=0$ para $r$ alto, $K$ y $L$ se detienen | Note que aunque $s(r)$ anule la inversión neta para $r$ grande, el crecimiento continuo de $L$ reduce $r$ y evita el estado estacionario clásico. |
| `D-C10-02` | Impuesto siempre reduce ahorro | conceptual_swap | high | Todo impuesto $t>0$ contrae el ahorro a $s(1-t)$ | Incorpore la fracción pública invertida $v$: la tasa efectiva $s+(v-s)t$ aumenta respecto a $s$ siempre que el Estado invierta más que el sector privado ($v>s$). |
| `D-C10-03` | Ahorro variable desestabiliza r* | conceptual_swap | high | Un $s(r)$ decreciente provoca crecimiento explosivo de $r$ | Observe que cuando $s'(r)<0$, un $r$ elevado reduce el ahorro y frena la acumulación, garantizando estabilidad si $s(r)$ se anula. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C10-01` | - | Ahorro positivo en la tasa de rendimiento capital $q/p$ ($s'(r)<0$) | Si el ahorro aumentara con $r$ ($s'(r)>0$), la variabilidad del ahorro podría desestabilizar el equilibrio. | - |

---

### [C-11] Población Endógena y Trampa (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 27: Población Endógena y Trampa
- **Prerequisites:** C-08
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 27)

#### Description & Cognitive Model
Dinámica con crecimiento poblacional endógeno $\dot{r}=sF(r,1)-n(r)r$: coexistencia de un equilibrio bajo estable $r_1$ (estancamiento) y un umbral crítico inestable $r_2$ que separa el retorno a $r_1$ de la expansión autosostenida.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C11-01` | Umbral r2 es estable | conceptual_swap | high | Cualquier $r$ cercano a $r_2$ converge hacia $r_2$ | Analice el signo de $\dot{r}$ alrededor de $r_2$ en la Figura IX: por debajo $\dot{r}<0$ vuelve a $r_1$, y por encima $\dot{r}>0$ inicia expansión. |
| `D-C11-02` | Requiere rendimientos crecientes | conceptual_swap | high | La trampa de estancamiento exige rendimientos crecientes | Destaque que con rendimientos constantes y sin indivisibilidades basta la forma no lineal de $n(r)r$ para generar trampa y umbral crítico. |
| `D-C11-03` | Impulso pequeño basta | conceptual_swap | high | Cualquier ahorro adicional saca del equilibrio $r_1$ | Verifique que acumulaciones pequeñas por debajo de $r_2$ retornan a $r_1$; solo un impulso que supere $r_2$ sostiene el crecimiento per cápita. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C11-01` | - | Tasa poblacional $n(r)$ dependiente exclusivamente del ingreso per cápita $F(r,1)$ | Si $n$ es exógeno y constante, la curva $n(r)r$ se vuelve una recta y desaparece la multiplicidad de equilibrios. | - |

---

### [Hab-08] Rigidez Salarial y Liquidez (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 29: Rigidez Salarial y Liquidez
- **Prerequisites:** C-06, C-08
- **Recommended Modalities:** open_symbolic, adversarial_break, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 29)

#### Description & Cognitive Model
Implicaciones de rigideces keynesianas en el modelo neoclásico: salario real rígido $\bar{w}/p$ que fija $\bar{r}$ con crecimiento del empleo $\dot{L}/L=(s/\bar{r})F(\bar{r},1)$ frente a $n$, y preferencia por la liquidez $\bar{M}=Q(F,F_K)$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | Desempleo si pendiente supera n | skipped_step | high | Si $(s/\bar{r})F(\bar{r},1)>n$, surge desempleo creciente | Compare la tasa de expansión del empleo $(s/\bar{r})F(\bar{r},1)$ con el crecimiento laboral $n$: si es menor que $n$, se acumula desempleo. |
| `D-Hab08-02` | Razón r sigue variando | skipped_step | high | Con salario rígido $\bar{w}/p$, $r$ sigue ajustándose | Recuerde que la productividad marginal $\partial F/\partial L$ depende solo de $r$; fijar $\bar{w}/p$ fija ineludiblemente $r=\bar{r}$ y ajusta $L$. |
| `D-Hab08-03` | Omite efecto sobre capital en trampa | conceptual_swap | high | La trampa de liquidez solo genera desempleo laboral | Observe que cuando la tasa de interés es rígida por encima del nivel de equilibrio, el resultado análogo es la subutilización del capital. |
| `D-Hab08-04` | Modelo real basta con dinero | conceptual_swap | high | El modelo real describe bien la preferencia por liquidez | Note que al asignar riqueza entre efectivo y capital, el precio del bien compuesto importa y se requiere una dinámica monetaria explícita. |
| `D-Hab08-05` | Escasez de trabajo con ṙ<0 | conceptual_swap | high | Si $\bar{r}$ cae en zona $\dot{r}<0$, hay escasez laboral | Verifique que en la zona $\dot{r}<0$ el rayo hacia $sF(\bar{r},1)$ es más plano que $n$, por lo que el empleo crece más lento que $n$ y hay desempleo. |
| `D-Hab08-06` | Toda política lleva al mismo ahorro | conceptual_swap | high | Pleno empleo fija una única tasa de inversión | Recuerde que combinar política monetaria barata y superávit fiscal permite pleno empleo con distinta formación de capital y crecimiento. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab08-01` | - | Salario real rígido $\bar{w}/p$ o elasticidad infinita de demanda de saldos ociosos | Con precios y salarios perfectamente flexibles y sin preferencia por liquidez, se restablece el pleno empleo continuo. | - |

---
