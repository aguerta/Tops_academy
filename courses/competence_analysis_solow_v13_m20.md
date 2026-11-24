# Cognitive Task Analysis (CTA): Solow V13 M20

- **Course ID:** `solow_v13_m20`
- **Macro-Competency:** Dominio y aplicación analítica integral de Solow V13 M20
- **Structure:** 20 total competencies (1 Facts, 11 Concepts, 8 Skills) with 88 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `PRE-01` | Acumulación y Función Neoclásica | Fact | Understand | Unidad 3: Acumulación y Función Neoclásica | - | 3 |
| `C-01` | Función de Producción Neoclásica y Forma Intensiva | Concept | Analyze | Unidad 2: Función de Producción Neoclásica y Forma Intensiva | PRE-01 | 3 |
| `Hab-01` | Derivación de la Ecuación Fundamental de Solow | Skill | Evaluate | Unidad 3: Derivación de la Ecuación Fundamental de Solow | C-01 | 6 |
| `C-02` | Análisis Cualitativo, Equilibrio y Estabilidad | Concept | Evaluate | Unidad 3: Análisis Cualitativo, Equilibrio y Estabilidad | Hab-01 | 3 |
| `C-03` | Estado Uniforme y Progreso Tecnológico Exógeno | Concept | Evaluate | Unidad 4: Estado Uniforme y Progreso Tecnológico Exógeno | C-02 | 3 |
| `Hab-02` | Solución Cuantitativa con Función Cobb-Douglas | Skill | Evaluate | Unidad 5: Solución Cuantitativa con Función Cobb-Douglas | Hab-01, C-02 | 6 |
| `C-04` | Ecuación Diferencial de Solow | Concept | Evaluate | Unidad 6: Ecuación Diferencial de Solow | PRE-01 | 3 |
| `C-05` | Estabilidad del Crecimiento Balanceado | Concept | Evaluate | Unidad 7: Estabilidad del Crecimiento Balanceado | C-04 | 3 |
| `C-06` | Equilibrios Múltiples y No Existencia | Concept | Analyze | Unidad 8: Equilibrios Múltiples y No Existencia | C-05 | 3 |
| `Hab-03` | Análisis de Proporciones Fijas | Skill | Evaluate | Unidad 11: Análisis de Proporciones Fijas | C-04 | 6 |
| `Hab-04` | Solución y Equilibrio Cobb-Douglas | Skill | Evaluate | Unidad 13: Solución y Equilibrio Cobb-Douglas | C-05 | 6 |
| `Hab-05` | Umbral Crítico con Sustituibilidad Parcial | Skill | Evaluate | Unidad 14: Umbral Crítico con Sustituibilidad Parcial | C-06 | 6 |
| `C-07` | Precios Competitivos de los Factores y Arbitraje | Concept | Analyze | Unidad 16: Precios Competitivos de los Factores | C-04 | 7 |
| `C-09` | Isocuantas y Razón Salario-Renta | Concept | Evaluate | Unidad 19: Isocuantas y Razón Salario-Renta | C-07 | 3 |
| `Hab-06` | Participación Factorial en Equilibrio | Skill | Evaluate | Unidad 21: Participación Factorial en Equilibrio | C-07, C-09 | 6 |
| `Hab-07` | Progreso Técnico Neutral | Skill | Analyze | Unidad 22: Progreso Técnico Neutral | C-07 | 6 |
| `C-10` | Oferta de Trabajo Elástica | Concept | Evaluate | Unidad 24: Oferta de Trabajo Elástica | C-07 | 3 |
| `Hab-08` | Ahorro Variable y Política Fiscal | Skill | Analyze | Unidad 26: Ahorro Variable y Política Fiscal | C-09 | 6 |
| `C-11` | Población Endógena y Trampas | Concept | Evaluate | Unidad 27: Población Endógena y Trampas | C-09 | 3 |
| `C-12` | Rigidez Salarial y Liquidez | Concept | Evaluate | Unidad 29: Rigidez Salarial y Liquidez | C-07, C-09 | 3 |

---

## Detailed Competency Specifications

### [PRE-01] Acumulación y Función Neoclásica (Fact)

- **Bloom Level:** Understand
- **Session:** Unidad 3: Acumulación y Función Neoclásica
- **Prerequisites:** None
- **Recommended Modalities:** fill_in_the_blank, multiple_select, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 3)

#### Description & Cognitive Model
Identifica la identidad de inversión neta $\dot{K} = sY$, la función de producción homogénea de grado 1 $Y = F(K, L)$ y el crecimiento exógeno del trabajo $L(t) = L_0 e^{nt}$ bajo pleno empleo.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-PRE01-01` | Rendimientos decrecientes a escala | conceptual_swap | high | $F(\lambda K, \lambda L) < \lambda F(K, L)$ | Recuerde que Solow asume rendimientos constantes a escala sin tierra escasa, por lo que $F$ es homogénea de primer grado. |
| `D-PRE01-02` | Ahorro sobre el capital | conceptual_swap | high | $\dot{K} = sK$ | La inversión neta proviene de ahorrar una fracción $s$ del producto neto $Y = F(K, L)$, no del acervo de capital $K$. |
| `D-PRE01-03` | Trabajo constante o endógeno | conceptual_swap | high | $L(t) = L_0$ | En el modelo base de Solow, la fuerza laboral crece exógenamente a tasa constante $n$ según $L(t) = L_0 e^{nt}$. |

---

### [C-01] Función de Producción Neoclásica y Forma Intensiva (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 2: Función de Producción Neoclásica y Forma Intensiva
- **Prerequisites:** PRE-01
- **Recommended Modalities:** multiple_select, adversarial_break, concept_matching
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
Representación de $Q=f(K,L)$ con proporciones variables, retornos marginales decrecientes y homogeneidad lineal en forma intensiva $Q=L\phi(k)$ con $k\equiv K/L$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Proporciones fijas tipo Domar | conceptual_swap | high | $Q = \rho K$ | Distinga el modelo de Domar de proporciones fijas del de Solow, donde $K$ y $L$ se combinan en proporciones variables $Q=f(K,L)$. |
| `D-C01-02` | Segunda derivada positiva | conceptual_swap | high | $\phi''(k) > 0$ | Recuerde que $f_{KK} = \phi''(k)/L < 0$ implica retornos marginales decrecientes del capital por trabajador, por lo que $\phi''(k) < 0$. |
| `D-C01-03` | Omite factor trabajo L | conceptual_swap | high | $Q = \phi(k)$ | Aplique la homogeneidad de grado uno $f(K,L) = L f(K/L, 1) = L\phi(k)$ sin omitir el factor multiplicativo $L$ del producto agregado. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Homogeneidad lineal: $f(\theta K, \theta L) = \theta f(K, L)$ para todo $\theta > 0$. | Sin retornos constantes a escala no es posible reducir $f(K,L)$ a la función univariada $\phi(k)$. | - |
| `A-C01-02` | - | Productos marginales positivos y decrecientes: $f_K, f_L > 0$ y $f_{KK}, f_{LL} < 0$. | Si $\phi''(k) \ge 0$, la curva $s\phi(k)$ no sería cóncava y podría no existir un equilibrio estable único. | - |

---

### [Hab-01] Derivación de la Ecuación Fundamental de Solow (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Derivación de la Ecuación Fundamental de Solow
- **Prerequisites:** C-01
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, proof_dag
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
Deducción de la ecuación diferencial $\dot{k}=s\phi(k)-\lambda k$ a partir de $\dot{K}=sQ$, $\dot{L}/L=\lambda$ y la diferenciación de $K=kL$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Olvida regla del producto | skipped_step | high | $\dot{K} = L\dot{k}$ | Aplique la regla del producto al diferenciar $K=kL$ respecto al tiempo: $\dot{K} = L\dot{k} + k\dot{L} = L\dot{k} + k\lambda L$. |
| `D-Hab01-02` | Signo positivo en dilución | skipped_step | high | $\dot{k} = s\phi(k) + \lambda k$ | Al igualar $L\dot{k} + k\lambda L = sL\phi(k)$ y despejar $\dot{k}$, el término $\lambda k$ pasa restando al miembro derecho. |
| `D-Hab01-03` | Omite dividir entre L | conceptual_swap | high | $\dot{k} = sL\phi(k) - \lambda k$ | Elimine el factor común $L > 0$ de ambos lados de $L\dot{k} + \lambda kL = sL\phi(k)$ para obtener la ecuación en términos intensivos. |
| `D-Hab01-04` | Confunde Q con k en ahorro | conceptual_swap | high | $\dot{K} = sk$ | Recuerde que la inversión $\dot{K}$ es una fracción constante $s$ del producto agregado $Q = L\phi(k)$, no del capital per cápita $k$. |
| `D-Hab01-05` | Invierte signos en tasa de crecimiento | conceptual_swap | high | $\dot{k}/k = \lambda - s\phi(k)/k$ | Divida $\dot{k} = s\phi(k) - \lambda k$ término a término entre $k$ para obtener $\dot{k}/k = s\phi(k)/k - \lambda$. |
| `D-Hab01-06` | Tasa de ahorro aplicada a L | conceptual_swap | high | $\dot{k} = s\lambda k - \phi(k)$ | Asocie la propensión al ahorro $s$ exclusivamente con el producto por trabajador $\phi(k)$ y la tasa $\lambda$ con el crecimiento laboral. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Propensión marginal al ahorro $s \in (0,1)$ constante y tasa de crecimiento laboral $\lambda > 0$ constante. | Si $s$ o $\lambda$ variaran arbitrariamente, la ecuación diferencial dejaría de ser autónoma en $k$. | - |

---

### [C-02] Análisis Cualitativo, Equilibrio y Estabilidad (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Análisis Cualitativo, Equilibrio y Estabilidad
- **Prerequisites:** Hab-01
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
Interpretación de la intersección $s\phi(\bar{k})=\lambda\bar{k}$ y de la línea de fase $\dot{k}=s\phi(k)-\lambda k$ para determinar existencia y estabilidad de $\bar{k}$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Equilibrio inestable por pendiente positiva | conceptual_swap | high | $\frac{d\dot{k}}{dk}\big|_{\bar{k}} > 0$ implica estabilidad | Verifique que para converger hacia $\bar{k}$ desde ambos lados se requiere $\dot{k}>0$ si $k<\bar{k}$ y $\dot{k}<0$ si $k>\bar{k}$, es decir, pendiente negativa. |
| `D-C02-02` | Confunde distancia vertical con nivel de k | conceptual_swap | high | $\dot{k} = s\phi(k) + \lambda k$ | Recuerde que $\dot{k} = s\phi(k) - \lambda k$ se mide como la distancia vertical entre la curva $s\phi(k)$ y el rayo $\lambda k$. |
| `D-C02-03` | Iguala pendiente en vez de nivel | conceptual_swap | high | $s\phi'(\bar{k}) = \lambda$ | Distinga el equilibrio $\dot{k}=0$, donde se igualan los niveles $s\phi(\bar{k}) = \lambda\bar{k}$, de la condición de máximo de $\dot{k}$ donde $s\phi'(k)=\lambda$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | El capital es indispensable ($\phi(0)=0$) y existe $k>0$ tal que $s\phi(k) > \lambda k$. | Si $s\phi(k) < \lambda k$ para todo $k>0$, no existe equilibrio positivo $\bar{k}$ y $k(t)$ colapsa hacia cero. | - |

---

### [C-03] Estado Uniforme y Progreso Tecnológico Exógeno (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Estado Uniforme y Progreso Tecnológico Exógeno
- **Prerequisites:** C-02
- **Recommended Modalities:** adversarial_break, multiple_select, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
Caracterización del estado uniforme donde $K$, $L$, $Q$ y $\dot{K}$ crecen a tasa $\lambda$, y efecto de $Q=T(t)f(K,L)$ con $dT/dt>0$ sobre $\bar{k}$ y la productividad.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Confunde estado uniforme con estacionario | conceptual_swap | high | $\dot{K} = \dot{L} = \dot{Q} = 0$ | Distinga el estado estacionario (tasa cero) del estado uniforme, donde $k=\bar{k}$ es constante pero $K, L, Q$ y $\dot{K}$ crecen a tasa $\lambda$. |
| `D-C03-02` | Tecnología reduce capital de equilibrio | conceptual_swap | high | $\frac{dT}{dt} > 0 \Rightarrow \bar{k}\downarrow$ | Observe que un término multiplicativo creciente $T(t)$ eleva el producto por trabajador, desplaza $s\phi(k)$ hacia arriba y genera un $\bar{k}$ mayor. |
| `D-C03-03` | Inversión neta crece a tasa distinta de lambda | conceptual_swap | high | $\dot{K} = \text{constante}$ | Si $K = Ae^{\lambda t}$ en estado uniforme, su derivada $\dot{K} = \lambda Ae^{\lambda t}$ también crece exactamente a la tasa exponencial $\lambda$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | Progreso tecnológico exógeno multiplicativo $Q = T(t)f(K,L)$ con $dT/dt > 0$. | Sin mejora tecnológica ($T$ constante), el capital por trabajador $\bar{k}$ queda fijo en un único estado uniforme. | - |

---

### [Hab-02] Solución Cuantitativa con Función Cobb-Douglas (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Solución Cuantitativa con Función Cobb-Douglas
- **Prerequisites:** Hab-01, C-02
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 5)

#### Description & Cognitive Model
Linealización de la ecuación de Bernoulli $\dot{k}+\lambda k=sk^\alpha$ mediante $z=k^{1-\alpha}$ para hallar la trayectoria $k(t)$ y el límite $(s/\lambda)^{\frac{1}{1-\alpha}}$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Exponente directo en lugar de recíproco | skipped_step | high | $k^* = (s/\lambda)^{1-\alpha}$ | Al obtener $k^{1-\alpha} \to s/\lambda$, eleve ambos miembros a la potencia recíproca $1/(1-\alpha)$ para despejar $k$. |
| `D-Hab02-02` | Omite factor (1-alpha) en derivada | skipped_step | high | $\frac{dz}{dt} + \lambda z = s$ | Diferencie $z=k^{1-\alpha}$ por regla de la cadena: $\dot{z}=(1-\alpha)k^{-\alpha}\dot{k}$, por lo que ambos coeficientes llevan $(1-\alpha)$. |
| `D-Hab02-03` | Signo positivo en exponente temporal | conceptual_swap | high | $e^{+(1-\alpha)\lambda t}$ | En $\dot{z}+az=b$ con $a=(1-\alpha)\lambda>0$, la solución homogénea decae con $e^{-at}=e^{-(1-\alpha)\lambda t}$ garantizando convergencia. |
| `D-Hab02-04` | Invierte razón s y lambda | conceptual_swap | high | $k^* = (\lambda/s)^{\frac{1}{1-\alpha}}$ | Divida el término constante $b=(1-\alpha)s$ entre el coeficiente $a=(1-\alpha)\lambda$ para obtener $s/\lambda$; mayor $s$ eleva $k^*$. |
| `D-Hab02-05` | Olvida restar s/lambda a z(0) | conceptual_swap | high | $z(t) = z(0)e^{-(1-\alpha)\lambda t} + \frac{s}{\lambda}$ | Evalúe la condición inicial en $t=0$: $z(0)=C+s/\lambda$ exige que la constante de integración sea $C = z(0) - s/\lambda$. |
| `D-Hab02-06` | Sustitución incorrecta de z | conceptual_swap | high | $z = k^{\alpha}$ | Para una ecuación de Bernoulli con exponente $m=\alpha$, el cambio linealizador estándar es $z = k^{1-m} = k^{1-\alpha}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Participación del capital $\alpha \in (0,1)$ y tasa de crecimiento laboral $\lambda > 0$. | Si $\alpha \ge 1$ o $\lambda \le 0$, el exponente $-(1-\alpha)\lambda t$ no sería negativo y $k(t)$ no convergería a $(s/\lambda)^{1/(1-\alpha)}$. | - |

---

### [C-04] Ecuación Diferencial de Solow (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 6: Ecuación Diferencial de Solow
- **Prerequisites:** PRE-01
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 6)

#### Description & Cognitive Model
Deriva e interpreta la ecuación fundamental $\dot{r} = sF(r, 1) - nr$ para la razón capital-trabajo $r = K/L$ a partir de $\dot{K} = sF(K, L)$ y rendimientos constantes a escala.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Omite dilución poblacional | conceptual_swap | high | $\dot{r} = sF(r, 1)$ | Al diferenciar $r = K/L$ respecto al tiempo aparece el término de dilución $-nr$ por el crecimiento laboral a tasa $n$. |
| `D-C04-02` | Suma crecimiento laboral | conceptual_swap | high | $\dot{r} = sF(r, 1) + nr$ | Como $\dot{r}/r = \dot{K}/K - \dot{L}/L$, el crecimiento de la fuerza laboral $n$ reduce la razón capital-trabajo, generando $-nr$. |
| `D-C04-03` | División incorrecta por L | conceptual_swap | high | $\dot{r} = sF(r, L) - nr$ | Por homogeneidad de grado 1, $F(K, L)/L = F(K/L, 1) = F(r, 1)$, eliminando la dependencia explícita de $L$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | La función de producción $F(K, L)$ es homogénea de grado 1. | Sin rendimientos constantes a escala no puede reducirse $\dot{K}$ a una EDO autónoma en $r$. | - |
| `A-C04-02` | - | El producto $Y$ es neto tras reponer la depreciación del capital. | Si $Y$ fuera producto bruto, debería restarse explícitamente la depreciación $\delta r$ en $\dot{r}$. | - |

---

### [C-05] Estabilidad del Crecimiento Balanceado (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 7: Estabilidad del Crecimiento Balanceado
- **Prerequisites:** C-04
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 7)

#### Description & Cognitive Model
Evalúa la existencia y estabilidad del equilibrio $r^*$ donde $sF(r^*, 1) = nr^*$: si $r < r^* \Rightarrow \dot{r} > 0$ y si $r > r^* \Rightarrow \dot{r} < 0$, convergiendo al crecimiento balanceado a tasa $n$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Inestabilidad tipo filo de navaja | conceptual_swap | high | $r > r^* \Rightarrow \dot{r} > 0$ | Bajo productividad marginal decreciente de $K$, para $r > r^*$ se cumple $nr > sF(r, 1)$, por lo que $\dot{r} < 0$ y $r$ retorna a $r^*$. |
| `D-C05-02` | Tasa de crecimiento igual a s | conceptual_swap | high | $\dot{K}/K = s$ en $r^*$ | En el estado de crecimiento balanceado ($\dot{r} = 0$), el capital, el trabajo y el producto crecen todos a la tasa natural $n$. |
| `D-C05-03` | Crecimiento exponencial exacto fuera de r* | conceptual_swap | high | $K(t) = K_0 e^{nt}$ para todo $t$ si $r_0 \neq r^*$ | Cuando $r_0 \neq r^*$, la trayectoria de $K$ y $Y$ solo converge a la tasa exponencial $n$ de manera asintótica al acercarse a $r^*$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | La curva $F(r, 1)$ pasa por el origen, es cóncava y cumple productividad marginal decreciente. | Si la concavidad o el cruce con $nr$ fallan, puede desaparecer la unicidad o estabilidad global de $r^*$. | - |

---

### [C-06] Equilibrios Múltiples y No Existencia (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 8: Equilibrios Múltiples y No Existencia
- **Prerequisites:** C-05
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 8)

#### Description & Cognitive Model
Analiza configuraciones no estándar de $sF(r, 1)$ frente a $nr$: múltiples intersecciones con equilibrios estables ($r_1, r_3$) e inestable ($r_2$), o ausencia total de equilibrio cuando $sF(r, 1)$ no corta a $nr$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Equilibrio intermedio estable | conceptual_swap | high | $r_2$ es estable y $r_1, r_3$ son inestables | Cuando $sF(r, 1)$ corta a $nr$ desde abajo en $r_2$, un aumento de $r$ vuelve $\dot{r} > 0$, haciendo a $r_2$ inestable. |
| `D-C06-02` | Ingreso per cápita nulo si no hay cruce | conceptual_swap | high | Si $s_1 F^1(r, 1) > nr$ para todo $r > 0$, $r \to 0$ | Si $s_1 F^1(r, 1) > nr$ para todo $r$, entonces $\dot{r} > 0$ siempre y tanto $r$ como el ingreso por trabajador crecen sin cota. |
| `D-C06-03` | Origen como equilibrio con F(0,1)>0 | conceptual_swap | high | El origen $r = 0$ es equilibrio aunque $F(0, 1) > 0$ | Si es posible producir sin capital ($sF(0, 1) > 0$), en $r = 0$ se tiene $\dot{r} > 0$, por lo que el origen no es equilibrio. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | La función $F(r, 1)$ es no decreciente y representa rendimientos constantes a escala al multiplicarse por $L$. | Permite construir diversas curvas $sF(r, 1)$ con cero, uno o múltiples cruces con el rayo $nr$. | - |

---

### [Hab-03] Análisis de Proporciones Fijas (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 11: Análisis de Proporciones Fijas
- **Prerequisites:** C-04
- **Recommended Modalities:** open_symbolic, adversarial_break, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 11)

#### Description & Cognitive Model
Resuelve la dinámica $\dot{r} = s\min(r/a, 1/b) - nr$ del caso Harrod-Domar $Y = \min(K/a, L/b)$, identificando la tasa garantizada $s/a$ y los regímenes de redundancia laboral o exceso de capacidad.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Tasa garantizada errónea | skipped_step | high | La tasa garantizada es $s/b$ | Para $r < a/b$, el capital es el cuello de botella y $\dot{r} = (s/a - n)r$, por lo que la tasa garantizada es $s/a$. |
| `D-Hab03-02` | Redundancia invertida para n < s/a | skipped_step | high | Si $n_3 < s/a$, el trabajo se vuelve redundante | Cuando $n_3 < s/a$, $r$ converge a $s/(n_3 b) > a/b$, donde el trabajo es el cuello de botella y el capital resulta redundante. |
| `D-Hab03-03` | Proporción de capital empleado errónea | conceptual_swap | high | Proporción de capital empleada $= s/(an_3)$ | Con $r = s/(n_3 b)$ y capital necesario por trabajador $a/b$, la proporción empleada es $(a/b)/r = an_3/s < 1$. |
| `D-Hab03-04` | Umbral de pleno uso incorrecto | conceptual_swap | high | El cambio de régimen ocurre en $r = b/a$ | Al igualar $r/a = 1/b$ se obtiene el umbral de pleno uso de ambos factores en $r = a/b$, no $b/a$. |
| `D-Hab03-05` | Equilibrio único cuando n = s/a | conceptual_swap | high | Si $n_2 = s/a$ y $r_0 < a/b$, $r$ sube hasta $a/b$ | Si $n_2 = s/a$ y $r_0 < a/b$, entonces $\dot{r} = (s/a - n_2)r = 0$, preservándose indefinidamente la redundancia laboral inicial. |
| `D-Hab03-06` | Desempleo nulo cuando n > s/a | conceptual_swap | high | Si $n_1 > s/a$, $r$ converge a $s/(n_1 b) > 0$ | Como $n_1 > s/a \Rightarrow s/(n_1 b) < a/b$, $r$ cruza $a/b$ en tiempo finito $t_1$ y luego decrece hacia cero por $\dot{r} = (s/a - n_1)r$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | La función de producción tiene isocuantas en ángulo recto con coeficientes fijos $a, b > 0$. | Impide la sustitución entre capital y trabajo, originando la rigidez del filo de navaja. | - |

---

### [Hab-04] Solución y Equilibrio Cobb-Douglas (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 13: Solución y Equilibrio Cobb-Douglas
- **Prerequisites:** C-05
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 13)

#### Description & Cognitive Model
Integra $\dot{K} = sK^a(L_0 e^{nt})^{1-a}$ para obtener $K(t) = [K_0^b - \frac{s}{n}L_0^b + \frac{s}{n}L_0^b e^{nbt}]^{1/b}$ con $b = 1 - a$, y calcula $r^* = (s/n)^{1/(1-a)}$ y $K/Y = s/n$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Exponente invertido en r* | skipped_step | high | $r^* = (s/n)^{1-a}$ | De $sr^a = nr$ se obtiene $r^{1-a} = s/n$, por lo que al despejar $r^*$ debe elevarse al exponente recíproco $1/(1 - a)$. |
| `D-Hab04-02` | Razón n/s en equilibrio | skipped_step | high | $r^* = (n/s)^{\frac{1}{1-a}}$ | Mayor tasa de ahorro $s$ y menor crecimiento laboral $n$ elevan $r^*$, por lo que la base correcta es $s/n$. |
| `D-Hab04-03` | Ingreso per cápita sin exponente a | conceptual_swap | high | $Y/L \to (s/n)^{1-a}$ | Como $Y/L = r^a$ y $r^* = (s/n)^{1/(1-a)}$, el producto por trabajador tiende a $(s/n)^{a/(1-a)}$. |
| `D-Hab04-04` | Coeficiente de capital invertido | conceptual_swap | high | $K/Y \to n/s$ | En equilibrio $sY = nK$, de modo que la razón capital-producto es $C = K/Y = s/n$ y se cumple $n = s/C$. |
| `D-Hab04-05` | Olvida condición inicial en K(t) | conceptual_swap | high | $K(t) = [(s/n)L_0^b e^{nbt}]^{1/b}$ | La integración exacta desde $K(0) = K_0$ requiere incluir $K_0^b - (s/n)L_0^b$ para satisfacer la condición inicial. |
| `D-Hab04-06` | Exponente b incorrecto en integración | conceptual_swap | high | $b = a$ en $K(t)$ | La sustitución de Bernoulli usa $u = K^{1-a}$, por lo que $b = 1 - a$ y $\dot{u} = (1 - a)K^{-a}\dot{K}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | La elasticidad del producto respecto al capital satisface $0 < a < 1$. | Si $a \ge 1$, la curva $sr^a$ no cruza desde arriba a $nr$ y desaparece el equilibrio estable. | - |

---

### [Hab-05] Umbral Crítico con Sustituibilidad Parcial (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 14: Umbral Crítico con Sustituibilidad Parcial
- **Prerequisites:** C-06
- **Recommended Modalities:** open_symbolic, adversarial_break, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 14)

#### Description & Cognitive Model
Analiza $\dot{r} = s(a\sqrt{r} + 1)^2 - nr$ para $Y = (a\sqrt{K} + \sqrt{L})^2$: determina el umbral $sa^2 \gtreqless n$ de no existencia o convergencia a $r^* = (1/(\sqrt{n/s} - a))^2$ e ingreso per cápita $1/(1 - a\sqrt{s/n})^2$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Umbral lineal en a | skipped_step | high | No hay equilibrio si $sa > n$ | Al expandir $s(a\sqrt{r} + 1)^2$, el coeficiente cuadrático que domina para $r$ grande es $sa^2$, por lo que el umbral es $sa^2 > n$. |
| `D-Hab05-02` | Invierte signo en r* | skipped_step | high | $r^* = (1/(\sqrt{n/s} + a))^2$ | Al agrupar $\sqrt{r}(\sqrt{n/s} - a) = 1$, el término $a$ pasa restando al denominador: $r^* = (1/(\sqrt{n/s} - a))^2$. |
| `D-Hab05-03` | Olvida elevar al cuadrado r* | conceptual_swap | high | $r^* = 1/(\sqrt{n/s} - a)$ | La ecuación linealizada resuelve para $\sqrt{r^*}$, por lo que debe elevarse al cuadrado para obtener $r^*$. |
| `D-Hab05-04` | Altura inicial nula en r = 0 | conceptual_swap | high | $sF(0, 1) = 0$ | En esta función es posible producir solo con trabajo ($K = 0$), de modo que la ordenada al origen de $sF(r, 1)$ es $s > 0$. |
| `D-Hab05-05` | Ingreso per cápita erróneo | conceptual_swap | high | $\lim Y/L = 1/(1 - a\sqrt{n/s})^2$ | Sustituyendo $r^* = (1/(\sqrt{n/s} - a))^2$ en $(a\sqrt{r^*} + 1)^2$ resulta $1/(1 - a\sqrt{s/n})^2$. |
| `D-Hab05-06` | Condición de equilibrio invertida | conceptual_swap | high | Si $sa^2 > n$, converge a $r^*$ | Si $sa^2 > n$, la curva $s(a\sqrt{r} + 1)^2$ crece más rápido que $nr$ y permanece por encima, haciendo que $r \to \infty$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | El parámetro de la familia $(aK^p + L^p)^{1/p}$ cumple $0 < p < 1$ (aquí $p = 1/2$) y $a > 0$. | Garantiza isocuantas con convexidad estándar y rendimientos marginales decrecientes. | - |

---

### [C-07] Precios Competitivos de los Factores y Arbitraje (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 16: Precios Competitivos de los Factores
- **Prerequisites:** C-04
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 16)

#### Description & Cognitive Model
Determinación competitiva del salario real $\frac{\partial F}{\partial L} = \frac{w}{p}$ y la renta real del capital $\frac{\partial F}{\partial K} = \frac{q}{p}$ que bajo rendimientos constantes solo dependen de $r = K/L$, junto con la condición de arbitraje $i(t) = q(t)/p(t) + \dot{p}(t)/p(t)$.

#### Fused Distractor Models (7)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Dependencia de la escala absoluta | conceptual_swap | high | $\partial F/\partial K$ depende de $K$ y $L$ por separado | Por el teorema de Euler para funciones homogéneas de grado 1, las derivadas parciales son homogéneas de grado 0 y solo dependen de $r = K/L$. |
| `D-C07-04` | Iguala tasa nominal y real | conceptual_swap | high | $i(t)=q(t)/p(t)$ siempre | Incluya la ganancia o pérdida de capital $\dot{p}(t)/p(t)$ en la condición de arbitraje entre dinero y capital físico. |
| `D-C07-02` | Confusión entre salario nominal y real | conceptual_swap | high | $\partial F/\partial L = w$ | La productividad marginal física del trabajo iguala al salario real $w/p$, ya que el nivel absoluto de precios $p(t)$ queda indeterminado en el sistema real. |
| `D-C07-05` | Signo invertido en inflación | conceptual_swap | high | $i(t)=q(t)/p(t)-\dot{p}(t)/p(t)$ | Verifique que una caída de precios ($\dot{p}<0$) exige una renta propia $q/p$ mayor que $i$ para inducir la tenencia de capital. |
| `D-C07-03` | Oferta elástica a corto plazo | conceptual_swap | high | El capital preexistente se ajusta elásticamente al alquiler $q/p$ | En cada instante, el stock de capital acumulado $K$ y la fuerza laboral $L$ se ofrecen inelásticamente, ajustándose $w/p$ y $q/p$ para vaciar los mercados. |
| `D-C07-06` | Confunde producto medio y marginal | conceptual_swap | high | $w/p=Y/L$ y $q/p=Y/K$ | Aplique las ecuaciones de productividad marginal $\partial F/\partial L$ y $\partial F/\partial K$, pues los factores reciben su aporte marginal. |
| `D-C07-07` | Determina nivel absoluto | conceptual_swap | high | El modelo real fija $p(t)$ | Recuerde que en un sistema puramente real sin ecuación monetaria el nivel absoluto de precios $p(t)$ queda indeterminado. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Los mercados de factores son competitivos y $w/p$, $q/p$ se ajustan instantáneamente. | Sin ajuste instantáneo de precios reales o con rigideces keynesianas puede surgir desempleo. | - |
| `A-C07-02` | - | Competencia perfecta y rendimientos constantes a escala en $F(K,L)$ | Sin competencia ni homogeneidad de grado 1, las productividades marginales no agotan el producto ni dependen solo de $r$. | - |
| `A-C07-03` | - | Previsión perfecta, ausencia de riesgo y arbitraje sin fricciones | Con incertidumbre o preferencias por liquidez, $p(t)$ no iguala el valor presente descontado de rentas futuras. | - |

---

### [C-09] Isocuantas y Razón Salario-Renta (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 19: Isocuantas y Razón Salario-Renta
- **Prerequisites:** C-07
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 19)

#### Description & Cognitive Model
Trayectorias de crecimiento en el mapa de isocuantas de $F(K,L)$, constancia de $w/q$ sobre rayos $K=rL$ e indeterminación en proporciones fijas

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Caída indefinida del salario | conceptual_swap | high | El salario real cae sin límite hacia $r^*$ | Distinga el ajuste finito hacia el equilibrio estable $r^*$ de la posición de Harrod, pues $w/q$ converge a un límite finito. |
| `D-C09-02` | Precios determinados en esquina | conceptual_swap | high | $w$ y $q$ únicos en $r=a/b$ en Harrod-Domar | Recuerde que en proporciones fijas solo $aq+bw=p$ restringe los precios en $r=a/b$, siendo indeterminados dentro de esa recta. |
| `D-C09-03` | Pendiente varía en el rayo | conceptual_swap | high | La relación $w/q$ cambia a lo largo de un rayo $K=rL$ | Use los rendimientos constantes a escala: las isocuantas son homotéticas y mantienen pendiente y razón $w/q$ constantes sobre cada rayo. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | Isocuantas convexas y diferenciables en el caso neoclásico frente a esquinas en Harrod-Domar | Si las isocuantas tienen esquinas en $r=a/b$, el factor excedente recibe productividad marginal nula y precio cero. | - |

---

### [Hab-06] Participación Factorial en Equilibrio (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 21: Participación Factorial en Equilibrio
- **Prerequisites:** C-07, C-09
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 21)

#### Description & Cognitive Model
Cálculo de $w/p$, $q/p$ y participación laboral $(w/p)(L/Y)$ en equilibrio para Cobb-Douglas $Y=K^aL^{1-a}$ y para $Y=(a\sqrt{K}+\sqrt{L})^2$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Participación constante universal | skipped_step | high | $(w/p)(L/Y)$ es independiente de $s$ y $n$ siempre | Evalúe $(w/p)(L/Y)=1-a\sqrt{s/n}$ en el tercer ejemplo: solo bajo Cobb-Douglas la participación laboral es invariante ante $s$ y $n$. |
| `D-Hab06-02` | Invierte efecto de n | skipped_step | high | Mayor $n$ reduce la participación laboral en $Y=(a\sqrt{K}+\sqrt{L})^2$ | Calcule el cociente $(w/p)/(Y/L)=1-a\sqrt{s/n}$: al subir $n$ cae $s/n$, sube la participación del trabajo aunque caiga $w/p$. |
| `D-Hab06-03` | Exponente erróneo en salario | conceptual_swap | high | $w/p=(1-a)(s/n)^{1/(1-a)}$ en Cobb-Douglas | Sustituya $r^*=(s/n)^{1/(1-a)}$ en $w/p=(1-a)r^a$ multiplicando los exponentes para obtener $(1-a)(s/n)^{a/(1-a)}$. |
| `D-Hab06-04` | Omite factor a en renta | conceptual_swap | high | $q/p=n/s$ en equilibrio Cobb-Douglas | Evalúe $q/p=a(r^*)^{a-1}=a(s/n)^{-1}=an/s$, conservando la participación del capital $a$ en la renta real. |
| `D-Hab06-05` | Derivada incompleta | conceptual_swap | high | $\partial Y/\partial L=a\sqrt{r}$ en $Y=(a\sqrt{K}+\sqrt{L})^2$ | Aplique la regla de la cadena a $(a\sqrt{K}+\sqrt{L})^2$ respecto a $L$: $\partial Y/\partial L=a\sqrt{K/L}+1=a\sqrt{r}+1$. |
| `D-Hab06-06` | Confunde w/q con w/p | conceptual_swap | high | $w/q=\frac{1-a}{a}r^{a}$ en Cobb-Douglas | Divida $(1-a)r^a$ entre $ar^{a-1}$ simplificando las potencias de $r$ para obtener la relación lineal $w/q=\frac{1-a}{a}r$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Parámetros $a\in(0,1)$ y condición de equilibrio $\sqrt{n/s}>a$ en el tercer ejemplo | Si $\sqrt{n/s}\le a$, no existe razón capital-trabajo estacionaria finita y la fórmula de participación diverge. | - |

---

### [Hab-07] Progreso Técnico Neutral (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 22: Progreso Técnico Neutral
- **Prerequisites:** C-07
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 22)

#### Description & Cognitive Model
Resolución de $\dot{K}=se^{gt}K^a(L_0e^{nt})^{1-a}$ con $b=1-a$ y derivación de tasas asintóticas de crecimiento para $K$, $Y$ y $K/L$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Omite efecto directo de A(t) | skipped_step | high | $\dot{Y}/Y$ converge a $n+ag/b$ y $K/Y$ crece a tasa $g$ | Derive $\ln Y=gt+a\ln K+(1-a)\ln L$ sumando el término directo $g$ a $a(n+g/b)+bn$, obteniendo $n+g/b$ y $K/Y$ constante. |
| `D-Hab07-02` | Supone r estacionario | skipped_step | high | $K/L$ converge a un valor constante con $g>0$ | Observe que la mayor capacidad de ahorro eleva $K$ más rápido que $L$, haciendo crecer $K/L$ asintóticamente a tasa $g/(1-a)$. |
| `D-Hab07-03` | Tasa errónea en K | conceptual_swap | high | El capital crece a tasa $n+g$ en el largo plazo | Tome la raíz $1/b$ del término dominante $e^{(nb+g)t}$ en la solución de $K(t)$ para obtener la tasa relativa $(nb+g)/b=n+g/b$. |
| `D-Hab07-04` | Participación laboral creciente | conceptual_swap | high | La participación del trabajo sube al crecer $K/L$ | Recuerde que en Cobb-Douglas el salario real crece ilimitadamente con $K/L$, pero la participación laboral permanece fija en $1-a$. |
| `D-Hab07-05` | Exponente sin b en solución | conceptual_swap | high | $K(t)$ tiene exponente $e^{(n+g)t}$ dentro del corchete | Multiplique por $b=1-a$ al integrar $K^{-a}\dot{K}$, lo que transforma la tasa exponencial en $(n(1-a)+g)t=(nb+g)t$. |
| `D-Hab07-06` | Descuenta n al restar | conceptual_swap | high | $K/L$ crece a tasa $n+g/b$ | Reste la tasa de crecimiento poblacional $n$ de la tasa del capital $n+g/b$ para hallar la tasa asintótica de $K/L$, igual a $g/b$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Progreso técnico neutral multiplicativo $A(t)=e^{gt}$ y función Cobb-Douglas con $a\in(0,1)$ | Si el progreso técnico no es neutral o $a\ge 1$, no se obtiene la forma cerrada de Bernoulli para $K(t)$. | - |

---

### [C-10] Oferta de Trabajo Elástica (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 24: Oferta de Trabajo Elástica
- **Prerequisites:** C-07
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 24)

#### Description & Cognitive Model
Extensión de la ecuación de acumulación con oferta laboral $L=G(t,w/p)$ y condición de invariancia de $r^*$ bajo elasticidad constante $L=L_0e^{nt}(w/p)^h$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C10-01` | Elasticidad altera r* siempre | conceptual_swap | high | Toda oferta laboral elástica cambia el equilibrio $r^*$ | Note que en el equilibrio $\dot{r}=0$ se cumple $\dot{w}=0$, por lo que $r^*$ solo cambia si $(1/G)(\partial G/\partial t)\neq n$. |
| `D-C10-02` | Crecimiento distinto a n | conceptual_swap | high | Con $L=L_0e^{nt}(w/p)^h$, $K$ e $Y$ crecen a tasa $n+h$ | Recuerde que en el estado estacionario $r$ y $w/p$ son constantes, por lo que $L$, $K$ e $Y$ crecen exactamente a la tasa $n$. |
| `D-C10-03` | Desestabiliza el equilibrio | conceptual_swap | high | La elasticidad $h>0$ vuelve inestable al equilibrio | Verifique que para $a,h,r>0$ el factor de ajuste es positivo, preservando la estabilidad hacia el mismo equilibrio $r^*$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C10-01` | - | Nivel de precios $p$ constante y oferta laboral $L=G(t,w/p)$ diferenciable sin cota superior | Si existe un máximo demográfico de trabajo disponible, la curva de elasticidad constante falla para salarios reales muy altos. | - |

---

### [Hab-08] Ahorro Variable y Política Fiscal (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 26: Ahorro Variable y Política Fiscal
- **Prerequisites:** C-09
- **Recommended Modalities:** fill_in_the_blank, open_symbolic, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 26)

#### Description & Cognitive Model
Dinámica con tasa de ahorro variable $\dot{r}=s(r)F(r,1)-nr$ (estabilización al anularse $s(r)$) y efecto de impuesto proporcional $t$ con fracción invertida $v$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | Estado estacionario clásico | skipped_step | high | Si $s(r)=0$ para $r$ alto, $K$ y $L$ se detienen | Distinga el cese de inversión neta del estado estacionario clásico: como $L$ sigue creciendo a tasa $n$, $r$ cae y reactiva el ahorro. |
| `D-Hab08-02` | Impuesto siempre reduce ahorro | skipped_step | high | Un impuesto $t$ baja la tasa de ahorro a $s(1-t)$ siempre | Aplique la fórmula general $s_{\text{eff}}=s+(v-s)t$: el ahorro efectivo aumenta si la fracción pública invertida $v$ supera a $s$. |
| `D-Hab08-03` | Error algebraico en $s_eff$ | conceptual_swap | high | $s_{\text{eff}}=s(1-t)+vt=s+vt$ | Distribuya correctamente $s(1-t)+vt=s-st+vt=s+(v-s)t$ para comparar la propensión pública $v$ frente a la privada $s$. |
| `D-Hab08-04` | Signo de s'(r) invertido | conceptual_swap | high | El ahorro $s(r)$ crece al subir la razón capital-trabajo $r$ | Recuerde que un mayor $r$ reduce el rendimiento real del capital $q/p$, por lo que bajo $s$ creciente en el rendimiento, $s(r)$ decrece. |
| `D-Hab08-05` | Permite fuga indefinida | conceptual_swap | high | Aunque $s(r)\to 0$ para $r$ grande, $r\to\infty$ es posible | Observe que si $s(r)$ se anula para $r$ grande, $s(r)F(r,1)$ queda bajo $nr$ y la última intersección es necesariamente estable. |
| `D-Hab08-06` | Efecto unidireccional en r* | conceptual_swap | high | Sustituir $s$ por $s(r)$ siempre aumenta (o siempre baja) $r^*$ | Compare la curva variable con la constante en el punto de cruce: el nuevo $r^*$ puede ser mayor o menor según dónde cruce a $nr$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab08-01` | - | Tasa de ahorro decreciente en $r$ ($s'(r)<0$) e impuesto proporcional $t\in(0,1)$ con fracción invertida $v\in[0,1]$ | Si el impuesto es no proporcional o $s(r)$ es creciente en $r$, se alteran la estabilidad y el desplazamiento uniforme de $sF(r,1)$. | - |

---

### [C-11] Población Endógena y Trampas (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 27: Población Endógena y Trampas
- **Prerequisites:** C-09
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 27)

#### Description & Cognitive Model
Endogeneización de la tasa demográfica $n(r)$ en $\dot{r}=sF(r,1)-n(r)r$ generando equilibrios múltiples: estancamiento estable $r_1$ y umbral inestable $r_2$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C11-01` | Invierte estabilidad de r1 y r2 | conceptual_swap | high | $r_1$ es umbral inestable y $r_2$ es equilibrio estable | Verifique el signo de $\dot{r}=sF(r,1)-n(r)r$: debajo de $r_2$ la curva $n(r)r$ supera a $sF(r,1)$, empujando el sistema de vuelta a $r_1$. |
| `D-C11-02` | Requiere rendimientos crecientes | conceptual_swap | high | Las trampas de pobreza exigen indivisibilidades o $F$ no CRS | Observe que la interacción entre $F(r,1)$ con rendimientos constantes y $n(r)$ no monótona basta para generar un umbral crítico $r_2$. |
| `D-C11-03` | Cualquier ahorro rompe r1 | conceptual_swap | high | Una pequeña acumulación inicial desde $r_1$ lleva a crecimiento sostenido | Distinga entre un impulso menor a $r_2$ (que revierte a $r_1$) y un gran impulso de inversión capaz de superar el umbral inestable $r_2$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C11-01` | - | Tasa demográfica $n(r)$ dependiente del ingreso per cápita $F(r,1)$ con subida inicial y caída a ingresos altos | Si $n(r)$ es constante o estrictamente monótona, desaparece la intersección múltiple y no hay trampa de equilibrio bajo. | - |

---

### [C-12] Rigidez Salarial y Liquidez (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 29: Rigidez Salarial y Liquidez
- **Prerequisites:** C-07, C-09
- **Recommended Modalities:** adversarial_break, multiple_select, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 29)

#### Description & Cognitive Model
Obstáculos al pleno empleo: salario real rígido $\bar{w}/p$ que fija $r=\bar{r}$ con $\dot{L}/L=(s/\bar{r})F(\bar{r},1)$ y trampa de liquidez en $\bar{M}=Q(Y,q/p)$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C12-01` | Rigidez salarial fija el empleo | conceptual_swap | high | Con $\bar{w}/p$ fijo, el nivel de empleo $L$ permanece constante | Note que $K$ sigue creciendo por ahorro, de modo que $L=K/\bar{r}$ crece exponencialmente a tasa $(s/\bar{r})F(\bar{r},1)$, generando desempleo solo si es menor que $n$. |
| `D-C12-02` | Signo erróneo de desempleo | conceptual_swap | high | Si $(s/\bar{r})F(\bar{r},1)>n$, surge desempleo creciente | Compare la tasa de demanda de empleo $(s/\bar{r})F(\bar{r},1)$ con el crecimiento demográfico $n$: si la supera, hay escasez de trabajo, no desempleo. |
| `D-C12-03` | Modelo real basta para liquidez | conceptual_swap | high | La trampa de liquidez se resuelve sin dinámica monetaria | Reconozca la conclusión de Solow: al elegir entre efectivo y capital físico, el precio del bien compuesto y los factores monetarios se vuelven esenciales. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C12-01` | - | Salario real rígido en $\bar{w}/p$ o demanda de saldos ociosos infinitamente elástica a tasa positiva | Con precios y salarios perfectamente flexibles sin trampa de liquidez, el mercado laboral y de capital se vacían continuamente. | - |

---
