# Cognitive Task Analysis (CTA): Solow V17 M20

- **Course ID:** `solow_v17_m20`
- **Macro-Competency:** Dominio y aplicación analítica integral de Solow V17 M20
- **Structure:** 19 total competencies (1 Facts, 9 Concepts, 9 Skills) with 90 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `PRE-01` | Supuestos Neoclásicos y Forma Per Cápita | Fact | Understand | Unidad 2: Supuestos Neoclásicos y Forma Per Cápita | - | 7 |
| `C-01` | Ecuación Fundamental y Línea de Fase | Concept | Evaluate | Unidad 3: Ecuación Fundamental y Línea de Fase | PRE-01 | 4 |
| `C-02` | Estado Uniforme y Progreso Tecnológico | Concept | Analyze | Unidad 4: Estado Uniforme y Progreso Tecnológico | C-01 | 3 |
| `Hab-01` | Linealización de Bernoulli Cobb-Douglas | Skill | Evaluate | Unidad 4: Linealización de Bernoulli Cobb-Douglas | C-01 | 6 |
| `Hab-02` | Trayectoria Temporal y Equilibrio Asintótico | Skill | Evaluate | Unidad 5: Trayectoria Temporal y Equilibrio Asintótico | Hab-01, C-02 | 6 |
| `C-03` | Ecuación Fundamental Capital-Trabajo | Concept | Evaluate | Unidad 6: Ecuación Fundamental Capital-Trabajo | PRE-01 | 3 |
| `C-04` | Estabilidad y Múltiples Equilibrios | Concept | Evaluate | Unidad 7: Estabilidad y Múltiples Equilibrios | C-03 | 3 |
| `Hab-03` | Dinámica Harrod-Domar con Proporciones Fijas | Skill | Evaluate | Unidad 10: Dinámica Harrod-Domar con Proporciones Fijas | C-04 | 6 |
| `Hab-04` | Solución Explícita Cobb-Douglas | Skill | Evaluate | Unidad 13: Solución Explícita Cobb-Douglas | C-03, C-04 | 6 |
| `Hab-05` | Equilibrio con Sustitución Parcial p=1/2 | Skill | Evaluate | Unidad 14: Equilibrio con Sustitución Parcial p=1/2 | C-04 | 6 |
| `C-05` | Precios Competitivos y Productividad Marginal | Concept | Evaluate | Unidad 16: Precios Competitivos y Productividad Marginal | PRE-01, C-03 | 3 |
| `C-06` | Arbitraje y Precios Factoriales | Concept | Evaluate | Unidad 17: Arbitraje y Precios Factoriales | C-05 | 3 |
| `C-07` | Dinámica de Isocuantas y Precios | Concept | Analyze | Unidad 19: Dinámica de Isocuantas y Precios | C-06 | 3 |
| `Hab-06` | Participaciones Factoriales en Equilibrio | Skill | Evaluate | Unidad 21: Participaciones Factoriales en Equilibrio | C-06, C-07 | 6 |
| `Hab-07` | Progreso Tecnológico Neutral | Skill | Evaluate | Unidad 22: Progreso Tecnológico Neutral | C-06 | 6 |
| `C-08` | Oferta Laboral Elástica y Ahorro Variable | Concept | Evaluate | Unidad 24: Oferta Laboral Elástica y Ahorro Variable | C-06 | 4 |
| `Hab-08` | Incidencia Fiscal en el Ahorro | Skill | Analyze | Unidad 26: Incidencia Fiscal en el Ahorro | C-08 | 6 |
| `C-09` | Población Endógena y Trampa de Pobreza | Concept | Evaluate | Unidad 28: Población Endógena y Trampa de Pobreza | C-08 | 3 |
| `Hab-09` | Rigideces Nominales y Desempleo | Skill | Evaluate | Unidad 29: Rigideces Nominales y Desempleo | C-06, C-07 | 6 |

---

## Detailed Competency Specifications

### [PRE-01] Supuestos Neoclásicos y Forma Per Cápita (Fact)

- **Bloom Level:** Understand
- **Session:** Unidad 2: Supuestos Neoclásicos y Forma Per Cápita
- **Prerequisites:** None
- **Recommended Modalities:** fill_in_the_blank, multiple_select, concept_matching
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2), `solow1956.pdf` (page 3)

#### Description & Cognitive Model
Formulación base del modelo neoclásico de Solow con función de producción $Y=F(K,L)=L\phi(k)$ con rendimientos constantes a escala ($k\equiv K/L$, $\phi'(k)>0$, $\phi''(k)<0$), acumulación $\dot{K}=sY$ con ahorro constante $s$ y crecimiento laboral exógeno $\dot{L}/L=n>0$ en pleno empleo.

#### Fused Distractor Models (7)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-PRE01-01` | Proporciones fijas | conceptual_swap | high | $Q=\rho K$ | Distinga el modelo de proporciones variables de Solow $Q=f(K,L)$ de la función de proporciones fijas de Domar. |
| `D-PRE01-05` | Proporciones fijas | conceptual_swap | high | $Y=\min(K/a,L/b)$ como único caso | Recuerde que Solow reemplaza las proporciones fijas de Harrod-Domar por sustitución neoclásica continua entre capital y trabajo. |
| `D-PRE01-02` | Retornos crecientes | conceptual_swap | high | $\phi''(k)>0$ | Recuerde que la productividad marginal decreciente del capital $f_{KK}<0$ implica concavidad estricta $\phi''(k)<0$. |
| `D-PRE01-06` | Rendimientos decrecientes a escala | conceptual_swap | high | $F(\lambda K,\lambda L)<\lambda F(K,L)$ | Aplique homogeneidad de grado uno en capital y trabajo para poder expresar el producto por trabajador solo en función de $r=K/L$. |
| `D-PRE01-03` | Ahorro sobre capital | conceptual_swap | high | $\dot{K}=sK$ | Aplique la propensión marginal al ahorro $s$ sobre el flujo de producto $Q$, nunca sobre el stock de capital $K$. |
| `D-PRE01-07` | Desempleo estructural | conceptual_swap | high | $L_{\text{emp}}<L_0 e^{nt}$ | Considere que el modelo neoclásico base supone ajuste instantáneo del salario real para mantener pleno empleo perpetuo $L(t)=L_0 e^{nt}$. |
| `D-PRE01-04` | Fuerza laboral fija | conceptual_swap | high | $\dot{L}=0$ | Considere que la mano de obra crece exponencialmente a tasa exógena positiva $\dot{L}/L=\lambda>0$ en el modelo. |

---

### [C-01] Ecuación Fundamental y Línea de Fase (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Ecuación Fundamental y Línea de Fase
- **Prerequisites:** PRE-01
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
Derivación y análisis cualitativo-gráfico de la ecuación fundamental $\dot{k}=s\phi(k)-\lambda k$ mediante la intersección de $s\phi(k)$ y $\lambda k$ en el equilibrio estable $\bar{k}$

#### Fused Distractor Models (4)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Omite dilución laboral | conceptual_swap | high | $\dot{k}=s\phi(k)$ | Incluya el término $-\lambda k$ proveniente de diferenciar $K=kL$ mediante la regla del producto al dividir por $L$. |
| `D-C01-02` | Signo invertido en fase | conceptual_swap | high | $\dot{k}=\lambda k-s\phi(k)$ | Recuerde que la acumulación $s\phi(k)$ impulsa $\dot{k}$ positivamente y el crecimiento laboral $\lambda k$ lo diluye. |
| `D-C01-03` | Pendiente positiva estable | conceptual_swap | high | Equilibrio estable con $d\dot{k}/dk>0$ | Verifique en la línea de fase que la convergencia desde cualquier $k(0)>0$ exige pendiente negativa en $\bar{k}$. |
| `D-C01-04` | Ahorro sin producto | conceptual_swap | high | $s\phi(0)>0$ | Considere que el capital es indispensable en producción: si $K=0$ y $k=0$, entonces $Q=0$ y $s\phi(0)=0$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Capital indispensable $\phi(0)=0$ y cruce positivo con $\lambda k$ | Sin cruce positivo no existe equilibrio intertemporal $\bar{k}>0$. | - |
| `A-C01-02` | - | Pendiente negativa de la línea de fase en $\bar{k}$ | Si $d\dot{k}/dk>0$ en $\bar{k}$, el equilibrio sería inestable. | - |

---

### [C-02] Estado Uniforme y Progreso Tecnológico (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 4: Estado Uniforme y Progreso Tecnológico
- **Prerequisites:** C-01
- **Recommended Modalities:** adversarial_break, multiple_select, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
Caracterización del estado uniforme en $\bar{k}$ donde $K$, $L$, $Q$ e inversión neta $\dot{K}$ crecen a tasa común $\lambda$, y desplazamiento ascendente de $\bar{k}$ ante progreso tecnológico $Q=T(t)f(K,L)$ con $dT/dt>0$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Confunde uniforme con estacionario | conceptual_swap | high | $\dot{K}=\dot{Q}=0$ en $\bar{k}$ | Distinga estado estacionario (tasa cero) de estado uniforme: en $\bar{k}$ la razón $k$ es constante pero $K,L,Q$ crecen a tasa $\lambda$. |
| `D-C02-02` | Inversión neta nula | conceptual_swap | high | $\dot{K}=0$ en equilibrio | Observe que $K=kL$ con $k=\bar{k}$ constante y $L$ creciendo a tasa $\lambda$ implica que $\dot{K}=sL\phi(\bar{k})$ crece también a tasa $\lambda$. |
| `D-C02-03` | Desplazamiento inverso | conceptual_swap | high | $dT/dt>0$ reduce $\bar{k}$ | Note que un aumento en $T(t)$ desplaza hacia arriba $s\phi(k)$ y genera intersecciones más altas con el rayo $\lambda k$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | Progreso tecnológico multiplicativo $Q=T(t)f(K,L)$ con $dT/dt>0$ | Si $T$ es constante, no hay sucesión creciente de estados uniformes. | - |

---

### [Hab-01] Linealización de Bernoulli Cobb-Douglas (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Linealización de Bernoulli Cobb-Douglas
- **Prerequisites:** C-01
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, adversarial_break
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
Transformación de la ecuación fundamental de Solow con producción Cobb-Douglas $Q=K^\alpha L^{1-\alpha}$ en ecuación de Bernoulli $\dot{k}+\lambda k=sk^\alpha$ y su versión linealizada $\frac{dz}{dt}+(1-\alpha)\lambda z=(1-\alpha)s$ mediante $z=k^{1-\alpha}$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Sustitución errónea z | skipped_step | high | $z=k^\alpha$ | Aplique la sustitución estándar de Bernoulli $z=k^{1-m}$ con exponente $m=\alpha$, es decir $z=k^{1-\alpha}$. |
| `D-Hab01-02` | Omite factor regla cadena | skipped_step | high | $\frac{dz}{dt}+\lambda z=s$ | Multiplique ambos términos de $\dot{k}+\lambda k=sk^\alpha$ por $(1-\alpha)k^{-\alpha}$ al aplicar la regla de la cadena. |
| `D-Hab01-03` | Exponente m negativo | conceptual_swap | high | $z=k^{\alpha-1}$ | Verifique el signo del exponente en Bernoulli: para $\dot{k}+\lambda k=sk^\alpha$ corresponde $z=k^{1-\alpha}$ con $\alpha\in(0,1)$. |
| `D-Hab01-04` | Conserva k en término fuente | conceptual_swap | high | $\frac{dz}{dt}+(1-\alpha)\lambda z=(1-\alpha)sk^\alpha$ | Cancele $k^\alpha$ con $k^{-\alpha}$ al multiplicar la ecuación de Bernoulli por $(1-\alpha)k^{-\alpha}$ para lograr linealidad. |
| `D-Hab01-05` | Signo cambiado en lambda | conceptual_swap | high | $\frac{dz}{dt}-(1-\alpha)\lambda z=(1-\alpha)s$ | Mantenga el signo positivo del término de dilución al pasar $-\lambda k$ al miembro izquierdo: $\dot{k}+\lambda k=sk^\alpha$. |
| `D-Hab01-06` | Forma per cápita incorrecta | conceptual_swap | high | $\phi(k)=k^{1-\alpha}$ | Divida $Q=K^\alpha L^{1-\alpha}$ entre $L$ para obtener $Q/L=(K/L)^\alpha=k^\alpha$, por lo que $\phi(k)=k^\alpha$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Elasticidad del capital $\alpha\in(0,1)$ en $Q=K^\alpha L^{1-\alpha}$ | Si $\alpha=1$, $1-\alpha=0$ y colapsa la transformación $z=k^{1-\alpha}$. | - |

---

### [Hab-02] Trayectoria Temporal y Equilibrio Asintótico (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Trayectoria Temporal y Equilibrio Asintótico
- **Prerequisites:** Hab-01, C-02
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model, adversarial_break
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 5)

#### Description & Cognitive Model
Resolución de la trayectoria temporal $k(t)^{1-\alpha}=\left[k(0)^{1-\alpha}-\frac{s}{\lambda}\right]e^{-(1-\alpha)\lambda t}+\frac{s}{\lambda}$ y obtención del equilibrio asintótico $\bar{k}=\left(\frac{s}{\lambda}\right)^{1/(1-\alpha)}$ cuando $t\to\infty$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Exponente asintótico directo | skipped_step | high | $\bar{k}=(s/\lambda)^{1-\alpha}$ | Despeje $k$ desde $k^{1-\alpha}=s/\lambda$ elevando ambos miembros a la potencia recíproca $1/(1-\alpha)$. |
| `D-Hab02-02` | Omite factor en exponencial | skipped_step | high | $e^{-\lambda t}$ | Use el coeficiente completo $a=(1-\alpha)\lambda$ de la ecuación linealizada dentro del exponente $-at=-(1-\alpha)\lambda t$. |
| `D-Hab02-03` | Invierte razón s sobre lambda | conceptual_swap | high | $\bar{k}=(\lambda/s)^{1/(1-\alpha)}$ | Recuerde que $\bar{k}$ varía directamente con el ahorro $s$ e inversamente con $\lambda$, por lo que la razón es $s/\lambda$. |
| `D-Hab02-04` | Olvida raíz en condición inicial | conceptual_swap | high | $k(t)=\left[k(0)-\frac{s}{\lambda}\right]e^{-(1-\alpha)\lambda t}+\frac{s}{\lambda}$ | Recuerde que la solución lineal aplica a $z(t)=k(t)^{1-\alpha}$ con condición inicial $z(0)=k(0)^{1-\alpha}$, no a $k(t)$. |
| `D-Hab02-05` | Término particular erróneo | conceptual_swap | high | $b=\frac{(1-\alpha)s}{\lambda}$ | Simplifique el factor común $(1-\alpha)$ al calcular el estado particular $b/a=\frac{(1-\alpha)s}{(1-\alpha)\lambda}=\frac{s}{\lambda}$. |
| `D-Hab02-06` | Exponente positivo divergente | conceptual_swap | high | $e^{+(1-\alpha)\lambda t}$ | Note que $dz/dt+az=b$ con $a=(1-\alpha)\lambda>0$ tiene solución homogénea decreciente $e^{-at}$ que converge cuando $t\to\infty$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Positividad de $(1-\alpha)\lambda>0$ y condición inicial $k(0)>0$ | Si $(1-\alpha)\lambda\le 0$, el término exponencial no decae a cero. | - |

---

### [C-03] Ecuación Fundamental Capital-Trabajo (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 6: Ecuación Fundamental Capital-Trabajo
- **Prerequisites:** PRE-01
- **Recommended Modalities:** proof_dag, open_symbolic, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 6)

#### Description & Cognitive Model
Derivación e interpretación de la ecuación diferencial $\dot{r}=sF(r,1)-nr$ para la razón capital-trabajo $r=K/L$ bajo rendimientos constantes a escala

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Omite dilución laboral | conceptual_swap | high | $\dot{r}=sF(r,1)$ | Reste el término de dilución $nr$ al ahorro per cápita $sF(r,1)$, pues el crecimiento laboral $n$ reduce el capital por trabajador. |
| `D-C03-02` | Multiplica por L | conceptual_swap | high | $\dot{r}=sF(K,L)-nK$ | Divida ambos miembros de $\dot{K}=sF(K,L)$ entre $L$ usando $F(K,L)=LF(r,1)$ y $\dot{r}/r=\dot{K}/K-\dot{L}/L$ para aislar $r$. |
| `D-C03-03` | Signo invertido | conceptual_swap | high | $\dot{r}=nr-sF(r,1)$ | Verifique que el ahorro $sF(r,1)$ incrementa la razón capital-trabajo mientras el crecimiento poblacional $nr$ la diluye. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | Homogeneidad de primer grado $F(K,L)=L\cdot F(K/L,1)$ | Sin rendimientos constantes a escala no puede reducirse la dinámica a la única variable $r$. | - |

---

### [C-04] Estabilidad y Múltiples Equilibrios (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 7: Estabilidad y Múltiples Equilibrios
- **Prerequisites:** C-03
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 7)

#### Description & Cognitive Model
Análisis cualitativo de $\dot{r}=0$ en $sF(r,1)=nr$: estabilidad asintótica cuando $sF(r,1)$ cruza $nr$ desde arriba (Fig. I), equilibrios múltiples (Fig. II) o inexistencia (Fig. III)

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Confunde cruce inestable | conceptual_swap | high | $r_2$ es estable en Fig. II | Evalúe el signo de $\dot{r}=sF(r,1)-nr$ a ambos lados del cruce: solo es estable si $\dot{r}>0$ a la izquierda y $\dot{r}<0$ a la derecha. |
| `D-C04-02` | Estabilidad universal | conceptual_swap | high | Siempre existe un único $r^*>0$ | Compruebe si la productividad marginal permite que $sF(r,1)$ corte a $nr$: si $s_1 F^1(r,1)>nr$ siempre, $r$ diverge sin equilibrio. |
| `D-C04-03` | Origen siempre equilibrio | conceptual_swap | high | $r=0$ es equilibrio aunque $F(0,1)>0$ | Verifique si $F(0,1)=0$; cuando es posible producir sin capital ($F(0,1)>0$), en $r=0$ resulta $\dot{r}=sF(0,1)>0$ y el sistema despega. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | Productividad marginal decreciente $F_{rr}(r,1)<0$ para concavidad de $sF(r,1)$ | Sin concavidad o condiciones de pendiente adecuadas pueden surgir equilibrios múltiples o divergencia. | - |

---

### [Hab-03] Dinámica Harrod-Domar con Proporciones Fijas (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 10: Dinámica Harrod-Domar con Proporciones Fijas
- **Prerequisites:** C-04
- **Recommended Modalities:** open_symbolic, adversarial_break, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 10)

#### Description & Cognitive Model
Resolución de $\dot{r}=s\min(r/a,1/b)-nr$ en los tres regímenes entre tasa natural $n$ y garantizada $s/a$: redundancia laboral ($n>s/a$), equilibrio neutro ($n=s/a$) y exceso de capital ($n<s/a$)

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Ignora cuello de botella | skipped_step | high | $\dot{r}=sr/a-nr$ para todo $r$ | Compare $r$ con el umbral $a/b$ antes de resolver: para $r\ge a/b$ la producción por trabajador se satura en $1/b$ y $\dot{r}=s/b-nr$. |
| `D-Hab03-02` | Invierte fracción empleada | skipped_step | high | Proporción empleada $s/(an_3)$ | Divida el capital requerido por trabajador $a/b$ entre el equilibrio $r^*=s/(n_3 b)$ para obtener la proporción empleada $an_3/s<1$. |
| `D-Hab03-03` | Confunde tasas n y s/a | conceptual_swap | high | $n>s/a$ genera exceso de capital | Analice que si $n_1>s/a$, la recta $n_1 r$ supera a $s\min(r/a,1/b)$ en todo $r>0$, haciendo caer $r$ por debajo de $a/b$ con redundancia laboral. |
| `D-Hab03-04` | Estabilidad única en n=s/a | conceptual_swap | high | Si $n_2=s/a$, siempre converge a $a/b$ | Distinga que cuando $n_2=s/a$ y $r_0<a/b$, resulta $\dot{r}=(s/a-n_2)r=0$, preservando indefinidamente el porcentaje inicial de desempleo. |
| `D-Hab03-05` | Error en empleo efectivo | conceptual_swap | high | Empleo es $aK/b$ con capital limitante | Recuerde que con $K$ como cuello de botella el producto es $K/a$ y cada unidad de producto requiere $b$ trabajadores, dando empleo $bK/a$. |
| `D-Hab03-06` | Omite régimen transitorio | conceptual_swap | high | Salta directo a $r=0$ si $n_1>s/a$ | Resuelva primero $\dot{r}=s/b-n_1 r$ desde $r_0>a/b$ hasta el instante $t_1$ en que $r=a/b$, y luego $\dot{r}=(s/a-n_1)r$ para $t\ge t_1$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | Coeficientes técnicos fijos $a>0$ y $b>0$ sin sustituibilidad factorial | Si existe sustituibilidad continua entre factores, desaparece la rigidez de esquina y el filo de navaja. | - |

---

### [Hab-04] Solución Explícita Cobb-Douglas (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 13: Solución Explícita Cobb-Douglas
- **Prerequisites:** C-03, C-04
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 13)

#### Description & Cognitive Model
Integración directa de $\dot{K}=sK^a(L_0 e^{nt})^{1-a}$ con $b=1-a$ y determinación asintótica de $r^*=(s/n)^{1/(1-a)}$, producto per cápita $(s/n)^{a/(1-a)}$ y razón capital-producto $C=s/n$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Exponente sin invertir | skipped_step | high | $r^*=(s/n)^{1-a}$ | Despeje $r$ en $sr^a=nr$ dividiendo por $r^a$ para obtener $r^{1-a}=s/n$, y eleve ambos lados al recíproco $1/(1-a)=1/b$. |
| `D-Hab04-02` | Invierte razón s/n | skipped_step | high | $r^*=(n/s)^{1/(1-a)}$ | Verifique el sentido económico: mayor tasa de ahorro $s$ y menor crecimiento laboral $n$ deben elevar el capital de equilibrio $r^*$. |
| `D-Hab04-03` | Exponente erróneo en Y/L | conceptual_swap | high | $Y/L\to (s/n)^{1/(1-a)}$ | Sustituya $r^*=(s/n)^{1/b}$ en la función intensiva $Y/L=r^a$ para obtener el ingreso per cápita límite $(s/n)^{a/b}$. |
| `D-Hab04-04` | Coeficiente capital erróneo | conceptual_swap | high | $C=K/Y=n/s$ | Calcule $C=K/Y=r^*/(r^*)^a=(r^*)^{1-a}=s/n$, de modo que la tasa natural $n=s/C$ coincide endógenamente con la garantizada. |
| `D-Hab04-05` | Olvida condición inicial K0 | conceptual_swap | high | $K(t)=[(s/n)L_0^b e^{nbt}]^{1/b}$ | Incluya la constante de integración evaluada en $t=0$ al resolver la ecuación de Bernoulli $\dot{K}=sK^a(L_0 e^{nt})^{1-a}$. |
| `D-Hab04-06` | Tasa de crecimiento errónea | conceptual_swap | high | $K(t)$ crece a tasa $nb$ | Aplique la potencia exterior $1/b$ sobre $e^{nbt}$ cuando $t\to\infty$ para comprobar que $K(t)$ crece asintóticamente a tasa $n$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Elasticidad del capital $a\in(0,1)$ estrictamente menor que la unidad | Si $a\ge 1$, la curva $sr^a$ no cruza desde arriba a $nr$ y desaparece el equilibrio estable. | - |

---

### [Hab-05] Equilibrio con Sustitución Parcial p=1/2 (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 14: Equilibrio con Sustitución Parcial p=1/2
- **Prerequisites:** C-04
- **Recommended Modalities:** open_symbolic, adversarial_break, fill_in_the_blank
- **Evidence Citations:** `solow1956.pdf` (page 14)

#### Description & Cognitive Model
Análisis de $\dot{r}=s(a\sqrt{r}+1)^2-nr$ para $Y=(a\sqrt{K}+\sqrt{L})^2$: condición de existencia $sa^2<n$, cálculo de $r^*=(1/(\sqrt{n/s}-a))^2$ e ingreso límite $1/(1-a\sqrt{s/n})^2$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Condición de existencia invertida | skipped_step | high | Existe $r^*$ cuando $sa^2>n$ | Observe que si $sa^2>n$, entonces $\sqrt{n/s}-a<0$ y $s(a\sqrt{r}+1)^2$ permanece siempre por encima de $nr$, haciendo diverger $r\to\infty$. |
| `D-Hab05-02` | Olvida elevar al cuadrado | skipped_step | high | $r^*=1/(\sqrt{n/s}-a)$ | Recuerde que $\sqrt{s}(a\sqrt{r}+1)=\sqrt{n}\sqrt{r}$ despeja $\sqrt{r^*}$, por lo que debe elevar al cuadrado para obtener $r^*$. |
| `D-Hab05-03` | Error en intercepto r=0 | conceptual_swap | high | $sF(0,1)=0$ en Fig. V | Evalúe $F(0,1)=(a\cdot 0+1)^2=1$, de modo que la curva $sF(r,1)$ parte de altura positiva $s$ en $r=0$ porque solo el trabajo produce. |
| `D-Hab05-04` | Error en ingreso límite | conceptual_swap | high | $Y/L\to 1/(1-a\sqrt{n/s})^2$ | Sustituya $\sqrt{r^*}=1/(\sqrt{n/s}-a)$ en $(a\sqrt{r^*}+1)^2$ y simplifique $(\frac{\sqrt{n/s}}{\sqrt{n/s}-a})^2=1/(1-a\sqrt{s/n})^2$. |
| `D-Hab05-05` | Falta factor 2a en expansión | conceptual_swap | high | $Y=a^2 K+L$ | Desarrolle correctamente el binomio al cuadrado $Y=a^2 K+L+2a\sqrt{KL}$ antes de dividir por $L$ o factorizar la ecuación diferencial. |
| `D-Hab05-06` | Signo erróneo en factorización | conceptual_swap | high | $A=a+\sqrt{n/s}$ y $B=a+\sqrt{n/s}$ | Factorice $(a^2-n/s)r+2a\sqrt{r}+1=(A\sqrt{r}+1)(B\sqrt{r}+1)$ con $A=a-\sqrt{n/s}$ y $B=a+\sqrt{n/s}$ para integrar. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | Parámetro de curvatura $0<p<1$ en $Y=(aK^p+L^p)^{1/p}$ | Si $p>1$ las isocuantas tienen convexidad incorrecta y si $p=1$ hay sustitución perfecta sin rendimientos decrecientes. | - |

---

### [C-05] Precios Competitivos y Productividad Marginal (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 16: Precios Competitivos y Productividad Marginal
- **Prerequisites:** PRE-01, C-03
- **Recommended Modalities:** proof_dag, multiple_select, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 16)

#### Description & Cognitive Model
Determinación competitiva del salario real $w/p=\partial F/\partial L$ y la renta real del capital $q/p=\partial F/\partial K$ que vacían los mercados, dependiendo únicamente de $r=K/L$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Dependencia de escala | conceptual_swap | high | $\partial F/\partial L$ depende de $K$ y $L$ por separado | Aplique el teorema de Euler para funciones homogéneas de grado uno: las derivadas parciales son homogéneas de grado cero y solo dependen de $r$. |
| `D-C05-02` | Determinación del nivel de precios | conceptual_swap | high | El modelo real determina $p(t)$ | Recuerde que en el sistema real de Solow nada determina el nivel absoluto de precios, por lo que $p(t)$ se toma como dado. |
| `D-C05-03` | Confunde renta con tasa de interés | conceptual_swap | high | $\partial F/\partial K=i(t)$ directamente | Distinga la renta real del servicio del capital $q/p=\partial F/\partial K$ del precio de transferencia $p(t)$ y la tasa de interés $i(t)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Competencia pura y ajuste instantáneo de precios factoriales para vaciar el mercado | Con rigideces nominales o competencia monopolística falla la igualdad estricta entre retribución real y productividad marginal. | - |

---

### [C-06] Arbitraje y Precios Factoriales (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 17: Arbitraje y Precios Factoriales
- **Prerequisites:** C-05
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 17)

#### Description & Cognitive Model
Determinación competitiva del salario real $\frac{w}{p}=\frac{\partial F}{\partial L}$, renta real $\frac{q}{p}=\frac{\partial F}{\partial K}$ y condición de no arbitraje $i(t)=\frac{q(t)}{p(t)}+\frac{\dot{p}(t)}{p(t)}$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Iguala tasa nominal y renta | conceptual_swap | high | $i(t)=q(t)/p(t)$ | Incluya la variación porcentual del precio del bien $\dot{p}(t)/p(t)$ para igualar el rendimiento monetario de bonos y capital físico. |
| `D-C06-02` | Signo invertido en inflación | conceptual_swap | high | $i(t)=q(t)/p(t)-\dot{p}(t)/p(t)$ | Recuerde que si el precio del capital sube ($\dot{p}>0$), su tenencia genera ganancia de capital que se suma al alquiler real $q/p$. |
| `D-C06-03` | Confunde renta nominal con real | conceptual_swap | high | $q(t)=\partial F/\partial K$ | Divida la renta monetaria $q$ por el precio del producto $p$ porque la productividad marginal $\partial F/\partial K$ se mide en unidades reales. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Previsión perfecta y ausencia de riesgo e incertidumbre en la tenencia de activos | Sin previsión perfecta ni neutralidad al riesgo surgen primas de liquidez que rompen la igualdad exacta de arbitraje. | - |
| `A-C06-02` | - | Competencia perfecta con rendimientos constantes a escala en $F(K,L)$ | Sin competencia perfecta los precios factoriales dejan de igualar las productividades marginales. | - |

---

### [C-07] Dinámica de Isocuantas y Precios (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 19: Dinámica de Isocuantas y Precios
- **Prerequisites:** C-06
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 19)

#### Description & Cognitive Model
Relación entre la razón capital-trabajo $r=K/L$ y los precios relativos $w/q$ a lo largo de rayos desde el origen en isocuantas neoclásicas y de Harrod-Domar

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Invierte monotonía de w/q | conceptual_swap | high | Al aumentar $r$, la razón $w/q$ disminuye | Observe que bajo convexidad normal de las isocuantas, al subir $r=K/L$ el capital se vuelve más abundante y $w/q$ aumenta hacia su equilibrio. |
| `D-C07-02` | Excluye indeterminación en a/b | conceptual_swap | high | En $r=a/b$ los precios $w$ y $q$ son únicos | Verifique que en el ángulo recto $r=a/b$ ambos factores son escasos y solo se restringe $aq+bw=p$, quedando indeterminada la imputación. |
| `D-C07-03` | Atribuye producto al factor redundante | conceptual_swap | high | Si $r>a/b$, entonces $w=0$ y $q=p/a$ | Identifique cuál factor es redundante: cuando $r>a/b$ sobra capital ($q=0$) y todo el producto se imputa al trabajo ($w=p/b$). |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Rendimientos constantes a escala que mantienen invariante la pendiente de las isocuantas sobre cada rayo $K=rL$ | Si los rendimientos no fueran constantes, $w/q$ dependería de la escala absoluta y no solo de $r$. | - |

---

### [Hab-06] Participaciones Factoriales en Equilibrio (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 21: Participaciones Factoriales en Equilibrio
- **Prerequisites:** C-06, C-07
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 21)

#### Description & Cognitive Model
Cálculo analítico de $w/p$, $q/p$ y la participación laboral $(w/p)(L/Y)$ en crecimiento balanceado para Cobb-Douglas y $Y=(a\sqrt{K}+\sqrt{L})^2$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Participación constante en ejemplo 3 | skipped_step | high | $(w/p)(L/Y)=1-a$ para $Y=(a\sqrt{K}+\sqrt{L})^2$ | Calcule $(w/p)(L/Y)$ usando $r^*=(\sqrt{n/s}-a)^{-2}$: en $Y=(a\sqrt{K}+\sqrt{L})^2$ la participación laboral depende de $s$ y $n$. |
| `D-Hab06-02` | Signo erróneo en participación | skipped_step | high | $(w/p)(L/Y)=1+a\sqrt{s/n}$ | Simplifique $\frac{1}{1-a\sqrt{s/n}}\cdot(1-a\sqrt{s/n})^2=1-a\sqrt{s/n}$; las participaciones factoriales deben estar entre cero y uno. |
| `D-Hab06-03` | Invierte razón s/n | conceptual_swap | high | $(w/p)(L/Y)=1-a\sqrt{n/s}$ | Revise el despeje desde $w/p=\frac{1}{\sqrt{n/s}-a}+1=\frac{1}{1-a\sqrt{s/n}}$ para conservar la razón correcta $\sqrt{s/n}$. |
| `D-Hab06-04` | Omite exponente de r* en Cobb-Douglas | conceptual_swap | high | $w/p=(1-a)(s/n)$ | Sustituya $r^*=(s/n)^{1/(1-a)}$ en $w/p=(1-a)r^a$ para obtener el salario real de equilibrio $(1-a)(s/n)^{a/(1-a)}$. |
| `D-Hab06-05` | Invierte renta real Cobb-Douglas | conceptual_swap | high | $q/p=as/n$ | Evalúe $q/p=ar^{a-1}$ en $r^*=(s/n)^{1/(1-a)}$: el exponente negativo invierte la fracción a $q/p=an/s$. |
| `D-Hab06-06` | Confunde salario real con participación | conceptual_swap | high | $(w/p)(L/Y)=\frac{1}{1-a\sqrt{s/n}}$ | Divida el salario real $w/p$ por el producto medio del trabajo $Y/L=(1-a\sqrt{s/n})^{-2}$ para obtener la participación relativa. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Existencia de equilibrio balanceado interior con $\sqrt{n/s}>a$ en el tercer ejemplo | Si $\sqrt{n/s}\le a$, no existe razón $r^*$ finita y la fórmula de participación carece de sentido. | - |

---

### [Hab-07] Progreso Tecnológico Neutral (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 22: Progreso Tecnológico Neutral
- **Prerequisites:** C-06
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 22)

#### Description & Cognitive Model
Resolución de $\dot{K}=se^{gt}K^a(L_0e^{nt})^{1-a}$ en $Y=A(t)F(K,L)$ para derivar las tasas asintóticas de crecimiento de $K$, $Y$, $K/L$ y $K/Y$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Omite efecto compuesto en K | skipped_step | high | La tasa asintótica de $K$ es $n+g$ | Integre la ecuación diferencial con $b=1-a$: el exponente temporal $(nb+g)t$ elevado a $1/b$ produce una tasa asintótica $n+g/(1-a)$. |
| `D-Hab07-02` | Iguala crecimiento de Y y K | skipped_step | high | La tasa asintótica de $Y$ es $n+\frac{g}{1-a}$ | Sustituya $K\sim e^{(n+g/b)t}$ en $Y=e^{gt}K^a L^{1-a}$: el crecimiento de $Y$ resulta $g+a(n+g/b)+(1-a)n=n+ag/b$. |
| `D-Hab07-03` | Supone K/L estacionario | conceptual_swap | high | $K/L$ converge a un equilibrio constante | Compare las tasas de $K$ ($n+g/b$) y $L$ ($n$): la diferencia $g/(1-a)>0$ implica que $K/L$ crece indefinidamente. |
| `D-Hab07-04` | Confunde tasa de K/Y con g/b | conceptual_swap | high | El coeficiente capital-producto $K/Y$ crece a tasa $\frac{g}{1-a}$ | Reste la tasa de $Y$ ($n+ag/b$) de la tasa de $K$ ($n+g/b$): como $b=1-a$, se obtiene $(1-a)g/b=g$. |
| `D-Hab07-05` | Omite factor b en la solución | conceptual_swap | high | $K(t)$ tiene coeficiente $\frac{s}{n+g}L_0^b$ | Use $\frac{d}{dt}(K^b)=bK^{b-1}\dot{K}$ antes de integrar el término exponencial $e^{(nb+g)t}$, lo que introduce $\frac{bs}{nb+g}$. |
| `D-Hab07-06` | Participación laboral creciente | conceptual_swap | high | Al subir $K/L$ indefinidamente, la participación laboral aumenta | Recuerde que en Cobb-Douglas el alza de $K/L$ eleva el salario real pero deja la participación del trabajo constante en $1-a$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Progreso técnico neutral multiplicativo $A(t)=e^{gt}$ con $g>0$ y función Cobb-Douglas $a\in(0,1)$ | Si el cambio técnico no es multiplicativo o $a\notin(0,1)$, la ecuación diferencial no admite esa solución cerrada. | - |

---

### [C-08] Oferta Laboral Elástica y Ahorro Variable (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 24: Oferta Laboral Elástica y Ahorro Variable
- **Prerequisites:** C-06
- **Recommended Modalities:** adversarial_break, multiple_select, proof_dag
- **Evidence Citations:** `solow1956.pdf` (page 24)

#### Description & Cognitive Model
Extensión de $\dot{r}$ a oferta laboral elástica $L=L_0e^{nt}(w/p)^h$ o $G(t,w/p)$ y a tasa de ahorro decreciente $s(r)$ dependiente del rendimiento del capital

#### Fused Distractor Models (4)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Cambia r* en (14) Cobb-Douglas | conceptual_swap | high | Con $L=L_0e^{nt}(w/p)^h$, el equilibrio $r^*$ cambia con $h$ | Observe $\dot{r}=(sF(r,1)-nr)(1+ah/r)^{-1}$: el factor $(1+ah/r)^{-1}$ modifica la velocidad de ajuste pero no el cero $sF(r^*,1)=nr^*$. |
| `D-C08-02` | Generaliza invarianza a todo G | conceptual_swap | high | Para cualquier $L=G(t,w/p)$, $r^*$ permanece inalterado | Verifique en (6b) que $sF(r,1)=\frac{r}{G}\frac{\partial G}{\partial t}$; salvo que $\frac{1}{G}\frac{\partial G}{\partial t}=n$, $r^*$ sí se ve afectado. |
| `D-C08-03` | Ahorro creciente con r | conceptual_swap | high | $s(r)$ es una función creciente de $r=K/L$ | Recuerde que un mayor rendimiento del capital $q/p$ estimula el ahorro; como $q/p$ cae al subir $r$, $s(r)$ es decreciente en $r$. |
| `D-C08-04` | Permite crecimiento ilimitado con s(r)=0 | conceptual_swap | high | Aunque $s(r)=0$ para $r$ grande, $r\to\infty$ sigue siendo posible | Note que si $s(r)$ se anula para $r$ suficientemente grande, $s(r)F(r,1)-nr<0$ y el último corte con $nr$ es necesariamente estable. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C08-01` | - | La tasa de ahorro responde positivamente a la renta real del capital $q/p$, implicando $s'(r)<0$ | Si el ahorro respondiera negativamente al rendimiento del capital, $s(r)$ sería creciente y podría desestabilizar $r^*$. | - |

---

### [Hab-08] Incidencia Fiscal en el Ahorro (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 26: Incidencia Fiscal en el Ahorro
- **Prerequisites:** C-08
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 26)

#### Description & Cognitive Model
Derivación de la tasa de ahorro efectiva $s_{\text{ef}}=s+(v-s)t$ bajo impuesto proporcional sobre la renta $t$ con fracción $v$ invertida por el Estado

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | Omite ahorro privado reducido | skipped_step | high | $s_{\text{ef}}=s+vt$ | Calcule $\dot{K}=s(1-t)Y+vtY$ factorizando $Y$: el término $-st$ refleja la reducción del ahorro privado debida al impuesto. |
| `D-Hab08-02` | Ahorro siempre sube con impuesto | skipped_step | high | Todo impuesto $t>0$ con $v>0$ eleva la tasa de ahorro | Compare $v$ con $s$ en $s+(v-s)t$: la tasa efectiva solo aumenta si el Estado invierte una fracción mayor que el sector privado ($v>s$). |
| `D-Hab08-03` | Confunde v=0 con v=1 | conceptual_swap | high | Si el impuesto se consume ($v=0$), $s_{\text{ef}}=s+t(1-s)$ | Evalúe $s+(v-s)t$ en $v=0$ para obtener $s(1-t)$ cuando el ingreso fiscal se consume, y en $v=1$ para obtener $s+t(1-s)$. |
| `D-Hab08-04` | Invierte signo de (v-s) | conceptual_swap | high | $s_{\text{ef}}=s+(s-v)t$ | Desarrolle $s(1-t)+vt=s-st+vt=s+(v-s)t$ verificando que el coeficiente de $v$ sea positivo. |
| `D-Hab08-05` | Multiplica v por (1-t) | conceptual_swap | high | $s_{\text{ef}}=s(1-t)+v(1-t)$ | Recuerde que el Estado recauda $tY$ e invierte una fracción $v$ de esa recaudación, aportando $vtY$ a la formación de capital. |
| `D-Hab08-06` | Desplaza solo la recta nr | conceptual_swap | high | El impuesto desplaza la recta $nr$ sin alterar $sF(r,1)$ | Represente el cambio de $s$ a $s+(v-s)t$ como una expansión o contracción uniforme de la curva $sF(r,1)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab08-01` | - | Impuesto proporcional sobre la renta a tasa $t\in(0,1)$ sin distorsión directa sobre el crecimiento poblacional $n$ | Con impuestos no proporcionales la curva $sF(r,1)$ sufre giros no uniformes y $s_{\text{ef}}$ deja de ser constante. | - |

---

### [C-09] Población Endógena y Trampa de Pobreza (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 28: Población Endógena y Trampa de Pobreza
- **Prerequisites:** C-08
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 28)

#### Description & Cognitive Model
Análisis de equilibrios múltiples en $\dot{r}=sF(r,1)-n(r)r$ cuando el crecimiento poblacional $n(r)$ responde endógenamente al ingreso per cápita

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Invierte estabilidad de r1 y r2 | conceptual_swap | high | $r_1$ es inestable y $r_2$ es estable | Verifique el signo de $\dot{r}=sF(r,1)-n(r)r$: entre $r_1$ y $r_2$ la curva $n(r)r$ supera a $sF(r,1)$ ($\dot{r}<0$), atrayendo hacia $r_1$ y repeliendo desde $r_2$. |
| `D-C09-02` | Requiere rendimientos crecientes | conceptual_swap | high | La trampa de estancamiento exige rendimientos crecientes a escala | Note que Solow muestra la aparición de una trampa de estancamiento bajo rendimientos constantes a escala puramente por la no linealidad de $n(r)$. |
| `D-C09-03` | Retorno desde encima de r2 | conceptual_swap | high | Si $r_0>r_2$, la economía converge de regreso a $r_1$ | Observe que para $r_0>r_2$ se cumple $sF(r,1)>n(r)r$ ($\dot{r}>0$), por lo que un impulso inicial sobre $r_2$ desata expansión autosostenida. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | La tasa de crecimiento poblacional $n(r)$ es negativa a ingresos muy bajos, positiva en niveles medios y se estabiliza o declina a ingresos altos | Si $n(r)$ fuera constante o estrictamente monótona sin cruce múltiple, desaparecería el umbral inestable $r_2$. | - |

---

### [Hab-09] Rigideces Nominales y Desempleo (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 29: Rigideces Nominales y Desempleo
- **Prerequisites:** C-06, C-07
- **Recommended Modalities:** open_symbolic, adversarial_break, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 29)

#### Description & Cognitive Model
Cálculo del crecimiento del empleo $\frac{\dot{L}}{L}=\frac{s}{\bar{r}}F(\bar{r},1)$ con salario real rígido $\bar{w}/p$ y análisis de subutilización de capital bajo trampa de liquidez

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab09-01` | Invierte condición de desempleo | skipped_step | high | Surge desempleo si $\frac{s}{\bar{r}}F(\bar{r},1)>n$ | Compare la tasa de crecimiento del empleo $\frac{s}{\bar{r}}F(\bar{r},1)$ con $n$: si es menor que $n$ crece el desempleo; si es mayor aparece escasez de trabajo. |
| `D-Hab09-02` | Permite variar r con salario fijo | skipped_step | high | Con $\bar{w}/p$ fijo, $r$ se ajusta libremente para mantener pleno empleo | Recuerde que bajo CRS el producto marginal del trabajo depende solo de $r$, por lo que fijar $\bar{w}/p$ fija ineludiblemente $r=\bar{r}$. |
| `D-Hab09-03` | Omite dividir por r barra | conceptual_swap | high | $\frac{\dot{L}}{L}=sF(\bar{r},1)$ | Parta de $\dot{K}=\bar{r}\dot{L}=sF(\bar{r}L,L)=sLF(\bar{r},1)$ y divida ambos lados por $\bar{r}L$ para obtener $\frac{\dot{L}}{L}=\frac{s}{\bar{r}}F(\bar{r},1)$. |
| `D-Hab09-04` | Trampa de liquidez por debajo de r* | conceptual_swap | high | La trampa de liquidez subutiliza capital si la tasa rígida está por debajo de su equilibrio | Verifique que la subutilización de capital ocurre cuando la tasa de interés queda rígida por encima del nivel correspondiente al equilibrio. |
| `D-Hab09-05` | Confunde K en uso con K disponible | conceptual_swap | high | En (15), $K$ representa todo el stock físico acumulado | Distinga que en $\bar{M}=Q(F(K,L),F_K(K,L))$ la variable $K$ denota el capital efectivamente empleado, que puede diferir del stock disponible. |
| `D-Hab09-06` | Modelo real basta con liquidez | conceptual_swap | high | El modelo real neoclásico describe completamente la trampa de liquidez | Reconozca que al introducir preferencia por la liquidez el precio $p$ y los factores monetarios cobran apalancamiento directo y exigen dinámica monetaria. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab09-01` | - | Salario real rígido en $\bar{w}/p$ o tasa de interés rígida por demanda infinitamente elástica de saldos ociosos | Si los precios y salarios fueran flexibles, $\bar{r}$ se ajustaría y se restauraría el pleno empleo y uso del capital. | - |

---
