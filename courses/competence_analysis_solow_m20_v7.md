# Cognitive Task Analysis (CTA): Solow M20 V7

- **Course ID:** `solow_m20_v7`
- **Macro-Competency:** Dominio y aplicación analítica integral de Solow M20 V7
- **Structure:** 20 total competencies (2 Facts, 11 Concepts, 7 Skills) with 86 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `PRE-02` | Rendimientos Constantes a Escala | Fact | Understand | Unidad 4: Rendimientos Constantes a Escala | - | 3 |
| `PRE-01` | Forma Intensiva y Dinámica | Fact | Understand | Unidad 2: Forma Intensiva y Dinámica | PRE-02 | 3 |
| `Hab-01` | Ecuación Fundamental de Solow | Skill | Evaluate | Unidad 2: Ecuación Fundamental de Solow | PRE-01 | 6 |
| `C-01` | Línea de Fase y Estabilidad | Concept | Evaluate | Unidad 3: Línea de Fase y Estabilidad | Hab-01 | 4 |
| `C-02` | Progreso Tecnológico Secular | Concept | Analyze | Unidad 4: Progreso Tecnológico Secular | C-01 | 3 |
| `C-03` | Pleno Empleo y Acumulación de Capital | Concept | Analyze | Unidad 5: Pleno Empleo y Acumulación de Capital | PRE-02 | 3 |
| `Hab-03` | Derivación de la Ecuación Fundamental | Skill | Evaluate | Unidad 6: Derivación de la Ecuación Fundamental | C-03 | 6 |
| `C-04` | Estabilidad y Multiplicidad del Equilibrio | Concept | Evaluate | Unidad 8: Estabilidad y Multiplicidad del Equilibrio | Hab-03 | 3 |
| `Hab-02` | Solución Analítica y Equilibrio Cobb-Douglas | Skill | Evaluate | Unidad 5: Solución Cuantitativa Cobb-Douglas | Hab-01, C-01, Hab-03, C-04 | 10 |
| `C-05` | Proporciones Fijas y Redundancia de Factores | Concept | Evaluate | Unidad 11: Proporciones Fijas y Redundancia de Factores | Hab-03 | 3 |
| `Hab-05` | Dinámica con Función CES Particular (p = 1/2) | Skill | Evaluate | Unidad 14: Dinámica con Función CES Particular (p = 1/2) | Hab-03, C-04 | 6 |
| `C-06` | Precios Competitivos y Productividad Marginal | Concept | Analyze | Unidad 16: Precios Competitivos y Productividad Marginal | C-03, PRE-02 | 3 |
| `C-07` | Arbitraje entre Renta Real y Tasa de Interés | Concept | Evaluate | Unidad 17: Arbitraje entre Renta Real y Tasa de Interés | C-06 | 3 |
| `Hab-06` | Cálculo de Precios Factoriales y Participación Laboral | Skill | Evaluate | Unidad 21: Cálculo de Precios Factoriales y Participación Laboral | C-07 | 6 |
| `Hab-07` | Dinámica con Cambio Tecnológico Neutral | Skill | Evaluate | Unidad 22: Dinámica con Cambio Tecnológico Neutral | Hab-06 | 6 |
| `C-08` | Oferta de Trabajo Elástica al Salario Real | Concept | Analyze | Unidad 24: Oferta de Trabajo Elástica al Salario Real | C-07 | 3 |
| `C-09` | Tasa de Ahorro Variable y Estabilidad | Concept | Evaluate | Unidad 25: Tasa de Ahorro Variable y Estabilidad | C-07 | 3 |
| `Hab-08` | Tasa de Ahorro Efectiva bajo Impuesto a la Renta | Skill | Evaluate | Unidad 26: Tasa de Ahorro Efectiva bajo Impuesto a la Renta | C-09 | 6 |
| `C-10` | Crecimiento Poblacional Endógeno y Trampas de Equilibrio | Concept | Evaluate | Unidad 28: Crecimiento Poblacional Endógeno y Trampas de Equilibrio | C-09 | 3 |
| `C-11` | Rigidez Salarial y Preferencia por la Liquidez | Concept | Evaluate | Unidad 29: Rigidez Salarial y Preferencia por la Liquidez | C-07 | 3 |

---

## Detailed Competency Specifications

### [PRE-02] Rendimientos Constantes a Escala (Fact)

- **Bloom Level:** Understand
- **Session:** Unidad 4: Rendimientos Constantes a Escala
- **Prerequisites:** None
- **Recommended Modalities:** fill_in_the_blank, multiple_select, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 4)

#### Description & Cognitive Model
Función de producción agregada $Y = F(K, L)$ homogénea de primer grado, $F(\lambda K, \lambda L) = \lambda Y$, en ausencia de recursos no aumentables como la tierra.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-PRE02-01` | Rendimientos decrecientes globales | conceptual_swap | high | $F(\lambda K, \lambda L) < \lambda F(K, L)$ | Distinga los rendimientos marginales decrecientes de un factor respecto a los rendimientos constantes a escala al variar ambos insumos. |
| `D-PRE02-02` | Homogeneidad de grado cero | conceptual_swap | high | $F(\lambda K, \lambda L) = F(K, L)$ | Recuerde que la homogeneidad de grado uno implica que duplicar capital y trabajo duplica exactamente el producto total. |
| `D-PRE02-03` | Incluye tierra fija | conceptual_swap | high | $Y = F(K, L, T_0)$ con $T_0$ fijo | En el modelo de Solow se abstrae la tierra escasa para mantener rendimientos constantes a escala en capital y trabajo. |

---

### [PRE-01] Forma Intensiva y Dinámica (Fact)

- **Bloom Level:** Understand
- **Session:** Unidad 2: Forma Intensiva y Dinámica
- **Prerequisites:** PRE-02
- **Recommended Modalities:** fill_in_the_blank, multiple_select, concept_matching
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
Función de producción linealmente homogénea $Q=f(K,L)=L\phi(k)$ con $k\equiv K/L$, $\phi'(k)>0$, $\phi''(k)<0$, ahorro $\dot{K}=sQ$ y crecimiento laboral $\dot{L}/L=\lambda>0$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-PRE01-01` | Proporción fija | conceptual_swap | high | $Q=\rho K$ | Recuerde que Solow permite proporciones variables entre capital y mano de obra mediante $Q=f(K,L)$, a diferencia del modelo de Domar. |
| `D-PRE01-02` | Retornos crecientes | conceptual_swap | high | $\phi''(k)>0$ | Verifique que $f_{KK}<0$ implica directamente $\phi''(k)<0$, es decir, el producto crece con $k$ a una tasa decreciente. |
| `D-PRE01-03` | Ahorro sobre capital | conceptual_swap | high | $\dot{K}=sK$ | Aplique la propensión marginal al ahorro $s$ sobre el flujo de producto $Q$, nunca sobre el stock de capital $K$. |

---

### [Hab-01] Ecuación Fundamental de Solow (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 2: Ecuación Fundamental de Solow
- **Prerequisites:** PRE-01
- **Recommended Modalities:** open_symbolic, proof_dag, adversarial_break
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
Derivación de la ecuación diferencial fundamental $\dot{k}=s\phi(k)-\lambda k$ diferenciando $K=kL$ mediante regla del producto e igualando con $\dot{K}=sL\phi(k)$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Omite regla del producto | skipped_step | high | $\dot{K}=L\dot{k}$ | Aplique la regla del producto completa al diferenciar $K=kL$ respecto al tiempo: $\dot{K}=L\dot{k}+k\dot{L}$, incluyendo el término $k\dot{L}$. |
| `D-Hab01-02` | Signo positivo en dilución | skipped_step | high | $\dot{k}=s\phi(k)+\lambda k$ | Al despejar $L\dot{k}=sL\phi(k)-k\lambda L$, el crecimiento laboral $\lambda k$ resta al ahorro por trabajador porque diluye el capital. |
| `D-Hab01-03` | Conserva factor L | conceptual_swap | high | $\dot{k}=sL\phi(k)-\lambda k$ | Divida ambos miembros de $L\dot{k}+k\lambda L=sL\phi(k)$ por el factor común $L>0$ para obtener una ecuación en $k$ solamente. |
| `D-Hab01-04` | Sustituye lambda por s | conceptual_swap | high | $\dot{k}=s\phi(k)-sk$ | Distinga la propensión al ahorro $s$ (que multiplica a $\phi(k)$) de la tasa de crecimiento laboral $\lambda$ (que multiplica a $k$). |
| `D-Hab01-05` | Omite phi(k) | conceptual_swap | high | $\dot{k}=sk-\lambda k$ | Mantenga la función intensiva $\phi(k)$ proveniente de $Q=L\phi(k)$, ya que el producto por trabajador no es lineal en $k$. |
| `D-Hab01-06` | Tasa relativa errónea | conceptual_swap | high | $\dot{k}/k=s\phi(k)-\lambda$ | Si divide $\dot{k}=s\phi(k)-\lambda k$ entre $k$, debe dividir también el término de ahorro por $k$: $\dot{k}/k=s\phi(k)/k-\lambda$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Fuerza laboral positiva $L>0$ en todo instante | Sin $L>0$ no es válido cancelar el factor común $L$ en la ecuación. | - |
| `A-Hab01-02` | - | Proporciones variables y homogeneidad lineal de $f(K,L)$ | Sin ellas $Q/L$ no se reduce a una función $\phi(k)$ de una sola variable. | - |

---

### [C-01] Línea de Fase y Estabilidad (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Línea de Fase y Estabilidad
- **Prerequisites:** Hab-01
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
Análisis cualitativo-gráfico de $\dot{k}=s\phi(k)-\lambda k$: equilibrio intertemporal $\bar{k}>0$ donde $s\phi(\bar{k})=\lambda\bar{k}$, estabilidad con pendiente negativa y estado uniforme a tasa $\lambda$.

#### Fused Distractor Models (4)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Equilibrio inestable | conceptual_swap | high | Pendiente positiva en $\bar{k}$ indica estabilidad | En la línea de fase $\dot{k}$ contra $k$, la convergencia hacia $\bar{k}$ exige pendiente negativa: $\dot{k}>0$ si $k<\bar{k}$ y $\dot{k}<0$ si $k>\bar{k}$. |
| `D-C01-02` | Confunde estado uniforme | conceptual_swap | high | En estado uniforme $K, L, Q$ crecen a tasa cero | Distinga el estado estacionario (tasa cero) del estado uniforme, donde $k=\bar{k}$ es constante pero $K$, $L$, $\dot{K}$ y $Q$ crecen todos a tasa $\lambda$. |
| `D-C01-03` | Intersección en el origen | conceptual_swap | high | $s\phi(k)$ inicia con ordenada positiva en $k=0$ | Dado que el capital $K$ es un factor indispensable, si $K=0$ entonces $k=0$ y $Q=0$, por lo que la curva $s\phi(k)$ parte del origen. |
| `D-C01-04` | Filo de navaja de Domar | conceptual_swap | high | Solo un $k(0)=\bar{k}$ inicial evita divergencia | El aporte central de Solow es mostrar que cualquier $k(0)>0$ converge automáticamente a $\bar{k}$ sin requerir el delicado balance de Domar. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | El capital $K$ es indispensable: $\phi(0)=0$ | Si $\phi(0)>0$, la curva $s\phi(k)$ no partiría del origen. | - |
| `A-C01-02` | - | Existe un intervalo donde $s\phi(k)>\lambda k$ | Sin él no habría intersección positiva $\bar{k}>0$ ni crecimiento positivo inicial. | - |

---

### [C-02] Progreso Tecnológico Secular (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 4: Progreso Tecnológico Secular
- **Prerequisites:** C-01
- **Recommended Modalities:** adversarial_break, multiple_select, invariant_canvas
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
Modificación de la función de producción $Q=T(t)f(K,L)$ con $dT/dt>0$: desplaza hacia arriba $s\phi(k)$, elevando sucesivamente $\bar{k}$ y la productividad por trabajador.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Desplazamiento del rayo | conceptual_swap | high | $dT/dt>0$ aumenta la pendiente del rayo $\lambda k$ | El término tecnológico $T(t)$ multiplica al producto $f(K,L)$, por lo que desplaza hacia arriba la curva $s\phi(k)$ sin alterar el rayo $\lambda k$. |
| `D-C02-02` | Caída del capital | conceptual_swap | high | Mayor $T(t)$ reduce el nivel de equilibrio $\bar{k}$ | Un desplazamiento secular hacia arriba de $s\phi(k)$ genera intersecciones sucesivamente más altas con $\lambda k$, aumentando $\bar{k}$ y la productividad. |
| `D-C02-03` | Efecto aditivo nulo | conceptual_swap | high | $T(t)$ solo acelera $L$ sin cambiar $k$ de equilibrio | Al incrementar el producto obtenido con los mismos $K$ y $L$, el ahorro $s\phi(k)$ sube y permite sostener mayor capital por trabajador en estados uniformes. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | Tecnología creciente en el tiempo $dT/dt>0$ | Si $dT/dt=0$, la función es invariante y $\bar{k}$ permanece fijo. | - |

---

### [C-03] Pleno Empleo y Acumulación de Capital (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 5: Pleno Empleo y Acumulación de Capital
- **Prerequisites:** PRE-02
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 5)

#### Description & Cognitive Model
Ecuación de acumulación $\dot{K} = sF(K, L_0 e^{nt})$ bajo ahorro proporcional constante $s$, crecimiento laboral exógeno $L(t) = L_0 e^{nt}$ y pleno empleo continuo.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Ahorro sobre capital | conceptual_swap | high | $\dot{K} = sK$ | Aplique la propensión a ahorrar $s$ sobre el flujo de ingreso neto $Y = F(K, L)$, nunca sobre el stock acumulado $K$. |
| `D-C03-02` | Trabajo fijo | conceptual_swap | high | $\dot{K} = sF(K, L_0)$ | Sustituya la oferta inelástica creciente $L(t) = L_0 e^{nt}$ en la función de producción para captar el crecimiento demográfico. |
| `D-C03-03` | Desempleo estructural | conceptual_swap | high | $L_{\text{emp}} < L_0 e^{nt}$ por rigidez salarial | En el modelo base el salario real se ajusta instantáneamente para garantizar pleno empleo perpetuo del trabajo y del capital. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | La tasa de ahorro $s \in (0, 1)$ es constante y todo ahorro se invierte sin fricciones. | Si ahorro e inversión difieren o $s$ varía, $\dot{K} = sY$ deja de cumplirse. | - |
| `A-C03-02` | - | La fuerza de trabajo crece exógenamente a tasa $n$ y se ofrece de forma inelástica. | Con oferta laboral elástica al salario real se requiere una ecuación adicional de oferta. | - |

---

### [Hab-03] Derivación de la Ecuación Fundamental (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 6: Derivación de la Ecuación Fundamental
- **Prerequisites:** C-03
- **Recommended Modalities:** proof_dag, open_symbolic, fill_in_the_blank
- **Evidence Citations:** `solow1956.pdf` (page 6)

#### Description & Cognitive Model
Reducción de $\dot{K} = sF(K, L_0 e^{nt})$ mediante la razón capital-trabajo $r = K/L$ y homogeneidad de grado uno para obtener $\dot{r} = sF(r, 1) - nr$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Omite dilución poblacional | skipped_step | high | $\dot{r} = sF(r, 1)$ | Al diferenciar $K = r L_0 e^{nt}$ respecto al tiempo, incluya la regla del producto que genera el término $nr$ al restar. |
| `D-Hab03-02` | Signo invertido en nr | skipped_step | high | $\dot{r} = sF(r, 1) + nr$ | Recuerde que $\dot{r}/r = \dot{K}/K - \dot{L}/L$; el crecimiento laboral $n$ diluye el capital por trabajador y debe restarse. |
| `D-Hab03-03` | Divide F por L sin r | conceptual_swap | high | $\dot{r} = sF(K, 1) - nr$ | Por homogeneidad de grado uno, al factorizar $L$ fuera de $F(K, L)$ ambos argumentos deben dividirse entre $L$, dando $F(r, 1)$. |
| `D-Hab03-04` | Omite factor r en tasa | conceptual_swap | high | $\dot{r} = \frac{sF(r, 1)}{r} - n$ | Multiplique toda la expresión de la tasa relativa $\dot{r}/r = sF(r,1)/r - n$ por $r$ para despejar correctamente $\dot{r}$. |
| `D-Hab03-05` | Conserva L en término n | conceptual_swap | high | $\dot{r} = sF(r, 1) - nr L_0 e^{nt}$ | Divida ambos miembros de $(\dot{r} + nr)L_0 e^{nt} = s L_0 e^{nt} F(r, 1)$ entre el factor común positivo $L_0 e^{nt}$. |
| `D-Hab03-06` | Resta n sin multiplicar por r | conceptual_swap | high | $\dot{r} = sF(r, 1) - n$ | Verifique la homogeneidad dimensional: $sF(r,1)$ es flujo por trabajador, por lo que debe restarse $nr$ y no solo $n$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | La función $F(K, L)$ es diferenciable y homogénea de grado uno en $(K, L)$. | Sin homogeneidad de grado uno no es posible reducir el sistema a la única variable $r$. | - |

---

### [C-04] Estabilidad y Multiplicidad del Equilibrio (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 8: Estabilidad y Multiplicidad del Equilibrio
- **Prerequisites:** Hab-03
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 8)

#### Description & Cognitive Model
Análisis gráfico de $\dot{r} = sF(r, 1) - nr$: equilibrio estable único $r^*$ (Figura I), equilibrios múltiples con umbral inestable $r_2$ (Figura II) y ausencia de equilibrio (Figura III).

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Todos los cruces estables | conceptual_swap | high | $r_1, r_2, r_3$ son todos estables | Un equilibrio es estable solo si $sF(r,1) > nr$ a su izquierda y $sF(r,1) < nr$ a su derecha; en $r_2$ ocurre lo inverso. |
| `D-C04-02` | Crecimiento explosivo como equilibrio | conceptual_swap | high | $sF(r,1) > nr$ implica convergencia a $r^*$ | Cuando $sF(r,1) > nr$ para todo $r > 0$, $\dot{r} > 0$ siempre y la razón capital-trabajo crece indefinidamente sin equilibrio. |
| `D-C04-03` | Origen siempre equilibrio | conceptual_swap | high | $r = 0$ es siempre equilibrio estable | En la Figura II la producción es posible sin capital ($sF(0,1) > 0$), por lo que $\dot{r} > 0$ en $r=0$ y el origen no es equilibrio. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | La función $F(r, 1)$ es continua y no decreciente en $r \ge 0$. | Discontinuidades o pendientes negativas alterarían la dirección de ajuste de $\dot{r}$. | - |

---

### [Hab-02] Solución Analítica y Equilibrio Cobb-Douglas (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Solución Cuantitativa Cobb-Douglas
- **Prerequisites:** Hab-01, C-01, Hab-03, C-04
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 5), `solow1956.pdf` (page 13)

#### Description & Cognitive Model
Resolución de la dinámica Cobb-Douglas mediante la ecuación de Bernoulli $\dot{k}+\lambda k=sk^\alpha$ ($z=k^{1-\alpha}$) e integración directa de $\dot{K}=sK^a(L_0 e^{nt})^{1-a}$ ($b=1-a$), obteniendo $k(t)$, $K(t)$, razón estacionaria $r^*=(s/n)^{1/b}$, ingreso per cápita $(s/n)^{a/b}$ y coeficiente de capital $C=s/n$.

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Sustitución incorrecta | skipped_step | high | Usa $z=k^\alpha$ para linealizar | En la ecuación de Bernoulli $\dot{k}+\lambda k=sk^\alpha$ con $m=\alpha$, la transformación linealizadora correcta es $z=k^{1-m}=k^{1-\alpha}$. |
| `D-Hab02-07` | Exponente sin invertir | skipped_step | high | $r^* = (s/n)^{1-a}$ | Al resolver $s r^a = nr$, se obtiene $r^{1-a} = s/n$, por lo que debe elevar ambos lados a la potencia $\frac{1}{1-a}$. |
| `D-Hab02-02` | Omite factor (1-alpha) | skipped_step | high | $\dot{z}+\lambda z=s$ | Al diferenciar $z=k^{1-\alpha}$, aparece el factor $(1-\alpha)$ por regla de la cadena, resultando $\dot{z}+(1-\alpha)\lambda z=(1-\alpha)s$. |
| `D-Hab02-08` | Invierte razón s/n | skipped_step | high | $r^* = (n/s)^{\frac{1}{1-a}}$ | Un mayor ahorro $s$ eleva el capital estacionario y un mayor $n$ lo diluye; por ello $r^* = (s/n)^{1/(1-a)}$. |
| `D-Hab02-03` | Exponente sin invertir | conceptual_swap | high | $k(\infty)=(s/\lambda)^{1-\alpha}$ | Como $k^{1-\alpha}\to s/\lambda$ cuando $t\to\infty$, al despejar $k$ debe elevar ambos lados al exponente recíproco $1/(1-\alpha)$. |
| `D-Hab02-09` | Ingreso per cápita erróneo | conceptual_swap | high | $(Y/L)^* = (s/n)^{1/b}$ | Como $Y/L = r^a$, sustituya $r^* = (s/n)^{1/b}$ en $r^a$ para obtener $(Y/L)^* = (s/n)^{a/b}$. |
| `D-Hab02-04` | Invierte razón s/lambda | conceptual_swap | high | $k(\infty)=(\lambda/s)^{1/(1-\alpha)}$ | El equilibrio varía directamente con el ahorro $s$ e inversamente con $\lambda$, por lo que la base de la potencia debe ser $s/\lambda$. |
| `D-Hab02-10` | Coeficiente capital invertido | conceptual_swap | high | $C = K/Y = n/s$ | En equilibrio $sY = nK$ (ahorro igual a dilución del capital), de modo que $C = K/Y = s/n$ y $n = s/C$. |
| `D-Hab02-05` | Signo positivo exponente | conceptual_swap | high | $e^{+(1-\alpha)\lambda t}$ en $z(t)$ | La ecuación lineal $\dot{z}+az=b$ con $a=(1-\alpha)\lambda>0$ tiene factor integrante $e^{at}$, dando solución homogénea decreciente $e^{-at}$. |
| `D-Hab02-11` | Omite condición inicial K0 | conceptual_swap | high | $K(t) = \left[\frac{s}{n}L_0^b e^{nbt}\right]^{1/b}$ | La solución exacta de $\dot{K} = sK^a L_0^b e^{nbt}$ debe satisfacer $K(0) = K_0$, conservando $K_0^b - \frac{s}{n}L_0^b$. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Elasticidad del capital $\alpha\in(0,1)$ y $\lambda>0$ | Si $\alpha\ge 1$ o $\lambda\le 0$, el término exponencial no converge a cero. | - |
| `A-Hab02-02` | - | Capital inicial positivo $k(0)>0$ | Si $k(0)=0$, el producto inicial es nulo y la trayectoria permanece en cero. | - |
| `A-Hab02-03` | - | La participación del capital cumple $a \in (0, 1)$ y el crecimiento laboral $n > 0$. | Si $a \ge 1$, la curva $s r^a$ no cruza desde arriba a $nr$ y desaparece el equilibrio estable. | - |

---

### [C-05] Proporciones Fijas y Redundancia de Factores (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 11: Proporciones Fijas y Redundancia de Factores
- **Prerequisites:** Hab-03
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 11)

#### Description & Cognitive Model
Caso Harrod-Domar $Y = \min(K/a, L/b)$ con $\dot{r} = s\min(r/a, 1/b) - nr$: comparación entre tasa natural $n$ y tasa garantizada $s/a$ que genera desempleo o exceso de capacidad.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Desempleo cuando n < s/a | conceptual_swap | high | $n < s/a$ genera redundancia de trabajo | Cuando $n < s/a$, el capital crece más rápido que el trabajo, $r$ converge a $s/(nb) > a/b$ y el factor redundante es el capital. |
| `D-C05-02` | Ajuste neoclásico en min | conceptual_swap | high | $r$ converge a $a/b$ para todo $n$ | Con proporciones fijas no hay sustitución de factores; si $n > s/a$, $r$ cae hacia cero y si $n < s/a$, converge a $s/(nb)$. |
| `D-C05-03` | Tasa garantizada errónea | conceptual_swap | high | La tasa garantizada es $s/b$ | El coeficiente de aceleración capital-producto es $a$, por lo que la pendiente inicial de $s\min(r/a, 1/b)$ es $s/a$, la tasa garantizada. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Los coeficientes técnicos $a > 0$ y $b > 0$ son estrictamente fijos (isocuantas en ángulo recto). | Si se permite sustitución en un rango $[r_{\min}, r_{\max}]$, reaparece una zona estable de tasas $n$. | - |

---

### [Hab-05] Dinámica con Función CES Particular (p = 1/2) (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 14: Dinámica con Función CES Particular (p = 1/2)
- **Prerequisites:** Hab-03, C-04
- **Recommended Modalities:** open_symbolic, unstructured_model, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 14)

#### Description & Cognitive Model
Análisis de $Y = (a\sqrt{K} + \sqrt{L})^2$ con $\dot{r} = s(a\sqrt{r}+1)^2 - nr$: umbral $sa^2 \lessgtr n$, equilibrio $r^* = (1/(\sqrt{n/s}-a))^2$ e ingreso límite $1/(1-a\sqrt{s/n})^2$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Invierte condición de equilibrio | skipped_step | high | Hay equilibrio estable si $sa^2 > n$ | Cuando $sa^2 > n$, el coeficiente cuadrático $(a^2 - n/s)$ es positivo y $s(a\sqrt{r}+1)^2 > nr$ siempre, impidiendo el equilibrio. |
| `D-Hab05-02` | Olvida elevar al cuadrado r* | skipped_step | high | $r^* = \frac{1}{\sqrt{n/s} - a}$ | De $s(a\sqrt{r^*}+1)^2 = nr^*$ se despeja $\sqrt{r^*} = \frac{1}{\sqrt{n/s}-a}$; eleve al cuadrado para hallar $r^*$. |
| `D-Hab05-03` | Signo erróneo en raíz | conceptual_swap | high | $r^* = \left(\frac{1}{\sqrt{n/s} + a}\right)^2$ | Como $\sqrt{r^*} > 0$, la única raíz admisible proviene de $A\sqrt{r^*} + 1 = 0$ con $A = a - \sqrt{n/s} < 0$. |
| `D-Hab05-04` | Supone equilibrio en origen | conceptual_swap | high | $r = 0$ es equilibrio cuando $sa^2 < n$ | En esta función es posible producir solo con trabajo: en $r=0$ la curva $sF(r,1)$ parte de altura positiva $s > 0$. |
| `D-Hab05-05` | Ingreso límite sin cuadrado | conceptual_swap | high | $(Y/L)^* = \frac{1}{1 - a\sqrt{s/n}}$ | Dado $Y/L = (a\sqrt{r}+1)^2$, al sustituir $\sqrt{r^*}$ se obtiene $\left(\frac{\sqrt{n/s}}{\sqrt{n/s}-a}\right)^2 = \frac{1}{(1-a\sqrt{s/n})^2}$. |
| `D-Hab05-06` | Aplica condición sin s | conceptual_swap | high | El umbral de equilibrio es $a^2 < n$ | El término dominante de $\dot{r}$ para $r$ grande es $(sa^2 - n)r$, por lo que la condición crítica involucra el producto $sa^2$ frente a $n$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | El parámetro de sustitución cumple $0 < p < 1$ ($p = 1/2$) con $a > 0$ y $s, n > 0$. | Si $p \ge 1$, las isocuantas pierden convexidad estricta y falla el pleno empleo competitivo. | - |

---

### [C-06] Precios Competitivos y Productividad Marginal (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 16: Precios Competitivos y Productividad Marginal
- **Prerequisites:** C-03, PRE-02
- **Recommended Modalities:** adversarial_break, multiple_select, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 16)

#### Description & Cognitive Model
Determinación de salario real $w/p = \partial F/\partial L$ y renta real del capital $q/p = \partial F/\partial K$ en competencia perfecta, con nivel de precios $p(t)$ indeterminado y productividades dependientes solo de $r$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Precios dependen de escala | conceptual_swap | high | $w/p$ y $q/p$ dependen de $K$ y $L$ por separado | Por homogeneidad de grado uno de $F(K, L)$, sus derivadas parciales son homogéneas de grado cero y dependen exclusivamente de $r = K/L$. |
| `D-C06-02` | Nivel absoluto determinado | conceptual_swap | high | El modelo real determina $p(t)$ unívocamente | El sistema real carece de ecuación monetaria; solo determina las razones reales $w/p$ y $q/p$, tomando $p(t)$ como dado. |
| `D-C06-03` | Iguala productividad a precio nominal | conceptual_swap | high | $\frac{\partial F}{\partial L} = w$ sin dividir por $p$ | Las unidades de $\partial F/\partial L$ son producto por unidad de trabajo, por lo que deben igualarse al salario real $w/p$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Los mercados de factores son competitivos y $w/p$, $q/p$ se ajustan instantáneamente. | Con competencia monopolística o rigideces de precios no rigen $\partial F/\partial L = w/p$ ni pleno empleo. | - |

---

### [C-07] Arbitraje entre Renta Real y Tasa de Interés (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 17: Arbitraje entre Renta Real y Tasa de Interés
- **Prerequisites:** C-06
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 17)

#### Description & Cognitive Model
Precios competitivos $\frac{\partial F}{\partial L}=\frac{w}{p}$, $\frac{\partial F}{\partial K}=\frac{q}{p}$ y condición de arbitraje $i(t)=\frac{q(t)}{p(t)}+\frac{\dot{p}(t)}{p(t)}$ que iguala mantener capital o fondos prestables.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Iguala i con q/p siempre | conceptual_swap | high | $i(t) = \frac{q(t)}{p(t)}$ sin variación de precios | Incluya la ganancia o pérdida de capital $\dot{p}(t)/p(t)$ al comparar la tasa monetaria $i(t)$ con la renta propia real $q(t)/p(t)$. |
| `D-C07-02` | Signo inverso de deflación | conceptual_swap | high | $i(t) = \frac{q(t)}{p(t)} - \frac{\dot{p}(t)}{p(t)}$ | Verifique que si el precio cae ($\dot{p}<0$), la renta propia $q/p$ debe superar a $i$ para compensar la pérdida de valor del bien. |
| `D-C07-03` | Confunde renta nominal con real | conceptual_swap | high | $i(t) = q(t) + \frac{\dot{p}(t)}{p(t)}$ | Divida el alquiler monetario $q(t)$ entre el precio del producto $p(t)$ para expresar el rendimiento en unidades del bien compuesto. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Arbitraje perfecto sin riesgo ni preferencias de liquidez entre capital y bonos | Con incertidumbre o riesgo, $i(t)$ y $q(t)/p(t)+\dot{p}(t)/p(t)$ pueden divergir. | - |
| `A-C07-02` | - | Previsión perfecta sobre alquileres futuros $q(u)$ y tasas $i(z)$ | Sin previsión perfecta, $p(t)$ no iguala el valor presente descontado de rentas. | - |

---

### [Hab-06] Cálculo de Precios Factoriales y Participación Laboral (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 21: Cálculo de Precios Factoriales y Participación Laboral
- **Prerequisites:** C-07
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 21)

#### Description & Cognitive Model
Cálculo de la razón factorial $w/q$, salarios reales $w/p$, renta real $q/p$ y participación laboral $(w/p)(L/Y)$ en los casos Harrod-Domar, Cobb-Douglas y $Y=(a\sqrt{K}+\sqrt{L})^2$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Invierte razón Cobb-Douglas | skipped_step | high | $\frac{w}{q} = \frac{a}{1-a}r$ | Divida $\partial F/\partial L = (1-a)r^a$ entre $\partial F/\partial K = ar^{a-1}$ para obtener correctamente la razón $(1-a)r/a$. |
| `D-Hab06-02` | Participación constante en raíz | skipped_step | high | $\frac{w}{p}\frac{L}{Y} = 1-a$ para $Y=(a\sqrt{K}+\sqrt{L})^2$ | Evalúe $(w/p)(L/Y)=1-a\sqrt{s/n}$ en equilibrio: a diferencia de Cobb-Douglas, aquí la participación depende de $s$ y $n$. |
| `D-Hab06-03` | Precio factorial en Harrod exceso capital | conceptual_swap | high | $q = p/a$ cuando $r > a/b$ | Recuerde que si $r>a/b$ el capital es redundante ($q=0$) y todo el valor del producto se imputa al trabajo ($w=p/b$). |
| `D-Hab06-04` | Determinación única en r=a/b | conceptual_swap | high | $w = p/b$ y $q = p/a$ simultáneamente en $r=a/b$ | En el equilibrio exacto $r=a/b$ de Harrod-Domar los precios factoriales son indeterminados sujetos solo a $aq/p + bw/p = 1$. |
| `D-Hab06-05` | Exponente erróneo en salario Cobb-Douglas | conceptual_swap | high | $\frac{w}{p} = (1-a)(s/n)^{\frac{1}{1-a}}$ | Sustituya $r^*=(s/n)^{1/(1-a)}$ dentro de $w/p=(1-a)r^a$ para obtener el exponente correcto $a/(1-a)$ del salario real. |
| `D-Hab06-06` | Renta real invertida en Cobb-Douglas | conceptual_swap | high | $\frac{q}{p} = \frac{as}{n}$ | Sustituya $r^*=(s/n)^{1/(1-a)}$ en $q/p=ar^{a-1}=ar^{-(1-a)}$ para verificar que el alquiler real de equilibrio es $an/s$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Rendimientos constantes a escala y competencia perfecta en mercados de factores | Sin rendimientos constantes, las productividades marginales no dependen solo de $r$. | - |

---

### [Hab-07] Dinámica con Cambio Tecnológico Neutral (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 22: Dinámica con Cambio Tecnológico Neutral
- **Prerequisites:** Hab-06
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 22)

#### Description & Cognitive Model
Solución y análisis asintótico de $Y=e^{gt}K^a(L_0 e^{nt})^{1-a}$ con $b=1-a$: tasas de crecimiento de largo plazo $n+g/b$ para $K$, $n+ag/b$ para $Y$, $g/b$ para $K/L$ y $g$ para $K/Y$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Tasa de K igual a n+g | skipped_step | high | $\dot{K}/K \to n + g$ | Observe el exponente $(nb+g)t$ dividido entre $b$ en la solución de $K(t)$: la tasa asintótica del capital es $n + g/b$, mayor que $n+g$. |
| `D-Hab07-02` | Tasa de Y igual a n+g | skipped_step | high | $\dot{Y}/Y \to n + g$ | Combine el crecimiento directo $g$ con el efecto acumulado en $K$ ponderado por $a$: la tasa de $Y$ converge a $n + ag/b$. |
| `D-Hab07-03` | Razón K/L estacionaria | conceptual_swap | high | $K/L$ converge a un equilibrio constante $r^*$ | Con progreso técnico neutral $e^{gt}$ la función $sF(r,1)$ sube continuamente y $K/L$ crece sin límite a tasa asintótica $g/b$. |
| `D-Hab07-04` | Razón K/Y constante | conceptual_swap | high | $\frac{d(K/Y)/dt}{K/Y} \to 0$ | Reste la tasa de $Y$ ($n+ag/b$) a la de $K$ ($n+g/b$): como $b=1-a$, el coeficiente $K/Y$ crece asintóticamente a tasa $g$. |
| `D-Hab07-05` | Salario real acotado | conceptual_swap | high | $\frac{w}{p}$ converge a un límite finito | Como $K/L$ crece sin cota a tasa $g/b$, la productividad marginal del trabajo y el salario real $w/p$ crecen indefinidamente. |
| `D-Hab07-06` | Participación laboral creciente | conceptual_swap | high | $\frac{w}{p}\frac{L}{Y}$ crece con $t$ | En la función Cobb-Douglas con cambio neutral $A(t)K^aL^{1-a}$, la participación relativa del trabajo permanece constante en $1-a$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Cambio tecnológico neutral multiplicativo $A(t)=e^{gt}$ con $g>0$ y $a\in(0,1)$ | Si $A(t)$ no es multiplicativo o $a\ge 1$, no aplica la solución cerrada. | - |

---

### [C-08] Oferta de Trabajo Elástica al Salario Real (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 24: Oferta de Trabajo Elástica al Salario Real
- **Prerequisites:** C-07
- **Recommended Modalities:** adversarial_break, multiple_select, proof_dag
- **Evidence Citations:** `solow1956.pdf` (page 24)

#### Description & Cognitive Model
Comparación entre oferta laboral de elasticidad constante $L=L_0 e^{nt}(w/p)^h$ (ec. 6a, con $r^*$ inalterado) y la forma general $L=G(t,w/p)$ (ec. 6b, donde $sF(r,1)=\frac{r}{G}\frac{\partial G}{\partial t}$).

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Elasticidad h cambia r* | conceptual_swap | high | En (6a), $h > 0$ modifica el valor de equilibrio $r^*$ | Note que $\dot{r}=0$ ocurre exactamente cuando $sF(r,1)-nr=0$, pues $(1+ah/r)^{-1}>0$ solo reescala la velocidad de ajuste, no $r^*$. |
| `D-C08-02` | Cualquier G(t,w/p) preserva r* | conceptual_swap | high | Para todo $L=G(t,w/p)$, $r^*$ coincide con el caso inelástico | En la forma general (6b), $r^*$ queda determinado por $sF(r,1)=\frac{r}{G}\frac{\partial G}{\partial t}$, por lo que cambia salvo si $\frac{1}{G}\frac{\partial G}{\partial t}=n$. |
| `D-C08-03` | Tasa de crecimiento distinta de n | conceptual_swap | high | En (6a), $K$ y $Y$ crecen más rápido que $n$ | Dado que $r$ converge a $r^*$, el salario real $w/p$ se estabiliza y $K$, $L$ e $Y$ crecen en el largo plazo a la misma tasa $n$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C08-01` | - | Nivel de precios $p$ constante y función de producción Cobb-Douglas para (6a) | Si $p$ varía o $F$ no es Cobb-Douglas, $\dot{w}/w = a\dot{r}/r$ deja de cumplirse. | - |

---

### [C-09] Tasa de Ahorro Variable y Estabilidad (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 25: Tasa de Ahorro Variable y Estabilidad
- **Prerequisites:** C-07
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 25)

#### Description & Cognitive Model
Tasa de ahorro endógena $s(r)$ decreciente en $r$ dentro de $\dot{r}=s(r)F(r,1)-nr$ (ec. 6c): efecto estabilizador y eliminación de crecimiento ilimitado de $r$ cuando $s(r)\to 0$ para $r$ grande.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | s(r) creciente en r | conceptual_swap | high | $s(r)$ aumenta con $r$ al depender del rendimiento del capital | Como el alquiler real $q/p$ disminuye al subir $r$ y el ahorro responde positivamente a $q/p$, $s(r)$ es una función decreciente de $r$. |
| `D-C09-02` | Genera estado estacionario clásico | conceptual_swap | high | Si $s(r)=0$ para $r$ alto, la economía queda en estado estacionario | Aunque el ahorro se anule para $r$ muy alto, la fuerza laboral sigue creciendo a tasa $n>0$, reduciendo $r$ y reactivando el ahorro. |
| `D-C09-03` | Siempre r* es menor | conceptual_swap | high | El nuevo equilibrio $r^*$ con $s(r)$ es necesariamente menor | Compare ambas curvas en el cruce donde $s(r)=s$: a la izquierda $s(r)F(r,1)$ está por encima, por lo que $r^*$ puede ser mayor o menor. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | La tasa de ahorro responde positivamente al alquiler real $q/p$ (inversamente a $r$) | Si el ahorro respondiera negativamente al rendimiento, $s(r)$ podría ser creciente. | - |

---

### [Hab-08] Tasa de Ahorro Efectiva bajo Impuesto a la Renta (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 26: Tasa de Ahorro Efectiva bajo Impuesto a la Renta
- **Prerequisites:** C-09
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 26)

#### Description & Cognitive Model
Deducción y aplicación de $s_{\mathrm{eff}} = s + (v-s)t$ ante un impuesto proporcional al ingreso $t$ con fracción invertida $v$, evaluando el desplazamiento de $sF(r,1)$ y del equilibrio $r^*$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | Omite ahorro privado perdido | skipped_step | high | $s_{\mathrm{eff}} = s + vt$ | Considere que el impuesto reduce el ingreso disponible a $(1-t)Y$, por lo que el ahorro privado cae a $s(1-t)Y$ antes de sumar $vtY$. |
| `D-Hab08-02` | Invierte signo de (v-s) | skipped_step | high | $s_{\mathrm{eff}} = s + (s-v)t$ | Expanda $\dot{K}=s(1-t)Y+vtY$ factorizando $Y$: el coeficiente neto de $t$ es $v-s$, positivo solo si el Estado invierte más que el sector privado. |
| `D-Hab08-03` | Impuesto siempre reduce r* | conceptual_swap | high | Todo impuesto $t>0$ contrae $sF(r,1)$ y reduce $r^*$ | Compare $v$ con $s$: si la fracción pública invertida $v$ supera la propensión privada $s$, $s_{\mathrm{eff}}>s$ y $r^*$ aumenta. |
| `D-Hab08-04` | Caso consumo puro erróneo | conceptual_swap | high | Si $v=0$, entonces $s_{\mathrm{eff}} = s - t$ | Sustituya $v=0$ en $s+(v-s)t$ para obtener $s(1-t)$: el impuesto solo grava la fracción $s$ que se habría ahorrado. |
| `D-Hab08-05` | Caso inversión pura erróneo | conceptual_swap | high | Si $v=1$, entonces $s_{\mathrm{eff}} = s + t$ | Sustituya $v=1$ en $s+(v-s)t$ para obtener $s+t(1-s)$, pues la fracción $st$ ya era ahorrada por el sector privado. |
| `D-Hab08-06` | Giro no uniforme de curva | conceptual_swap | high | El impuesto proporcional tuerce $sF(r,1)$ de forma no uniforme | Un impuesto proporcional $t$ escala uniformemente la curva $sF(r,1)$ por el factor constante $s_{\mathrm{eff}}/s$; solo impuestos no proporcionales la tuercen. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab08-01` | - | Impuesto proporcional único $t\in(0,1)$ y fracción constante $v\in[0,1]$ invertida | Con impuestos progresivos o no proporcionales, la curva $sF(r,1)$ se tuerce. | - |

---

### [C-10] Crecimiento Poblacional Endógeno y Trampas de Equilibrio (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 28: Crecimiento Poblacional Endógeno y Trampas de Equilibrio
- **Prerequisites:** C-09
- **Recommended Modalities:** invariant_canvas, adversarial_break, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 28)

#### Description & Cognitive Model
Tasa de crecimiento poblacional endógena $n(r)$ en $\dot{r}=sF(r,1)-n(r)r$ (Figura IX): equilibrio estable bajo $r_1$ y umbral inestable $r_2$, donde un impulso sobre $r_2$ inicia expansión autosostenida sin rendimientos crecientes.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C10-01` | Invierte estabilidad de r1 y r2 | conceptual_swap | high | $r_1$ es inestable y $r_2$ es estable en la Figura IX | Verifique el signo de $\dot{r}=sF(r,1)-n(r)r$: debajo de $r_2$ resulta $\dot{r}<0$ regresando a $r_1$ (estable), y sobre $r_2$ resulta $\dot{r}>0$. |
| `D-C10-02` | Requiere rendimientos crecientes | conceptual_swap | high | La trampa de estancamiento exige indivisibilidades o rendimientos crecientes | Note que $F(K,L)$ mantiene rendimientos constantes a escala; la trampa surge exclusivamente de la forma no lineal de $n(r)r$ respecto a $sF(r,1)$. |
| `D-C10-03` | Confunde rayo nr con curva n(r)r | conceptual_swap | high | $n(r)r$ sigue siendo una recta desde el origen | Al depender $n$ del ingreso per cápita $F(r,1)$, la pendiente $n(r)$ varía con $r$ y tuerce el rayo $nr$ en una curva con múltiples cruces. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C10-01` | - | La tasa $\dot{L}/L=n(r)$ depende únicamente del ingreso per cápita $Y/L=F(r,1)$ | Si $n$ es exógeno y constante, desaparecen los equilibrios múltiples de la Figura IX. | - |

---

### [C-11] Rigidez Salarial y Preferencia por la Liquidez (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 29: Rigidez Salarial y Preferencia por la Liquidez
- **Prerequisites:** C-07
- **Recommended Modalities:** adversarial_break, multiple_select, proof_dag
- **Evidence Citations:** `solow1956.pdf` (page 29)

#### Description & Cognitive Model
Obstáculos al pleno empleo: salario real rígido $\bar{w}/p$ fija $\bar{r}$ con crecimiento del empleo $\frac{\dot{L}}{L}=\frac{s}{\bar{r}}F(\bar{r},1)$ (desempleo si $<n$), y preferencia por liquidez $\bar{M}=Q(Y,q/p)$ que genera subutilización de capital en la trampa de liquidez.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C11-01` | Desempleo cuando pendiente > n | conceptual_swap | high | Si $\frac{s}{\bar{r}}F(\bar{r},1) > n$, se desarrolla desempleo creciente | Compare la tasa de crecimiento del empleo $(s/\bar{r})F(\bar{r},1)$ con la de la fuerza laboral $n$: si la supera hay escasez; si es menor hay desempleo. |
| `D-C11-02` | Trampa de liquidez sin efecto real | conceptual_swap | high | La trampa de liquidez solo afecta precios sin alterar el uso del capital | Si la tasa de interés se vuelve rígida por encima del nivel de equilibrio, se produce subutilización de capital y urge una dinámica monetaria. |
| `D-C11-03` | Salario rígido permite variar r | conceptual_swap | high | Con $\bar{w}/p$ fijo, la razón capital-trabajo $r$ sigue ajustándose | Como la productividad marginal $\partial F/\partial L$ depende solo de $r$, fijar el salario real en $\bar{w}/p$ fija necesariamente $r=\bar{r}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C11-01` | - | Salario real fijo $\bar{w}/p$ o demanda de saldos ociosos infinitamente elástica | Con precios y salarios flexibles y sin preferencia por liquidez, se recupera el pleno empleo. | - |

---
