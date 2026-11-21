# Cognitive Task Analysis (CTA): Solow M20 V3

- **Course ID:** `solow_m20_v3`
- **Macro-Competency:** Dominio y aplicación analítica integral de Solow M20 V3
- **Structure:** 20 total competencies (1 Facts, 9 Concepts, 10 Skills) with 91 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Forma Intensiva de Producción | Concept | Understand | Unidad 2: Forma Intensiva de Producción | - | 3 |
| `H-01` | Hipótesis Dinámicas de Solow | Fact | Remember | Unidad 2: Hipótesis Dinámicas de Solow | C-01 | 3 |
| `Hab-01` | Ecuación Fundamental de Solow | Skill | Apply | Unidad 3: Ecuación Fundamental de Solow | C-01, H-01 | 6 |
| `C-02` | Línea de Fase y Estado Uniforme | Concept | Analyze | Unidad 3: Línea de Fase y Estado Uniforme | Hab-01 | 3 |
| `Hab-02` | Solución Cuantitativa Cobb-Douglas | Skill | Apply | Unidad 4: Solución Cuantitativa Cobb-Douglas | Hab-01, C-02 | 6 |
| `C-03` | Acumulación Neoclásica y Pleno Empleo | Concept | Understand | Unidad 4: Acumulación Neoclásica y Pleno Empleo | C-01, H-01 | 3 |
| `Hab-03` | Derivación de la Ecuación Fundamental | Skill | Apply | Unidad 6: Derivación de la Ecuación Fundamental | C-03 | 6 |
| `C-04` | Equilibrio Estacionario y Estabilidad | Concept | Understand | Unidad 7: Equilibrio Estacionario y Estabilidad | Hab-03 | 3 |
| `C-05` | Equilibrios Múltiples y No Existencia | Concept | Analyze | Unidad 8: Equilibrios Múltiples y No Existencia | C-04 | 3 |
| `Hab-04` | Modelo de Proporciones Fijas | Skill | Apply | Unidad 11: Modelo de Proporciones Fijas | Hab-03 | 6 |
| `Hab-05` | Solución Explícita Cobb-Douglas | Skill | Apply | Unidad 13: Solución Explícita Cobb-Douglas | Hab-03, C-04 | 6 |
| `Hab-06` | Familia CES p=1/2 y Umbral $sa^2$ | Skill | Analyze | Unidad 14: Familia CES p=1/2 y Umbral sa^2 | C-05, Hab-05 | 6 |
| `C-06` | Precios Competitivos y Productividad Marginal | Concept | Understand | Unidad 16: Precios Competitivos y Productividad Marginal | C-03 | 4 |
| `Hab-07` | Arbitraje entre Interés y Renta del Capital | Skill | Apply | Unidad 17: Arbitraje entre Interés y Renta del Capital | C-06 | 6 |
| `C-08` | Relación Salario-Renta en Isocuantas y Proporciones Fijas | Concept | Analyze | Unidad 19: Relación Salario-Renta en Isocuantas y Proporciones Fijas | C-06 | 3 |
| `Hab-08` | Precios de Equilibrio y Participación del Trabajo | Skill | Apply | Unidad 21: Precios de Equilibrio y Participación del Trabajo | C-06, C-08 | 6 |
| `Hab-09` | Crecimiento con Cambio Tecnológico Neutral | Skill | Apply | Unidad 22: Crecimiento con Cambio Tecnológico Neutral | Hab-08 | 6 |
| `C-09` | Oferta Elástica de Trabajo y Tasa de Ahorro Variable | Concept | Analyze | Unidad 24: Oferta Elástica de Trabajo y Tasa de Ahorro Variable | C-06 | 3 |
| `C-10` | Tributación sobre la Renta y Crecimiento Poblacional Endógeno | Concept | Analyze | Unidad 27: Tributación sobre la Renta y Crecimiento Poblacional Endógeno | C-09 | 3 |
| `Hab-10` | Rigidez Salarial y Preferencia por la Liquidez | Skill | Evaluate | Unidad 29: Rigidez Salarial y Preferencia por la Liquidez | C-06, C-10 | 6 |

---

## Detailed Competency Specifications

### [C-01] Forma Intensiva de Producción (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 2: Forma Intensiva de Producción
- **Prerequisites:** None
- **Recommended Modalities:** concept_matching, adversarial_break, invariant_canvas
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
Reducción de la función de producción homogénea lineal $Q=f(K,L)$ a forma intensiva $Q=L\phi(k)$ con $k\equiv K/L$, $\phi'(k)>0$ y $\phi''(k)<0$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Omite factor trabajo | conceptual_swap | high | $Q=\phi(k)$ | Multiplique la función intensiva $\phi(k)$ por la fuerza laboral $L$, pues $\phi(k)=Q/L$ mide el producto por trabajador. |
| `D-C01-02` | Segunda derivada positiva | conceptual_swap | high | $\phi''(k)>0$ | Verifique que $f_{KK}<0$ implica $\phi''(k)=Lf_{KK}<0$, por lo que la función $\phi(k)$ crece a una tasa decreciente. |
| `D-C01-03` | Proporción fija Domar | conceptual_swap | high | $Q=\rho K$ | Distinga el modelo de Solow con proporciones variables $f(K,L)$ del supuesto de proporción fija del modelo de Domar. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Homogeneidad lineal $f(\lambda K,\lambda L)=\lambda f(K,L)$ | Sin retornos constantes a escala no es posible factorizar $L$ para obtener $\phi(k)$. | - |
| `A-C01-02` | - | Productos marginales positivos $f_K>0$ y decrecientes $f_{KK}<0$ | Si $\phi''(k)\ge 0$, la productividad media no exhibe retornos decrecientes en $k$. | - |

---

### [H-01] Hipótesis Dinámicas de Solow (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 2: Hipótesis Dinámicas de Solow
- **Prerequisites:** C-01
- **Recommended Modalities:** multiple_select, fill_in_the_blank, concept_matching
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
Reglas de acumulación de capital $\dot{K}=sQ$ con propensión marginal al ahorro constante $s$ y crecimiento exponencial laboral $\dot{L}/L=\lambda>0$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Ahorro sobre capital | conceptual_swap | high | $\dot{K}=sK$ | Recuerde que la inversión bruta $\dot{K}$ es una proporción constante $s$ del flujo de producto $Q$, nunca del stock $K$. |
| `D-H01-02` | Trabajo estacionario | conceptual_swap | high | $\dot{L}/L=0$ | Considere la hipótesis dinámica (15.27) donde la mano de obra crece exponencialmente a una tasa constante $\lambda>0$. |
| `D-H01-03` | Ahorro dependiente del tiempo | conceptual_swap | high | $s=s(t)$ | Mantenga $s$ como parámetro constante en las ecuaciones (15.26) a (15.30) que definen el modelo básico de Solow. |

---

### [Hab-01] Ecuación Fundamental de Solow (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 3: Ecuación Fundamental de Solow
- **Prerequisites:** C-01, H-01
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, proof_dag
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
Derivación de la ecuación diferencial fundamental $\dot{k}=s\phi(k)-\lambda k$ combinando $\dot{K}=sL\phi(k)$ con la regla del producto en $K=kL$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Omite dilución laboral | skipped_step | high | $\dot{k}=s\phi(k)$ | Aplique la regla del producto en $\dot{K}=L\dot{k}+k\dot{L}$ antes de dividir entre $L$ para incluir la dilución $-\lambda k$. |
| `D-Hab01-02` | Signo positivo en dilución | skipped_step | high | $\dot{k}=s\phi(k)+\lambda k$ | Transponga el término $k\lambda$ al lado derecho con signo negativo al despejar $\dot{k}$ desde $\dot{k}+\lambda k=s\phi(k)$. |
| `D-Hab01-03` | Conserva factor L | conceptual_swap | high | $\dot{k}=sL\phi(k)-\lambda k$ | Elimine el factor común $L>0$ en ambos miembros al igualar $sL\phi(k)=L\dot{k}+k\lambda L$ para obtener $\dot{k}$. |
| `D-Hab01-04` | Dilución sobre phi(k) | conceptual_swap | high | $\dot{k}=(s-\lambda)\phi(k)$ | Note que $\dot{L}/L=\lambda$ multiplica a $k=K/L$ en la regla del producto, no a la función de producto medio $\phi(k)$. |
| `D-Hab01-05` | Invierte parámetros s y lambda | conceptual_swap | high | $\dot{k}=\lambda\phi(k)-sk$ | Asocie la propensión al ahorro $s$ con la inversión $s\phi(k)$ y la tasa laboral $\lambda$ con la dilución $\lambda k$. |
| `D-Hab01-06` | Confunde derivada con tasa | conceptual_swap | high | $\dot{k}=s\phi(k)/k-\lambda$ | Distinga la derivada absoluta $\dot{k}=s\phi(k)-\lambda k$ de la tasa de crecimiento relativa $\dot{k}/k=s\phi(k)/k-\lambda$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Identidad $K=kL$ diferenciable respecto al tiempo $t$ con $L>0$ | Sin derivar el producto $kL$ ni dividir entre $L>0$ no surge la ecuación en $k$. | - |

---

### [C-02] Línea de Fase y Estado Uniforme (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 3: Línea de Fase y Estado Uniforme
- **Prerequisites:** Hab-01
- **Recommended Modalities:** invariant_canvas, adversarial_break, concept_matching
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
Análisis cualitativo mediante línea de fase $\dot{k}=s\phi(k)-\lambda k$: equilibrio $\bar{k}$, estabilidad cuando $d\dot{k}/dk<0$ y desplazamiento por $T(t)$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Estabilidad con pendiente positiva | conceptual_swap | high | Estable si $d\dot{k}/dk>0$ en $\bar{k}$ | Recuerde que la convergencia hacia $\bar{k}$ exige pendiente negativa en la línea de fase: $\dot{k}>0$ si $k<\bar{k}$ y $\dot{k}<0$ si $k>\bar{k}$. |
| `D-C02-02` | Crecimiento nulo en estado uniforme | conceptual_swap | high | $\dot{K}=\dot{L}=\dot{Q}=0$ en $\bar{k}$ | Distinga el estado uniforme donde $K$, $L$, $Q$ e inversión crecen a tasa $\lambda>0$ del estado estacionario de tasa cero. |
| `D-C02-03` | Desplazamiento tecnológico descendente | conceptual_swap | high | $T(t)$ creciente reduce $\bar{k}$ | Verifique que $dT/dt>0$ eleva el producto para cada $k$, desplazando $s\phi(k)$ hacia arriba y aumentando el equilibrio $\bar{k}$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | Capital indispensable $\phi(0)=0$ y tramo con $s\phi(k)>\lambda k$ para $k>0$ | Sin un tramo donde el ahorro supere la dilución no existe un equilibrio positivo $\bar{k}$. | - |
| `A-C02-02` | - | Progreso tecnológico multiplicativo $Q=T(t)f(K,L)$ con $dT/dt>0$ | Si $T$ es invariante en el tiempo, la curva $s\phi(k)$ no experimenta desplazamiento secular. | - |

---

### [Hab-02] Solución Cuantitativa Cobb-Douglas (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 4: Solución Cuantitativa Cobb-Douglas
- **Prerequisites:** Hab-01, C-02
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
Linealización de la ecuación de Bernoulli $\dot{k}+\lambda k=sk^\alpha$ vía $z=k^{1-\alpha}$ para obtener $k(t)$ y el límite asintótico $(s/\lambda)^{1/(1-\alpha)}$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Exponente sin invertir | skipped_step | high | $k^*=(s/\lambda)^{1-\alpha}$ | Eleve ambos miembros de $k^{1-\alpha}=s/\lambda$ al recíproco $1/(1-\alpha)$ para despejar correctamente el equilibrio de $k$. |
| `D-Hab02-02` | Sustitución z errónea | skipped_step | high | $z=k^\alpha$ | Aplique la transformación de Bernoulli $z=k^{1-m}$ con $m=\alpha$, es decir $z=k^{1-\alpha}$, para obtener una EDO lineal. |
| `D-Hab02-03` | Invierte razón s/lambda | conceptual_swap | high | $k^*=(\lambda/s)^{1/(1-\alpha)}$ | Compruebe la estática comparativa: mayor ahorro $s$ eleva $\bar{k}$ y mayor tasa laboral $\lambda$ lo reduce, dando $s/\lambda$. |
| `D-Hab02-04` | Omite factor (1-alpha) | conceptual_swap | high | $\frac{dz}{dt}+\lambda z=s$ | Derive $z=k^{1-\alpha}$ respecto a $t$ usando $\dot{z}=(1-\alpha)k^{-\alpha}\dot{k}$ para conservar el factor $(1-\alpha)$. |
| `D-Hab02-05` | Exponencial divergente | conceptual_swap | high | $e^{+(1-\alpha)\lambda t}$ | Resuelva $\dot{z}+(1-\alpha)\lambda z=(1-\alpha)s$ con exponente negativo $e^{-(1-\alpha)\lambda t}$ para que converja cuando $t\to\infty$. |
| `D-Hab02-06` | Condición inicial sin potencia | conceptual_swap | high | $z(0)=k(0)$ | Aplique la definición $z=k^{1-\alpha}$ también en $t=0$ para escribir $z(0)=k(0)^{1-\alpha}$ dentro de la solución final. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Función Cobb-Douglas $Q=K^\alpha L^{1-\alpha}$ con $\alpha\in(0,1)$ y $\lambda>0$ | Si $\alpha\ge 1$ o $\lambda\le 0$, el término exponencial no converge a cero cuando $t\to\infty$. | - |

---

### [C-03] Acumulación Neoclásica y Pleno Empleo (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 4: Acumulación Neoclásica y Pleno Empleo
- **Prerequisites:** C-01, H-01
- **Recommended Modalities:** concept_matching, adversarial_break, fill_in_the_blank
- **Evidence Citations:** `solow1956.pdf` (page 4)

#### Description & Cognitive Model
Ecuación básica de acumulación de capital $\dot{K}=sF(K,L_0 e^{nt})$ bajo rendimientos constantes a escala, ahorro proporcional $sY$ y crecimiento exógeno del trabajo $L(t)=L_0 e^{nt}$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Ahorro sobre capital | conceptual_swap | high | $\dot{K}=sK$ | Multiplique la propensión a ahorrar $s$ por el producto neto $Y=F(K,L)$, nunca por el stock de capital $K$. |
| `D-C03-02` | Trabajo constante | conceptual_swap | high | $L(t)=L_0$ | Incorpore el crecimiento exógeno de la fuerza laboral $L(t)=L_0 e^{nt}$ a tasa natural $n$ dentro de $F(K,L)$. |
| `D-C03-03` | Rendimientos decrecientes globales | conceptual_swap | high | $F(\lambda K,\lambda L)<\lambda F(K,L)$ | Recuerde que sin un factor fijo no aumentable como la tierra, la función de producción presenta rendimientos constantes a escala. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | Rendimientos constantes a escala $F(\lambda K,\lambda L)=\lambda F(K,L)$ sin factor fijo como la tierra | Con rendimientos decrecientes a escala no es posible reducir el sistema a la variable $r=K/L$. | - |
| `A-C03-02` | - | Pleno empleo perpetuo de la fuerza laboral $L(t)=L_0 e^{nt}$ y del stock de capital | Si hay desempleo involuntario, la identidad $L=L_0 e^{nt}$ deja de determinar el empleo efectivo. | - |

---

### [Hab-03] Derivación de la Ecuación Fundamental (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 6: Derivación de la Ecuación Fundamental
- **Prerequisites:** C-03
- **Recommended Modalities:** open_symbolic, proof_dag, fill_in_the_blank
- **Evidence Citations:** `solow1956.pdf` (page 6)

#### Description & Cognitive Model
Derivación de la ecuación diferencial $\dot{r}=sF(r,1)-nr$ para el ratio capital-trabajo $r=K/L$ aplicando diferenciación respecto al tiempo y homogeneidad de grado uno

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Signo positivo en nr | skipped_step | high | $\dot{r}=sF(r,1)+nr$ | Al diferenciar $K=rL_0 e^{nt}$ se obtiene $\dot{K}=L_0 e^{nt}\dot{r}+nrL_0 e^{nt}$, por lo que $nr$ pasa restando al despejar $\dot{r}$. |
| `D-Hab03-02` | Olvida multiplicar por L | skipped_step | high | $F(K,L)=F(r,1)$ | Por homogeneidad de grado uno, al dividir ambos argumentos de $F(K,L)$ entre $L$ debe multiplicar la función por $L$. |
| `D-Hab03-03` | Confunde tasa relativa con nivel | skipped_step | high | $\dot{r}=\frac{\dot{K}}{K}-\frac{\dot{L}}{L}$ | La diferencia de tasas relativas equivale a $\dot{r}/r$, por lo que debe multiplicar ambos lados por $r$ para obtener $\dot{r}$. |
| `D-Hab03-04` | Omite la tasa de ahorro s | conceptual_swap | high | $\dot{r}=F(r,1)-nr$ | Conserve la propensión al ahorro $s$ multiplicando el producto por trabajador $F(r,1)$, pues solo se acumula la fracción ahorrada. |
| `D-Hab03-05` | Divide nr por r | conceptual_swap | high | $\dot{r}=sF(r,1)-n$ | El término de dilución por crecimiento poblacional es proporcional al ratio actual $r$, dando $nr$ y no una constante $n$. |
| `D-Hab03-06` | Usa F(1,r) invertido | conceptual_swap | high | $\dot{r}=sF(1,r)-nr$ | Como $r=K/L$, dividir $(K,L)$ entre $L$ produce $(r,1)$, que representa el producto por trabajador como función del capital por trabajador. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | Homogeneidad de primer grado $F(K,L)=LF(K/L,1)$ con $L(t)=L_0 e^{nt}>0$ | Sin homogeneidad de primer grado, $L$ no se cancela y $\dot{r}$ sigue dependiendo del tamaño absoluto $L$. | - |

---

### [C-04] Equilibrio Estacionario y Estabilidad (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 7: Equilibrio Estacionario y Estabilidad
- **Prerequisites:** Hab-03
- **Recommended Modalities:** invariant_canvas, adversarial_break, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 7)

#### Description & Cognitive Model
Existencia y estabilidad del equilibrio $r^*$ donde $nr=sF(r,1)$ ($\dot{r}=0$), con convergencia hacia $r^*$ cuando $sF(r,1)$ cruza al rayo $nr$ desde arriba

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Invierte signo de r punto | conceptual_swap | high | $r>r^* \Rightarrow \dot{r}>0$ | Cuando $r>r^*$ el rayo $nr$ supera a $sF(r,1)$, de modo que $\dot{r}=sF(r,1)-nr<0$ y el ratio $r$ disminuye hacia $r^*$. |
| `D-C04-02` | Crecimiento nulo en equilibrio | conceptual_swap | high | $\dot{r}=0 \Rightarrow \dot{K}=0$ | Cuando $\dot{r}=0$, el ratio $K/L$ es constante, lo que implica que el capital y el producto crecen exactamente a la tasa natural $n$. |
| `D-C04-03` | Convergencia desde cero capital | conceptual_swap | high | $K=0 \Rightarrow r \to r^*$ | Si $K=0$ entonces $r=0$ y sin capital no hay producto ni acumulación cuando ambos insumos son esenciales, impidiendo despegar. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | Productividad marginal del capital positiva y decreciente con $F(0,1)=0$ y cruce único | Si la curva $sF(r,1)$ no es cóncava o no cruza a $nr$, el equilibrio puede ser múltiple o inexistente. | - |

---

### [C-05] Equilibrios Múltiples y No Existencia (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 8: Equilibrios Múltiples y No Existencia
- **Prerequisites:** C-04
- **Recommended Modalities:** invariant_canvas, adversarial_break, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 8)

#### Description & Cognitive Model
Configuraciones alternativas de $\dot{r}=sF(r,1)-nr$: tres intersecciones ($r_1,r_3$ estables y $r_2$ inestable) o ausencia de equilibrio cuando $sF(r,1)$ no corta a $nr$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Estabilidad del punto intermedio | conceptual_swap | high | $r_2$ es estable y $r_1,r_3$ inestables | En $r_2$ la curva $sF(r,1)$ cruza a $nr$ desde abajo, por lo que cualquier perturbación aleja al sistema hacia $r_1$ o $r_3$. |
| `D-C05-02` | Origen como equilibrio con F(0,1)>0 | conceptual_swap | high | $r=0$ es equilibrio si $F(0,1)>0$ | Si la producción es posible sin capital ($F(0,1)>0$), entonces $sF(0,1)>0$ y en $r=0$ se tiene $\dot{r}>0$, luego no es equilibrio. |
| `D-C05-03` | Caída del ingreso agregado | conceptual_swap | high | $s_2 F^2(r,1)<nr \Rightarrow \dot{Y}<0$ | Aunque el ingreso per cápita caiga indefinidamente cuando $s_2 F^2(r,1)<nr$, la inversión neta y el trabajo crecen, por lo que $Y$ sube. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Curvas $F(r,1)$ no decrecientes que pueden cruzar varias veces o no cruzar al rayo $nr$ | Restringir $F(r,1)$ al caso Cobb-Douglas elimina la posibilidad de equilibrios múltiples o inexistentes. | - |

---

### [Hab-04] Modelo de Proporciones Fijas (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 11: Modelo de Proporciones Fijas
- **Prerequisites:** Hab-03
- **Recommended Modalities:** open_symbolic, unstructured_model, fill_in_the_blank
- **Evidence Citations:** `solow1956.pdf` (page 11)

#### Description & Cognitive Model
Resolución explícita de $\dot{r}=s\min(r/a,1/b)-nr$ en el caso Harrod-Domar $Y=\min(K/a,L/b)$ según $n>s/a$, $n=s/a$ o $n<s/a$ y cálculo de capacidad ociosa o desempleo

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Umbral de quiebre incorrecto | skipped_step | high | Quiebre en $r=b/a$ | La igualdad $r/a=1/b$ ocurre exactamente cuando el ratio capital-trabajo alcanza $r=a/b$, no su recíproco $b/a$. |
| `D-Hab04-02` | Tasa garantizada invertida | skipped_step | high | Tasa garantizada igual a $a/s$ | En el tramo $r<a/b$ la ecuación es $\dot{r}=(s/a-n)r$, por lo que la tasa garantizada de crecimiento es $s/a$. |
| `D-Hab04-03` | Desempleo cuando capital abunda | conceptual_swap | high | $n<s/a \Rightarrow$ redundancia de trabajo | Si $n<s/a$, el ratio converge a $r=s/(nb)>a/b$, donde la productividad marginal del capital cae a cero y sobra capital. |
| `D-Hab04-04` | Proporción de capital empleado errónea | conceptual_swap | high | Proporción empleada $\frac{s}{an_3}$ | En $r=s/(n_3 b)$, solo se requiere $a/b$ por trabajador, de modo que la fracción del capital empleada es $(a/b)/r=an_3/s$. |
| `D-Hab04-05` | Estabilidad asintótica en cero errónea | conceptual_swap | high | $n_1>s/a \Rightarrow r \to \frac{s}{n_1 b}$ | Como $s/(n_1 b)<a/b$, al cruzar $r=a/b$ cambia la rama a $\dot{r}=(s/a-n_1)r<0$ y el ratio sigue cayendo hacia cero. |
| `D-Hab04-06` | Empleo cuando capital limita | conceptual_swap | high | Empleo igual a $\frac{aK}{b}$ | Cuando el capital es el cuello de botella, el producto es $K/a$ y, como cada unidad requiere $b$ trabajadores, el empleo es $b(K/a)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Isoquantas en ángulo recto $Y=\min(K/a,L/b)$ sin sustitución entre capital y trabajo | Si existe sustituibilidad positiva entre factores, desaparece la rigidez de filo de navaja. | - |

---

### [Hab-05] Solución Explícita Cobb-Douglas (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 13: Solución Explícita Cobb-Douglas
- **Prerequisites:** Hab-03, C-04
- **Recommended Modalities:** open_symbolic, proof_dag, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 13)

#### Description & Cognitive Model
Integración directa de $\dot{K}=sK^a(L_0 e^{nt})^{1-a}$ con $b=1-a$ para obtener $K(t)$, el equilibrio $r^*=(s/n)^{1/(1-a)}$ y el coeficiente de capital de largo plazo $C=K/Y=s/n$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Exponente sin invertir | skipped_step | high | $r^*=(s/n)^{1-a}$ | Al igualar $sr^a=nr$ se obtiene $r^{1-a}=s/n$, por lo que debe elevar ambos miembros al recíproco $1/(1-a)$. |
| `D-Hab05-02` | Invierte razón s/n | skipped_step | high | $r^*=(n/s)^{\frac{1}{1-a}}$ | Un mayor ahorro $s$ eleva el capital estacionario y un mayor crecimiento $n$ lo diluye, por lo que el cociente es $s/n$. |
| `D-Hab05-03` | Omite condición inicial en K(t) | conceptual_swap | high | $K(t)=\left[\frac{s}{n}L_0^b e^{nbt}\right]^{1/b}$ | La integración exacta desde $t=0$ conserva la constante $K_0^b-\frac{s}{n}L_0^b$, que solo se vuelve despreciable asintóticamente. |
| `D-Hab05-04` | Ingreso per cápita sin potencia a | conceptual_swap | high | $Y/L \to (s/n)^{\frac{1}{1-a}}$ | Como $Y/L=(K/L)^a=r^a$, el límite del producto por trabajador es $(r^*)^a=(s/n)^{a/(1-a)}$, no $(s/n)^{1/(1-a)}$. |
| `D-Hab05-05` | Coeficiente de capital invertido | conceptual_swap | high | $C=K/Y=n/s$ | En la senda de equilibrio $n=s/C$, de modo que el coeficiente capital-producto resulta $C=K/Y=s/n$. |
| `D-Hab05-06` | Exponente erróneo en $e^{nt}$ | conceptual_swap | high | $K(t) \sim (s/n)^{1/b} L_0 e^{nt/b}$ | Dentro del corchete figura $e^{nbt}$; al elevar a $1/b$ los exponentes $b$ se cancelan y $K(t)$ crece exactamente como $e^{nt}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | Elasticidad producto-capital $a\in(0,1)$ en la función Cobb-Douglas $Y=K^a L^{1-a}$ | Si $a\ge 1$, la productividad marginal del capital no decrece hacia cero y no hay equilibrio único. | - |

---

### [Hab-06] Familia CES p=1/2 y Umbral $sa^2$ (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 14: Familia CES p=1/2 y Umbral sa^2
- **Prerequisites:** C-05, Hab-05
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 14)

#### Description & Cognitive Model
Análisis de $\dot{r}=s(a\sqrt{r}+1)^2-nr$ para $Y=(a\sqrt{K}+\sqrt{L})^2$: divergencia indefinida si $sa^2>n$ y equilibrio estable $r^*=(1/(\sqrt{n/s}-a))^2$ si $sa^2<n$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Invierte desigualdad de equilibrio | skipped_step | high | $sa^2>n \Rightarrow$ existe equilibrio $r^*$ | Si $sa^2>n$, la curva $s(a\sqrt{r}+1)^2$ permanece siempre sobre $nr$, por lo que $r$ crece sin límite y no hay equilibrio. |
| `D-Hab06-02` | Olvida elevar al cuadrado en r* | skipped_step | high | $r^*=\frac{1}{\sqrt{n/s}-a}$ | De $\sqrt{s}(a\sqrt{r}+1)=\sqrt{nr}$ se despeja $\sqrt{r^*}=1/(\sqrt{n/s}-a)$, por lo que debe elevar al cuadrado para hallar $r^*$. |
| `D-Hab06-03` | Invierte signo en el denominador | conceptual_swap | high | $r^*=\left(\frac{1}{a-\sqrt{n/s}}\right)^2$ | Como la existencia de equilibrio exige $sa^2<n$, se cumple $\sqrt{n/s}>a$ y el denominador positivo es $\sqrt{n/s}-a$. |
| `D-Hab06-04` | Altura inicial en cero errónea | conceptual_swap | high | $sF(0,1)=0$ | En esta familia es posible producir solo con trabajo ($K=0$), de modo que cuando $r=0$ la curva parte de altura positiva $s$. |
| `D-Hab06-05` | Ingreso límite mal despejado | conceptual_swap | high | $\lim Y/L = \frac{1}{1-a\sqrt{n/s}}$ | Evaluando $F(r^*,1)=(a\sqrt{r^*}+1)^2$ con $\sqrt{r^*}=1/(\sqrt{n/s}-a)$ se obtiene el ingreso por trabajador límite $1/(1-a\sqrt{s/n})^2$. |
| `D-Hab06-06` | Convexidad errónea para p>1 | conceptual_swap | high | $p>1$ da rendimientos decrecientes | En $Y=(aK^p+L^p)^{1/p}$, las isocuantas tienen la convexidad estándar y rendimientos marginales decrecientes solo si $0<p<1$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Parámetro de sustitución $0<p<1$ (en particular $p=1/2$) para asegurar isocuantas convexas | Si $p\ge 1$, las isocuantas son lineales o tienen convexidad inversa, invalidando el pleno empleo competitivo. | - |

---

### [C-06] Precios Competitivos y Productividad Marginal (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 16: Precios Competitivos y Productividad Marginal
- **Prerequisites:** C-03
- **Recommended Modalities:** concept_matching, adversarial_break, fill_in_the_blank, open_symbolic
- **Evidence Citations:** `solow1956.pdf` (page 16)

#### Description & Cognitive Model
En competencia perfecta con rendimientos constantes a escala, el salario real $\frac{w}{p}=\frac{\partial F}{\partial L}$ y la renta real del capital $\frac{q}{p}=\frac{\partial F}{\partial K}$ dependen únicamente de la razón capital-trabajo $r=K/L$.

#### Fused Distractor Models (4)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Dependencia de la escala absoluta | conceptual_swap | high | $\frac{\partial F}{\partial K}$ depende de $K$ y $L$ por separado | Por homogeneidad de grado cero de las derivadas parciales bajo rendimientos constantes, ambos productos marginales dependen solo de $r=K/L$. |
| `D-C06-04` | Invierte cociente | conceptual_swap | high | $\frac{\partial F}{\partial L}=\frac{p}{w}$ | Divida el salario nominal $w$ entre el nivel de precios $p$ para expresar la remuneración en unidades de producto real. |
| `D-C06-02` | Determinación del nivel de precios p | conceptual_swap | high | El modelo real determina $p(t)$ | En el sistema real no hay ecuación monetaria que fije el nivel absoluto de precios, por lo que $p(t)$ se toma como dado. |
| `D-C06-03` | Confunde renta q con tasa de interés i | conceptual_swap | high | $\frac{\partial F}{\partial K}=i$ | La productividad marginal del capital iguala a la renta real por unidad de tiempo $q/p$, mientras $i(t)$ se vincula vía arbitraje. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Competencia perfecta con oferta inelástica instantánea de capital y trabajo y precios flexibles | Con rigideces de precios o competencia monopolística, las ecuaciones marginales dejan de limpiar los mercados. | - |
| `A-C06-02` | - | Competencia perfecta y rendimientos constantes a escala en $F(K,L)$ | Sin competencia perfecta o escala constante, los precios factoriales no igualan productividades marginales dependientes solo de $r$. | - |

---

### [Hab-07] Arbitraje entre Interés y Renta del Capital (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 17: Arbitraje entre Interés y Renta del Capital
- **Prerequisites:** C-06
- **Recommended Modalities:** open_symbolic, proof_dag, fill_in_the_blank
- **Evidence Citations:** `solow1956.pdf` (page 17)

#### Description & Cognitive Model
Condición de arbitraje perfecto $i(t)=\frac{q(t)}{p(t)}+\frac{\dot{p}(t)}{p(t)}$ que iguala el rendimiento del dinero prestado con la renta real más la ganancia de capital, derivada de $p(t)=\int_t^\infty q(u)e^{-\int_t^u i(z)\,dz}\,du$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Omite variación de p | skipped_step | high | $i(t)=\frac{q(t)}{p(t)}$ | Incluya la tasa de variación del precio $\dot{p}(t)/p(t)$ al comparar activos reales con préstamos nominales cuando el nivel de precios cambia. |
| `D-Hab07-02` | Signo invertido | skipped_step | high | $i(t)=\frac{q(t)}{p(t)}-\frac{\dot{p}(t)}{p(t)}$ | Sume la inflación esperada $\dot{p}/p$ a la tasa propia $q/p$: si el precio cae ($\dot{p}<0$), $q/p$ debe superar a $i$ para compensar la pérdida. |
| `D-Hab07-03` | Sin dividir por p | conceptual_swap | high | $i(t)=q(t)+\dot{p}(t)$ | Divida tanto la renta monetaria $q(t)$ como $\dot{p}(t)$ entre el precio de transferencia $p(t)$ para obtener tasas instantáneas por dólar invertido. |
| `D-Hab07-04` | Descuenta con q | conceptual_swap | high | $p(t)=\int_t^\infty i(u)e^{-\int_t^u q(z)\,dz}\,du$ | Descuente el flujo futuro de rentas netas $q(u)$ utilizando la tasa de interés nominal acumulada $\int_t^u i(z)\,dz$ en el exponente. |
| `D-Hab07-05` | Error en límite h | conceptual_swap | high | $1+i(t)h=\frac{q(t)}{p(t)}h$ | Agregue el término $p(t+h)/p(t)$ correspondiente a la venta del capital al final del intervalo $[t,t+h]$ antes de tomar $h\to 0$. |
| `D-Hab07-06` | Renta nominal fija | conceptual_swap | high | $\frac{q}{p}=i$ si $\dot{p}<0$ | Observe que cuando el nivel de precios desciende ($\dot{p}/p<0$), la tasa propia $q/p$ debe exceder al interés $i$ para sostener el arbitraje. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Previsión perfecta, ausencia de riesgo y arbitraje sin fricciones | Con incertidumbre o preferencia por liquidez aparecen primas de riesgo y el arbitraje exacto deja de cumplirse. | - |

---

### [C-08] Relación Salario-Renta en Isocuantas y Proporciones Fijas (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 19: Relación Salario-Renta en Isocuantas y Proporciones Fijas
- **Prerequisites:** C-06
- **Recommended Modalities:** invariant_canvas, adversarial_break, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 19)

#### Description & Cognitive Model
La razón factorial de precios $\frac{w}{q}$ coincide con la pendiente de las isocuantas y permanece constante a lo largo de rayos desde el origen; en proporciones fijas Harrod-Domar ($r=a/b$), los precios sufren saltos discontinuos a $q=0$ o $w=0$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Indeterminación fuera de a/b | conceptual_swap | high | $w/q$ indeterminado si $r>a/b$ | Recuerde que para $r>a/b$ el capital es redundante ($q=0$) y todo el producto se imputa al trabajo ($w=p/b$); solo en $r=a/b$ hay indeterminación. |
| `D-C08-02` | Invierte exceso en Harrod | conceptual_swap | high | $r>a/b \Rightarrow w=0$ | Verifique qué factor es redundante: si $K/L>a/b$ sobra capital, por lo que su productividad marginal y renta $q$ se anulan, no el salario $w$. |
| `D-C08-03` | Pendiente decrece con r | conceptual_swap | high | $r\uparrow \Rightarrow w/q\downarrow$ | Note que bajo convexidad normal de isocuantas, un aumento de $r=K/L$ vuelve al trabajo relativamente más escaso y eleva la razón $w/q$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C08-01` | - | Isocuantas convexas suaves o vértices rectos de Leontief en proporciones fijas | Sin convexidad o estructura homogénea, la correspondencia monótona entre $r$ y $w/q$ puede romperse. | - |

---

### [Hab-08] Precios de Equilibrio y Participación del Trabajo (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 21: Precios de Equilibrio y Participación del Trabajo
- **Prerequisites:** C-06, C-08
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 21)

#### Description & Cognitive Model
Cálculo de precios reales y participación laboral en equilibrio: en Cobb-Douglas $Y=K^a L^{1-a}$ la participación es constante $1-a$, mientras que en $Y=(a\sqrt{K}+\sqrt{L})^2$ resulta $\frac{w}{p}\frac{L}{Y}=1-a\sqrt{s/n}$, creciente en $n$ y decreciente en $s$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | Participación constante general | skipped_step | high | $\frac{w}{p}\frac{L}{Y}$ independiente de $s,n$ | Calcule $(w/p)(L/Y)$ explícitamente para cada función: en $Y=(a\sqrt{K}+\sqrt{L})^2$ la participación laboral depende de $s/n$ en estado estacionario. |
| `D-Hab08-02` | Signo de s/n invertido | skipped_step | high | $\frac{w}{p}\frac{L}{Y}=1-a\sqrt{n/s}$ | Sustituya $r^*=(\frac{1}{\sqrt{n/s}-a})^2$ en $\frac{w}{p}=a\sqrt{r}+1$ y divida por $Y/L=(\frac{1}{1-a\sqrt{s/n}})^2$ para obtener $1-a\sqrt{s/n}$. |
| `D-Hab08-03` | Invierte razón Cobb-Douglas | conceptual_swap | high | $\frac{w}{q}=\frac{a}{1-a}r$ | Divida $\partial Y/\partial L=(1-a)r^a$ entre $\partial Y/\partial K=ar^{a-1}$ para obtener $\frac{w}{q}=\frac{1-a}{a}r$, no su recíproco. |
| `D-Hab08-04` | Exponente erróneo en w/p | conceptual_swap | high | $\frac{w}{p}=(1-a)(s/n)^{\frac{1}{1-a}}$ | Eleve $r^*=(s/n)^{\frac{1}{1-a}}$ a la potencia $a$ al evaluar $w/p=(1-a)r^a$, obteniendo $(1-a)(s/n)^{\frac{a}{1-a}}$. |
| `D-Hab08-05` | Renta de equilibrio errónea | conceptual_swap | high | $\frac{q}{p}=a\frac{s}{n}$ | Sustituya $r^*=(s/n)^{\frac{1}{1-a}}$ en $q/p=ar^{a-1}$: como $(a-1)/(1-a)=-1$, se invierte la razón a $an/s$. |
| `D-Hab08-06` | Efecto de n sobre participación | conceptual_swap | high | $n\uparrow \Rightarrow \frac{w}{p}\frac{L}{Y}\downarrow$ | Distinga el nivel del salario real (que baja al crecer $n$) de la participación relativa $1-a\sqrt{s/n}$, que aumenta con $n$ en este ejemplo. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab08-01` | - | Existencia de equilibrio balanceado con $\sqrt{n/s}>a$ en el tercer ejemplo | Si $\sqrt{n/s}\le a$, no existe razón capital-trabajo estacionaria finita y la fórmula de equilibrio carece de validez. | - |

---

### [Hab-09] Crecimiento con Cambio Tecnológico Neutral (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 22: Crecimiento con Cambio Tecnológico Neutral
- **Prerequisites:** Hab-08
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, proof_dag
- **Evidence Citations:** `solow1956.pdf` (page 22)

#### Description & Cognitive Model
Con cambio tecnológico neutral $Y=A(t)F(K,L)$ y $A(t)=e^{gt}$ en Cobb-Douglas ($b=1-a$), la ecuación $\dot{K}=se^{gt}K^a(L_0e^{nt})^{1-a}$ implica tasas asintóticas de $n+\frac{g}{b}$ para $K$, $n+\frac{ag}{b}$ para $Y$, $\frac{g}{b}$ para $K/L$ y $g$ para $K/Y$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab09-01` | Tasa de Y igual a n+g | skipped_step | high | $\frac{\dot{Y}}{Y}\to n+g$ | Tome en cuenta el efecto compuesto de mayor ahorro sobre $K$: la tasa de $Y$ converge a $n+\frac{ag}{1-a}$, distinta de $n+g$ salvo si $a=1/2$. |
| `D-Hab09-02` | Razón K/L estacionaria | skipped_step | high | $K/L$ converge a constante | Observe que el ahorro creciente hace crecer $K$ más rápido que $L$, por lo que $K/L$ crece sin límite a tasa asintótica $g/(1-a)$. |
| `D-Hab09-03` | Confunde tasa de K y Y | conceptual_swap | high | $\frac{\dot{K}}{K}\to n+\frac{ag}{b}$ | Diferencie la solución explícita de $K(t)$: el exponente dominante es $(nb+g)/b=n+g/b$, mayor que la tasa $n+ag/b$ del producto. |
| `D-Hab09-04` | Coeficiente K/Y constante | conceptual_swap | high | $K/Y$ permanece constante | Reste las tasas de crecimiento de $K$ y $Y$: $(n+g/b)-(n+ag/b)=g(1-a)/b=g>0$, por lo que el coeficiente capital-producto crece a tasa $g$. |
| `D-Hab09-05` | Salario real acotado | conceptual_swap | high | $w/p$ converge a un límite finito | Dado que $K/L$ crece indefinidamente, el salario real $w/p=(1-a)e^{gt}(K/L)^a$ también aumenta sin límite mientras la participación laboral sigue en $1-a$. |
| `D-Hab09-06` | Descuida definición b | conceptual_swap | high | Usa $b=a$ en las tasas | Recuerde la notación del modelo donde $b=1-a$ es la participación del trabajo, de modo que $g/b=g/(1-a)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab09-01` | - | Progreso técnico neutral de Hicks-Solow multiplicativo $A(t)=e^{gt}$ | Si el cambio tecnológico no es neutral o no es exponencial, el mapa de isocuantas cambia y las tasas asintóticas constantes no aplican. | - |

---

### [C-09] Oferta Elástica de Trabajo y Tasa de Ahorro Variable (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 24: Oferta Elástica de Trabajo y Tasa de Ahorro Variable
- **Prerequisites:** C-06
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 24)

#### Description & Cognitive Model
Con oferta laboral $L=L_0 e^{nt}(w/p)^h$ en Cobb-Douglas resulta $\dot{r}=(sF(r,1)-nr)(1+\frac{ah}{r})^{-1}$ manteniendo $r^*$ invariante; con ahorro endógeno $s(r)$ decreciente en $r$, la ecuación $\dot{r}=s(r)F(r,1)-nr$ ejerce un efecto estabilizador.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Elasticidad cambia r* siempre | conceptual_swap | high | $h>0$ altera $r^*$ en (14) | Verifique en $\dot{r}=(sF(r,1)-nr)(1+ah/r)^{-1}$ que $\dot{r}=0$ ocurre exactamente donde $sF(r,1)=nr$, dejando $r^*$ intacto bajo la forma (14). |
| `D-C09-02` | Ahorro variable da estado estacionario | conceptual_swap | high | $s(r)=0 \Rightarrow$ cesa $L$ y $K$ | Note que aunque $s(r)=0$ detenga la acumulación de $K$ para $r$ muy alto, el crecimiento continuo de $L$ a tasa $n$ reduce $r$ y reactiva el ahorro. |
| `D-C09-03` | Signo del ahorro s(r) | conceptual_swap | high | $s'(r)>0$ al caer rendimiento | Considere el supuesto del experimento: el ahorro depende positivamente del rendimiento $q/p$ y, por ende, inversamente de la razón capital-trabajo $r$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | Elasticidad constante $h$ en (14) y función de ahorro $s(r)$ decreciente | Bajo una oferta laboral general $L=G(t,w/p)$ la razón $r^*$ sí cambia, y si $s(r)$ fuera creciente podría desestabilizar el equilibrio. | - |

---

### [C-10] Tributación sobre la Renta y Crecimiento Poblacional Endógeno (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 27: Tributación sobre la Renta y Crecimiento Poblacional Endógeno
- **Prerequisites:** C-09
- **Recommended Modalities:** invariant_canvas, concept_matching, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 27)

#### Description & Cognitive Model
Un impuesto proporcional $t$ cuya fracción $v$ se invierte transforma la tasa de ahorro en $s+(v-s)t$; al endogenizar la población vía $n(r)$, la ecuación $\dot{r}=sF(r,1)-n(r)r$ puede generar un equilibrio estable $r_1$ y un umbral crítico inestable $r_2$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C10-01` | Impuesto siempre reduce ahorro | conceptual_swap | high | $s_{ef}=s(1-t)$ siempre | Incluya la fracción $v$ de la recaudación $tY$ invertida por el Estado: $s_{ef}=s(1-t)+vt=s+(v-s)t$, que supera a $s$ si $v>s$. |
| `D-C10-02` | Confunde estabilidad de r1 y r2 | conceptual_swap | high | $r_1$ inestable y $r_2$ estable | Analice el signo de $\dot{r}=sF(r,1)-n(r)r$: debajo de $r_2$ pero encima de $r_1$ se cumple $\dot{r}<0$ regresando a $r_1$, mientras que $r>r_2$ dispara expansión sostenida. |
| `D-C10-03` | Requiere rendimientos crecientes | conceptual_swap | high | Trampa exige $F$ no cóncava | Observe que el umbral de estancamiento-expansión surge únicamente de la curvatura de $n(r)r$ con rendimientos constantes a escala y sin indivisibilidades. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C10-01` | - | Impuesto proporcional $t$ con fracción invertida $v$ y tasa poblacional $n(r)$ | Impuestos no proporcionales distorsionan los diagramas de forma no uniforme y otra forma de $n(r)$ altera el número de equilibrios. | - |

---

### [Hab-10] Rigidez Salarial y Preferencia por la Liquidez (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 29: Rigidez Salarial y Preferencia por la Liquidez
- **Prerequisites:** C-06, C-10
- **Recommended Modalities:** unstructured_model, adversarial_break, open_symbolic
- **Evidence Citations:** `solow1956.pdf` (page 29)

#### Description & Cognitive Model
Un salario real rígido $\bar{w}/p$ fija la razón capital-trabajo en $\bar{r}$ y el crecimiento del empleo en $\frac{\dot{L}}{L}=\frac{s}{\bar{r}}F(\bar{r},1)$ (desempleo si es menor que $n$); además, la demanda monetaria $\bar{M}=Q(Y,q/p)$ determina el capital en uso $K(t)$ y genera subutilización en una trampa de liquidez.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab10-01` | Desempleo si tasa > n | skipped_step | high | $\frac{s}{\bar{r}}F(\bar{r},1)>n \Rightarrow$ desempleo | Compare el crecimiento del empleo con el de la fuerza laboral $n$: cuando $\frac{s}{\bar{r}}F(\bar{r},1)<n$ aparece desempleo; si es mayor, surge escasez de mano de obra. |
| `D-Hab10-02` | r sigue variando | skipped_step | high | $K/L$ ajusta libremente con $\bar{w}/p$ | Recuerde que $\partial F/\partial L$ depende solo de $r$; al fijar $\bar{w}/p$, la empresa fija $\bar{r}$ y ajusta la cantidad empleada $L$ a tasa $sF(\bar{r},1)/\bar{r}$. |
| `D-Hab10-03` | Confunde pendiente del rayo | conceptual_swap | high | $\frac{s}{\bar{r}}F(\bar{r},1)$ es derivada $sF'(\bar{r},1)$ | Identifique geométricamente $\frac{s}{\bar{r}}F(\bar{r},1)$ como la pendiente del rayo desde el origen hasta la curva $sF(r,1)$ en el punto $\bar{r}$. |
| `D-Hab10-04` | Trampa con interés bajo | conceptual_swap | high | Subutilización si $i$ rígido bajo $r^*$ | Note que la subutilización del capital ocurre cuando el piso rígido de la tasa de interés queda por encima del nivel correspondiente al $r^*$ de equilibrio. |
| `D-Hab10-05` | Omite papel monetario | conceptual_swap | high | Modelo real basta con preferencia por liquidez | Reconozca que al elegir entre efectivo y capital físico mediante $\bar{M}=Q(Y,q/p)$, el nivel de precios $p$ y la dinámica monetaria se vuelven esenciales. |
| `D-Hab10-06` | K en uso igual a K disponible | conceptual_swap | high | $K(t)$ de (15) siempre iguala al stock total | Contraste el capital en uso $K(t)$ resuelto de $\bar{M}=Q(F(K,L),F_K(K,L))$ frente al stock disponible acumulado para medir el exceso de oferta o demanda. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab10-01` | - | Salario real rígido $\bar{w}/p$ o tasa de interés rígida en trampa de liquidez | Si salarios y precios son plenamente flexibles sin fricciones monetarias, se restaura el pleno empleo neoclásico. | - |

---
