# Cognitive Task Analysis (CTA): Solow M20 V8

- **Course ID:** `solow_m20_v8`
- **Macro-Competency:** Dominio y aplicación analítica integral de Solow M20 V8
- **Structure:** 18 total competencies (1 Facts, 10 Concepts, 7 Skills) with 82 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `H-01` | Hipótesis y Forma Intensiva de Solow | Fact | Understand | Unidad 2: Hipótesis y Forma Intensiva de Solow | - | 3 |
| `C-03` | Acumulación Neoclásica y Pleno Empleo | Concept | Evaluate | Unidad 3: Acumulación Neoclásica y Pleno Empleo | H-01 | 3 |
| `Hab-01` | Derivación de la Ecuación Fundamental | Skill | Analyze | Unidad 2: Derivación de la Ecuación Fundamental | H-01, C-03 | 9 |
| `C-01` | Línea de Fase y Estabilidad del Equilibrio | Concept | Evaluate | Unidad 3: Línea de Fase y Estabilidad del Equilibrio | Hab-01 | 3 |
| `C-02` | Estado Uniforme y Progreso Tecnológico | Concept | Evaluate | Unidad 4: Estado Uniforme y Progreso Tecnológico | C-01 | 3 |
| `C-04` | Equilibrio Estacionario y Estabilidad | Concept | Evaluate | Unidad 7: Equilibrio Estacionario y Estabilidad | Hab-01 | 3 |
| `Hab-02` | Solución Explícita Cobb-Douglas | Skill | Evaluate | Unidad 5: Solución Cuantitativa Cobb-Douglas | Hab-01, C-01, C-04 | 10 |
| `Hab-04` | Modelo de Proporciones Fijas (Harrod-Domar) | Skill | Evaluate | Unidad 11: Modelo de Proporciones Fijas (Harrod-Domar) | Hab-01, C-04 | 6 |
| `Hab-06` | Equilibrio y Divergencia en Función CES (p=1/2) | Skill | Evaluate | Unidad 14: Equilibrio y Divergencia en Función CES (p=1/2) | Hab-01, C-04 | 6 |
| `C-05` | Productividades Marginales y Precios Reales | Concept | Analyze | Unidad 16: Productividades Marginales y Precios Reales | C-03, C-04 | 3 |
| `C-06` | Precios Competitivos y Arbitraje de Capital | Concept | Evaluate | Unidad 16: Precios Competitivos y Arbitraje de Capital | C-05 | 3 |
| `C-07` | Isocuantas, Trayectorias y Precios Relativos | Concept | Analyze | Unidad 19: Isocuantas, Trayectorias y Precios Relativos | C-06 | 3 |
| `Hab-07` | Cálculo de Precios y Participación Factorial | Skill | Evaluate | Unidad 21: Cálculo de Precios y Participación Factorial | C-06, C-07 | 6 |
| `Hab-08` | Dinámica con Cambio Tecnológico Neutral | Skill | Evaluate | Unidad 22: Dinámica con Cambio Tecnológico Neutral | C-06, Hab-07 | 6 |
| `C-08` | Oferta Elástica de Trabajo y Equilibrio | Concept | Evaluate | Unidad 23: Oferta Elástica de Trabajo y Equilibrio | C-06 | 3 |
| `Hab-09` | Tasa de Ahorro Variable e Impuesto al Ingreso | Skill | Analyze | Unidad 26: Tasa de Ahorro Variable e Impuesto al Ingreso | C-07 | 6 |
| `C-09` | Crecimiento Poblacional Endógeno y Trampas | Concept | Evaluate | Unidad 27: Crecimiento Poblacional Endógeno y Trampas | C-07 | 3 |
| `C-10` | Rigidez Salarial y Preferencia por la Liquidez | Concept | Evaluate | Unidad 29: Rigidez Salarial y Preferencia por la Liquidez | C-06, C-07 | 3 |

---

## Detailed Competency Specifications

### [H-01] Hipótesis y Forma Intensiva de Solow (Fact)

- **Bloom Level:** Understand
- **Session:** Unidad 2: Hipótesis y Forma Intensiva de Solow
- **Prerequisites:** None
- **Recommended Modalities:** fill_in_the_blank, multiple_select, concept_matching
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
Función de producción linealmente homogénea $Q=L\phi(k)$ con $k\equiv K/L$, $\phi'(k)>0$, $\phi''(k)<0$ e hipótesis dinámicas $\dot{K}=sQ$ y $\dot{L}/L=\lambda$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Proporción fija Domar | conceptual_swap | high | $Q=\rho K$ | Distinga el modelo de Solow con proporciones variables $Q=f(K,L)$ del supuesto de proporción fija de Domar. |
| `D-H01-02` | Rendimientos crecientes | conceptual_swap | high | $\phi''(k)>0$ | Recuerde que los retornos decrecientes del capital $f_{KK}<0$ implican $\phi''(k)<0$ en la forma intensiva. |
| `D-H01-03` | Ahorro sobre capital | conceptual_swap | high | $\dot{K}=sK$ | Aplique la propensión marginal al ahorro $s$ sobre el flujo de producto $Q$, nunca sobre el stock de capital $K$. |

---

### [C-03] Acumulación Neoclásica y Pleno Empleo (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Acumulación Neoclásica y Pleno Empleo
- **Prerequisites:** H-01
- **Recommended Modalities:** multiple_select, adversarial_break, open_symbolic
- **Evidence Citations:** `solow1956.pdf` (page 3)

#### Description & Cognitive Model
Modelo agregado con un bien compuesto $Y=F(K,L)$ homogéneo de grado $1$, ahorro constante $\dot{K}=sY$ y oferta laboral exógena $L(t)=L_0 e^{nt}$ que implica $\dot{K}=sF(K,L_0 e^{nt})$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Ahorro sobre capital | conceptual_swap | high | $\dot{K}=sK$ | Recuerde que la inversión neta proviene de ahorrar una fracción $s$ del ingreso neto $Y=F(K,L)$, no del stock $K$ acumulado. |
| `D-C03-02` | Rendimientos crecientes | conceptual_swap | high | $F(\lambda K,\lambda L)=\lambda^2 F(K,L)$ | Aplique la hipótesis neoclásica de rendimientos constantes a escala, donde multiplicar ambos factores por $\lambda$ escala el producto por $\lambda$. |
| `D-C03-03` | Desempleo estructural | conceptual_swap | high | $L(t)<L_0 e^{nt}$ | Identifique que en la sección II los salarios reales se ajustan para mantener pleno empleo perpetuo de $L(t)=L_0 e^{nt}$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | Rendimientos constantes a escala $F(\lambda K,\lambda L)=\lambda F(K,L)$ sin factor fijo como tierra | Sin homogeneidad de grado uno no es posible reducir el sistema a variables per cápita. | - |
| `A-C03-02` | - | Pleno empleo continuo de $L(t)=L_0 e^{nt}$ y del capital preexistente mediante precios flexibles | Si existe rigidez salarial o desempleo involuntario, $\dot{K}=sF(K,L_0 e^{nt})$ deja de regir. | - |

---

### [Hab-01] Derivación de la Ecuación Fundamental (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 2: Derivación de la Ecuación Fundamental
- **Prerequisites:** H-01, C-03
- **Recommended Modalities:** proof_dag, open_symbolic, fill_in_the_blank
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2), `solow1956.pdf` (page 6)

#### Description & Cognitive Model
Condensación de la función de producción homogénea de grado $1$ ($Q=L\phi(k)$ o $Y=F(K,L)$), tasa de ahorro $\dot{K}=sY$ y crecimiento laboral $\dot{L}/L=n$ (o $\lambda$) diferenciando la razón capital-trabajo $k=K/L$ (o $r=K/L$) para obtener la ecuación fundamental $\dot{k}=s\phi(k)-\lambda k$ (equivalente a $\dot{r}=sF(r,1)-nr$).

#### Fused Distractor Models (9)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Omite regla producto | skipped_step | high | $\dot{K}=L\dot{k}$ | Aplique la regla del producto al diferenciar $K=kL$ respecto al tiempo: $\dot{K}=L\dot{k}+k\dot{L}$. |
| `D-Hab01-07` | Omite dilución laboral | skipped_step | high | $\dot{r}=sF(r,1)$ | Incluya la dilución $-nr$ al derivar $K=rL_0 e^{nt}$, pues el crecimiento de la fuerza laboral reduce el capital por trabajador. |
| `D-Hab01-02` | Signo positivo en lambda | skipped_step | high | $\dot{k}=s\phi(k)+\lambda k$ | Pase el término $\lambda k$ al miembro derecho con signo negativo al igualar $L\dot{k}+k\lambda L=sL\phi(k)$. |
| `D-Hab01-08` | Suma crecimiento laboral | skipped_step | high | $\dot{r}=sF(r,1)+nr$ | Verifique que $\dot{r}/r=\dot{K}/K-\dot{L}/L$; el crecimiento poblacional $n$ resta y no suma a la tasa de cambio de $r$. |
| `D-Hab01-03` | Conserva factor L | conceptual_swap | high | $\dot{k}=sL\phi(k)-\lambda k$ | Divida toda la ecuación $L\dot{k}+k\lambda L=sL\phi(k)$ entre el factor común positivo $L$ para eliminar $L$. |
| `D-Hab01-09` | Olvida multiplicar por r | conceptual_swap | high | $\dot{r}=sF(r,1)-n$ | Despeje $\dot{r}$ desde $\dot{r}/r=\dot{K}/K-n$ multiplicando ambos términos por $r$, lo que produce $-nr$ y no $-n$. |
| `D-Hab01-04` | Sustituye lambda por L | conceptual_swap | high | $\dot{k}=s\phi(k)-Lk$ | Sustituya $\dot{L}/L=\lambda$ en $\dot{L}=\lambda L$ antes de dividir por $L$ para que aparezca el parámetro $\lambda$. |
| `D-Hab01-05` | Invierte cociente ahorro | conceptual_swap | high | $\dot{k}=\frac{\phi(k)}{s}-\lambda k$ | Mantenga la propensión al ahorro $s$ multiplicando a $\phi(k)$, pues la inversión es una fracción $sQ$ del producto. |
| `D-Hab01-06` | Omite k en dilución | conceptual_swap | high | $\dot{k}=s\phi(k)-\lambda$ | Conserve el factor $k$ en $k\dot{L}=k\lambda L$ al derivar $K=kL$, obteniendo el término de dilución $\lambda k$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Fuerza laboral positiva $L(t)>0$ y diferenciable en $t$ | Si $L=0$, no puede definirse $k=K/L$ ni dividirse la ecuación por $L$. | - |
| `A-Hab01-02` | - | Positividad de la fuerza laboral $L(t)=L_0 e^{nt}>0$ con tasa constante $n$ | Si $L=0$ o $n$ varía en el tiempo, la razón $r=K/L$ y $-nr$ pierden validez. | - |

---

### [C-01] Línea de Fase y Estabilidad del Equilibrio (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Línea de Fase y Estabilidad del Equilibrio
- **Prerequisites:** Hab-01
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
Análisis cualitativo-gráfico de $\dot{k}=s\phi(k)-\lambda k$ en la línea de fase: intersección $\bar{k}>0$, pendiente negativa y convergencia global

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Confunde pendiente positiva | conceptual_swap | high | Pendiente positiva en $\bar{k}$ implica estabilidad | Verifique el signo de $\dot{k}$ a cada lado de $\bar{k}$: se requiere pendiente negativa para que $k$ retorne a $\bar{k}$. |
| `D-C01-02` | Distancia horizontal | conceptual_swap | high | $\dot{k}$ es la distancia horizontal entre curvas | Mida $\dot{k}=s\phi(k)-\lambda k$ como la distancia vertical entre la curva $s\phi(k)$ y el rayo $\lambda k$ para cada $k$. |
| `D-C01-03` | Origen es equilibrio estable | conceptual_swap | high | $k=0$ es el equilibrio convergente para $k(0)>0$ | Observe que cuando $s\phi(k)>\lambda k$ cerca del origen, $\dot{k}>0$ aleja a $k$ de cero hacia el equilibrio positivo $\bar{k}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Capital indispensable $\phi(0)=0$ y existencia de rango con $s\phi(k)>\lambda k$ | Sin esta condición no existe un equilibrio positivo $\bar{k}>0$ donde se crucen ambas curvas. | - |

---

### [C-02] Estado Uniforme y Progreso Tecnológico (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Estado Uniforme y Progreso Tecnológico
- **Prerequisites:** C-01
- **Recommended Modalities:** adversarial_break, multiple_select, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
En el estado uniforme $\bar{k}$, las variables $K$, $L$, $Q$ e inversión neta crecen a tasa $\lambda$; con progreso tecnológico $Q=T(t)f(K,L)$ ($dT/dt>0$), $\bar{k}$ aumenta secularmente

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Crecimiento nulo en equilibrio | conceptual_swap | high | $\dot{K}=\dot{Q}=0$ en $\bar{k}$ | Distinga estado uniforme de estado estacionario: en $\bar{k}$, $k$ es constante pero $K$, $L$ y $Q$ crecen todos a la tasa $\lambda$. |
| `D-C02-02` | Desplazamiento hacia abajo | conceptual_swap | high | $dT/dt>0$ desplaza $s\phi(k)$ hacia abajo | Note que $T(t)$ creciente eleva el producto por trabajador, desplazando $s\phi(k)$ hacia arriba y elevando el nivel $\bar{k}$. |
| `D-C02-03` | Requiere delicado balance | conceptual_swap | high | La economía no converge a $\lambda$ sin ajuste exógeno | Recuerde que en Solow la convergencia hacia la tasa común $\lambda$ ocurre de forma automática gracias a las proporciones variables. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | Función de producción invariante en el tiempo en el caso base, o $dT/dt>0$ con progreso tecnológico | Si $T(t)$ varía arbitrariamente sin signo definido, no hay desplazamiento secular monotónico de $\bar{k}$. | - |

---

### [C-04] Equilibrio Estacionario y Estabilidad (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 7: Equilibrio Estacionario y Estabilidad
- **Prerequisites:** Hab-01
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 7)

#### Description & Cognitive Model
Análisis gráfico y cualitativo de $\dot{r}=sF(r,1)-nr$: intersección $nr=sF(r^*,1)$, estabilidad cuando $sF(r,1)$ cruza $nr$ desde arriba, equilibrios múltiples y no existencia.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Confunde estabilidad | conceptual_swap | high | $\dot{r}>0 \text{ para } r>r^*$ | Observe en la Figura I que para $r>r^*$ el rayo $nr$ supera a $sF(r,1)$, por lo que $\dot{r}<0$ y $r$ converge hacia $r^*$. |
| `D-C04-02` | Todo cruce es estable | conceptual_swap | high | $r_2 \text{ es estable}$ | Evalúe la pendiente relativa en $r_2$: allí $sF(r,1)$ cruza $nr$ desde abajo, generando $\dot{r}<0$ a la izquierda y $\dot{r}>0$ a la derecha. |
| `D-C04-03` | Crecimiento nulo en r* | conceptual_swap | high | $\dot{K}/K=0 \text{ en } r^*$ | Distinga la constancia de la razón $r^*=K/L$ ($\dot{r}=0$) del crecimiento agregado, donde $K$, $L$ y $Y$ crecen a tasa $n$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | Productividad marginal del capital positiva y decreciente en el caso estándar de la Figura I | Sin concavidad estricta pueden surgir múltiples equilibrios como en la Figura II o divergencia. | - |

---

### [Hab-02] Solución Explícita Cobb-Douglas (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Solución Cuantitativa Cobb-Douglas
- **Prerequisites:** Hab-01, C-01, C-04
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 5), `solow1956.pdf` (page 13)

#### Description & Cognitive Model
Resolución analítica de la dinámica de Solow con tecnología Cobb-Douglas mediante linealización de Bernoulli $\dot{k}+\lambda k=sk^\alpha$ ($z=k^{1-\alpha}$) o integración directa de $\dot{K}=sK^a(L_0 e^{nt})^{1-a}$, obteniendo la trayectoria temporal, el estado estacionario $r^*=(s/n)^{1/(1-a)}$, el producto per cápita $(s/n)^{a/(1-a)}$ y el coeficiente capital-producto $C=s/n$.

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Sustitución errónea z | skipped_step | high | $z=k^\alpha$ | Use la sustitución estándar de Bernoulli $z=k^{1-m}$ con $m=\alpha$, es decir, $z=k^{1-\alpha}$, para obtener una EDO lineal. |
| `D-Hab02-07` | Exponente sin invertir | skipped_step | high | $r^*=(s/n)^{1-a}$ | Al igualar $sr^a=nr$ se obtiene $r^{1-a}=s/n$; eleve ambos miembros al recíproco $1/(1-a)$ para hallar $r^*$. |
| `D-Hab02-02` | Omite factor (1-alpha) | skipped_step | high | $\frac{dz}{dt}+\lambda z=s$ | Multiplique ambos coeficientes por $(1-\alpha)$ al derivar $z=k^{1-\alpha}$, obteniendo $dz/dt+(1-\alpha)\lambda z=(1-\alpha)s$. |
| `D-Hab02-08` | Razón n/s invertida | skipped_step | high | $r^*=(n/s)^{1/(1-a)}$ | Verifique que mayor ahorro $s$ o menor crecimiento laboral $n$ elevan el capital por trabajador de equilibrio $r^*=(s/n)^{1/b}$. |
| `D-Hab02-03` | Exponente invertido en límite | conceptual_swap | high | $k\to(s/\lambda)^{1-\alpha}$ | Despeje $k$ de $k^{1-\alpha}\to s/\lambda$ elevando al recíproco $\frac{1}{1-\alpha}$ para obtener el estado uniforme correcto. |
| `D-Hab02-09` | Ingreso per cápita errado | conceptual_swap | high | $y^*=(s/n)^{1/b}$ | Evalúe $Y/L=r^a$ en el equilibrio $r^*=(s/n)^{1/b}$, lo cual produce el límite $(s/n)^{a/b}$ y no $(s/n)^{1/b}$. |
| `D-Hab02-04` | Invierte cociente s/lambda | conceptual_swap | high | $k\to(\lambda/s)^{\frac{1}{1-\alpha}}$ | Verifique que el equilibrio varía directamente con $s$ e inversamente con $\lambda$, manteniendo el cociente $s/\lambda$. |
| `D-Hab02-10` | Coeficiente capital-producto errado | conceptual_swap | high | $C=n/s$ | Observe que $K/Y=r/r^a=r^{1-a}=r^b$, que en estado estacionario vale $s/n$, implicando la igualdad $n=s/C$. |
| `D-Hab02-05` | Signo positivo en exponente t | conceptual_swap | high | $e^{(1-\alpha)\lambda t}$ | Conserve el signo negativo en $e^{-(1-\alpha)\lambda t}$ para que el término transitorio se anule cuando $t\to\infty$. |
| `D-Hab02-11` | Error en integral de K | conceptual_swap | high | $K(t)=[K_0^b+(s/n)L_0^b e^{nbt}]^{1/b}$ | Aplique la condición inicial en $t=0$ al integrar $\dot{K}K^{-a}=sL_0^b e^{nbt}$ para conservar el término $-(s/n)L_0^b$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Parámetros $\alpha\in(0,1)$ y $\lambda>0$ en la función Cobb-Douglas $Q=K^\alpha L^{1-\alpha}$ | Si $\alpha\ge 1$ o $\lambda\le 0$, el término exponencial no tiende a cero y no hay convergencia. | - |
| `A-Hab02-02` | - | Parámetro tecnológico $a\in(0,1)$ en la función Cobb-Douglas $Y=K^a L^{1-a}$ | Si $a\ge 1$, desaparece el rendimiento decreciente del capital y no cruza el rayo $nr$. | - |

---

### [Hab-04] Modelo de Proporciones Fijas (Harrod-Domar) (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 11: Modelo de Proporciones Fijas (Harrod-Domar)
- **Prerequisites:** Hab-01, C-04
- **Recommended Modalities:** unstructured_model, adversarial_break, open_symbolic
- **Evidence Citations:** `solow1956.pdf` (page 11)

#### Description & Cognitive Model
Resolución de $\dot{r}=s\min(r/a,1/b)-nr$ bajo tecnología de Leontief $Y=\min(K/a,L/b)$, comparando la tasa garantizada $s/a$ con la tasa natural $n$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Invierte tasa garantizada | skipped_step | high | $a/s$ | Recuerde que la pendiente inicial de $s\min(r/a,1/b)$ es $s/a$, que representa la tasa garantizada de Harrod-Domar. |
| `D-Hab04-02` | Ignora desempleo en n1>s/a | skipped_step | high | $r \to a/b \text{ si } n_1>s/a$ | Note que si $n_1>s/a$, el rayo $n_1 r$ supera siempre a $s\min(r/a,1/b)$, por lo que $r$ cae hacia $0$ con desempleo creciente. |
| `D-Hab04-03` | Desempleo cuando n3<s/a | conceptual_swap | high | $L \text{ redundante si } n_3<s/a$ | Identifique que cuando $n_3<s/a$, $r$ converge a $s/(n_3 b)>a/b$, haciendo redundante al capital con fracción empleada $an_3/s$. |
| `D-Hab04-04` | Omite umbral a/b | conceptual_swap | high | $\dot{r}=s/b-nr \text{ para todo } r$ | Compare $r/a$ con $1/b$: solo cuando $r\ge a/b$ el factor limitante es el trabajo y la curva adopta altura constante $s/b$. |
| `D-Hab04-05` | Empleo errado | conceptual_swap | high | $L_{\text{emp}}=K/a$ | Multiplique el producto limitado por el capital $Y=K/a$ por el requerimiento unitario de trabajo $b$ para obtener empleo $bK/a$. |
| `D-Hab04-06` | Fracción invertida | conceptual_swap | high | $s/(an_3)$ | Divida el capital requerido $(a/b)L$ entre el capital disponible $r^* L=(s/(n_3 b))L$, obteniendo la fracción $an_3/s<1$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Proporciones fijas con coeficientes técnicos positivos $a>0$ y $b>0$ sin sustitución entre factores | Si existe flexibilidad de proporciones al menos en un rango, desaparece el filo de navaja rígido. | - |

---

### [Hab-06] Equilibrio y Divergencia en Función CES (p=1/2) (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 14: Equilibrio y Divergencia en Función CES (p=1/2)
- **Prerequisites:** Hab-01, C-04
- **Recommended Modalities:** open_symbolic, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 14)

#### Description & Cognitive Model
Análisis de $Y=(a\sqrt{K}+\sqrt{L})^2$ con $\dot{r}=s(a\sqrt{r}+1)^2-nr$: condición de bifurcación $sa^2<n$ vs $sa^2>n$ y cálculo de $r^*=(1/(\sqrt{n/s}-a))^2$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Signo errado en raíz | skipped_step | high | $r^*=(1/(\sqrt{n/s}+a))^2$ | Despeje $\sqrt{r}$ de $\sqrt{s}(a\sqrt{r}+1)=\sqrt{nr}$, obteniendo $\sqrt{r}(\sqrt{n/s}-a)=1$ cuando $sa^2<n$. |
| `D-Hab06-02` | Condición de equilibrio invertida | skipped_step | high | $sa^2>n \Rightarrow \text{equilibrio estable}$ | Compare las pendientes asintóticas: si $sa^2>n$, la curva $s(a\sqrt{r}+1)^2$ permanece sobre $nr$ y $r$ crece sin límite. |
| `D-Hab06-03` | Origen es equilibrio | conceptual_swap | high | $sF(0,1)=0$ | Evalúe $F(0,1)=(a\cdot 0+1)^2=1$, de modo que la curva inicia en altura positiva $s$ sobre el eje vertical. |
| `D-Hab06-04` | Olvida elevar al cuadrado | conceptual_swap | high | $r^*=1/(\sqrt{n/s}-a)$ | Recuerde que la ecuación linealizada resuelve para $\sqrt{r^*}$, por lo que debe elevar el resultado al cuadrado. |
| `D-Hab06-05` | Ingreso límite errado | conceptual_swap | high | $y^*=1/(1+a\sqrt{s/n})^2$ | Sustituya $r^*$ en $(a\sqrt{r^*}+1)^2$ y simplifique para obtener el ingreso límite por trabajador $1/(1-a\sqrt{s/n})^2$. |
| `D-Hab06-06` | Convexidad para p>1 | conceptual_swap | high | $p>1 \Rightarrow \text{rendimientos decrecientes}$ | Verifique que solo para $0<p<1$ las isocuantas tienen la convexidad usual con productividad marginal decreciente. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Restricción paramétrica $0<p<1$ (específicamente $p=1/2$) y condición $sa^2<n$ para equilibrio finito | Si $p\ge 1$ falla la convexidad; si $sa^2>n$ no existe equilibrio de crecimiento balanceado. | - |

---

### [C-05] Productividades Marginales y Precios Reales (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 16: Productividades Marginales y Precios Reales
- **Prerequisites:** C-03, C-04
- **Recommended Modalities:** multiple_select, adversarial_break, open_symbolic
- **Evidence Citations:** `solow1956.pdf` (page 16)

#### Description & Cognitive Model
Determinación competitiva del salario real $\partial F/\partial L=w/p$ y la renta real del capital $\partial F/\partial K=q/p$, invariancia de escala y papel del nivel de precios $p(t)$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Dependencia de escala | conceptual_swap | high | $\partial F/\partial K \text{ depende de } L$ | Aplique la homogeneidad de grado cero de las derivadas parciales bajo rendimientos constantes a escala: solo dependen de $r=K/L$. |
| `D-C05-02` | Determinación de p(t) | conceptual_swap | high | $p(t) \text{ determinado internamente}$ | Identifique que en un sistema puramente real solo se determinan precios relativos ($w/p$, $q/p$), tomando $p(t)$ como dado. |
| `D-C05-03` | Igualación a precios nominales | conceptual_swap | high | $\partial F/\partial L=w$ | Divida el salario monetario $w$ entre el precio del producto $p$ para igualar la productividad física marginal al salario real $w/p$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Competencia pura con empresas idénticas que permiten definir una función agregada de rendimientos constantes | Bajo competencia monopolística con tangencia de grupo grande falla la construcción agregada. | - |

---

### [C-06] Precios Competitivos y Arbitraje de Capital (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 16: Precios Competitivos y Arbitraje de Capital
- **Prerequisites:** C-05
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 16)

#### Description & Cognitive Model
Determinación competitiva del salario real $\frac{\partial F}{\partial L}=\frac{w}{p}$ y renta real $\frac{\partial F}{\partial K}=\frac{q}{p}$, junto con la condición de arbitraje perfecto $i(t)=\frac{q(t)}{p(t)}+\frac{\dot{p}(t)}{p(t)}$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Iguala tasa monetaria y renta real | conceptual_swap | high | $i(t)=q(t)/p(t)$ | Sume la tasa de variación de precios $\dot{p}(t)/p(t)$ a la renta propia $q(t)/p(t)$ para igualar el retorno de prestar dinero y poseer capital. |
| `D-C06-02` | Confunde producto marginal con precio nominal | conceptual_swap | high | $\frac{\partial F}{\partial K}=q$ | Divida la renta monetaria $q$ entre el precio del producto $p$, pues la productividad marginal se mide en unidades reales de producto. |
| `D-C06-03` | Signo invertido en ganancia de capital | conceptual_swap | high | $i(t)=\frac{q(t)}{p(t)}-\frac{\dot{p}(t)}{p(t)}$ | Sume $\dot{p}/p$ al rendimiento propio $q/p$, ya que la apreciación del bien de capital incrementa el retorno nominal de mantenerlo. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Previsión perfecta y ausencia de riesgo e incertidumbre en el arbitraje | Con riesgo o preferencia por activos, la igualdad exacta de arbitraje deja de cumplirse. | - |
| `A-C06-02` | - | Competencia perfecta con rendimientos constantes a escala en $F(K,L)$ | Sin competencia ni homogeneidad de grado uno, las productividades marginales no agotan el producto. | - |

---

### [C-07] Isocuantas, Trayectorias y Precios Relativos (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 19: Isocuantas, Trayectorias y Precios Relativos
- **Prerequisites:** C-06
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 19)

#### Description & Cognitive Model
Relación geométrica entre rayos de equilibrio $K=r^*L$, pendiente constante de las isocuantas $\frac{w}{q}$ bajo rendimientos constantes a escala y contraste con proporciones fijas Harrod-Domar

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Pendiente varía sobre el rayo | conceptual_swap | high | $w/q$ cambia sobre $K=r^*L$ | Recuerde que bajo rendimientos constantes a escala las productividades marginales dependen solo de $r=K/L$, manteniendo constante $w/q$ sobre cada rayo. |
| `D-C07-02` | Precios determinados en Harrod-Domar | conceptual_swap | high | $w/q$ único en $r=a/b$ | Note que en $r=a/b$ ambos factores son escasos y solo se fija $aq+bw=p$, dejando indeterminados los precios individuales de los factores. |
| `D-C07-03` | Caída indefinida de la tasa de interés | conceptual_swap | high | $q/p\to 0$ siempre en equilibrio | Distinga el ajuste finito hacia $r^*$ estable de la tesis de Harrod: si existe equilibrio estable, el ajuste de $q/p$ o $w/p$ es acotado. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Isocuantas convexas y diferenciables en el caso neoclásico frente a esquinas en Harrod-Domar | Si hay esquinas rectas $r=a/b$, ocurren saltos discontinuos e indeterminación de precios. | - |

---

### [Hab-07] Cálculo de Precios y Participación Factorial (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 21: Cálculo de Precios y Participación Factorial
- **Prerequisites:** C-06, C-07
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 21)

#### Description & Cognitive Model
Cálculo analítico de salarios reales, rentas de equilibrio y participación relativa del trabajo en funciones Cobb-Douglas $Y=K^aL^{1-a}$ y $Y=(a\sqrt{K}+\sqrt{L})^2$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Invierte exponente de salario Cobb-Douglas | skipped_step | high | $\frac{w}{p}=(1-a)(s/n)^{\frac{1-a}{a}}$ | Sustituya $r^*=(s/n)^{1/(1-a)}$ dentro de $r^a$ multiplicando los exponentes para obtener correctamente $(s/n)^{a/(1-a)}$. |
| `D-Hab07-02` | Participación constante fuera de Cobb-Douglas | skipped_step | high | $(w/p)(L/Y)$ independiente de $s$ y $n$ | Evalúe $(w/p)(L/Y)=1-a\sqrt{s/n}$ en equilibrio: fuera de Cobb-Douglas, mayor $n$ y menor $s$ elevan la participación del trabajo. |
| `D-Hab07-03` | Error en renta real Cobb-Douglas | conceptual_swap | high | $q/p=as/n$ | Note que $r^{a-1}=r^{-(1-a)}$ invierte la razón $s/n$ de $r^*$, dando una renta real de equilibrio $q/p=an/s$. |
| `D-Hab07-04` | Omite factor a en renta real | conceptual_swap | high | $q/p=n/s$ | Conserve el coeficiente $a$ proveniente de derivar $K^aL^{1-a}$ respecto a $K$ antes de sustituir el capital-trabajo estacionario. |
| `D-Hab07-05` | Invierte razón s/n en participación | conceptual_swap | high | $(w/p)(L/Y)=1-a\sqrt{n/s}$ | Verifique algebraicamente que $w/p=(1-a\sqrt{s/n})^{-1}$ y $Y/L=(1-a\sqrt{s/n})^{-2}$, por lo que $(w/p)(L/Y)=1-a\sqrt{s/n}$. |
| `D-Hab07-06` | Confunde w/q con w/p | conceptual_swap | high | $w/p=\frac{1-a}{a}r$ | Distinga la razón de precios factoriales $w/q=\frac{1-a}{a}r$ del salario real $w/p=(1-a)r^a$ en unidades de producto. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Existencia de equilibrio balanceado con $\sqrt{n/s}>a$ en $Y=(a\sqrt{K}+\sqrt{L})^2$ | Si $\sqrt{n/s}\le a$, no existe razón capital-trabajo estacionaria finita. | - |

---

### [Hab-08] Dinámica con Cambio Tecnológico Neutral (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 22: Dinámica con Cambio Tecnológico Neutral
- **Prerequisites:** C-06, Hab-07
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 22)

#### Description & Cognitive Model
Resolución de la trayectoria de largo plazo con cambio tecnológico neutral $Y=A(t)F(K,L)$ y $A(t)=e^{gt}$ en Cobb-Douglas para tasas de crecimiento de $K$, $Y$ y $K/L$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | Tasa de capital sin efecto multiplicador | skipped_step | high | $\dot{K}/K\to n+g$ | Integre $\dot{K}=sK^aL_0^{1-a}e^{(n(1-a)+g)t}$ y divida el exponente temporal entre $b=1-a$ para obtener la tasa $n+g/(1-a)$. |
| `D-Hab08-02` | Tasa de producto igual a tasa de capital | skipped_step | high | $\dot{Y}/Y\to n+g/(1-a)$ | Sustituya las tasas de $K$, $L$ y $A(t)$ en $Y=e^{gt}K^aL^{1-a}$ para verificar que $Y$ crece a $n+ag/(1-a)$ mientras $K/Y$ crece a tasa $g$. |
| `D-Hab08-03` | Capital por trabajador estacionario | conceptual_swap | high | $K/L\to\text{constante}$ | Advierta que la mayor capacidad de ahorro e inversión hace crecer $K/L$ indefinidamente a tasa asintótica $g/(1-a)$. |
| `D-Hab08-04` | Tasa de K/Y nula | conceptual_swap | high | $K/Y$ constante en el largo plazo | Reste las tasas asintóticas de $K$ y $Y$: $(n+g/b)-(n+ag/b)=g>0$, por lo que $K/Y$ crece continuamente a tasa $g$. |
| `D-Hab08-05` | Salario real estancado | conceptual_swap | high | $w/p$ converge a un límite finito | Relacione el crecimiento perpetuo de $K/L$ con la productividad marginal del trabajo: tanto $A(t)$ como $K/L$ impulsan al alza $w/p$ sin límite. |
| `D-Hab08-06` | Cambia participación del trabajo | conceptual_swap | high | Participación laboral crece con $g$ | Recuerde que la función Cobb-Douglas mantiene constante la participación del trabajo en $1-a$ incluso bajo cambio tecnológico neutral. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab08-01` | - | Progreso técnico neutral multiplicativo $A(t)=e^{gt}$ con $g>0$ y $b=1-a\in(0,1)$ | Si el cambio técnico no es neutral, la forma de las isocuantas se altera en el tiempo. | - |

---

### [C-08] Oferta Elástica de Trabajo y Equilibrio (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 23: Oferta Elástica de Trabajo y Equilibrio
- **Prerequisites:** C-06
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 23)

#### Description & Cognitive Model
Incorporación de oferta laboral elástica $L=L_0e^{nt}(w/p)^h$ y forma general $L=G(t,w/p)$ en la ecuación fundamental de $\dot{r}$ y su efecto sobre el equilibrio $r^*$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Elasticidad h desplaza r* | conceptual_swap | high | $h>0$ altera el equilibrio $r^*$ | Observe el factor $(1+ah/r)^{-1}$ en $\dot{r}=(sF(r,1)-nr)(1+ah/r)^{-1}$: $\dot{r}=0$ ocurre exactamente en el mismo $r^*$ que cuando $h=0$. |
| `D-C08-02` | Tasa asintótica distinta de n | conceptual_swap | high | $K$ crece a tasa $n+h$ con (14) | Recuerde que en equilibrio $\dot{r}=0$ implica $\dot{w}=0$, por lo que el término salarial no aporta crecimiento y $K,Y,L$ crecen a tasa $n$. |
| `D-C08-03` | Invariancia bajo cualquier G(t,w/p) | conceptual_swap | high | $r^*$ nunca cambia con oferta elástica | Evalúe la condición general $sF(r,1)=\frac{r}{G}\frac{\partial G}{\partial t}$: solo si $\frac{1}{G}\frac{\partial G}{\partial t}=n$ se preserva $r^*$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C08-01` | - | Salarios reales moderados donde $L=L_0e^{nt}(w/p)^h$ no excede la fuerza laboral física | A salarios muy altos debe imponerse un tope máximo a la oferta de trabajo. | - |

---

### [Hab-09] Tasa de Ahorro Variable e Impuesto al Ingreso (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 26: Tasa de Ahorro Variable e Impuesto al Ingreso
- **Prerequisites:** C-07
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 26)

#### Description & Cognitive Model
Análisis de tasa de ahorro endógena $s(r)$ dependiente del rendimiento del capital en $\dot{r}=s(r)F(r,1)-nr$ y cálculo del ahorro efectivo bajo impuesto proporcional $t$ con fracción invertida $v$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab09-01` | Error en ahorro efectivo con impuesto | skipped_step | high | $s_{\mathrm{eff}}=s(1-t)+vt$ sin simplificar | Sume el ahorro privado sobre el ingreso disponible $s(1-t)$ y la inversión pública $vt$ para obtener $s_{\mathrm{eff}}=s+(v-s)t$. |
| `D-Hab09-02` | Impuesto siempre reduce ahorro efectivo | skipped_step | high | $s_{\mathrm{eff}}<s$ para todo $v\in[0,1]$ | Compare la propensión a invertir estatal $v$ con la privada $s$: si $v>s$, entonces $(v-s)t>0$ y el ahorro efectivo aumenta. |
| `D-Hab09-03` | Ahorro variable crea estado estacionario | conceptual_swap | high | $s(r)=0\Rightarrow L$ deja de crecer | Note que la fuerza laboral sigue creciendo a tasa exógena $n$; si $r$ anula el ahorro, el crecimiento de $L$ reduce nuevamente $r$. |
| `D-Hab09-04` | Signo erróneo de s'(r) | conceptual_swap | high | $s(r)$ creciente con $r$ | Recuerde que la productividad marginal del capital $q/p$ cae al subir $r$, por lo que una respuesta positiva a $q/p$ implica $s(r)$ decreciente en $r$. |
| `D-Hab09-05` | Permite crecimiento ilimitado de r | conceptual_swap | high | $s(r)\to 0$ permite $r\to\infty$ | Verifique que si $s(r)$ se vuelve cero para $r$ suficientemente grande, la última intersección de $s(r)F(r,1)$ con $nr$ es necesariamente estable. |
| `D-Hab09-06` | Omite efecto sobre equilibrio | conceptual_swap | high | $r^*$ no cambia con impuesto | Observe que cambiar $s$ por $s+(v-s)t$ escala uniformemente la curva $sF(r,1)$ hacia arriba o abajo, desplazando la intersección $r^*$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab09-01` | - | Tasa de ahorro $s(r)$ decreciente en $r$ e impuesto proporcional $t\in(0,1)$ con fracción invertida $v\in[0,1]$ | Impuestos no proporcionales introducen torsiones no uniformes en $sF(r,1)$. | - |

---

### [C-09] Crecimiento Poblacional Endógeno y Trampas (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 27: Crecimiento Poblacional Endógeno y Trampas
- **Prerequisites:** C-07
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 27)

#### Description & Cognitive Model
Dinámica de $\dot{r}=sF(r,1)-n(r)r$ con tasa poblacional endógena $n(r)$: equilibrio estable $r_1$, umbral inestable $r_2$ y expansión autosostenida sin indivisibilidades

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Clasificación invertida de estabilidad | conceptual_swap | high | $r_1$ inestable y $r_2$ estable | Examine el signo de $\dot{r}=sF(r,1)-n(r)r$ alrededor de cada cruce: para $r<r_2$ el sistema retorna a $r_1$ (estable), y para $r>r_2$ diverge. |
| `D-C09-02` | Requiere rendimientos crecientes | conceptual_swap | high | Trampa exige rendimientos crecientes | Destaque el resultado clave de Solow: con rendimientos constantes a escala, $n(r)$ no lineal basta para generar trampa bajo $r_2$ y despegue sobre $r_2$. |
| `D-C09-03` | Rayo nr sigue siendo recto | conceptual_swap | high | $n(r)r$ es una recta por el origen | Recuerde que al depender $n$ del ingreso per cápita $F(r,1)$, el rayo $nr$ se curva en $n(r)r$ reflejando la respuesta demográfica. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | Tasa demográfica $\dot{L}/L=n(r)$ determinada exclusivamente por el ingreso per cápita $F(r,1)$ | Si la demografía responde a rezagos o factores exógenos, la ecuación unidimensional pierde validez. | - |

---

### [C-10] Rigidez Salarial y Preferencia por la Liquidez (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 29: Rigidez Salarial y Preferencia por la Liquidez
- **Prerequisites:** C-06, C-07
- **Recommended Modalities:** adversarial_break, proof_dag, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 29)

#### Description & Cognitive Model
Efectos de rigidez del salario real $\bar{w}/p$ fijando $\bar{r}$ con crecimiento del empleo $\frac{\dot{L}}{L}=\frac{s}{\bar{r}}F(\bar{r},1)$ y preferencia por la liquidez $\bar{M}=Q(Y,q/p)$ en la trampa monetaria

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C10-01` | Invierte condición de desempleo | conceptual_swap | high | $\frac{s}{\bar{r}}F(\bar{r},1)>n$ causa desempleo | Compare las tasas: si $\frac{s}{\bar{r}}F(\bar{r},1)<n$ (pendiente menor que $n$), el empleo crece más lento que la fuerza laboral y surge desempleo. |
| `D-C10-02` | Trampa de liquidez afecta salario | conceptual_swap | high | Trampa de liquidez fija $w/p$ | Note que la demanda infinitamente elástica de saldos ociosos fija la tasa de interés por encima del nivel de equilibrio, subutilizando el capital. |
| `D-C10-03` | Modelo real basta con preferencia por liquidez | conceptual_swap | high | Modelo sin dinero explica la trampa | Reconozca la limitación señalada por Solow: cuando hay elección entre efectivo y capital, el precio del bien compuesto exige dinámica monetaria. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C10-01` | - | Salario real fijo $\bar{w}/p$ o tasa de interés rígida bajo nivel de precios constante | Con precios flexibles y dinámica monetaria completa, la demanda real de dinero cambia con $p(t)$. | - |

---
