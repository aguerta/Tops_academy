# Cognitive Task Analysis (CTA): Solow V15 M20

- **Course ID:** `solow_v15_m20`
- **Macro-Competency:** Dominio y aplicación analítica integral de Solow V15 M20
- **Structure:** 18 total competencies (1 Facts, 9 Concepts, 8 Skills) with 89 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Marco de Referencia de Solow | Concept | Analyze | Unidad 2: Marco de Referencia de Solow | - | 4 |
| `H-01` | Supuestos del Modelo de Solow | Fact | Understand | Unidad 3: Supuestos del Modelo de Solow | - | 3 |
| `Hab-01` | Ecuación Fundamental de Solow | Skill | Evaluate | Unidad 3: Ecuación Fundamental de Solow | C-01, H-01 | 10 |
| `C-02` | Análisis Cualitativo y Línea de Fase | Concept | Evaluate | Unidad 3: Análisis Cualitativo y Línea de Fase | Hab-01 | 3 |
| `C-04` | Estabilidad y Crecimiento Balanceado | Concept | Evaluate | Unidad 7: Estabilidad y Crecimiento Balanceado | Hab-01 | 3 |
| `C-03` | Estado Uniforme y Progreso Tecnológico | Concept | Evaluate | Unidad 4: Estado Uniforme y Progreso Tecnológico | C-02, C-04 | 3 |
| `Hab-02` | Solución Cuantitativa Cobb-Douglas | Skill | Evaluate | Unidad 5: Solución Cuantitativa Cobb-Douglas | Hab-01, C-02, C-04 | 10 |
| `C-05` | Modelo de Proporciones Fijas | Concept | Analyze | Unidad 10: Modelo de Proporciones Fijas | C-04 | 3 |
| `Hab-04` | Dinámica en Proporciones Fijas | Skill | Evaluate | Unidad 12: Dinámica en Proporciones Fijas | C-05 | 6 |
| `Hab-06` | Producción Sin Capital Esencial | Skill | Evaluate | Unidad 14: Producción Sin Capital Esencial | C-04 | 6 |
| `C-06` | Precios Competitivos de Factores | Concept | Analyze | Unidad 16: Precios Competitivos de Factores | H-01, C-04 | 5 |
| `Hab-07` | Arbitraje Intertemporal y Tasa Propia | Skill | Evaluate | Unidad 17: Arbitraje Intertemporal y Tasa Propia | C-06 | 6 |
| `C-08` | Dinámica de Precios Relativos en Isocuantas | Concept | Analyze | Unidad 19: Dinámica de Precios Relativos en Isocuantas | C-06 | 3 |
| `Hab-08` | Participación Factorial en Funciones de Producción | Skill | Evaluate | Unidad 21: Participación Factorial en Funciones de Producción | C-06 | 6 |
| `Hab-09` | Cambio Tecnológico Neutral y Crecimiento Asintótico | Skill | Evaluate | Unidad 22: Cambio Tecnológico Neutral y Crecimiento Asintótico | C-06 | 6 |
| `C-09` | Oferta Elástica de Trabajo y Ahorro Variable | Concept | Analyze | Unidad 24: Oferta Elástica de Trabajo y Ahorro Variable | C-06 | 3 |
| `Hab-10` | Tributación Proporcional y Población Endógena | Skill | Evaluate | Unidad 26: Tributación Proporcional y Población Endógena | C-09 | 6 |
| `C-10` | Rigidez Salarial y Preferencia por la Liquidez | Concept | Evaluate | Unidad 29: Rigidez Salarial y Preferencia por la Liquidez | C-06, C-08 | 3 |

---

## Detailed Competency Specifications

### [C-01] Marco de Referencia de Solow (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 2: Marco de Referencia de Solow
- **Prerequisites:** None
- **Recommended Modalities:** multiple_select, adversarial_break, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
Función de producción linealmente homogénea $Q=f(K,L)=L\phi(k)$ con $k\equiv K/L$, $\phi'(k)>0$, $\phi''(k)<0$ e hipótesis $\dot{K}=sQ$, $\dot{L}/L=\lambda$

#### Fused Distractor Models (4)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Proporciones fijas | conceptual_swap | high | $Q=\rho K$ | Distinga el modelo de Domar del marco de Solow, donde capital $K$ y trabajo $L$ se combinan en proporciones variables. |
| `D-C01-02` | Retornos crecientes | conceptual_swap | high | $\phi''(k)>0$ | Recuerde que los retornos marginales decrecientes $f_{KK}<0$ implican $\phi''(k)=Lf_{KK}<0$ para todo capital positivo. |
| `D-C01-03` | Ahorro sobre capital | conceptual_swap | high | $\dot{K}=sK$ | Aplique la propensión marginal al ahorro $s$ sobre el flujo de producto $Q$, nunca sobre el stock de capital $K$. |
| `D-C01-04` | Trabajo constante | conceptual_swap | high | $\dot{L}=0$ | Incluya la hipótesis dinámica de crecimiento exponencial de la mano de obra $\dot{L}/L=\lambda$ con tasa constante $\lambda>0$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Homogeneidad lineal de $f(K,L)$ con $K,L>0$ | Sin retornos constantes a escala no puede reducirse $Q$ a $L\phi(k)$. | - |
| `A-C01-02` | - | Productividades marginales positivas $f_K,f_L>0$ y decrecientes $f_{KK},f_{LL}<0$ | Sin concavidad $\phi''(k)<0$ no se garantiza productividad marginal decreciente de $k$. | - |

---

### [H-01] Supuestos del Modelo de Solow (Fact)

- **Bloom Level:** Understand
- **Session:** Unidad 3: Supuestos del Modelo de Solow
- **Prerequisites:** None
- **Recommended Modalities:** fill_in_the_blank, multiple_select, proof_dag
- **Evidence Citations:** `solow1956.pdf` (page 3)

#### Description & Cognitive Model
El modelo básico de crecimiento neoclásico combina acumulación $\dot{K}=sY$, producción homogénea de grado uno $Y=F(K,L)$ y oferta laboral inelástica $L(t)=L_0 e^{nt}$ en pleno empleo.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Ahorro sobre capital | conceptual_swap | high | $\dot{K}=sK$ | Aplique la tasa de ahorro $s$ sobre el flujo de ingreso neto $Y$, no sobre el stock de capital acumulado $K$. |
| `D-H01-02` | Rendimientos decrecientes globales | conceptual_swap | high | $F(\lambda K,\lambda L)<\lambda Y$ | Recuerde que la ausencia de factores fijos como la tierra implica rendimientos constantes a escala en capital y trabajo. |
| `D-H01-03` | Crecimiento lineal laboral | conceptual_swap | high | $L(t)=L_0+nt$ | Modele el crecimiento exógeno de la fuerza laboral a tasa relativa constante $n$ mediante la función exponencial $L_0 e^{nt}$. |

---

### [Hab-01] Ecuación Fundamental de Solow (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Ecuación Fundamental de Solow
- **Prerequisites:** C-01, H-01
- **Recommended Modalities:** proof_dag, open_symbolic, fill_in_the_blank, adversarial_break
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3), `solow1956.pdf` (page 6)

#### Description & Cognitive Model
Derivación de la ecuación diferencial fundamental $\dot{k}=s\phi(k)-\lambda k$ (o $\dot{r}=sF(r,1)-nr$) para la razón capital-trabajo $k=r=K/L$ diferenciando $K=kL$ y explotando la homogeneidad de grado uno de la función de producción.

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Omite regla producto | skipped_step | high | $\dot{k}=s\phi(k)$ | Aplique la regla del producto al diferenciar $K=kL$ para obtener $\dot{K}=L\dot{k}+k\dot{L}$ antes de sustituir $\dot{L}=\lambda L$. |
| `D-Hab01-07` | Omite dilución laboral | skipped_step | high | $\dot{r}=sF(r,1)$ | Al diferenciar $K=rL_0 e^{nt}$ respecto al tiempo, incluya el término de dilución $nr$ generado por el crecimiento laboral. |
| `D-Hab01-02` | Signo invertido | skipped_step | high | $\dot{k}=s\phi(k)+\lambda k$ | Al despejar $L\dot{k}=sL\phi(k)-k\lambda L$, reste el término de dilución $\lambda k$ en lugar de sumarlo. |
| `D-Hab01-08` | Signo invertido dilución | skipped_step | high | $\dot{r}=sF(r,1)+nr$ | Reste la tasa de crecimiento laboral $n$ al despejar $\dot{r}/r = \dot{K}/K - \dot{L}/L$, pues mayor población diluye $r$. |
| `D-Hab01-03` | Conserva factor L | skipped_step | high | $\dot{k}=sL\phi(k)-\lambda k$ | Divida ambos miembros de $L\dot{k}+k\lambda L=sL\phi(k)$ por el factor común positivo $L$ para quedar solo en $k$. |
| `D-Hab01-09` | No divide F por L | conceptual_swap | high | $\dot{r}=sF(r,L)-nr$ | Aplique la homogeneidad de primer grado dividiendo ambos argumentos de $F(K,L)$ entre $L$ para obtener $LF(r,1)$. |
| `D-Hab01-04` | Multiplica por s | conceptual_swap | high | $\dot{k}=s(\phi(k)-\lambda k)$ | Mantenga la propensión al ahorro $s$ multiplicando únicamente al producto per cápita $\phi(k)$, no a la dilución $\lambda k$. |
| `D-Hab01-05` | Confunde nivel con tasa | conceptual_swap | high | $\dot{k}/k=s\phi(k)-\lambda$ | Si divide la ecuación fundamental entre $k$, debe dividir también $s\phi(k)$ entre $k$ para obtener $s\phi(k)/k-\lambda$. |
| `D-Hab01-10` | Multiplica por L0 | conceptual_swap | high | $\dot{r}=sL_0 F(r,1)-nr$ | Cancele completamente el factor común $L_0 e^{nt}$ en ambos miembros de la ecuación tras factorizar $L$ desde $F(K,L)$. |
| `D-Hab01-06` | Invierte ahorro | conceptual_swap | high | $\dot{k}=\lambda\phi(k)-sk$ | Asocie $s$ a la inversión per cápita $s\phi(k)$ y $\lambda$ al crecimiento laboral que diluye el capital $k$. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Fuerza laboral estrictamente positiva $L(t)>0$ en todo instante | Si $L=0$, la razón $k=K/L$ es indefinida y no puede eliminarse $L$. | - |
| `A-Hab01-02` | - | Homogeneidad de primer grado $F(\lambda K,\lambda L)=\lambda F(K,L)$ | Sin rendimientos constantes a escala no puede reducirse el sistema a la única variable $r=K/L$. | - |
| `A-Hab01-03` | - | Pleno empleo continuo de capital y fuerza laboral $L(t)=L_0 e^{nt}$ | Si hay desempleo variable, la tasa de crecimiento del empleo difiere de $n$ y se invalida la ecuación. | - |

---

### [C-02] Análisis Cualitativo y Línea de Fase (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Análisis Cualitativo y Línea de Fase
- **Prerequisites:** Hab-01
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
Análisis de estabilidad del equilibrio intertemporal $\bar{k}>0$ mediante las curvas $s\phi(k)$, $\lambda k$ y la línea de fase $\dot{k}=s\phi(k)-\lambda k$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Pendiente positiva | conceptual_swap | high | $\frac{d\dot{k}}{dk}\big|_{\bar{k}}>0$ | Verifique en la línea de fase que la estabilidad requiere pendiente negativa en $\bar{k}$: $\dot{k}>0$ a la izquierda y $\dot{k}<0$ a la derecha. |
| `D-C02-02` | Equilibrio en origen | conceptual_swap | high | $\bar{k}=0$ es el único equilibrio | Reconozca que aunque $s\phi(0)=0=\lambda\cdot 0$, existe un cruce positivo $\bar{k}>0$ porque $s\phi(k)$ supera inicialmente a $\lambda k$. |
| `D-C02-03` | Distancia horizontal | conceptual_swap | high | $\dot{k}$ es distancia horizontal entre curvas | Mida el valor de $\dot{k}=s\phi(k)-\lambda k$ como la distancia vertical entre la curva $s\phi(k)$ y el rayo $\lambda k$ para cada $k$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | Existe un rango de $k>0$ donde $s\phi(k)>\lambda k$ y $K$ es indispensable ($\phi(0)=0$) | Si $s\phi(k)\le\lambda k$ para todo $k>0$, no existe intersección positiva $\bar{k}$. | - |

---

### [C-04] Estabilidad y Crecimiento Balanceado (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 7: Estabilidad y Crecimiento Balanceado
- **Prerequisites:** Hab-01
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 7)

#### Description & Cognitive Model
Análisis cualitativo de $\dot{r}=sF(r,1)-nr$: un equilibrio $r^*$ es estable cuando $sF(r,1)$ corta a $nr$ desde arriba, convergiendo al crecimiento balanceado a tasa $n$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Cruce inestable como estable | conceptual_swap | high | Todo punto donde $sF(r,1)=nr$ es estable | Verifique el signo de $\dot{r}$ a izquierda y derecha: si $sF(r,1)$ cruza a $nr$ desde abajo, el equilibrio $r_2$ es inestable. |
| `D-C04-02` | Existencia garantizada siempre | conceptual_swap | high | Siempre existe un equilibrio $r^*>0$ | Considere casos como $s_1 F^1(r,1)=nr+\sqrt{r}$ o $s_2 F^2(r,1)=nr/(r+1)$ donde las curvas nunca se intersectan. |
| `D-C04-03` | Crecimiento exponencial exacto | conceptual_swap | high | El capital crece a tasa $n$ para todo $t$ | Distinga la convergencia asintótica de la trayectoria transitoria: si $r<r^*$, el capital crece más rápido que $n$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | Productividad marginal del capital positiva y decreciente para el caso estándar | Si la curva $sF(r,1)$ no es cóncava hacia abajo, pueden surgir equilibrios múltiples o inestables. | - |
| `A-C04-02` | - | Stock inicial de capital estrictamente positivo $K_0>0$ | Si $K_0=0$ y ambos insumos son esenciales, $r=0$ y la economía no puede iniciar la acumulación. | - |

---

### [C-03] Estado Uniforme y Progreso Tecnológico (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Estado Uniforme y Progreso Tecnológico
- **Prerequisites:** C-02, C-04
- **Recommended Modalities:** adversarial_break, unstructured_model, multiple_select
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
Crecimiento equiproporcional a tasa $\lambda$ de $K,L,Q$ e inversión neta en $\bar{k}$, y desplazamiento al alza de $\bar{k}$ bajo progreso tecnológico $Q=T(t)f(K,L)$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Estado estacionario nulo | conceptual_swap | high | $\dot{K}=\dot{Q}=0$ en $\bar{k}$ | Distinga el estado estacionario (tasas cero) del estado uniforme, donde $K,L,Q$ y $\dot{K}$ crecen todos a la tasa idéntica $\lambda>0$. |
| `D-C03-02` | Desplazamiento rayo | conceptual_swap | high | $dT/dt>0$ desplaza $\lambda k$ hacia arriba | Note que $T(t)$ multiplica la función de producción, desplazando hacia arriba la curva $s\phi(k)$ y aumentando $\bar{k}$ con $\lambda k$ fijo. |
| `D-C03-03` | Menor capital por trabajador | conceptual_swap | high | $dT/dt>0$ reduce $\bar{k}$ | Al desplazarse hacia arriba $s\phi(k)$ frente al rayo $\lambda k$, las intersecciones sucesivas ocurren a niveles mayores de $\bar{k}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | Tecnología creciente $T(t)$ con $dT/dt>0$ en la función $Q=T(t)f(K,L)$ | Si $T(t)$ fuera constante, la curva $s\phi(k)$ sería invariante y $\bar{k}$ no crecería. | - |

---

### [Hab-02] Solución Cuantitativa Cobb-Douglas (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Solución Cuantitativa Cobb-Douglas
- **Prerequisites:** Hab-01, C-02, C-04
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 5), `solow1956.pdf` (page 13)

#### Description & Cognitive Model
Resolución analítica de la dinámica Cobb-Douglas mediante la ecuación de Bernoulli $\dot{k}+\lambda k=sk^\alpha$ o integración directa de $\dot{K}=sK^a(L_0 e^{nt})^{1-a}$ para hallar $k(t)$, $K(t)$, el estado uniforme $r^*=(s/n)^{1/(1-a)}$ y el coeficiente capital-producto $C=s/n$.

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Sustitución errónea | skipped_step | high | $z=k^\alpha$ | Para linealizar $\dot{k}+\lambda k=sk^\alpha$ (Bernoulli con $m=\alpha$), aplique el cambio $z=k^{1-m}=k^{1-\alpha}$, no $k^\alpha$. |
| `D-Hab02-07` | Exponente sin invertir | skipped_step | high | $r^*=(s/n)^{1-a}$ | Al despejar $r^{1-a}=s/n$, eleve ambos lados al recíproco $1/(1-a)$ para obtener el capital por trabajador estacionario. |
| `D-Hab02-02` | Omite factor 1-alpha | skipped_step | high | $\frac{dz}{dt}+\lambda z=s$ | Al diferenciar $z=k^{1-\alpha}$, aparece el factor $(1-\alpha)$ que multiplica tanto a $\lambda z$ como a $s$ en la ecuación lineal. |
| `D-Hab02-08` | Invierte razón s/n | skipped_step | high | $r^*=(n/s)^{\frac{1}{1-a}}$ | Iguale $sr^a=nr$ para obtener $r^{1-a}=s/n$; mayor ahorro $s$ eleva $r^*$ y mayor crecimiento laboral $n$ lo reduce. |
| `D-Hab02-03` | Exponente directo | skipped_step | high | $k\to(s/\lambda)^{1-\alpha}$ | Dado que $k^{1-\alpha}\to s/\lambda$, eleve ambos lados al exponente recíproco $1/(1-\alpha)$ para despejar el valor límite de $k$. |
| `D-Hab02-09` | Omite condición inicial K0 | conceptual_swap | high | $K(t)=[\frac{s}{n}L_0^b e^{nbt}]^{1/b}$ | Evalúe la constante de integración en $t=0$ para incluir el término transitorio $K_0^b-\frac{s}{n}L_0^b$ dentro del corchete. |
| `D-Hab02-04` | Razón invertida | conceptual_swap | high | $k\to(\lambda/s)^{\frac{1}{1-\alpha}}$ | Verifique que el término constante $b/a=((1-\alpha)s)/((1-\alpha)\lambda)=s/\lambda$ implica relación directa con $s$ e inversa con $\lambda$. |
| `D-Hab02-10` | Coeficiente capital-producto erróneo | conceptual_swap | high | $C=(s/n)^{a/b}$ | Distinga el ingreso por trabajador $Y/L=(s/n)^{a/b}$ de la razón capital-producto $K/Y=r/r^a=r^b=s/n$. |
| `D-Hab02-05` | Exponente positivo | conceptual_swap | high | $e^{+(1-\alpha)\lambda t}$ | Como el coeficiente de $z$ es $+(1-\alpha)\lambda>0$, el factor integrante produce $e^{-(1-\alpha)\lambda t}$, que converge a cero al crecer $t$. |
| `D-Hab02-11` | Exponente erróneo en exponencial | conceptual_swap | high | $e^{nt}$ dentro del corchete de $K(t)$ | Multiplique $(1-a)=b$ por $nt$ antes de integrar $e^{n(1-a)t}$, obteniendo $e^{nbt}/(nb)$ al resolver la ecuación lineal en $K^b$. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Parámetro Cobb-Douglas $\alpha\in(0,1)$ y crecimiento laboral $\lambda>0$ | Si $\alpha\ge 1$ o $\lambda\le 0$, el término exponencial no decae a cero ni hay convergencia. | - |
| `A-Hab02-02` | - | Participación del capital $0<a<1$ en la función Cobb-Douglas | Si $a\ge 1$, la productividad marginal del capital no decrece y desaparece el equilibrio estacionario único. | - |
| `A-Hab02-03` | - | Dotaciones iniciales positivas $K_0>0$ y $L_0>0$ | Si $K_0=0$ o $L_0=0$, el producto inicial es nulo y no hay acumulación. | - |

---

### [C-05] Modelo de Proporciones Fijas (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 10: Modelo de Proporciones Fijas
- **Prerequisites:** C-04
- **Recommended Modalities:** adversarial_break, invariant_canvas, multiple_select
- **Evidence Citations:** `solow1956.pdf` (page 10)

#### Description & Cognitive Model
En el caso Harrod-Domar $Y=\min(K/a, L/b)$, la ecuación $\dot{r}=s\min(r/a, 1/b)-nr$ genera rigidez de filo de navaja entre la tasa garantizada $s/a$ y la tasa natural $n$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Suma de factores | conceptual_swap | high | $Y=K/a+L/b$ | Represente las isocuantas en ángulo recto mediante $\min(K/a, L/b)$, pues el primer cuello de botella limita la producción. |
| `D-C05-02` | Tasa garantizada errónea | conceptual_swap | high | La tasa garantizada es $s/b$ | Divida la tasa de ahorro $s$ entre el coeficiente de aceleración del capital $a$ para obtener la tasa garantizada $s/a$. |
| `D-C05-03` | Ajuste por precios flexibles | conceptual_swap | high | La razón $r$ se ajusta sin redundancia | Reconozca que bajo proporciones fijas, si $n\neq s/a$, surge redundancia de trabajo o capital independientemente de precios. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Coeficientes técnicos fijos $a,b>0$ sin sustitución entre capital y trabajo | Si existe un rango variable entre $r_{\min}$ y $r_{\max}$, aparece toda una zona de tasas de crecimiento estables. | - |
| `A-C05-02` | - | Tasa de ahorro $s$ y crecimiento laboral $n$ constantes y exógenos | Cambios en $s$ o $n$ alteran la comparación crítica entre la tasa garantizada $s/a$ y la tasa natural. | - |

---

### [Hab-04] Dinámica en Proporciones Fijas (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 12: Dinámica en Proporciones Fijas
- **Prerequisites:** C-05
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 12)

#### Description & Cognitive Model
Resolución de las trayectorias $r(t)$ y cálculo de redundancia de trabajo o capital en $Y=\min(K/a,L/b)$ según $n>s/a$, $n=s/a$ o $n<s/a$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Equilibrio con exceso de capital | skipped_step | high | $r^*=a/b$ cuando $n_3 < s/a$ | Iguale $s/b - n_3 r = 0$ en el tramo horizontal de la función quebrada para obtener el equilibrio estable $r^*=s/(n_3 b)>a/b$. |
| `D-Hab04-02` | Fracción de capital invertida | skipped_step | high | Proporción empleada $s/(an_3)$ | Divida el capital requerido $(a/b)$ entre el capital disponible $s/(n_3 b)$ para obtener la proporción empleada $an_3/s < 1$. |
| `D-Hab04-03` | Estabilidad con n1 > s/a | conceptual_swap | high | $r\to s/(n_1 b)$ cuando $n_1 > s/a$ | Note que $s/(n_1 b)<a/b$, por lo que $r$ cruza $a/b$ en $t_1$ y luego decrece hacia cero siguiendo $\dot{r}=(s/a-n_1)r$. |
| `D-Hab04-04` | Empleo cuando K es cuello | conceptual_swap | high | Empleo igual a $aK/b$ | Multiplique el producto limitado por capital $Y=K/a$ por el requerimiento laboral unitario $b$ para obtener empleo $bK/a$. |
| `D-Hab04-05` | Equilibrio único cuando n2=s/a | conceptual_swap | high | Siempre converge a $a/b$ si $n_2=s/a$ | Verifique que para $r_0 < a/b$ se cumple $\dot{r}=(s/a-n_2)r=0$, preservando indefinidamente el porcentaje inicial de desempleo. |
| `D-Hab04-06` | Exceso de capacidad constante | conceptual_swap | high | El exceso absoluto de capital es constante | Recuerde que aunque la proporción empleada $an_3/s$ sea constante, el stock $K$ crece a tasa $n_3$ y la capacidad ociosa crece. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Parámetros positivos $s,a,b,n>0$ con tecnología de coeficientes fijos | Si alguno de los parámetros es nulo o variable, cambian los puntos de quiebre y las tasas de convergencia. | - |

---

### [Hab-06] Producción Sin Capital Esencial (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 14: Producción Sin Capital Esencial
- **Prerequisites:** C-04
- **Recommended Modalities:** open_symbolic, adversarial_break, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 14)

#### Description & Cognitive Model
Análisis de $Y=(a\sqrt{K}+\sqrt{L})^2$ mediante $\dot{r}=s(a\sqrt{r}+1)^2-nr$: condición de equilibrio estable $sa^2<n$ con $r^*=(1/(\sqrt{n/s}-a))^2$ y crecimiento perpetuo si $sa^2>n$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Umbral de convergencia invertido | skipped_step | high | Existe equilibrio estable si $sa^2 > n$ | Observe que cuando $sa^2 > n$, ambos factores $(a\pm\sqrt{n/s})$ o la asíntota de $s(a\sqrt{r}+1)^2$ superan siempre a $nr$. |
| `D-Hab06-02` | Signo erróneo en r* | skipped_step | high | $r^*=(\frac{1}{\sqrt{n/s}+a})^2$ | Iguale $\sqrt{s}(a\sqrt{r}+1)=\sqrt{n}\sqrt{r}$ y agrupe $(\sqrt{n/s}-a)\sqrt{r}=1$ para obtener el signo negativo en $-a$. |
| `D-Hab06-03` | Olvida elevar al cuadrado | conceptual_swap | high | $r^*=\frac{1}{\sqrt{n/s}-a}$ | Recuerde que $1/(\sqrt{n/s}-a)$ corresponde a $\sqrt{r^*}$, por lo que debe elevar al cuadrado para despejar $r^*$. |
| `D-Hab06-04` | Ordenada al origen nula | conceptual_swap | high | La curva $sF(r,1)$ pasa por el origen | Evalúe $s(a\sqrt{0}+1)^2=s>0$: como la producción es posible solo con trabajo, la curva parte desde altura $s$. |
| `D-Hab06-05` | Ingreso límite erróneo | conceptual_swap | high | $y^*=1/(1-a\sqrt{n/s})^2$ | Sustituya $\sqrt{r^*}$ en $(a\sqrt{r^*}+1)^2$ y divida numerador y denominador por $\sqrt{n/s}$ para obtener $1/(1-a\sqrt{s/n})^2$. |
| `D-Hab06-06` | Desarrollo binomial incompleto | conceptual_swap | high | $Y=a^2 K+L$ | Expanda el cuadrado del binomio $(a\sqrt{K}+\sqrt{L})^2$ incluyendo el doble producto $2a\sqrt{KL}$ en la función de producción. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Parámetro de sustitución $0<p<1$ en $Y=(aK^p+L^p)^{1/p}$ | Si $p\ge 1$, se pierde la convexidad estándar de las isocuantas y los rendimientos marginales decrecientes. | - |
| `A-Hab06-02` | - | Positividad de parámetros $a,s,n>0$ | Si $a=0$ o $s=0$, desaparece la contribución del capital o la acumulación neta. | - |

---

### [C-06] Precios Competitivos de Factores (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 16: Precios Competitivos de Factores
- **Prerequisites:** H-01, C-04
- **Recommended Modalities:** proof_dag, multiple_select, adversarial_break, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 16)

#### Description & Cognitive Model
En competencia perfecta bajo rendimientos constantes a escala, el salario real $\partial F/\partial L = w/p$ y la renta real del capital $\partial F/\partial K = q/p$ dependen únicamente de $r=K/L$.

#### Fused Distractor Models (5)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Dependencia de escala absoluta | conceptual_swap | high | $\partial F/\partial L$ depende de $K$ y $L$ por separado | Aplique el teorema de Euler para funciones homogéneas de grado uno: las derivadas parciales son homogéneas de grado cero en $(K,L)$. |
| `D-C06-04` | Dependencia de escala | conceptual_swap | high | $w/p$ y $q/p$ dependen del tamaño absoluto $L$ y $K$ | Recuerde que bajo rendimientos constantes a escala las derivadas parciales son homogéneas de grado cero y solo dependen de $r=K/L$. |
| `D-C06-02` | Determinación del nivel de precios | conceptual_swap | high | El modelo real determina el nivel absoluto $p(t)$ | Distinga precios relativos de precios nominales: sin ecuación monetaria, el sistema real solo fija $w/p$ y $q/p$, tomando $p(t)$ dado. |
| `D-C06-05` | Confusión nominal-real | conceptual_swap | high | $\partial F/\partial L = w$ sin dividir por $p$ | Divida el salario y la renta nominales por el precio del producto $p(t)$ porque las productividades marginales están en unidades físicas. |
| `D-C06-03` | Iguala renta a tasa de interés | conceptual_swap | high | $q/p$ siempre es igual a $i(t)$ sin ganancias de capital | Separe la renta física por unidad de capital $q/p$ del precio de transferencia $p(t)$ y la tasa de interés $i(t)$. |

#### Formal Mathematical Assumptions (4)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Mercados competitivos con ajuste instantáneo de salario y renta para vaciar factores | Con rigideces salariales o competencia monopolística, las productividades marginales dejan de igualar los precios reales. | - |
| `A-C06-02` | - | Nivel absoluto de precios $p(t)$ dado exógenamente en el sistema real | Sin fijar el numerario o una regla monetaria, los precios nominales $w(t)$ y $q(t)$ quedan indeterminados. | - |
| `A-C06-03` | - | Competencia perfecta y rendimientos constantes a escala en $F(K,L)$ | Sin homogeneidad de grado uno las productividades marginales dependerían de la escala. | - |
| `A-C06-04` | - | Nivel absoluto de precios $p(t)$ exógeno o dado | Solo se determinan los tres precios relativos o tasas ($w/p$, $q/p$, $i$). | - |

---

### [Hab-07] Arbitraje Intertemporal y Tasa Propia (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 17: Arbitraje Intertemporal y Tasa Propia
- **Prerequisites:** C-06
- **Recommended Modalities:** open_symbolic, proof_dag, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 17)

#### Description & Cognitive Model
Derivación y aplicación de la condición de arbitraje perfecto $i(t) = q(t)/p(t) + \dot{p}(t)/p(t)$ y su forma integral de valor presente $p(t) = \int_t^\infty q(u)e^{-\int_t^u i(z)dz}du$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Omite variación de precios | skipped_step | high | $i(t) = q(t)/p(t)$ siempre | Incluya la ganancia o pérdida de capital $\dot{p}(t)/p(t)$ al comparar el rendimiento monetario de prestar dinero frente a mantener capital. |
| `D-Hab07-02` | Signo invertido en inflación | skipped_step | high | $i(t) = q(t)/p(t) - \dot{p}(t)/p(t)$ | Si el precio cae ($\dot{p}<0$), el poseedor del bien sufre pérdida de capital y exige una tasa propia $q/p$ mayor que $i$ para mantenerlo. |
| `D-Hab07-03` | Confunde renta nominal con real | conceptual_swap | high | $i(t) = q(t) + \dot{p}(t)/p(t)$ | Exprese la renta nominal $q(t)$ como tasa propia dividiendo por el precio de transferencia $p(t)$ del bien de capital. |
| `D-Hab07-04` | Descuenta con tasa propia | conceptual_swap | high | $p(t) = \int_t^\infty q(u)e^{-\int_t^u (q(z)/p(z))dz}du$ | Descuente los flujos futuros de renta nominal $q(u)$ utilizando la tasa de interés monetaria $i(z)$ para obtener el precio $p(t)$. |
| `D-Hab07-05` | Omite horizonte infinito | conceptual_swap | high | $p(t) = q(t)/i(t)$ sin expectativas | Integre la trayectoria futura de $q(u)$ descontada por la integral de $i(z)$ cuando las rentas y tasas varían en el tiempo. |
| `D-Hab07-06` | Ignora ausencia de riesgo | conceptual_swap | high | Incluye prima de riesgo exógena en $i(t)$ | Recuerde que la ecuación (12) supone previsión perfecta y ausencia de riesgo, eliminando preferencias diferenciadas entre activos. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Previsión perfecta, arbitraje sin fricciones y ausencia de riesgo | Con incertidumbre la igualdad exacta entre $i$ y $q/p + \dot{p}/p$ deja de cumplirse. | - |

---

### [C-08] Dinámica de Precios Relativos en Isocuantas (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 19: Dinámica de Precios Relativos en Isocuantas
- **Prerequisites:** C-06
- **Recommended Modalities:** invariant_canvas, multiple_select, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 19)

#### Description & Cognitive Model
Análisis geométrico de la razón salarial-renta $w/q$ a lo largo de trayectorias hacia rayos de equilibrio en mapas de isocuantas (Fig. VI y VII) y su degeneración en proporciones fijas Harrod-Domar.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Indeterminación fuera de esquina | conceptual_swap | high | $w/q$ es indeterminado para cualquier $r$ en Harrod-Domar | Distinga que en Harrod-Domar solo es indeterminado en $r=a/b$; si $r>a/b$ entonces $q=0$ y $w=p/b$, mientras que si $r<a/b$ entonces $w=0$ y $q=p/a$. |
| `D-C08-02` | Dirección errónea de w/q | conceptual_swap | high | Cuando $r$ cae hacia $r^*$, la razón $w/q$ aumenta | Por convexidad normal de las isocuantas, si $r$ disminuye hacia $r^*$, el trabajo se vuelve relativamente más abundante y $w/q$ cae. |
| `D-C08-03` | Confunde rayo inestable con estable | conceptual_swap | high | El rayo interior $r_2$ de la Fig. VII atrae trayectorias cercanas | Identifique el rayo interior $r_2$ como frontera divisoria inestable entre las cuencas de atracción de los rayos estables $r_1$ y $r_3$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C08-01` | - | Isocuantas convexas y diferenciables en el caso neoclásico frente a esquinas rectas en Harrod-Domar | Sin convexidad estricta la razón $w/q$ puede no variar monótonamente con $r$. | - |

---

### [Hab-08] Participación Factorial en Funciones de Producción (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 21: Participación Factorial en Funciones de Producción
- **Prerequisites:** C-06
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 21)

#### Description & Cognitive Model
Cálculo analítico de $w/p$, $q/p$ y la participación del trabajo $(w/p)(L/Y)$ en equilibrio para Cobb-Douglas (constante $1-a$) y para $Y=(a\sqrt{K}+\sqrt{L})^2$ (dependiente de $s$ y $n$: $1-a\sqrt{s/n}$).

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | Participación constante universal | skipped_step | high | $(w/p)(L/Y)$ es independiente de $s$ y $n$ en toda función | Calcule explícitamente $(w/p)(L/Y)$ en $Y=(a\sqrt{K}+\sqrt{L})^2$: obtiene $1-a\sqrt{s/n}$, que sí depende de $s$ y $n$ fuera de Cobb-Douglas. |
| `D-Hab08-02` | Invierte efecto de n | skipped_step | high | Mayor crecimiento poblacional $n$ reduce la participación laboral en $Y=(a\sqrt{K}+\sqrt{L})^2$ | Note que aunque mayor $n$ reduce $w/p$, el término $a\sqrt{s/n}$ disminuye y eleva la participación total $1-a\sqrt{s/n}$ del trabajo. |
| `D-Hab08-03` | Exponente erróneo en salario Cobb-Douglas | conceptual_swap | high | $w/p = (1-a)(s/n)^{1/(1-a)}$ en equilibrio | Sustituya $r^*=(s/n)^{1/(1-a)}$ dentro de $w/p=(1-a)r^a$ para obtener el exponente correcto $a/(1-a)$. |
| `D-Hab08-04` | Renta de equilibrio errónea | conceptual_swap | high | $q/p = a(s/n)$ en Cobb-Douglas | Evalúe $q/p = a(r^*)^{a-1} = a((s/n)^{1/(1-a)})^{a-1} = an/s$ cuidando el signo negativo del exponente. |
| `D-Hab08-05` | Derivada parcial incompleta | conceptual_swap | high | $\partial Y/\partial L = a\sqrt{r}$ para $Y=(a\sqrt{K}+\sqrt{L})^2$ | Aplique la regla de la cadena: $\partial Y/\partial L = 2(a\sqrt{K}+\sqrt{L})\frac{1}{2\sqrt{L}} = a\sqrt{r} + 1$. |
| `D-Hab08-06` | Equilibrio r* incorrecto | conceptual_swap | high | $r^* = (\sqrt{n/s}-a)^2$ en el tercer ejemplo | Iguale $s(a\sqrt{r}+1)^2/r = n$ para despejar $\sqrt{r^*} = 1/(\sqrt{n/s}-a)$ antes de elevar al cuadrado. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab08-01` | - | Existencia de equilibrio balanceado con $\sqrt{n/s} > a$ en $Y=(a\sqrt{K}+\sqrt{L})^2$ | Si $\sqrt{n/s} \le a$, no existe razón capital-trabajo estacionaria finita. | - |

---

### [Hab-09] Cambio Tecnológico Neutral y Crecimiento Asintótico (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 22: Cambio Tecnológico Neutral y Crecimiento Asintótico
- **Prerequisites:** C-06
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 22)

#### Description & Cognitive Model
Resolución de $\dot{K} = s e^{gt} K^a L_0^{1-a} e^{n(1-a)t}$ ($b=1-a$) con progreso neutral $Y=A(t)F(K,L)$ ($A(t)=e^{gt}$), obteniendo crecimiento asintótico de $K$ y $Y$ a tasa $n+g/b$ y de $K/L$ a tasa $g/b$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab09-01` | Omite efecto de A(t) en Y | skipped_step | high | El producto $Y$ crece asintóticamente a tasa $n + ag/b$ | Sume la tasa de progreso técnico $g$ al aporte del capital $a(n+g/b)$ y del trabajo $bn$: $g + a(n+g/b) + bn = n + g/b$. |
| `D-Hab09-02` | Asume r* estacionario finito | skipped_step | high | $K/L$ converge a un nivel constante $r^*$ con $g>0$ | Observe que $A(t)=e^{gt}$ desplaza hacia arriba $sF(r,1)$ continuamente, haciendo que $K/L$ crezca indefinidamente a tasa asintótica $g/b$. |
| `D-Hab09-03` | Tasa de crecimiento de K errónea | conceptual_swap | high | $K$ crece asintóticamente a tasa $n + g$ | Note que al integrar $\dot{K}/K^a$ aparece el exponente $1/b$, lo que amplifica el efecto de $g$ por el multiplicador $1/(1-a)$. |
| `D-Hab09-04` | Confunde crecimiento de K/L | conceptual_swap | high | $K/L$ crece asintóticamente a tasa $n + g/b$ | Reste la tasa de crecimiento de $L$ ($n$) a la tasa de crecimiento de $K$ ($n+g/b$) para obtener la tasa de crecimiento de $K/L$: $g/b$. |
| `D-Hab09-05` | Coeficiente K/Y creciente | conceptual_swap | high | $K/Y$ crece indefinidamente a tasa $g$ | Verifique que tanto $K$ como $Y=e^{gt}K^a L^b$ crecen a la misma tasa asintótica $n+g/b$, por lo que $K/Y$ tiende a una constante. |
| `D-Hab09-06` | Participación laboral variable | conceptual_swap | high | La participación del trabajo $1-a$ cae con el tiempo | Recuerde que el cambio tecnológico neutral de Hicks deja intactas las proporciones de Cobb-Douglas y mantiene constante la participación en $1-a$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab09-01` | - | Progreso tecnológico neutral multiplicativo $Y=e^{gt}K^a L^{1-a}$ con $a \in (0,1)$ | Si el cambio técnico no es neutral o $a\ge 1$, la solución explícita de $K(t)$ cambia. | - |

---

### [C-09] Oferta Elástica de Trabajo y Ahorro Variable (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 24: Oferta Elástica de Trabajo y Ahorro Variable
- **Prerequisites:** C-06
- **Recommended Modalities:** multiple_select, proof_dag, invariant_canvas
- **Evidence Citations:** `solow1956.pdf` (page 24)

#### Description & Cognitive Model
Efecto de una oferta laboral elástica $L=G(t,w/p)$ (y caso isoelástico $L=L_0 e^{nt}(w/p)^h$ donde $r^*$ no cambia) y de una tasa de ahorro decreciente $s(r)$ en $\dot{r}=s(r)F(r,1)-nr$ sobre el equilibrio.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Generaliza invarianza de r* | conceptual_swap | high | Cualquier oferta laboral elástica $L=G(t,w/p)$ deja inalterado $r^*$ | Verifique en (6b) que $r^*$ solo permanece inalterado si $\frac{1}{G}\frac{\partial G}{\partial t} = n$ para todo $r$, como en el caso particular (14). |
| `D-C09-02` | Ahorro variable desestabiliza | conceptual_swap | high | Un $s(r)$ decreciente facilita el crecimiento ilimitado de $r$ | Analice que si $s(r)$ cae cuando $r$ sube (y se anula para $r$ grande), se frena la acumulación y se elimina el crecimiento explosivo de $r$. |
| `D-C09-03` | Estado estacionario de K | conceptual_swap | high | Si $s(r)$ se anula para $r$ alto, la economía permanece en estado estacionario sin caída de $r$ | Note que aunque $s(r)=0$ detenga la inversión neta, el crecimiento continuo de $L$ a tasa $n$ reduce $r=K/L$ hacia el equilibrio. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | Ahorro $s(q/p)$ dependiente positivamente del rendimiento del capital ($s'(r) < 0$) | Si el ahorro aumentara con $r$, el efecto sobre la estabilidad podría invertirse. | - |
| `A-C09-02` | - | Tasa exógena de crecimiento poblacional $n > 0$ bajo oferta laboral elástica | Sin crecimiento laboral exógeno positivo desaparece el arrastre $-nr$. | - |

---

### [Hab-10] Tributación Proporcional y Población Endógena (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 26: Tributación Proporcional y Población Endógena
- **Prerequisites:** C-09
- **Recommended Modalities:** open_symbolic, unstructured_model, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 26)

#### Description & Cognitive Model
Cálculo de la tasa efectiva de ahorro $s' = s + (v-s)t$ con impuesto proporcional $t$ y fracción pública invertida $v$, y análisis de equilibrios múltiples ($r_1$ estable, $r_2$ umbral inestable) bajo $n(r)$ endógeno.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab10-01` | Impuesto siempre reduce ahorro | skipped_step | high | $s' = s(1-t)$ sin importar cómo gaste el Estado | Sume la inversión pública $vt$ al ahorro privado $s(1-t)$ para obtener $s' = s + (v-s)t$, que supera a $s$ siempre que $v > s$. |
| `D-Hab10-02` | Trampa en umbral r2 | skipped_step | high | Si $r_0 < r_2$ la economía despega hacia crecimiento sostenido | Observe en $\dot{r}=sF(r,1)-n(r)r$ que entre $r_1$ y $r_2$ se cumple $n(r)r > sF(r,1)$, por lo que $\dot{r}<0$ devuelve el sistema a la trampa $r_1$. |
| `D-Hab10-03` | Confunde condición de aumento | conceptual_swap | high | $s'$ aumenta respecto a $s$ cuando $v < s$ | Note que $(v-s)t > 0$ requiere que el Estado invierta una fracción $v$ mayor que la propensión privada al ahorro $s$. |
| `D-Hab10-04` | Error algebraico en v=1 | conceptual_swap | high | Si $v=1$, entonces $s' = s + t$ | Aplique el ahorro privado $s$ sobre el ingreso neto $(1-t)Y$ antes de sumar $tY$, obteniendo $s(1-t)+t = s + t(1-s)$. |
| `D-Hab10-05` | Rayo lineal n(r)r | conceptual_swap | high | La curva $n(r)r$ sigue siendo una recta desde el origen | Recuerde que al depender $n$ del ingreso per cápita $F(r,1)$, el término $n(r)r$ se curva y permite múltiples intersecciones con $sF(r,1)$. |
| `D-Hab10-06` | Requiere rendimientos crecientes | conceptual_swap | high | Las trampas de estancamiento exigen rendimientos crecientes a escala | Destaque que la Fig. IX genera una trampa $r_1$ y un umbral $r_2$ bajo rendimientos constantes a escala estrictos gracias a $n(r)$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab10-01` | - | Impuesto proporcional a la renta $t \in (0,1)$ con fracción de inversión pública $v \in [0,1]$ | Impuestos no proporcionales deformarían $sF(r,1)$ de forma no uniforme. | - |
| `A-Hab10-02` | - | Tasa de crecimiento poblacional $n(r)$ dependiente del ingreso per cápita $F(r,1)$ | Si $n$ es constante, la curva $nr$ es lineal y desaparece esta fuente de equilibrios múltiples. | - |

---

### [C-10] Rigidez Salarial y Preferencia por la Liquidez (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 29: Rigidez Salarial y Preferencia por la Liquidez
- **Prerequisites:** C-06, C-08
- **Recommended Modalities:** adversarial_break, multiple_select, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 29)

#### Description & Cognitive Model
Implicaciones de rigidez en precios: un salario real fijo $\bar{w}/p$ fija $r=\bar{r}$ generando desempleo si $(s/\bar{r})F(\bar{r},1)<n$, y la trampa de liquidez en $\bar{M}=Q(F(K,L),F_K(K,L))$ provoca subutilización de capital.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C10-01` | Rigidez salarial mantiene r variable | conceptual_swap | high | Con $\bar{w}/p$ fijo, la razón $r$ sigue ajustándose al equilibrio | Recuerde que $\partial F/\partial L$ depende solo de $r$; fijar $\bar{w}/p$ clava $r=\bar{r}$ y traslada el ajuste al nivel de empleo $L$. |
| `D-C10-02` | Condición invertida de desempleo | conceptual_swap | high | Si $(s/\bar{r})F(\bar{r},1) > n$ se desarrolla desempleo creciente | Compare la tasa de crecimiento del empleo $\dot{L}/L = (s/\bar{r})F(\bar{r},1)$ con $n$: si es menor que $n$ ($\dot{r}<0$ en $\bar{r}$), surge desempleo. |
| `D-C10-03` | Trampa sin impacto real | conceptual_swap | high | La trampa de liquidez no afecta al capital en uso en el modelo real | Reconozca que una tasa de interés rígida sobre el nivel de equilibrio provoca subutilización de capital y exige una dinámica monetaria explícita. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C10-01` | - | Nivel general de precios constante y rigidez a la baja en $\bar{w}/p$ o en la tasa de interés | Con precios y salarios perfectamente flexibles se restablece el pleno empleo. | - |

---
