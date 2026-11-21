# Cognitive Task Analysis (CTA): Solow M20 V2

- **Course ID:** `solow_m20_v2`
- **Macro-Competency:** Dominio y aplicación analítica integral de Solow M20 V2
- **Structure:** 21 total competencies (2 Facts, 9 Concepts, 10 Skills) with 94 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Función de Producción Per Cápita | Concept | Understand | Unidad 2: Función de Producción Per Cápita | - | 3 |
| `Hab-01` | Ecuación Fundamental de Solow | Skill | Apply | Unidad 3: Ecuación Fundamental de Solow | C-01 | 6 |
| `C-02` | Línea de Fase y Estabilidad | Concept | Analyze | Unidad 3: Línea de Fase y Estabilidad | Hab-01 | 3 |
| `H-01` | Estado de Crecimiento Uniforme | Fact | Remember | Unidad 4: Estado de Crecimiento Uniforme | C-02 | 3 |
| `Hab-02` | Trayectoria Temporal Cobb-Douglas | Skill | Apply | Unidad 5: Trayectoria Temporal Cobb-Douglas | Hab-01, C-02 | 6 |
| `C-03` | Acumulación y Rendimientos Constantes | Concept | Understand | Unidad 3: Acumulación y Rendimientos Constantes | C-01 | 3 |
| `H-02` | Crecimiento Exógeno del Trabajo | Fact | Remember | Unidad 4: Crecimiento Exógeno del Trabajo | C-03 | 3 |
| `Hab-03` | Ecuación Fundamental Capital-Trabajo | Skill | Apply | Unidad 6: Ecuación Fundamental Capital-Trabajo | C-03, H-02 | 6 |
| `C-04` | Estabilidad y Equilibrios de Crecimiento | Concept | Analyze | Unidad 7: Estabilidad y Equilibrios de Crecimiento | Hab-03 | 3 |
| `Hab-04` | Proporciones Fijas Harrod-Domar | Skill | Analyze | Unidad 11: Proporciones Fijas Harrod-Domar | Hab-03 | 6 |
| `Hab-05` | Solución y Equilibrio Cobb-Douglas | Skill | Apply | Unidad 13: Solución y Equilibrio Cobb-Douglas | Hab-03 | 6 |
| `Hab-06` | Producción con un Solo Factor | Skill | Analyze | Unidad 14: Producción con un Solo Factor | Hab-03 | 6 |
| `C-05` | Precios Competitivos y Productividad Marginal | Concept | Understand | Unidad 16: Precios Competitivos de los Factores | C-03, Hab-03 | 4 |
| `Hab-07` | Arbitraje entre Interés y Alquiler | Skill | Apply | Unidad 17: Arbitraje entre Interés y Alquiler | C-05 | 6 |
| `C-07` | Isocuantas, Razón Salario-Alquiler y Proporciones Fijas | Concept | Analyze | Unidad 19: Isocuantas, Razón Salario-Alquiler y Proporciones Fijas | C-05 | 3 |
| `Hab-08` | Precios de Equilibrio y Participación Laboral | Skill | Apply | Unidad 21: Precios de Equilibrio y Participación Laboral | C-05, C-07 | 6 |
| `Hab-09` | Cambio Tecnológico Neutral y Crecimiento Asintótico | Skill | Apply | Unidad 22: Cambio Tecnológico Neutral y Crecimiento Asintótico | C-05, Hab-08 | 6 |
| `C-08` | Oferta de Trabajo Elástica al Salario Real | Concept | Analyze | Unidad 23: Oferta de Trabajo Elástica al Salario Real | C-05 | 3 |
| `C-09` | Tasa de Ahorro Variable e Impuesto sobre la Renta | Concept | Evaluate | Unidad 25: Tasa de Ahorro Variable e Impuesto sobre la Renta | C-05 | 3 |
| `C-10` | Crecimiento Poblacional Endógeno y Trampa de Estancamiento | Concept | Analyze | Unidad 27: Crecimiento Poblacional Endógeno y Trampa de Estancamiento | C-09 | 3 |
| `Hab-10` | Salarios Rígidos y Trampa de Liquidez | Skill | Evaluate | Unidad 29: Salarios Rígidos y Trampa de Liquidez | C-05, Hab-07 | 6 |

---

## Detailed Competency Specifications

### [C-01] Función de Producción Per Cápita (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 2: Función de Producción Per Cápita
- **Prerequisites:** None
- **Recommended Modalities:** concept_matching, invariant_canvas, adversarial_break
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
Transformación de la función de producción linealmente homogénea $Q=f(K,L)$ a su forma intensiva $Q=L\phi(k)$ con $k\equiv K/L$, $\phi'(k)>0$ y $\phi''(k)<0$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Omite factor trabajo | conceptual_swap | high | $Q=\phi(k)$ | Recuerde que $\phi(k)$ representa el producto medio del trabajo $Q/L$; multiplique por $L$ para recuperar el producto agregado $Q$. |
| `D-C01-02` | Segunda derivada positiva | conceptual_swap | high | $\phi''(k)>0$ | Distinga el signo de $f_K>0$ ($\phi'(k)>0$) del signo de $f_{KK}<0$ ($\phi''(k)<0$), que garantiza retornos marginales decrecientes. |
| `D-C01-03` | Proporción fija Domar | conceptual_swap | high | $Q=\rho K$ | Diferencie el modelo de Domar de proporciones fijas del modelo de Solow, donde $K$ y $L$ se combinan en proporciones variables. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Homogeneidad lineal de $f(K,L)$ (retornos constantes a escala) con $K,L>0$ | Sin homogeneidad de grado uno, $Q/L$ dependería de la escala $L$ y no solo de $k=K/L$. | - |
| `A-C01-02` | - | Productos marginales positivos ($f_K,f_L>0$) y decrecientes ($f_{KK},f_{LL}<0$) | Si $\phi''(k)\ge 0$, se pierde la concavidad estricta de la curva de producción per cápita. | - |

---

### [Hab-01] Ecuación Fundamental de Solow (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 3: Ecuación Fundamental de Solow
- **Prerequisites:** C-01
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, proof_dag
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
Derivación de la ecuación diferencial fundamental $\dot{k}=s\phi(k)-\lambda k$ a partir de $\dot{K}=sQ$, $\dot{L}/L=\lambda$ y la diferenciación de $K=kL$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Suma dilución laboral | skipped_step | high | $\dot{k}=s\phi(k)+\lambda k$ | Al igualar $L\dot{k}+k\lambda L=sL\phi(k)$ y despejar $\dot{k}$, pase el término de dilución $\lambda k$ restando al lado derecho. |
| `D-Hab01-02` | Omite crecimiento laboral | skipped_step | high | $\dot{k}=s\phi(k)$ | Aplique la regla del producto al diferenciar $K=kL$: $\dot{K}=L\dot{k}+k\dot{L}$, pues $L$ crece a tasa $\lambda>0$ con el tiempo. |
| `D-Hab01-03` | Confunde Q con k | conceptual_swap | high | $\dot{k}=sk-\lambda k$ | Recuerde que el ahorro bruto es una fracción $s$ del producto $Q=L\phi(k)$, no del stock de capital $K$; mantenga $\phi(k)$. |
| `D-Hab01-04` | Conserva factor L | conceptual_swap | high | $\dot{k}=sL\phi(k)-\lambda k$ | Elimine el factor común $L>0$ en todos los sumandos de la ecuación $L\dot{k}+k\lambda L=sL\phi(k)$ al dividir ambos miembros. |
| `D-Hab01-05` | Multiplica lambda por phi | conceptual_swap | high | $\dot{k}=s\phi(k)-\lambda\phi(k)$ | Observe que $k\dot{L}/L=k\lambda$, por lo que la dilución por crecimiento laboral es proporcional a $k$ y no a $\phi(k)$. |
| `D-Hab01-06` | Omite propensión al ahorro | conceptual_swap | high | $\dot{k}=\phi(k)-\lambda k$ | Incluya la propensión marginal al ahorro $s$ de la hipótesis $\dot{K}=sQ$, ya que solo se invierte una proporción $s$ del producto. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Propensión marginal al ahorro $s$ constante y tasa laboral $\lambda>0$ constante | Si $s$ o $\lambda$ varían con $k$ o $t$, la ecuación ya no es autónoma con parámetros constantes. | - |

---

### [C-02] Línea de Fase y Estabilidad (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 3: Línea de Fase y Estabilidad
- **Prerequisites:** Hab-01
- **Recommended Modalities:** invariant_canvas, adversarial_break, concept_matching
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
Análisis cualitativo-gráfico de $\dot{k}=s\phi(k)-\lambda k$: intersección de $s\phi(k)$ y $\lambda k$ en $\bar{k}$, estabilidad y desplazamiento por progreso tecnológico $T(t)$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Criterio pendiente invertido | conceptual_swap | high | Equilibrio estable si $\frac{d\dot{k}}{dk}\big|_{\bar{k}}>0$ | Verifique el flujo direccional: para estabilidad, $\dot{k}>0$ cuando $k<\bar{k}$ y $\dot{k}<0$ cuando $k>\bar{k}$, exigiendo pendiente negativa. |
| `D-C02-02` | Curva s*phi no parte de cero | conceptual_swap | high | $s\phi(0)>0$ | Como $K$ es un factor indispensable, si $K=0$ entonces $k=0$ y $Q=0$; por ello $\phi(0)=0$ y $s\phi(k)$ parte del origen. |
| `D-C02-03` | Tecnología reduce k barra | conceptual_swap | high | Aumento de $T(t)$ reduce $\bar{k}$ | Un término tecnológico creciente $T(t)$ ($dT/dt>0$) desplaza la curva $s\phi(k)$ hacia arriba, generando intersecciones $\bar{k}$ mayores. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | Capital indispensable ($\phi(0)=0$) y existencia de $k>0$ con $s\phi(k)>\lambda k$ | Sin esta condición, $s\phi(k)$ y $\lambda k$ podrían no intersecarse en ningún $\bar{k}>0$. | - |

---

### [H-01] Estado de Crecimiento Uniforme (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 4: Estado de Crecimiento Uniforme
- **Prerequisites:** C-02
- **Recommended Modalities:** multiple_select, fill_in_the_blank, concept_matching
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
Situación de estado uniforme en el equilibrio $\bar{k}$ donde $K$, $L$, el producto $Q$ y la inversión neta crecen automáticamente a la misma tasa $\lambda$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Confunde con estacionario | conceptual_swap | high | $K$, $L$ y $Q$ crecen a tasa cero | Distinga el estado estacionario (crecimiento cero) del estado uniforme, donde $k=\bar{k}$ es constante pero $K$, $L$ y $Q$ crecen a tasa $\lambda$. |
| `D-H01-02` | Solo crece el trabajo | conceptual_swap | high | $\dot{K}/K=0$ y $\dot{L}/L=\lambda$ | Si $k=K/L$ permanece invariante en $\bar{k}$, el numerador $K$ debe crecer exactamente a la misma tasa $\lambda$ que el denominador $L$. |
| `D-H01-03` | Requiere ajuste exógeno | conceptual_swap | high | Equilibrio frágil tipo Domar | En Solow el estado uniforme surge automáticamente desde cualquier $k(0)>0$ sin requerir el delicado balance del filo de la navaja de Domar. |

---

### [Hab-02] Trayectoria Temporal Cobb-Douglas (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 5: Trayectoria Temporal Cobb-Douglas
- **Prerequisites:** Hab-01, C-02
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 5)

#### Description & Cognitive Model
Solución cuantitativa de $\dot{k}+\lambda k=sk^{\alpha}$ mediante $z=k^{1-\alpha}$ para hallar $k^{1-\alpha}(t)$ y su límite asintótico $k\to(s/\lambda)^{\frac{1}{1-\alpha}}$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Omite factor 1 menos alfa | skipped_step | high | $\frac{dz}{dt}+\lambda z=s$ | Al diferenciar $z=k^{1-\alpha}$ se obtiene $\dot{z}=(1-\alpha)k^{-\alpha}\dot{k}$; multiplique toda la ecuación linealizada por $(1-\alpha)$. |
| `D-Hab02-02` | Exponente inverso errado | skipped_step | high | $k\to(s/\lambda)^{1-\alpha}$ | Dado que $k^{1-\alpha}\to s/\lambda$ cuando $t\to\infty$, eleve ambos lados al recíproco $\frac{1}{1-\alpha}$ para despejar $k$. |
| `D-Hab02-03` | Razón lambda entre s | conceptual_swap | high | $k\to(\lambda/s)^{\frac{1}{1-\alpha}}$ | Verifique el signo de la estática comparativa: el capital de equilibrio crece con el ahorro $s$ y decrece con la tasa laboral $\lambda$. |
| `D-Hab02-04` | Exponente temporal positivo | conceptual_swap | high | $e^{+(1-\alpha)\lambda t}$ | En $\frac{dz}{dt}+az=b$ con $a=(1-\alpha)\lambda>0$, la solución homogénea decae como $e^{-at}=e^{-(1-\alpha)\lambda t}\to 0$. |
| `D-Hab02-05` | Omite condición inicial | conceptual_swap | high | $k^{1-\alpha}=\frac{s}{\lambda}e^{-(1-\alpha)\lambda t}$ | Incluya la solución particular constante $s/\lambda$ y la desviación inicial $[k(0)^{1-\alpha}-s/\lambda]$ multiplicada por el decaimiento. |
| `D-Hab02-06` | Potencia alfa en lugar de 1-alfa | conceptual_swap | high | $k\to(s/\lambda)^{\alpha}$ | Recuerde que la ecuación de Bernoulli con $m=\alpha$ exige la sustitución $z=k^{1-m}=k^{1-\alpha}$, no $k^{\alpha}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Función de producción Cobb-Douglas linealmente homogénea $Q=K^{\alpha}L^{1-\alpha}$ con $0<\alpha<1$ | Si $\alpha\ge 1$, $(1-\alpha)\lambda\le 0$ y el término exponencial no converge a cero. | - |

---

### [C-03] Acumulación y Rendimientos Constantes (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 3: Acumulación y Rendimientos Constantes
- **Prerequisites:** C-01
- **Recommended Modalities:** concept_matching, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 3)

#### Description & Cognitive Model
Identidad de inversión neta $\dot{K}=sY$ con tasa de ahorro constante $s$ y función de producción $Y=F(K,L)$ homogénea de primer grado

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Ahorro sobre capital | conceptual_swap | high | $\dot{K}=sK$ | Aplique la tasa de ahorro $s$ sobre el flujo de ingreso neto $Y=F(K,L)$, no sobre el stock acumulado $K$. |
| `D-C03-02` | Rendimientos decrecientes globales | conceptual_swap | high | $F(\lambda K,\lambda L)<\lambda Y$ | Recuerde que en el modelo base no hay tierra escasa no aumentable, por lo que $F(K,L)$ muestra rendimientos constantes a escala. |
| `D-C03-03` | Producto bruto sin depreciación | conceptual_swap | high | $Y$ incluye depreciación sin reponer | Interprete $Y=F(K,L)$ como producto neto tras reponer la depreciación del capital, de modo que $sY$ es acumulación neta. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | Homogeneidad de grado 1 $F(\lambda K,\lambda L)=\lambda F(K,L)$ sin recursos fijos como tierra | Si hubiera tierra escasa habría rendimientos decrecientes a escala y el modelo sería ricardiano. | - |
| `A-C03-02` | - | Tasa de ahorro exógena y constante $s$ con producto neto $Y$ consumido o invertido | Si $s$ variara endógenamente, $\dot{K}=sF(K,L)$ requeriría una ecuación adicional de ahorro. | - |

---

### [H-02] Crecimiento Exógeno del Trabajo (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 4: Crecimiento Exógeno del Trabajo
- **Prerequisites:** C-03
- **Recommended Modalities:** multiple_select, fill_in_the_blank, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 4)

#### Description & Cognitive Model
La fuerza laboral crece exponencialmente a tasa natural $n$, $L(t)=L_0 e^{nt}$, con oferta inelástica y pleno empleo perpetuo

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H02-01` | Crecimiento lineal del trabajo | conceptual_swap | high | $L(t)=L_0(1+nt)$ | Use la trayectoria exponencial continua $L(t)=L_0 e^{nt}$ que corresponde a una tasa relativa constante $\dot{L}/L=n$. |
| `D-H02-02` | Oferta laboral elástica al salario | conceptual_swap | high | $L(t)$ depende del salario real $w/p$ | Note que Solow fija $L(t)=L_0 e^{nt}$ de forma completamente inelástica y deja que el salario real ajuste para mantener pleno empleo. |
| `D-H02-03` | Desempleo estructural en ecuación | conceptual_swap | high | $\dot{K}=sF(K,L_{\text{emp}})$ con $L_{\text{emp}}<L_0 e^{nt}$ | Identifique empleo total y oferta laboral disponible $L_0 e^{nt}$ para obtener la ecuación $\dot{K}=sF(K,L_0 e^{nt})$ de pleno empleo. |

---

### [Hab-03] Ecuación Fundamental Capital-Trabajo (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 6: Ecuación Fundamental Capital-Trabajo
- **Prerequisites:** C-03, H-02
- **Recommended Modalities:** proof_dag, open_symbolic, fill_in_the_blank
- **Evidence Citations:** `solow1956.pdf` (page 6)

#### Description & Cognitive Model
Derivación e interpretación de $\dot{r}=sF(r,1)-nr$ para la razón capital-trabajo $r=K/L$ mediante rendimientos constantes a escala

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Olvida término de dilución | skipped_step | high | $\dot{r}=sF(r,1)$ | Aplique la regla del cociente $\dot{r}/r=\dot{K}/K-\dot{L}/L$: como $\dot{L}/L=n$, debe restar $nr$ al incremento de capital $sF(r,1)$. |
| `D-Hab03-02` | Signo invertido en dilución | skipped_step | high | $\dot{r}=sF(r,1)+nr$ | Recuerde que un mayor crecimiento laboral $n$ diluye el capital por trabajador y reduce $r$, por lo que el término $nr$ entra restando. |
| `D-Hab03-03` | Divide mal por L | skipped_step | high | $\dot{r}=sF(K,1)-nr$ | Use la homogeneidad de grado 1 de $F$ dividiendo ambos argumentos por $L$: $F(K,L)=L F(K/L,1)=L F(r,1)$. |
| `D-Hab03-04` | Confunde r con producto por trabajador | conceptual_swap | high | $r=Y/L$ | Distinga $r=K/L$ (capital por trabajador) de $F(r,1)=Y/L$ (producto por trabajador como función de $r$). |
| `D-Hab03-05` | Omite r en término nr | conceptual_swap | high | $\dot{r}=sF(r,1)-n$ | Multiplique la tasa relativa $n=\dot{L}/L$ por el nivel $r$ al despejar $\dot{r}$ desde $\dot{r}/r=sF(r,1)/r-n$. |
| `D-Hab03-06` | Falta s en el primer término | conceptual_swap | high | $\dot{r}=F(r,1)-nr$ | Incluya la propensión al ahorro $s$ frente a $F(r,1)$, pues solo la fracción ahorrada $sY$ se acumula como nuevo capital. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | Rendimientos constantes a escala $F(K,L)=L F(r,1)$ con $L=L_0 e^{nt}>0$ | Sin homogeneidad de grado 1 no se reduce el sistema a una ecuación en la sola variable $r$. | - |

---

### [C-04] Estabilidad y Equilibrios de Crecimiento (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 7: Estabilidad y Equilibrios de Crecimiento
- **Prerequisites:** Hab-03
- **Recommended Modalities:** invariant_canvas, adversarial_break, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 7)

#### Description & Cognitive Model
Análisis cualitativo de $\dot{r}=sF(r,1)-nr$: equilibrio único estable $r^*$, equilibrios múltiples ($r_1,r_3$ estables; $r_2$ inestable) o inexistencia

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Invierte criterio de estabilidad | conceptual_swap | high | $r_2$ es estable y $r_1,r_3$ son inestables | Verifique el signo de $\dot{r}=sF(r,1)-nr$: un equilibrio es estable solo si $sF(r,1)>nr$ a la izquierda y $sF(r,1)<nr$ a la derecha. |
| `D-C04-02` | Supone convergencia universal | conceptual_swap | high | Siempre existe un equilibrio $r^*>0$ estable | Observe la Figura III: si $s_1 F^1(r,1)$ está siempre por encima de $nr$, $r$ crece sin límite; si está debajo, $r\to 0$. |
| `D-C04-03` | Confunde tasas transitorias | conceptual_swap | high | Si $r<r^*$, el producto crece más lento que $n$ | Recuerde que si $r<r^*$ y $\dot{r}>0$, el capital y el producto crecen más rápido que la fuerza laboral hasta acercarse a $r^*$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | Capital inicial positivo $K_0>0$ cuando no hay producción sin capital ($F(0,1)=0$) | Si $K=0$ y $F(0,1)=0$, entonces $r=0$ y la economía no puede iniciar la acumulación. | - |
| `A-C04-02` | - | Productividad marginal del capital positiva y decreciente en el caso neoclásico estándar | Si la concavidad falla o $sF(r,1)$ no cruza $nr$, aparecen equilibrios múltiples o ausencia de estado estacionario. | - |

---

### [Hab-04] Proporciones Fijas Harrod-Domar (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 11: Proporciones Fijas Harrod-Domar
- **Prerequisites:** Hab-03
- **Recommended Modalities:** open_symbolic, unstructured_model, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 11)

#### Description & Cognitive Model
Análisis de $Y=\min(K/a,L/b)$ en $\dot{r}=s\min(r/a,1/b)-nr$: filo de navaja entre $s/a$ y $n$ y redundancia de trabajo o capital

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Confunde tasa garantizada | skipped_step | high | La tasa garantizada es $s/b$ | Identifique $a$ como el coeficiente acelerador de capital ($K/Y=a$), de modo que la tasa garantizada de Harrod es $s/a$. |
| `D-Hab04-02` | Invierte factor redundante cuando n > s/a | skipped_step | high | Si $n_1>s/a$, sobra capital | Note que si $n_1>s/a$, $r$ cae por debajo de $a/b$ hacia cero y el capital se vuelve cuello de botella, generando desempleo creciente de trabajo. |
| `D-Hab04-03` | Olvida equilibrio de capital redundante | conceptual_swap | high | Si $n_3<s/a$, $r$ crece sin límite | Recuerde que para $r\ge a/b$ la curva es horizontal en $s/b$, por lo que $r$ converge al equilibrio estable $r^*=s/(n_3 b)$ con exceso de capital. |
| `D-Hab04-04` | Fracción de capital empleada invertida | conceptual_swap | high | Proporción de capital empleada es $s/(a n_3)$ | Calcule la razón entre capital requerido $aY=aL/b$ y capital disponible $r^* L=sL/(n_3 b)$, que resulta en $a n_3 / s < 1$. |
| `D-Hab04-05` | Umbral de pleno uso incorrecto | conceptual_swap | high | El quiebre de $\min(r/a,1/b)$ ocurre en $r=b/a$ | Iguale ambos argumentos de $\min(r/a,1/b)$: $r/a=1/b \Rightarrow r=a/b$ separa ambos regímenes. |
| `D-Hab04-06` | Neutralidad cuando r < a/b y n = s/a | conceptual_swap | high | Si $n_2=s/a$ y $r<a/b$, $r$ converge a $a/b$ | Observe que si $n_2=s/a$ y $r<a/b$, entonces $\dot{r}=(s/a-n_2)r=0$, así que $r$ permanece constante preservando el porcentaje inicial de desempleo. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Coeficientes técnicos fijos $a>0$ y $b>0$ sin sustitución entre capital y trabajo | Al permitir sustitución variable entre factores desaparece el filo de navaja y surge una zona de tasas compatibles. | - |

---

### [Hab-05] Solución y Equilibrio Cobb-Douglas (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 13: Solución y Equilibrio Cobb-Douglas
- **Prerequisites:** Hab-03
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 13)

#### Description & Cognitive Model
Resolución explícita de $\dot{K}=sK^a(L_0 e^{nt})^{1-a}$ y equilibrio $r^*=(s/n)^{1/(1-a)}$ con coeficiente de capital endógeno $C=K/Y=s/n$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Exponente sin invertir | skipped_step | high | $r^*=(s/n)^{1-a}$ | Al resolver $s r^a = n r$, obtenga $r^{1-a}=s/n$ y eleve ambos lados al recíproco $1/(1-a)$ para hallar $r^*=(s/n)^{1/(1-a)}$. |
| `D-Hab05-02` | Ingreso per cápita sin potencia a | skipped_step | high | $Y/L \to (s/n)^{1/b}$ | Sustituya $r^*$ en $Y/L=r^a$ para obtener el límite del producto por trabajador $(s/n)^{a/(1-a)}$. |
| `D-Hab05-03` | Invierte razón s/n | conceptual_swap | high | $r^*=(n/s)^{1/(1-a)}$ | Verifique la estática comparativa: mayor ahorro $s$ y menor crecimiento laboral $n$ elevan $r^*$, por lo que $s/n$ va en la base. |
| `D-Hab05-04` | Coeficiente de capital exógeno | conceptual_swap | high | $C=K/Y$ permanece fijo e independiente de $s$ y $n$ | Calcule $K/Y=r/r^a=r^{1-a}$: en equilibrio $C=s/n$, de modo que la relación $n=s/C$ se cumple por ajuste de demanda y oferta. |
| `D-Hab05-05` | Exponente del tiempo incorrecto | conceptual_swap | high | $K(t)$ crece asintóticamente como $e^{nbt}$ | Aplique la potencia exterior $1/b$ de $K(t)=[\dots + (s/n)L_0^b e^{nbt}]^{1/b}$, por lo que asintóticamente $K(t)$ crece como $e^{nt}$. |
| `D-Hab05-06` | Permite equilibrio con a = 1 | conceptual_swap | high | $r^*=(s/n)^{1/(1-a)}$ vale también para $a=1$ | Recuerde que la convergencia requiere $a<1$ (productividad marginal decreciente del capital); si $a=1$, $b=1-a=0$ y la curva no cruza $nr$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | Elasticidad del capital $a\in(0,1)$ con $b=1-a>0$ | Si $a\ge 1$, la curva $s r^a$ no cruza desde arriba al rayo $nr$ y no hay crecimiento balanceado. | - |

---

### [Hab-06] Producción con un Solo Factor (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 14: Producción con un Solo Factor
- **Prerequisites:** Hab-03
- **Recommended Modalities:** open_symbolic, adversarial_break, fill_in_the_blank
- **Evidence Citations:** `solow1956.pdf` (page 14)

#### Description & Cognitive Model
Análisis de $Y=(a\sqrt{K}+\sqrt{L})^2$ ($p=1/2$): $\dot{r}=s(a\sqrt{r}+1)^2-nr$, crecimiento perpetuo si $sa^2>n$ y $r^*=(1/\sqrt{n/s}-a)^2$ si $sa^2<n$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Umbral sin elevar a al cuadrado | skipped_step | high | No hay equilibrio si $sa>n$ | Expanda $(a\sqrt{r}+1)^2=a^2 r + 2a\sqrt{r}+1$ en $\dot{r}$: el coeficiente de $r$ es $sa^2-n$, por lo que la condición crítica es $sa^2>n$. |
| `D-Hab06-02` | Error de signo en raíz de r* | skipped_step | high | $r^*=(1/\sqrt{n/s}+a)^2$ | Iguale $\sqrt{s}(a\sqrt{r}+1)=\sqrt{nr}$ y despeje $\sqrt{r}(\sqrt{n/s}-a)=1$, lo que da $\sqrt{r^*}=1/(\sqrt{n/s}-a)$. |
| `D-Hab06-03` | Curva parte del origen | conceptual_swap | high | $sF(0,1)=0$ en $r=0$ | Evalúe $F(r,1)=(a\sqrt{r}+1)^2$ en $r=0$: como la producción es posible solo con trabajo, la curva parte de altura $s>0$. |
| `D-Hab06-04` | Olvida elevar al cuadrado para r* | conceptual_swap | high | $r^*=1/(\sqrt{n/s}-a)$ | Eleve al cuadrado la expresión de $\sqrt{r^*}$ para obtener la razón capital-trabajo de equilibrio $r^*=(1/(\sqrt{n/s}-a))^2$. |
| `D-Hab06-05` | Ingreso per cápita igual a r* | conceptual_swap | high | $\lim Y/L = r^*$ | Evalúe $F(r^*,1)=(a\sqrt{r^*}+1)^2$: tras simplificar resulta $1/(1-a\sqrt{s/n})^2$. |
| `D-Hab06-06` | Aplica p >= 1 sin restricción | conceptual_swap | high | El análisis vale también para $p>1$ | Recuerde que si $p>1$ las isocuantas tienen la convexidad incorrecta y si $p=1$ son rectas, por lo que Solow restringe $0<p<1$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Parámetro de elasticidad $0<p<1$ (específicamente $p=1/2$) y $a>0$ | Si $p>1$ las isocuantas tienen convexidad errónea y no hay rendimientos marginales decrecientes. | - |

---

### [C-05] Precios Competitivos y Productividad Marginal (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 16: Precios Competitivos de los Factores
- **Prerequisites:** C-03, Hab-03
- **Recommended Modalities:** concept_matching, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 16)

#### Description & Cognitive Model
En economía competitiva con rendimientos constantes a escala, el salario real $\frac{\partial F}{\partial L}=\frac{w}{p}$ y la renta real $\frac{\partial F}{\partial K}=\frac{q}{p}$ dependen únicamente de la razón capital-trabajo $r=K/L$.

#### Fused Distractor Models (4)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Productividad marginal depende de escala | conceptual_swap | high | $\partial F/\partial K$ depende de $K$ y $L$ por separado | Recuerde que con rendimientos constantes a escala las derivadas parciales son homogéneas de grado 0 y dependen solo de la razón $r=K/L$. |
| `D-C05-04` | Iguala salarios nominales | conceptual_swap | high | $\frac{\partial F}{\partial L}=w$ | Divida el salario monetario $w$ y el alquiler $q$ entre el precio del producto $p$ para igualar productividades marginales reales. |
| `D-C05-02` | Sistema determina nivel absoluto de precios | conceptual_swap | high | El sistema real determina $p(t)$ endógenamente | Note que en el sistema real no hay ecuación monetaria que determine $p(t)$, por lo que el nivel de precios se toma como dado. |
| `D-C05-03` | Iguala productividad marginal al precio nominal | conceptual_swap | high | $\partial F/\partial L = w$ | Divida el salario monetario $w$ y la renta monetaria $q$ por $p$ para igualar las productividades marginales físicas a los retornos reales. |

#### Formal Mathematical Assumptions (4)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Competencia pura con ajuste instantáneo de $w/p$ y $q/p$ para vaciar los mercados de factores | Bajo competencia monopolística o rigideces de precios no se define una función agregada competitiva estándar. | - |
| `A-C05-02` | - | Precio de transferencia del capital igual al precio del producto $p(t)$ | Si el bien de capital difiere del bien de consumo, el retorno real requiere distinguir ambos precios. | - |
| `A-C05-03` | - | Competencia perfecta y rendimientos constantes a escala en $F(K,L)$ | Sin rendimientos constantes a escala, las productividades marginales dependen de la escala absoluta. | - |
| `A-C05-04` | - | Nivel absoluto de precios $p(t)$ tomado como dato exógeno | Si el sistema real determinara $p(t)$, habría una ecuación adicional faltante. | - |

---

### [Hab-07] Arbitraje entre Interés y Alquiler (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 17: Arbitraje entre Interés y Alquiler
- **Prerequisites:** C-05
- **Recommended Modalities:** proof_dag, open_symbolic, fill_in_the_blank
- **Evidence Citations:** `solow1956.pdf` (page 17)

#### Description & Cognitive Model
Condición de arbitraje perfecto entre tasa de interés monetaria y rendimiento propio del capital: $i(t)=\frac{q(t)}{p(t)}+\frac{\dot{p}(t)}{p(t)}$ derivada de igualar activos.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Omite ganancia de capital | skipped_step | high | $i(t)=\frac{q(t)}{p(t)}$ | Sume la tasa de variación del precio $\dot{p}(t)/p(t)$ al alquiler real $q(t)/p(t)$ cuando el nivel de precios no es constante. |
| `D-Hab07-02` | Resta inflación | skipped_step | high | $i(t)=\frac{q(t)}{p(t)}-\frac{\dot{p}(t)}{p(t)}$ | Recuerde que si el precio cae ($\dot{p}<0$), el rendimiento propio $q/p$ debe superar a $i(t)$ para compensar la pérdida de capital. |
| `D-Hab07-03` | Usa alquiler nominal | conceptual_swap | high | $i(t)=q(t)+\frac{\dot{p}(t)}{p(t)}$ | Exprese el alquiler por unidad monetaria invertida dividiendo $q(t)$ entre el precio de transferencia $p(t)$ del bien de capital. |
| `D-Hab07-04` | Derivada sin normalizar | conceptual_swap | high | $i(t)=\frac{q(t)}{p(t)}+\dot{p}(t)$ | Divida $\dot{p}(t)$ entre $p(t)$ al tomar el límite $h\to 0$ de $(p(t+h)-p(t))/(h p(t))$ para obtener tasa proporcional. |
| `D-Hab07-05` | Invierte razón de precios | conceptual_swap | high | $i(t)=\frac{p(t)}{q(t)}+\frac{\dot{p}(t)}{p(t)}$ | Calcule el rendimiento por dólar invertido comprando $1/p$ unidades de capital, lo que genera renta $(q/p)h$ y no $(p/q)h$. |
| `D-Hab07-06` | Confunde valor presente | conceptual_swap | high | $p(t)=\int_t^\infty q(u)e^{+\int_t^u i(z)dz}du$ | Aplique factor de descuento negativo $e^{-\int_t^u i(z)dz}$ al calcular el valor presente de los alquileres futuros $q(u)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Previsión perfecta, ausencia de riesgo y arbitraje continuo sin fricciones | Con incertidumbre o preferencia por liquidez, los activos no son sustitutos perfectos. | - |

---

### [C-07] Isocuantas, Razón Salario-Alquiler y Proporciones Fijas (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 19: Isocuantas, Razón Salario-Alquiler y Proporciones Fijas
- **Prerequisites:** C-05
- **Recommended Modalities:** invariant_canvas, adversarial_break, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 19)

#### Description & Cognitive Model
Bajo rendimientos constantes a escala, la pendiente de la isocuanta a lo largo de un rayo $r^*$ fija la razón de equilibrio $w/q$, mientras en Harrod-Domar los precios son indeterminados en $r=a/b$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Caída indefinida de salarios | conceptual_swap | high | $\frac{w}{p}\to 0$ siempre en equilibrio | Distinga el ajuste finito hacia el rayo estable $r^*$ de la hipótesis de Harrod sobre caída perpetua de la tasa de interés. |
| `D-C07-02` | Precios únicos en esquina | conceptual_swap | high | $r=\frac{a}{b} \Rightarrow q=0, w=\frac{p}{b}$ | Observe que en $r=a/b$ ambos factores son escasos y cualquier par $(w,q)$ que cumpla $aq+bw=p$ es compatible con el equilibrio. |
| `D-C07-03` | Pendiente varía en el rayo | conceptual_swap | high | $w/q$ cambia con la escala en un rayo | Recuerde que los rendimientos constantes a escala implican isocuantas homotéticas con pendiente constante sobre cada rayo desde el origen. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Convexidad normal de isocuantas frente a esquinas en ángulo recto de Harrod-Domar | Con esquinas en ángulo recto, cualquier desvío de $r=a/b$ vuelve redundante a un factor. | - |

---

### [Hab-08] Precios de Equilibrio y Participación Laboral (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 21: Precios de Equilibrio y Participación Laboral
- **Prerequisites:** C-05, C-07
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 21)

#### Description & Cognitive Model
Cálculo de precios factoriales de equilibrio y participación relativa del trabajo: constante $1-a$ en Cobb-Douglas frente a $1-a\sqrt{s/n}$ en $Y=(a\sqrt{K}+\sqrt{L})^2$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | Participación constante universal | skipped_step | high | $\frac{wL}{pY}=1-a$ para toda función | Calcule $(w/p)(L/Y)$ específicamente para cada función; en $Y=(a\sqrt{K}+\sqrt{L})^2$ la participación depende de $s$ y $n$. |
| `D-Hab08-02` | Invierte efecto de n | skipped_step | high | Mayor $n$ reduce la participación laboral | Verifique en $1-a\sqrt{s/n}$ que al aumentar $n$ cae el salario real de equilibrio pero sube la participación total del trabajo. |
| `D-Hab08-03` | Alquiler Cobb-Douglas errado | conceptual_swap | high | $\frac{q^*}{p}=\frac{as}{n}$ | Sustituya $r^*=(s/n)^{1/(1-a)}$ en $q/p=ar^{a-1}$ para obtener $q^*/p=an/s$, inversamente proporcional a la tasa de ahorro. |
| `D-Hab08-04` | Omite raíz en r* | conceptual_swap | high | $r^*=\frac{1}{\sqrt{n/s}-a}$ | Eleve al cuadrado la condición de equilibrio $\sqrt{r^*}=(\sqrt{n/s}-a)^{-1}$ al resolver $s(a\sqrt{r}+1)^2=nr$ para $r^*$. |
| `D-Hab08-05` | Derivada parcial incompleta | conceptual_swap | high | $\frac{\partial Y}{\partial L}=a\sqrt{r}$ | Aplique la regla de la cadena a $(a\sqrt{K}+\sqrt{L})^2$: $\partial Y/\partial L=(a\sqrt{K}+\sqrt{L})/\sqrt{L}=a\sqrt{r}+1$. |
| `D-Hab08-06` | Confunde razón w/q | conceptual_swap | high | $\frac{w}{q}=\frac{a}{1-a}r$ | Divida $\partial Y/\partial L=(1-a)r^a$ entre $\partial Y/\partial K=ar^{a-1}$ para obtener correctamente $w/q=\frac{1-a}{a}r$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab08-01` | - | Existencia de equilibrio balanceado $\sqrt{n/s}>a$ en $Y=(a\sqrt{K}+\sqrt{L})^2$ | Si $\sqrt{n/s}\le a$, no existe estado estacionario finito y $r$ crece indefinidamente. | - |

---

### [Hab-09] Cambio Tecnológico Neutral y Crecimiento Asintótico (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 22: Cambio Tecnológico Neutral y Crecimiento Asintótico
- **Prerequisites:** C-05, Hab-08
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, proof_dag
- **Evidence Citations:** `solow1956.pdf` (page 22)

#### Description & Cognitive Model
Con cambio tecnológico neutral $Y=e^{gt}K^a L^{1-a}$ y $b=1-a$, el capital crece asintóticamente a tasa $n+g/b$, el producto a $n+ag/b$ y la razón $K/L$ crece sin límite a tasa $g/b$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab09-01` | Equilibrio estacionario en r | skipped_step | high | $K/L$ converge a un $r^*$ finito | Note que al multiplicarse $sF(r,1)$ por $e^{gt}$, el ahorro por trabajador crece y la razón capital-trabajo $K/L$ crece para siempre a tasa $g/b$. |
| `D-Hab09-02` | Tasa de producto errónea | skipped_step | high | $\frac{\dot{Y}}{Y}=n+g$ | Combine el crecimiento de $K$ a $n+g/b$ con el de $L$ a $n$ y $A(t)$ a $g$: $g+a(n+g/b)+(1-a)n=n+ag/b$. |
| `D-Hab09-03` | Razón K/Y constante | conceptual_swap | high | $K/Y$ permanece constante en el largo plazo | Reste la tasa de crecimiento del producto $n+ag/b$ de la del capital $n+g/b$ para hallar que $K/Y$ crece a tasa $g$. |
| `D-Hab09-04` | Participación laboral creciente | conceptual_swap | high | $\frac{wL}{pY}\to 1$ cuando $K/L\to\infty$ | Recuerde que en la función Cobb-Douglas las participaciones factoriales permanecen constantes en $1-a$ y $a$ aunque $K/L\to\infty$. |
| `D-Hab09-05` | Salario real estancado | conceptual_swap | high | $w/p$ tiende a una constante finita | Dado que $K/L$ crece continuamente a tasa $g/b$ y el progreso técnico eleva la productividad, el salario real $w/p$ crece sin límite. |
| `D-Hab09-06` | Confunde b con a | conceptual_swap | high | $\frac{\dot{K}}{K}=n+\frac{g}{a}$ | Resuelva la ecuación diferencial lineal en $K^b$ con $b=1-a$: el exponente asintótico $(nb+g)/b$ da tasa $n+g/b$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab09-01` | - | Cambio tecnológico neutral de Hicks-Solow $Y=A(t)F(K,L)$ con $A(t)=e^{gt}$ | Cambios tecnológicos no neutrales alteran la forma del mapa de isocuantas y las participaciones. | - |

---

### [C-08] Oferta de Trabajo Elástica al Salario Real (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 23: Oferta de Trabajo Elástica al Salario Real
- **Prerequisites:** C-05
- **Recommended Modalities:** proof_dag, multiple_select, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 23)

#### Description & Cognitive Model
Al generalizar la oferta laboral a $L=L_0 e^{nt}(w/p)^h$ en Cobb-Douglas, $\dot{r}=(sF(r,1)-nr)(1+ah/r)^{-1}$ mantiene inalterado el equilibrio $r^*$ y su estabilidad.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Cambia r* en todo caso | conceptual_swap | high | $h>0 \Rightarrow r^*$ disminuye siempre | Iguale $\dot{r}=0$ en $(sF(r,1)-nr)(1+ah/r)^{-1}=0$: como el factor $(1+ah/r)^{-1}>0$, la raíz $r^*$ no cambia bajo la forma (14). |
| `D-C08-02` | Cambia crecimiento de Y | conceptual_swap | high | $\frac{\dot{Y}}{Y}=n(1+h)$ en largo plazo | Note que en equilibrio $r=r^*$ constante implica $w/p$ constante, por lo que $L$, $K$ y $Y$ siguen creciendo a la tasa $n$. |
| `D-C08-03` | Excluye caso general G | conceptual_swap | high | Toda oferta $L=G(t,w/p)$ deja $r^*$ fijo | Verifique en (6b) que $r^*$ solo permanece invariante si $\frac{1}{G}\frac{\partial G}{\partial t}=n$; en general $r^*$ sí se ve afectado. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C08-01` | - | Elasticidad constante $h$ de oferta laboral respecto al salario real $w/p$ | Para salarios reales muy altos debe existir un límite superior dado por el tamaño de la población. | - |

---

### [C-09] Tasa de Ahorro Variable e Impuesto sobre la Renta (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 25: Tasa de Ahorro Variable e Impuesto sobre la Renta
- **Prerequisites:** C-05
- **Recommended Modalities:** invariant_canvas, concept_matching, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 25)

#### Description & Cognitive Model
Cuando la tasa de ahorro depende inversamente de $r$, $\dot{r}=s(r)F(r,1)-nr$ tiene efecto estabilizador; con impuesto proporcional $t$ e inversión pública $v$, la tasa efectiva pasa a $s+(v-s)t$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Estado estacionario de K | conceptual_swap | high | $s(r)\to 0 \Rightarrow$ estado estacionario clásico | Recuerde que la fuerza laboral sigue creciendo exógenamente a tasa $n$; si $r$ asfixia el ahorro, el crecimiento de $L$ reduce $r$ de nuevo. |
| `D-C09-02` | Impuesto siempre reduce r* | conceptual_swap | high | $t>0 \Rightarrow s_{\text{ef}}<s$ siempre | Compare $v$ con $s$ en $s+(v-s)t$: si el Estado invierte una fracción $v>s$ de la recaudación, la tasa efectiva de ahorro aumenta. |
| `D-C09-03` | Confunde signo de s'(r) | conceptual_swap | high | $s'(r)>0$ porque mayor $r$ eleva rendimiento | Recuerde que mayor $r=K/L$ reduce la productividad marginal del capital $q/p$, lo que bajo ahorro creciente en el rendimiento hace caer $s(r)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | Tasa de ahorro decreciente en $r$ por relación inversa entre $r$ y alquiler real $q/p$ | Si el ahorro respondiera inversamente al rendimiento del capital, $s(r)$ sería creciente y desestabilizador. | - |

---

### [C-10] Crecimiento Poblacional Endógeno y Trampa de Estancamiento (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 27: Crecimiento Poblacional Endógeno y Trampa de Estancamiento
- **Prerequisites:** C-09
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 27)

#### Description & Cognitive Model
Si el crecimiento poblacional $n(r)$ depende del ingreso per cápita, $\dot{r}=sF(r,1)-n(r)r$ puede generar un equilibrio estable bajo $r_1$ y un umbral crítico inestable $r_2$ que separa estancamiento de expansión.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C10-01` | Requiere rendimientos crecientes | conceptual_swap | high | La trampa exige indivisibilidades o $F(\lambda K,\lambda L)>\lambda Y$ | Note que Solow demuestra la existencia de trampa de estancamiento $r_1$ y umbral $r_2$ manteniendo estrictamente rendimientos constantes a escala. |
| `D-C10-02` | Invierte estabilidad de r1 y r2 | conceptual_swap | high | $r_1$ es inestable y $r_2$ es estable | Observe en la Figura IX que para $r<r_2$ la curva $n(r)r$ supera a $sF(r,1)$ devolviendo el sistema a $r_1$, mientras $r>r_2$ genera expansión autosostenida. |
| `D-C10-03` | Población constante en expansión | conceptual_swap | high | Superar $r_2$ implica $n(r)=0$ | Verifique en el texto que tras superar el umbral crítico $r_2$, el ingreso per cápita crece de forma autosostenida mientras la población sigue creciendo. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C10-01` | - | Tasa $n(r)$ negativa a ingresos muy bajos, creciente a ingresos medios y decreciente a ingresos altos | Si $n(r)$ fuera estrictamente monótona o constante, desaparecería la multiplicidad de equilibrios. | - |

---

### [Hab-10] Salarios Rígidos y Trampa de Liquidez (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 29: Salarios Rígidos y Trampa de Liquidez
- **Prerequisites:** C-05, Hab-07
- **Recommended Modalities:** adversarial_break, open_symbolic, fill_in_the_blank
- **Evidence Citations:** `solow1956.pdf` (page 29)

#### Description & Cognitive Model
Con salario real rígido $\bar{w}/p$ que fija $r=\bar{r}$, el empleo crece a $\frac{\dot{L}}{L}=\frac{s}{\bar{r}}F(\bar{r},1)$ causando desempleo si es menor que $n$; análogamente, una tasa de interés rígida en trampa de liquidez subutiliza capital.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab10-01` | Desempleo si pendiente > n | skipped_step | high | $\frac{s}{\bar{r}}F(\bar{r},1)>n \Rightarrow$ desempleo creciente | Compare la tasa de crecimiento del empleo $(s/\bar{r})F(\bar{r},1)$ con $n$: si la pendiente del rayo es menor que $n$, falta capital para absorber la fuerza laboral. |
| `D-Hab10-02` | Desempleo con salario bajo | skipped_step | high | $\bar{r}>r^* \Rightarrow$ desempleo | Note que un salario real rígido demasiado alto implica $\bar{r}>r^*$ solo si $\dot{r}<0$; revise el signo de $\dot{r}=sF(\bar{r},1)-n\bar{r}<0$ que da $(s/\bar{r})F(\bar{r},1)<n$. |
| `D-Hab10-03` | Basta modelo real en trampa | conceptual_swap | high | El modelo real explica completamente la trampa de liquidez | Recuerde la advertencia de Solow: al haber asignación entre efectivo y capital, el nivel de precios importa y se requiere una dinámica monetaria. |
| `D-Hab10-04` | Pleno empleo de capital en trampa | conceptual_swap | high | En la trampa de liquidez todo el capital está en uso | Considere que si la tasa de interés queda rígida por encima del nivel correspondiente al equilibrio, resulta una subutilización del capital disponible. |
| `D-Hab10-05` | Confunde L y K en (15) | conceptual_swap | high | En $\bar{M}=Q(Y,q/p)$ se resuelve para $L(t)$ con salario rígido | Verifique que con pleno empleo laboral $L=L_0 e^{nt}$, la ecuación monetaria (15) determina el capital efectivamente empleado $K(t)$. |
| `D-Hab10-06` | Omite factor 1/$r_bar$ | conceptual_swap | high | $\frac{\dot{L}}{L}=sF(\bar{r},1)$ | Sustituya $K=\bar{r}L$ en $\dot{K}=sF(K,L)$ para obtener $\bar{r}\dot{L}=sLF(\bar{r},1)$, dividiendo luego por $\bar{r}L$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab10-01` | - | Rigidez a la baja del salario real $\bar{w}/p$ o elasticidad infinita de demanda de dinero | Con precios y salarios perfectamente flexibles, el mercado se vacía y no hay desempleo ni subutilización. | - |

---
