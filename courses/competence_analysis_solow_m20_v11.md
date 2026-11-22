# Cognitive Task Analysis (CTA): Solow M20 V11

- **Course ID:** `solow_m20_v11`
- **Macro-Competency:** Dominio y aplicación analítica integral de Solow M20 V11
- **Structure:** 20 total competencies (1 Facts, 11 Concepts, 8 Skills) with 89 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Función de Producción Neoclásica y Forma Intensiva | Concept | Evaluate | Unidad 2: Función de Producción Neoclásica y Forma Intensiva | - | 4 |
| `Hab-01` | Derivación de la Ecuación Fundamental de Solow | Skill | Evaluate | Unidad 3: Derivación de la Ecuación Fundamental de Solow | C-01 | 6 |
| `C-02` | Análisis Cualitativo-Gráfico y Estabilidad del Estado Uniforme | Concept | Evaluate | Unidad 3: Análisis Cualitativo-Gráfico y Estabilidad del Estado Uniforme | Hab-01 | 4 |
| `C-03` | Progreso Tecnológico y Desplazamiento del Estado Uniforme | Concept | Analyze | Unidad 4: Progreso Tecnológico y Desplazamiento del Estado Uniforme | C-02 | 3 |
| `Hab-02` | Solución Cuantitativa Cobb-Douglas y Trayectoria Temporal | Skill | Evaluate | Unidad 5: Solución Cuantitativa Cobb-Douglas y Trayectoria Temporal | Hab-01, C-02 | 6 |
| `H-01` | Acumulación y Oferta Laboral | Fact | Understand | Unidad 3: Acumulación y Oferta Laboral | - | 3 |
| `C-04` | Ecuación Fundamental de Solow | Concept | Evaluate | Unidad 6: Ecuación Fundamental de Solow | H-01, C-01 | 3 |
| `C-05` | Estabilidad del Estado Estacionario | Concept | Evaluate | Unidad 7: Estabilidad del Estado Estacionario | C-04 | 3 |
| `C-06` | Equilibrios Múltiples y Divergencia | Concept | Analyze | Unidad 8: Equilibrios Múltiples y Divergencia | C-05 | 3 |
| `Hab-03` | Dinámica de Proporciones Fijas | Skill | Evaluate | Unidad 10: Dinámica de Proporciones Fijas | C-04, C-05 | 6 |
| `Hab-04` | Solución Explícita Cobb-Douglas | Skill | Evaluate | Unidad 13: Solución Explícita Cobb-Douglas | C-04, C-05 | 6 |
| `Hab-05` | Modelo con Sustitución p=1/2 | Skill | Evaluate | Unidad 14: Modelo con Sustitución p=1/2 | C-04, C-05 | 6 |
| `C-07` | Precios Competitivos y Productividad Marginal | Concept | Analyze | Unidad 16: Precios Competitivos y Productividad | H-01, C-04 | 6 |
| `Hab-06` | Arbitraje y Tasa Propia de Capital | Skill | Evaluate | Unidad 17: Arbitraje y Tasa Propia de Capital | C-07 | 6 |
| `C-09` | Distribución Factorial: Proporciones Fijas vs. Sustitución | Concept | Analyze | Unidad 20: Distribución Factorial: Proporciones Fijas vs. Sustitución | C-07 | 3 |
| `Hab-07` | Crecimiento con Progreso Tecnológico Neutral | Skill | Evaluate | Unidad 22: Crecimiento con Progreso Tecnológico Neutral | C-07 | 6 |
| `C-10` | Oferta Elástica de Trabajo y Equilibrio | Concept | Analyze | Unidad 24: Oferta Elástica de Trabajo y Equilibrio | C-07 | 3 |
| `Hab-08` | Tasa de Ahorro Variable e Impuesto a la Renta | Skill | Analyze | Unidad 26: Tasa de Ahorro Variable e Impuesto a la Renta | C-07 | 6 |
| `C-11` | Crecimiento Poblacional Endógeno y Trampa de Equilibrio | Concept | Evaluate | Unidad 27: Crecimiento Poblacional Endógeno y Trampa de Equilibrio | C-07 | 3 |
| `C-12` | Rigidez Salarial y Preferencia por la Liquidez | Concept | Evaluate | Unidad 29: Rigidez Salarial y Preferencia por la Liquidez | C-07, Hab-06 | 3 |

---

## Detailed Competency Specifications

### [C-01] Función de Producción Neoclásica y Forma Intensiva (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 2: Función de Producción Neoclásica y Forma Intensiva
- **Prerequisites:** None
- **Recommended Modalities:** multiple_select, adversarial_break, concept_matching
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
Representación de la función de producción linealmente homogénea $Q = f(K, L) = L\phi(k)$ en términos de la relación capital-mano de obra $k \equiv K/L$, con $\phi'(k) > 0$ y $\phi''(k) < 0$.

#### Fused Distractor Models (4)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Proporción fija de factores | conceptual_swap | high | $Q = \rho K$ | Distinga el modelo de Domar de proporciones fijas del marco de Solow, donde capital y trabajo se combinan en proporciones variables. |
| `D-C01-02` | Retornos crecientes del capital | conceptual_swap | high | $\phi''(k) > 0$ | Verifique que $f_{KK} = \phi''(k)/L < 0$ implica rendimientos marginales decrecientes del capital y concavidad estricta de $\phi(k)$. |
| `D-C01-03` | Omite factor trabajo L | conceptual_swap | high | $Q = \phi(k)$ | Recuerde que la homogeneidad lineal permite factorizar $L$: $Q = L f(K/L, 1) = L\phi(k)$, donde $\phi(k)$ es el producto por trabajador. |
| `D-C01-04` | Producto marginal negativo | conceptual_swap | high | $\phi'(k) < 0$ | Relacione la identidad $f_K \equiv \mathrm{MPP}_K = \phi'(k)$ con el supuesto de productividad marginal positiva $f_K > 0$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Homogeneidad lineal $f(\theta K, \theta L) = \theta f(K, L)$ para $\theta > 0$ | Sin retornos constantes a escala no es posible reducir $Q = f(K,L)$ a la forma intensiva $L\phi(k)$. | - |
| `A-C01-02` | - | Productividad marginal positiva $f_K > 0, f_L > 0$ y decreciente $f_{KK} < 0, f_{LL} < 0$ | Si $f_{KK} \ge 0$, la curva $\phi(k)$ pierde concavidad y desaparece la convergencia única al equilibrio. | - |

---

### [Hab-01] Derivación de la Ecuación Fundamental de Solow (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Derivación de la Ecuación Fundamental de Solow
- **Prerequisites:** C-01
- **Recommended Modalities:** proof_dag, open_symbolic, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
Deducción de la ecuación diferencial fundamental $\dot{k} = s\phi(k) - \lambda k$ combinando $\dot{K} = sQ$, $\dot{L}/L = \lambda$ y la diferenciación temporal de $K = kL$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Omite regla del producto | skipped_step | high | $\dot{K} = L\dot{k}$ | Aplique la regla del producto al diferenciar $K = kL$ respecto al tiempo: $\dot{K} = L\dot{k} + k\dot{L}$, pues $L$ crece a tasa $\lambda$. |
| `D-Hab01-02` | Signo positivo en dilución | skipped_step | high | $\dot{k} = s\phi(k) + \lambda k$ | Despeje $L\dot{k}$ en $L\dot{k} + k\lambda L = sL\phi(k)$ restando $k\lambda L$ de ambos miembros para obtener el signo negativo. |
| `D-Hab01-03` | Conserva L en ecuación final | conceptual_swap | high | $\dot{k} = sL\phi(k) - \lambda k$ | Divida toda la igualdad $L\dot{k} + k\lambda L = sL\phi(k)$ entre el factor común $L > 0$ para eliminar $L$ en todos los términos. |
| `D-Hab01-04` | Confunde Q con k en ahorro | conceptual_swap | high | $\dot{k} = sk - \lambda k$ | Sustituya $Q$ por su forma intensiva $L\phi(k)$ antes de igualar con $L\dot{k} + k\lambda L$, manteniendo la función $\phi(k)$. |
| `D-Hab01-05` | Tasa de ahorro aplicada a k | conceptual_swap | high | $\dot{k} = s\phi(k) - s\lambda k$ | Separe las dos hipótesis dinámicas: $s$ multiplica únicamente al producto $Q = L\phi(k)$, mientras $\lambda$ proviene de $\dot{L}/L = \lambda$. |
| `D-Hab01-06` | Invierte tasa de crecimiento L | conceptual_swap | high | $\dot{k} = s\phi(k) - \frac{k}{\lambda}$ | Despeje correctamente $\dot{L} = \lambda L$ desde la definición de crecimiento exponencial $\dot{L}/L = \lambda$ antes de sustituir. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Propensión marginal al ahorro constante $s$ con $\dot{K} = sQ$ y $\dot{L}/L = \lambda > 0$ | Si $s$ o $\lambda$ varían endógenamente con el tiempo, la ecuación ya no es autónoma en $k$. | - |
| `A-Hab01-02` | - | Fuerza laboral estrictamente positiva $L(t) > 0$ en todo instante $t$ | Si $L = 0$, la relación $k \equiv K/L$ queda indefinida y no puede simplificarse el factor común $L$. | - |

---

### [C-02] Análisis Cualitativo-Gráfico y Estabilidad del Estado Uniforme (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Análisis Cualitativo-Gráfico y Estabilidad del Estado Uniforme
- **Prerequisites:** Hab-01
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
Análisis de la línea de fase $\dot{k} = s\phi(k) - \lambda k$ mediante la distancia vertical entre $s\phi(k)$ y $\lambda k$, identificando la intersección $\bar{k}$ como equilibrio estable de crecimiento uniforme.

#### Fused Distractor Models (4)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Confunde estado uniforme con estacionario | conceptual_swap | high | $\dot{K} = \dot{L} = \dot{Q} = 0$ en $\bar{k}$ | Distinga estado uniforme de estado estacionario: en $\bar{k}$ la razón $k = K/L$ es constante, pero $K$, $L$, $Q$ e inversión neta crecen a tasa $\lambda$. |
| `D-C02-02` | Pendiente positiva en equilibrio | conceptual_swap | high | $\frac{d\dot{k}}{dk} > 0$ implica estabilidad en $\bar{k}$ | Verifique en la línea de fase que la estabilidad requiere pendiente negativa en $\bar{k}$: si $k < \bar{k}$ entonces $\dot{k} > 0$, y si $k > \bar{k}$ entonces $\dot{k} < 0$. |
| `D-C02-03` | Curva s*phi(k) con ordenada positiva | conceptual_swap | high | $s\phi(0) > 0$ | Considere que el capital $K$ es un factor indispensable: si $K = 0$ entonces $k = 0$ y $Q = 0$, por lo que $s\phi(k)$ parte del origen. |
| `D-C02-04` | Equilibrio donde s*phi(k) es máximo | conceptual_swap | high | $\bar{k}$ ocurre cuando $s\phi'(k) = 0$ | Recuerde que el equilibrio $\bar{k}$ satisface $\dot{k} = 0$, es decir, la intersección donde $s\phi(\bar{k}) = \lambda\bar{k}$ y las dos curvas se cruzan. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | El capital es indispensable ($k = 0 \Rightarrow \phi(0) = 0$) y existe $k > 0$ con $s\phi(k) > \lambda k$ | Sin un intervalo donde $s\phi(k) > \lambda k$, las curvas no se intersecan en un nivel positivo $\bar{k}$. | - |

---

### [C-03] Progreso Tecnológico y Desplazamiento del Estado Uniforme (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 4: Progreso Tecnológico y Desplazamiento del Estado Uniforme
- **Prerequisites:** C-02
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
Incorporación del cambio tecnológico $Q = T(t)f(K, L)$ con $dT/dt > 0$, cuyo efecto multiplica el producto provocando un desplazamiento secular hacia arriba de $s\phi(k)$ y valores mayores de $\bar{k}$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Desplazamiento hacia abajo de s*phi(k) | conceptual_swap | high | $dT/dt > 0$ reduce $\bar{k}$ | Analice el término multiplicativo creciente $T(t)$: una cantidad fija de $K$ y $L$ genera más producto, desplazando $s\phi(k)$ hacia arriba y elevando $\bar{k}$. |
| `D-C03-02` | Giro del rayo lambda*k | conceptual_swap | high | $dT/dt > 0$ gira $\lambda k$ hacia arriba | Recuerde que la tecnología entra multiplicando la función de producción $T(t)f(K,L)$, por lo que altera $s\phi(k)$ sin modificar la pendiente $\lambda$ del rayo $\lambda k$. |
| `D-C03-03` | Tecnología constante en el tiempo | conceptual_swap | high | $dT/dt = 0$ genera sucesión creciente de $\bar{k}$ | Sin mejoramiento tecnológico ($dT/dt = 0$), la economía converge a un único $\bar{k}$ invariante en vez de una sucesión creciente de estados uniformes. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | Medición tecnológica creciente en el tiempo $T(t)$ con $dT/dt > 0$ | Si $dT/dt \le 0$, no hay desplazamiento secular ascendente de $s\phi(k)$ ni aumento sostenido de $\bar{k}$. | - |

---

### [Hab-02] Solución Cuantitativa Cobb-Douglas y Trayectoria Temporal (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Solución Cuantitativa Cobb-Douglas y Trayectoria Temporal
- **Prerequisites:** Hab-01, C-02
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 5)

#### Description & Cognitive Model
Resolución cuantitativa de $\dot{k} + \lambda k = sk^\alpha$ mediante la sustitución de Bernoulli $z = k^{1-\alpha}$ para obtener la trayectoria $k^{1-\alpha}(t)$ y su límite asintótico $\bar{k} = (s/\lambda)^{1/(1-\alpha)}$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Sustitución de Bernoulli incorrecta | skipped_step | high | $z = k^{\alpha}$ | En la ecuación de Bernoulli $\dot{k} + \lambda k = sk^\alpha$ con $m = \alpha$, aplique la sustitución estándar $z = k^{1-m} = k^{1-\alpha}$. |
| `D-Hab02-02` | Omite factor (1-alpha) al linealizar | skipped_step | high | $\frac{dz}{dt} + \lambda z = s$ | Al diferenciar $z = k^{1-\alpha}$, aparece el factor $(1-\alpha)$: la ecuación linealizada correcta es $\frac{dz}{dt} + (1-\alpha)\lambda z = (1-\alpha)s$. |
| `D-Hab02-03` | Invierte exponente en estado uniforme | conceptual_swap | high | $\bar{k} = \left(\frac{s}{\lambda}\right)^{1-\alpha}$ | Al tomar límite $t \to \infty$ resulta $k^{1-\alpha} \to s/\lambda$; eleve ambos lados a la potencia recíproca $1/(1-\alpha)$ para despejar $k$. |
| `D-Hab02-04` | Invierte razón s/lambda | conceptual_swap | high | $\bar{k} = \left(\frac{\lambda}{s}\right)^{\frac{1}{1-\alpha}}$ | Recuerde que en la solución lineal $b/a = \frac{(1-\alpha)s}{(1-\alpha)\lambda} = \frac{s}{\lambda}$, por lo que $\bar{k}$ varía directamente con $s$ e inversamente con $\lambda$. |
| `D-Hab02-05` | Exponente positivo en solución temporal | conceptual_swap | high | $e^{+(1-\alpha)\lambda t}$ | En $\frac{dz}{dt} + az = b$ con $a = (1-\alpha)\lambda > 0$, el término transitorio decae como $e^{-at} = e^{-(1-\alpha)\lambda t} \to 0$. |
| `D-Hab02-06` | Forma intensiva Cobb-Douglas errónea | conceptual_swap | high | $\phi(k) = k^{1-\alpha}$ | Factorice $L$ en $Q = K^\alpha L^{1-\alpha} = L(K/L)^\alpha = Lk^\alpha$, de modo que $\phi(k) = k^\alpha$ y no $k^{1-\alpha}$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Función Cobb-Douglas linealmente homogénea $Q = K^\alpha L^{1-\alpha}$ con $0 < \alpha < 1$ | Si $\alpha = 1$, $(1-\alpha) = 0$ y la transformación de Bernoulli $z = k^{1-\alpha}$ colapsa. | - |
| `A-Hab02-02` | - | Condición inicial positiva $k(0) > 0$ y tasa $\lambda > 0$ | Si $(1-\alpha)\lambda \le 0$, el término exponencial no converge a cero cuando $t \to \infty$. | - |

---

### [H-01] Acumulación y Oferta Laboral (Fact)

- **Bloom Level:** Understand
- **Session:** Unidad 3: Acumulación y Oferta Laboral
- **Prerequisites:** None
- **Recommended Modalities:** fill_in_the_blank, multiple_select, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 3)

#### Description & Cognitive Model
Identidad de acumulación $\dot{K}=sY$, función de producción con rendimientos constantes $Y=F(K,L)$ y fuerza laboral exógena $L(t)=L_0 e^{nt}$ bajo pleno empleo.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Ahorro sobre capital | conceptual_swap | high | $\dot{K}=sK$ | Aplique la tasa de ahorro $s$ sobre el producto neto $Y=F(K,L)$ y no sobre el stock de capital $K$. |
| `D-H01-02` | Crecimiento lineal laboral | conceptual_swap | high | $L(t)=L_0(1+nt)$ | Recuerde que la fuerza laboral crece a una tasa relativa constante $n$, lo que implica trayectoria exponencial $L_0 e^{nt}$. |
| `D-H01-03` | Rendimientos decrecientes totales | conceptual_swap | high | $F(\lambda K,\lambda L)<\lambda Y$ | En ausencia de tierra escasa no aumentable, la función de producción es homogénea de grado uno con rendimientos constantes. |

---

### [C-04] Ecuación Fundamental de Solow (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 6: Ecuación Fundamental de Solow
- **Prerequisites:** H-01, C-01
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 6)

#### Description & Cognitive Model
Derivación e interpretación de la ecuación diferencial de la razón capital-trabajo $\dot{r}=sF(r,1)-nr$ a partir de $r=K/L$ y homogeneidad de grado uno.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Omite dilución laboral | conceptual_swap | high | $\dot{r}=sF(r,1)$ | Al diferenciar $r=K/L$, reste el término de dilución $nr$ que refleja el crecimiento exponencial de la fuerza laboral. |
| `D-C04-02` | Signo invertido en tasa | conceptual_swap | high | $\dot{r}=nr-sF(r,1)$ | Calcule $\dot{r}/r=\dot{K}/K-\dot{L}/L$: el incremento de capital entra positivo y el crecimiento laboral $n$ entra restando. |
| `D-C04-03` | No divide por L | conceptual_swap | high | $\dot{r}=sF(K,L)-nr$ | Aplique los rendimientos constantes a escala para factorizar $L$ y expresar el producto por trabajador como $F(r,1)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | La función $F(K,L)$ es homogénea de primer grado. | Sin homogeneidad de grado uno no se elimina $L$ para obtener $\dot{r}=sF(r,1)-nr$. | - |

---

### [C-05] Estabilidad del Estado Estacionario (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 7: Estabilidad del Estado Estacionario
- **Prerequisites:** C-04
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 7)

#### Description & Cognitive Model
Análisis gráfico de la intersección $nr=sF(r,1)$ en la Figura I: convergencia asintótica estable hacia $r^*$ con crecimiento balanceado a tasa natural $n$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Equilibrio inestable | conceptual_swap | high | $\dot{r}>0$ si $r>r^*$ | Observe en la Figura I que para $r>r^*$ el rayo $nr$ supera a $sF(r,1)$, por lo que $\dot{r}<0$ y $r$ decrece hacia $r^*$. |
| `D-C05-02` | Crecimiento exponencial exacto | conceptual_swap | high | $K(t)=K_0 e^{nt}$ siempre | Distinga la transición del estado estacionario: si $r<r^*$, el capital y el producto crecen más rápido que $n$ hasta converger. |
| `D-C05-03` | Ignora trampa en origen | conceptual_swap | high | $r>0$ desde $K=0$ | Note que si $K=0$ y ambos insumos son esenciales, no hay producto ni acumulación y el sistema permanece estancado en $r=0$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Productividad marginal decreciente del capital y $F(0,1)=0$. | Sin concavidad estricta de $F(r,1)$ pueden surgir equilibrios múltiples o ausencia de equilibrio. | - |

---

### [C-06] Equilibrios Múltiples y Divergencia (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 8: Equilibrios Múltiples y Divergencia
- **Prerequisites:** C-05
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 8)

#### Description & Cognitive Model
Clasificación de estabilidad local en configuraciones no estándar: equilibrios estables ($r_1,r_3$) frente a inestable ($r_2$) en Figura II y ausencia de equilibrio en Figura III.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Confunde estabilidad de r2 | conceptual_swap | high | $r_2$ es atractor estable | Verifique el signo de $\dot{r}$ alrededor de $r_2$: a su izquierda $nr>sF(r,1)$ y a su derecha $sF(r,1)>nr$, luego cualquier desvío se amplifica. |
| `D-C06-02` | Origen como equilibrio | conceptual_swap | high | $r=0$ es equilibrio en Fig. II | En la Figura II la producción es posible sin capital ($F(0,1)>0$), por lo que $sF(0,1)>0$ impide que el origen sea equilibrio. |
| `D-C06-03` | Ingreso cae en Fig. III inferior | conceptual_swap | high | $Y(t)$ decrece cuando $s_2 F^2 < nr$ | Aunque el ingreso per cápita disminuya continuamente cuando $s_2 F^2(r,1)<nr$, la inversión neta positiva y $L$ creciente hacen subir $Y$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | La curva $sF(r,1)$ puede cruzar $nr$ múltiples veces o ninguna. | Si se restringe a Inada estrictas, se excluyen las dinámicas de las Figuras II y III. | - |

---

### [Hab-03] Dinámica de Proporciones Fijas (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 10: Dinámica de Proporciones Fijas
- **Prerequisites:** C-04, C-05
- **Recommended Modalities:** open_symbolic, unstructured_model, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 10)

#### Description & Cognitive Model
Resolución explícita de $\dot{r}=s\min(r/a,1/b)-nr$ en el caso Harrod-Domar para los regímenes $n_1>s/a$, $n_2=s/a$ y $n_3<s/a$, identificando redundancia de factores.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Invierte umbral a/b | skipped_step | high | $r<b/a \Rightarrow \dot{r}=(s/a-n)r$ | Iguale los argumentos de $\min(r/a,1/b)$: el cambio de régimen ocurre exactamente cuando la razón capital-trabajo alcanza $r=a/b$. |
| `D-Hab03-02` | Redundancia invertida en n1 | skipped_step | high | $n_1>s/a \Rightarrow$ exceso de capital | Cuando la tasa natural $n_1$ supera a la garantizada $s/a$, $r$ cae por debajo de $a/b$ y el factor redundante es el trabajo. |
| `D-Hab03-03` | Proporción de capital empleada | conceptual_swap | high | Empleo de capital $bn_3/s$ | En el equilibrio $r^*=s/(n_3 b)$, el capital necesario por trabajador es $a/b$, luego la fracción empleada es $(a/b)/r^*=an_3/s$. |
| `D-Hab03-04` | Equilibrio único con n2 | conceptual_swap | high | $n_2=s/a \Rightarrow r \to a/b$ siempre | Si $n_2=s/a$ y $r_0<a/b$, entonces $\dot{r}=(s/a-n_2)r=0$: el sistema queda en equilibrio neutro preservando el desempleo inicial. |
| `D-Hab03-05` | Solución exponencial errónea | conceptual_swap | high | $r(t)=r_0 e^{(s/b-n_1)t}$ para $r_0>a/b$ | Para $r>a/b$ la ecuación es $\dot{r}=s/b-n_1 r$, cuya solución incluye término constante $s/(n_1 b)$ más decaimiento exponencial. |
| `D-Hab03-06` | Empleo cuando capital limita | conceptual_swap | high | Empleo $= aK/b$ | Cuando el capital es el cuello de botella, el producto es $Y=K/a$ y cada unidad de producto requiere $b$ trabajadores, dando $bK/a$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | Coeficientes fijos $a>0$ y $b>0$ sin sustitución entre factores. | Si existe sustitución suave, desaparece el filo de la navaja y la redundancia rígida. | - |

---

### [Hab-04] Solución Explícita Cobb-Douglas (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 13: Solución Explícita Cobb-Douglas
- **Prerequisites:** C-04, C-05
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 13)

#### Description & Cognitive Model
Integración directa de $\dot{K}=sK^a(L_0 e^{nt})^{1-a}$ y cálculo de la razón de equilibrio $r^*=(s/n)^{1/(1-a)}$, producto per cápita $(s/n)^{a/(1-a)}$ y coeficiente $C=s/n$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Exponente sin invertir | skipped_step | high | $r^*=(s/n)^{1-a}$ | Al resolver $sr^a=nr$, se obtiene $r^{1-a}=s/n$, por lo que debe elevar ambos miembros al recíproco $1/(1-a)$. |
| `D-Hab04-02` | Invierte razón s/n | skipped_step | high | $r^*=(n/s)^{\frac{1}{1-a}}$ | Mayor tasa de ahorro $s$ y menor crecimiento laboral $n$ elevan el capital por trabajador de equilibrio, por lo que la razón es $s/n$. |
| `D-Hab04-03` | Error en ingreso per cápita | conceptual_swap | high | $(Y/L)^*=(s/n)^{\frac{1}{1-a}}$ | Sustituya $r^*$ en $Y/L=r^a$: el exponente del ingreso per cápita de estado estacionario es $a/(1-a)$, no $1/(1-a)$. |
| `D-Hab04-04` | Coeficiente de capital invertido | conceptual_swap | high | $C=K/Y=n/s$ | Divida $r^*=(s/n)^{1/b}$ entre $(Y/L)^*=(s/n)^{a/b}$ para obtener $K/Y=(s/n)^{(1-a)/b}=s/n$, verificando $n=s/C$. |
| `D-Hab04-05` | Omite condición inicial en K(t) | conceptual_swap | high | $K(t)=[(s/n)L_0^b e^{nbt}]^{1/b}$ | Al integrar la ecuación de Bernoulli $\dot{K}=sK^a(L_0 e^{nt})^b$, incluya la constante de integración determinada por $K(0)=K_0$. |
| `D-Hab04-06` | Exponente erróneo en $L_0$ | conceptual_swap | high | $K(t)$ usa $L_0^a$ en vez de $L_0^b$ | Como $L(t)$ aparece elevado a $1-a=b$ en la ecuación diferencial, el factor constante en la integral lleva exponente $b=1-a$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Elasticidad del capital $a\in(0,1)$ estrictamente menor que uno. | Si $a=1$ la función es lineal en $K$ y no cruza el rayo $nr$ cuando $s>n$. | - |

---

### [Hab-05] Modelo con Sustitución p=1/2 (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 14: Modelo con Sustitución p=1/2
- **Prerequisites:** C-04, C-05
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 14)

#### Description & Cognitive Model
Análisis de la función $Y=(a\sqrt{K}+\sqrt{L})^2$ mediante $\dot{r}=s(a\sqrt{r}+1)^2-nr$, condición de existencia $sa^2<n$ y cálculo del equilibrio $r^*=(1/(\sqrt{n/s}-a))^2$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Umbral de existencia invertido | skipped_step | high | $sa^2>n$ implica equilibrio estable | Si $sa^2>n$, el coeficiente cuadrático $(a^2-n/s)$ es positivo y $sF(r,1)$ crece más rápido que $nr$, impidiendo intersección. |
| `D-Hab05-02` | Olvida elevar al cuadrado r* | skipped_step | high | $r^*=1/(\sqrt{n/s}-a)$ | Tras resolver $a\sqrt{r^*}+1=\sqrt{n/s}\sqrt{r^*}$, debe elevar ambos miembros al cuadrado para obtener $r^*$ y no $\sqrt{r^*}$. |
| `D-Hab05-03` | Signo erróneo en denominador | conceptual_swap | high | $r^*=(1/(\sqrt{n/s}+a))^2$ | Agrupe los términos con $\sqrt{r}$ en $\sqrt{s}(a\sqrt{r}+1)=\sqrt{nr}$: al pasar $a\sqrt{r}$ al otro lado, aparece $\sqrt{n/s}-a$. |
| `D-Hab05-04` | Intercepto cero en sF(r,1) | conceptual_swap | high | $sF(0,1)=0$ | En esta familia la producción es posible sin capital ($F(0,1)=1$), por lo que la curva $sF(r,1)$ inicia a altura $s>0$ en $r=0$. |
| `D-Hab05-05` | Error en ingreso per cápita límite | conceptual_swap | high | $(Y/L)^*=1/(1-a\sqrt{n/s})^2$ | Sustituya $\sqrt{r^*}=1/(\sqrt{n/s}-a)$ en $Y/L=(a\sqrt{r}+1)^2$: simplificando el cociente se obtiene $1/(1-a\sqrt{s/n})^2$. |
| `D-Hab05-06` | Factorización errónea de $r_dot$ | conceptual_swap | high | $\dot{r}=s(A\sqrt{r}-1)(B\sqrt{r}-1)$ | Como el término independiente es $+1$ y el lineal es $+2a\sqrt{r}$, los factores son $(A\sqrt{r}+1)(B\sqrt{r}+1)$ con $A=a-\sqrt{n/s}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | Parámetro de sustitución $0<p<1$ (aquí $p=1/2$) y $sa^2<n$. | Si $p>1$ las isocuantas pierden convexidad; si $sa^2\ge n$ el sistema crece sin equilibrio. | - |

---

### [C-07] Precios Competitivos y Productividad Marginal (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 16: Precios Competitivos y Productividad
- **Prerequisites:** H-01, C-04
- **Recommended Modalities:** proof_dag, multiple_select, adversarial_break, invariant_canvas
- **Evidence Citations:** `solow1956.pdf` (page 16)

#### Description & Cognitive Model
En competencia con rendimientos constantes a escala, los precios reales de los factores igualan sus productividades marginales $\frac{\partial F}{\partial L}=\frac{w}{p}$ y $\frac{\partial F}{\partial K}=\frac{q}{p}$, que dependen exclusivamente de $r=K/L$ y determinan la pendiente de la isocuanta $w/q$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Igualdad nominal y real | conceptual_swap | high | $\partial F/\partial L=w$ | Las productividades marginales físicas determinan las remuneraciones reales $w/p$ y $q/p$, no los precios monetarios nominales. |
| `D-C07-04` | Depende de escala | conceptual_swap | high | $\frac{\partial F}{\partial K}$ depende de $K$ y $L$ por separado | Recuerde que bajo rendimientos constantes a escala las productividades marginales son homogéneas de grado cero y solo dependen de la razón $r=K/L$. |
| `D-C07-02` | Dependencia de escala K y L | conceptual_swap | high | $\partial F/\partial K$ depende de $L$ | Por el teorema de Euler para funciones homogéneas de grado uno, las derivadas parciales son homogéneas de grado cero y solo dependen de $r=K/L$. |
| `D-C07-05` | Iguala nominales | conceptual_swap | high | $\frac{\partial F}{\partial L}=w$ y $\frac{\partial F}{\partial K}=q$ | Divida los precios monetarios $w$ y $q$ entre el nivel de precios $p(t)$ para expresar las productividades marginales en unidades reales de producto. |
| `D-C07-03` | Nivel de precios endógeno | conceptual_swap | high | El modelo real determina $p(t)$ | En el sistema real de Solow no hay ecuación monetaria que fije el nivel absoluto de precios, por lo que $p(t)$ se toma como dado. |
| `D-C07-06` | Invierte razón w/q | conceptual_swap | high | La pendiente de la isocuanta refleja $q/w$ | Verifique con isocuantas convexas en el plano $(L,K)$ que al crecer $r=K/L$ a lo largo de rayos más empinados, la razón $w/q$ crece hacia su límite. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Competencia pura y ajuste instantáneo de $w/p$ y $q/p$ para vaciar mercados. | Bajo rigideces de precios o competencia monopolística no rige la igualdad con productividad marginal. | - |
| `A-C07-02` | - | Mercados competitivos sin rigideces y rendimientos constantes a escala en $F(K,L)$ | Bajo competencia monopolística las derivadas parciales no igualan los precios reales. | - |
| `A-C07-03` | - | El nivel absoluto de precios $p(t)$ se toma como dado en el sistema real | Sin $p(t)$ dado no quedan determinados los valores nominales $w(t)$ y $q(t)$. | - |

---

### [Hab-06] Arbitraje y Tasa Propia de Capital (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 17: Arbitraje y Tasa Propia de Capital
- **Prerequisites:** C-07
- **Recommended Modalities:** proof_dag, open_symbolic, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 17)

#### Description & Cognitive Model
Derivación de la condición de arbitraje perfecto $i(t)=\frac{q(t)}{p(t)}+\frac{\dot{p}(t)}{p(t)}$ entre el rendimiento propio del capital y el interés monetario, junto con su forma integral $p(t)=\int_t^\infty q(u)e^{-\int_t^u i(z)dz}du$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Omite ganancia capital | skipped_step | high | $i(t)=\frac{q(t)}{p(t)}$ siempre | Incluya la tasa de variación del precio $\dot{p}(t)/p(t)$ en la ecuación de arbitraje; solo si $p(t)$ es constante coinciden la tasa propia y la de interés. |
| `D-Hab06-02` | Signo inverso $p_dot$ | conceptual_swap | high | $i(t)=\frac{q(t)}{p(t)}-\frac{\dot{p}(t)}{p(t)}$ | Note que si el precio cae ($\dot{p}<0$), la tasa propia $q/p$ debe superar a $i(t)$ para compensar la pérdida de capital y sostener la tenencia de capital. |
| `D-Hab06-03` | Alquiler nominal | skipped_step | high | $i(t)=q(t)+\frac{\dot{p}(t)}{p(t)}$ | Divida el alquiler monetario $q(t)$ entre el precio $p(t)$ porque un dólar invertido compra $1/p(t)$ unidades físicas de capital en el periodo. |
| `D-Hab06-04` | Integral sin descuento | conceptual_swap | high | $p(t)=\int_t^\infty q(u)\,du$ | Descuente cada flujo futuro $q(u)$ por el factor acumulativo $e^{-\int_t^u i(z)dz}$ antes de integrar sobre el horizonte infinito para obtener $p(t)$. |
| `D-Hab06-05` | Multiplica por h | conceptual_swap | high | $1+i(t)h=\frac{q(t)}{p(t)}+\frac{p(t+h)}{p(t)}$ | Multiplique el alquiler instantáneo $q(t)/p(t)$ por la duración $h$ del intervalo antes de igualar con $1+i(t)h$ y tomar el límite cuando $h\to 0$. |
| `D-Hab06-06` | Excluye $p_dot$/p | conceptual_swap | high | $\dot{p}(t)/p(t)$ es el nivel de precios | Distinga la derivada logarítmica $\dot{p}(t)/p(t)$, que mide la tasa porcentual de inflación o deflación, del nivel absoluto de precios $p(t)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Arbitraje perfecto, previsión perfecta, ausencia de riesgo y sin preferencias de liquidez | Con incertidumbre o preferencia por liquidez los rendimientos no se igualan por arbitraje. | - |

---

### [C-09] Distribución Factorial: Proporciones Fijas vs. Sustitución (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 20: Distribución Factorial: Proporciones Fijas vs. Sustitución
- **Prerequisites:** C-07
- **Recommended Modalities:** adversarial_break, multiple_select, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 20)

#### Description & Cognitive Model
Contraste de precios y participación del trabajo según la tecnología: en Harrod-Domar ($r=a/b$) los factores redundantes tienen precio nulo e indeterminación en el vértice; en Cobb-Douglas la participación laboral es constante ($1-a$), mientras en $Y=(a\sqrt{K}+\sqrt{L})^2$ depende de $s$ y $n$ como $1-a\sqrt{s/n}$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Vértice determinado | conceptual_swap | high | En Harrod-Domar $w$ y $q$ son únicos cuando $r=a/b$ | Observe que en el vértice $r=a/b$ ambos factores son escasos y las isocuantas tienen esquina recta, por lo que solo se fija $aq+bw=p$ con $w,q$ indeterminados. |
| `D-C09-02` | Redundancia invertida | conceptual_swap | high | Si $r>a/b$ en Harrod-Domar, entonces $w=0$ y $q=p/a$ | Identifique qué factor es redundante: si $r>a/b$ sobra capital respecto al trabajo, su producto marginal es cero ($q=0$) y todo el producto va al trabajo ($w=p/b$). |
| `D-C09-03` | Participación universal | conceptual_swap | high | La participación del trabajo siempre es independiente de $s$ y $n$ | Compare Cobb-Douglas con $Y=(a\sqrt{K}+\sqrt{L})^2$: en esta última la participación laboral de equilibrio es $1-a\sqrt{s/n}$, mayor cuanto mayor es $n$ y menor $s$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | Existencia de equilibrio balanceado $\sqrt{n/s}>a$ en el ejemplo $Y=(a\sqrt{K}+\sqrt{L})^2$ | Si $\sqrt{n/s}\le a$, el modelo no converge a un equilibrio interior finito. | - |

---

### [Hab-07] Crecimiento con Progreso Tecnológico Neutral (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 22: Crecimiento con Progreso Tecnológico Neutral
- **Prerequisites:** C-07
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 22)

#### Description & Cognitive Model
Análisis de cambio tecnológico neutral $Y=A(t)F(K,L)$ con $A(t)=e^{gt}$ en Cobb-Douglas ($b=1-a$): $K$ crece asintóticamente a tasa $n+g/b$, $Y$ a tasa $n+ag/b$, la razón $K/L$ crece sin límite a tasa $g/b$ y $K/Y$ crece a tasa $g$ manteniendo constante la participación laboral $1-a$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Equilibrio finito K/L | skipped_step | high | Con $A(t)=e^{gt}$ la razón $K/L$ converge a un $r^*$ constante | Note que al crecer $A(t)=e^{gt}$ continuamente, el ahorro acumulado expande $K$ más rápido que $L$ y la razón $K/L$ crece asintóticamente a tasa $g/(1-a)$. |
| `D-Hab07-02` | Tasa de Y igual a n+g | skipped_step | high | El producto $Y$ crece exactamente a tasa $n+g$ | Calcule la tasa de $Y=e^{gt}K^a L^{1-a}$ usando la tasa asintótica de $K$: $g + a(n+g/b) + (1-a)n = n + ag/b$, que supera a $n+g$ si $a>1/2$. |
| `D-Hab07-03` | Tasa de K igual a n+g | conceptual_swap | high | El capital $K$ crece a tasa $n+g$ en el largo plazo | Eleve la solución $[ \dots e^{(nb+g)t} ]^{1/b}$ a la potencia $1/b$: el exponente dominante se divide por $b=1-a$, dando la tasa asintótica $n+g/b$. |
| `D-Hab07-04` | K/Y constante | conceptual_swap | high | El coeficiente de capital $K/Y$ permanece constante | Reste la tasa asintótica de $Y$ ($n+ag/b$) de la tasa de $K$ ($n+g/b$): como $b=1-a$, la razón $K/Y$ crece a tasa positiva $g$. |
| `D-Hab07-05` | Salario real cae | conceptual_swap | high | El salario real debe caer o estancarse en el largo plazo | Recuerde que como $K/L$ crece ilimitadamente a tasa $g/b$ y $A(t)$ aumenta, la productividad marginal del trabajo y el salario real crecen continuamente. |
| `D-Hab07-06` | Share laboral sube | conceptual_swap | high | La participación del trabajo $1-a$ aumenta con $g>0$ | Verifique que con tecnología Cobb-Douglas y progreso neutral $A(t)$ las participaciones relativas de los factores permanecen fijas en $a$ y $1-a$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Progreso técnico neutral de Hicks $Y=A(t)F(K,L)$ con $A(t)=e^{gt}$ y $a\in(0,1)$ | Si el cambio técnico no es neutral o $a\ge 1$, no aplica la solución cerrada de $K(t)$. | - |

---

### [C-10] Oferta Elástica de Trabajo y Equilibrio (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 24: Oferta Elástica de Trabajo y Equilibrio
- **Prerequisites:** C-07
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 24)

#### Description & Cognitive Model
Generalización de la oferta laboral a $L=L_0 e^{nt}(w/p)^h$ y a $L=G(t,w/p)$: en la ecuación diferencial (6a) y (6b), la especificación de elasticidad constante (14) deja inalterado el equilibrio estable $r^*$, mientras una función general $G(t,w/p)$ sí modifica $r^*$ salvo que $\frac{1}{G}\frac{\partial G}{\partial t}=n$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C10-01` | Cambia r* con (14) | conceptual_swap | high | La elasticidad $h>0$ en (14) desplaza la razón de equilibrio $r^*$ | Iguale a cero el lado derecho de $\dot{r}=(sF(r,1)-nr)(1+ah/r)^{-1}$: como $(1+ah/r)^{-1}>0$, la condición $sF(r,1)=nr$ se cumple exactamente en el mismo $r^*$. |
| `D-C10-02` | Invarianza general | conceptual_swap | high | Toda oferta elástica $L=G(t,w/p)$ preserva el mismo $r^*$ | Evalúe $\dot{r}=0\Rightarrow \dot{w}=0$ en (6b): el equilibrio satisface $sF(r,1)=\frac{r}{G}\frac{\partial G}{\partial t}$, por lo que $r^*$ cambia salvo si $\frac{1}{G}\frac{\partial G}{\partial t}=n$. |
| `D-C10-03` | Crecimiento distinto | conceptual_swap | high | Con (14) el capital y el producto crecen a tasa distinta de $n$ | Recuerde que en el estado estacionario $r=r^*$ y $w/p$ son constantes, por lo que la oferta laboral $L$, el capital $K$ y el producto $Y$ crecen a tasa $n$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C10-01` | - | Nivel de precios constante y relación directa entre $w/p$ y $r$ vía $\partial F/\partial L$ | Sin precios constantes o monotonicidad de $w/p$ en $r$ no se elimina $\dot{w}/w$ en (6a). | - |

---

### [Hab-08] Tasa de Ahorro Variable e Impuesto a la Renta (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 26: Tasa de Ahorro Variable e Impuesto a la Renta
- **Prerequisites:** C-07
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 26)

#### Description & Cognitive Model
Extensión de la ecuación fundamental con tasa de ahorro variable $s(r)$ decreciente en $r$, $\dot{r}=s(r)F(r,1)-nr$ (efecto estabilizador sin estado estacionario de capital), y con impuesto proporcional a la renta $t$ donde una fracción $v$ se invierte, resultando la tasa efectiva $s_{\text{eff}}=s+(v-s)t$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | Estado estacionario K | skipped_step | high | Si $s(r)=0$ para $r$ grande, la economía entra en estado estacionario sin crecimiento de $K$ | Observe que si $r$ sube hasta anular el ahorro, el crecimiento continuo de la fuerza laboral $n$ reduce $r$ de nuevo hacia $r^*$, evitando un estado estacionario. |
| `D-Hab08-02` | Ahorro creciente en r | conceptual_swap | high | $s(r)$ es creciente en $r$ porque mayor $r$ implica mayor rendimiento | Recuerde que con rendimientos decrecientes del capital, un mayor $r$ reduce el alquiler real $q/p$; si el ahorro responde positivamente al rendimiento, $s(r)$ decrece con $r$. |
| `D-Hab08-03` | Impuesto siempre reduce s | skipped_step | high | Un impuesto $t>0$ siempre reduce la tasa de ahorro efectiva a $s(1-t)$ | Incluya la inversión pública $vtY$ en $\dot{K}=s(1-t)Y+vtY$: la tasa efectiva es $s+(v-s)t$, que sube respecto a $s$ siempre que $v>s$. |
| `D-Hab08-04` | Suma directa s+t | conceptual_swap | high | Si todo el impuesto se invierte ($v=1$), la tasa efectiva es $s+t$ | Aplique la tasa privada $s$ solo al ingreso disponible $(1-t)Y$ antes de sumar $tY$: se obtiene $s(1-t)+t=s+t(1-s)$, menor que $s+t$. |
| `D-Hab08-05` | Crecimiento explosivo | conceptual_swap | high | Si $s(r)$ se anula para $r$ grande aún puede haber fuga indefinida $r\to\infty$ | Note que si $s(r)$ se anula para $r$ suficientemente grande, la curva $s(r)F(r,1)$ cae por debajo de $nr$ y garantiza una última intersección estable. |
| `D-Hab08-06` | Invierte signo v-s | conceptual_swap | high | La tasa efectiva aumenta cuando el estado invierte menos que el sector privado ($v<s$) | Evalúe el signo del término $(v-s)t$ en $s+(v-s)t$: la tasa efectiva solo supera a $s$ cuando la fracción invertida pública $v$ excede a la privada $s$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab08-01` | - | La tasa de ahorro responde positivamente al rendimiento $q/p$ e impuesto proporcional $t\in(0,1)$ | Si el ahorro es insensible al rendimiento o el impuesto no es proporcional, cambian las curvas. | - |

---

### [C-11] Crecimiento Poblacional Endógeno y Trampa de Equilibrio (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 27: Crecimiento Poblacional Endógeno y Trampa de Equilibrio
- **Prerequisites:** C-07
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 27)

#### Description & Cognitive Model
Endogeneización de la tasa de crecimiento poblacional $n=n(r)$ en $\dot{r}=sF(r,1)-n(r)r$: una curva no lineal $n(r)r$ genera un equilibrio estable $r_1$ de bajos ingresos y un umbral crítico inestable $r_2$, donde $r_0<r_2$ retorna a $r_1$ y $r_0>r_2$ inicia expansión autosostenida sin rendimientos crecientes.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C11-01` | r2 estable y r1 inestable | conceptual_swap | high | El equilibrio inferior $r_1$ es inestable y el superior $r_2$ es estable | Analice el signo de $\dot{r}=sF(r,1)-n(r)r$: a la izquierda de $r_1$ es positivo y entre $r_1$ y $r_2$ es negativo, por lo que $r_1$ atrae trayectorias y $r_2$ las repele. |
| `D-C11-02` | Requiere rendimientos crecientes | conceptual_swap | high | Sin rendimientos crecientes a escala es imposible una trampa de estancamiento | Note la conclusión de Solow en la Figura IX: incluso con rendimientos constantes a escala, la dependencia demográfica $n(r)$ genera trampa en $r_1$ y despegue sobre $r_2$. |
| `D-C11-03` | Acumulación pequeña basta | conceptual_swap | high | Cualquier incremento inicial sobre $r_1$ basta para sostener el crecimiento | Verifique que para $r_1<r_0<r_2$ se cumple $n(r)r>sF(r,1)$ ($\dot{r}<0$), por lo que la acumulación insuficiente revierte a $r_1$; se requiere superar el umbral $r_2$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C11-01` | - | La tasa demográfica $\dot{L}/L=n(r)$ depende únicamente del ingreso per cápita $F(r,1)$ | Si $n$ es exógeno o depende de otras variables, el rayo $nr$ no se curva como en Figura IX. | - |

---

### [C-12] Rigidez Salarial y Preferencia por la Liquidez (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 29: Rigidez Salarial y Preferencia por la Liquidez
- **Prerequisites:** C-07, Hab-06
- **Recommended Modalities:** adversarial_break, unstructured_model, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 29)

#### Description & Cognitive Model
Cualificaciones keynesianas al modelo neoclásico: un salario real rígido $\bar{w}/p$ fija $\bar{r}$ y hace crecer el empleo a tasa $\frac{\dot{L}}{L}=\frac{s}{\bar{r}}F(\bar{r},1)$ (desempleo si $<n$, escasez si $>n$); con preferencia por la liquidez $\overline{M}=Q(Y,q/p)$, la trampa de liquidez fija un interés alto que subutiliza capital.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C12-01` | Desempleo si pendiente > n | conceptual_swap | high | Si $\frac{s}{\bar{r}}F(\bar{r},1)>n$ con salario rígido $\bar{w}/p$, crece el desempleo | Compare la tasa de crecimiento del empleo $\dot{L}/L=(s/\bar{r})F(\bar{r},1)$ con la de la fuerza laboral $n$: si la supera, hay escasez de trabajo; si es menor, surge desempleo. |
| `D-C12-02` | Trampa sube empleo K | conceptual_swap | high | En la trampa de liquidez todo el stock de capital disponible se emplea plenamente | Note que si la tasa de interés queda rígida por encima del nivel correspondiente al equilibrio, el capital en uso $K(t)$ en $\overline{M}=Q(Y,q/p)$ queda por debajo del disponible. |
| `D-C12-03` | Modelo real basta | conceptual_swap | high | El modelo real sin dinero describe bien la asignación entre efectivo y capital | Recuerde la advertencia de Solow: cuando importa la asignación entre efectivo y capital, el precio de la mercancía compuesta exige una dinámica monetaria explícita. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C12-01` | - | Salario real fijo $\bar{w}/p$ o demanda de saldos ociosos infinitamente elástica a un interés positivo | Con salarios e intereses flexibles se recupera el pleno empleo neoclásico de ambos factores. | - |

---
