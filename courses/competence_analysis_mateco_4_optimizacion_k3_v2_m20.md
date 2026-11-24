# Cognitive Task Analysis (CTA): Mateco 4 Optimizacion K3 V2 M20

- **Course ID:** `mateco_4_optimizacion_k3_v2_m20`
- **Macro-Competency:** Dominio y aplicación analítica integral de Mateco 4 Optimizacion K3 V2 M20
- **Structure:** 27 total competencies (1 Facts, 14 Concepts, 12 Skills) with 164 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Formulación Variacional, Trayectorias y Optimalidad | Concept | Evaluate | Unidad 5: Forma Funcional y Trayectorias | - | 6 |
| `H-01` | Funcionales de Lagrange, Mayer y Bolza | Fact | Analyze | Unidad 8: Funcionales de Lagrange, Mayer y Bolza | C-01 | 3 |
| `C-02` | Ecuación de Euler | Concept | Evaluate | Unidad 9: Ecuación de Euler | C-01 | 3 |
| `C-03` | Condición de Legendre | Concept | Evaluate | Unidad 10: Condición de Legendre | C-02 | 3 |
| `C-04` | Condición de Suficiencia y Hessiano | Concept | Evaluate | Unidad 11: Condición de Suficiencia y Hessiano | C-02, C-03 | 3 |
| `C-05` | Casos Particulares de Euler | Concept | Evaluate | Unidad 18: Casos Particulares de Euler | C-02 | 3 |
| `Hab-01` | Resolución de EDO y Casos de Euler | Skill | Evaluate | Unidad 14: Resolución de EDO de Euler | C-02, C-05 | 10 |
| `Hab-02` | Verificación de Optimalidad Local y Global | Skill | Evaluate | Unidad 15: Verificación de Optimalidad Local y Global | C-03, C-04, Hab-01 | 6 |
| `C-08` | Modelado Económico Variacional e Inversión | Concept | Analyze | Unidad 27: Modelado Económico Variacional | C-05, C-01 | 6 |
| `Hab-05` | Solución de Desinflación Óptima | Skill | Evaluate | Unidad 29: Solución de Desinflación Óptima | C-08, Hab-01 | 6 |
| `Hab-06` | Trayectoria Óptima de Contaminación | Skill | Evaluate | Unidad 3: Trayectoria Óptima de Contaminación | C-01 | 6 |
| `C-12` | Planteamiento de Control Óptimo | Concept | Evaluate | Unidad 1: Planteamiento de Control Óptimo | H-01, C-02 | 3 |
| `PRE-01` | Principio del Máximo de Pontryagin y Hamiltoniano | Concept | Evaluate | Unidad 3: Principio del Máximo y Hamiltoniano | C-12 | 7 |
| `C-06` | Condición de Estado Terminal Libre | Concept | Evaluate | Unidad 21: Transversalidad Estado Final Libre | C-05, PRE-01 | 9 |
| `C-07` | Optimización de Horizonte Temporal $t_1$ | Concept | Evaluate | Unidad 24: Transversalidad Instante Final Libre | C-05, PRE-01 | 6 |
| `Hab-04` | Optimización con Frontera Libre | Skill | Evaluate | Unidad 22: Optimización con Frontera Libre | C-06, C-07 | 6 |
| `C-11` | Reducción Variacional e Identidades Dinámicas | Concept | Evaluate | Unidad 4: Reducción Variacional con Control | C-01, PRE-01 | 6 |
| `Hab-07` | Crecimiento y Daño Ambiental (Euler-Ramsey) | Skill | Evaluate | Unidad 5: Crecimiento y Daño Ambiental | C-08, C-11, PRE-01 | 9 |
| `Hab-08` | Suficiencia de Mangasarian y Extremos Fijos | Skill | Evaluate | Unidad 5: Mangasarian y Ecuación de Euler | PRE-01 | 10 |
| `Hab-09` | Hamiltoniano en Valor Corriente y Transversalidad | Skill | Evaluate | Unidad 6: Valor Corriente y Transversalidad | PRE-01 | 9 |
| `C-14` | Control Óptimo en Horizonte Infinito | Concept | Analyze | Unidad 7: Control Óptimo en Horizonte Infinito | PRE-01, Hab-09 | 3 |
| `Hab-11` | Ecuación de Euler y Regla de Oro RCK | Skill | Evaluate | Unidad 13: Ecuación de Euler y Regla de Oro RCK | Hab-09 | 6 |
| `C-18` | Diagrama de Fases, Isoclinas y Estado Estacionario | Concept | Evaluate | Unidad 14: Diagrama de Fases y Transversalidad RCK | Hab-11, Hab-07 | 6 |
| `Hab-12` | Modelo Dinámico de Contaminación | Skill | Evaluate | Unidad 16: Modelo Dinámico de Contaminación | C-06 | 6 |
| `Hab-13` | Resolución de Control Óptimo Cuadrático Lineal | Skill | Evaluate | Unidad 4: Resolución de Control Óptimo por Hamiltoniano | PRE-01, C-06 | 10 |
| `Hab-16` | Control Cuadrático Aplicado (Inventarios y Seguridad) | Skill | Evaluate | Unidad 1: Planificación Producción e Inventarios | C-06 | 10 |
| `C-23` | Estado Final Fijo y Permisos | Concept | Evaluate | Unidad 1: Estado Final Fijo y Permisos | C-06 | 3 |

---

## Detailed Competency Specifications

### [C-01] Formulación Variacional, Trayectorias y Optimalidad (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Forma Funcional y Trayectorias
- **Prerequisites:** None
- **Recommended Modalities:** invariant_canvas, adversarial_break, unstructured_model
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 5), `02_Set_Problem_Calculo_de_variaciones.pdf` (page 1)

#### Description & Cognitive Model
Caracterización de un problema de optimización dinámica mediante trayectorias admisibles $y(t)$, arcos $(t,y(t),y'(t))$, condiciones de frontera y el funcional variacional $V[y]=\int_0^T F(t,y(t),y'(t))\,dt$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Evalúa solo punto final | conceptual_swap | high | $V[y]=F[T,y(T),y'(T)]$ | Integre el valor $F[t,y(t),y'(t)]$ a lo largo de todo el intervalo $[0,T]$, no únicamente en el instante terminal. |
| `D-C01-04` | Omite derivada total | conceptual_swap | high | $\frac{\partial F}{\partial x} - \frac{\partial F}{\partial \dot{x}} = 0$ | Derive respecto al tiempo $t$ toda la expresión $\partial F/\partial \dot{x}$ incluyendo la dependencia implícita de $x(t)$ y $\dot{x}(t)$. |
| `D-C01-02` | Omite pendiente del arco | conceptual_swap | high | $V[y]=\int_0^T F[t,y(t)]\,dt$ | Incluya la dirección o tasa de cambio $y'(t)=\frac{dy}{dt}$ como argumento de $F$, pues múltiples arcos parten del mismo punto. |
| `D-C01-05` | Legendre insuficiente | conceptual_swap | high | $F_{\dot{x}\dot{x}} < 0 \Rightarrow \text{máximo global}$ | Verifique además la concavidad conjunta de $F(t,x,\dot{x})$ mediante toda la matriz Hessiana para garantizar optimalidad global. |
| `D-C01-03` | Confunde estado e instante libres | conceptual_swap | high | Estado final libre fija $y(T)=Z$ con $T$ variable | Distinga que con estado final libre la frontera es vertical ($t=T$), mientras con instante final libre la frontera es horizontal ($y=Z$). |
| `D-C01-06` | Signo invertido en mínimo | conceptual_swap | high | $F_{\dot{x}\dot{x}} \le 0$ para minimizar | Recuerde que minimizar un funcional convexo exige $F_{\dot{x}\dot{x}} \ge 0$ (y $>0$ para Legendre fuerte y unicidad). |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Las trayectorias admisibles $y(t)$ son diferenciables a trozos en $[0,T]$ | Sin diferenciabilidad de $y(t)$ no está definida la dirección $y'(t)$ en cada arco. | - |
| `A-C01-02` | - | Trayectorias admisibles suficientemente regulares $x \in C^2([0,T])$ con extremos fijos | Sin regularidad $C^2$ no existe la segunda derivada en Euler-Lagrange. | - |
| `A-C01-03` | - | Compatibilidad entre parámetros y condiciones de frontera $x(0)=x_0, x(T)=x_T$ | Sin compatibilidad el conjunto de trayectorias admisibles puede ser vacío. | - |

---

### [H-01] Funcionales de Lagrange, Mayer y Bolza (Fact)

- **Bloom Level:** Analyze
- **Session:** Unidad 8: Funcionales de Lagrange, Mayer y Bolza
- **Prerequisites:** C-01
- **Recommended Modalities:** multiple_select, fill_in_the_blank, proof_dag
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 8)

#### Description & Cognitive Model
Clasificación de los tres tipos de funcionales objetivo en tiempo continuo: Lagrange ($\int_0^T F\,dt$), Mayer ($G(T,y(T))$) y Bolza ($\int_0^T F\,dt + G(T,y(T))$)

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Confunde Lagrange con Bolza | conceptual_swap | high | Lagrange incluye término terminal $G(T,y(T))$ | Recuerde que el problema de Lagrange solo contiene la integral $\int_0^T F\,dt$, mientras que Bolza suma además la función terminal $G(T,y(T))$. |
| `D-H01-02` | Confunde Mayer con integral | conceptual_swap | high | Mayer es $\int_0^T G(t,y(t))\,dt$ | Distinga que el problema de Mayer depende exclusivamente del estado y tiempo finales $G(T,y(T))$ sin término integral. |
| `D-H01-03` | Omite término integral en Bolza | conceptual_swap | high | Bolza es $V[y]=G(T,y(T))$ | Incluya tanto el costo o beneficio acumulado $\int_0^T F[t,y(t),y'(t)]\,dt$ como el valor terminal $G(T,y(T))$ en la forma de Bolza. |

---

### [C-02] Ecuación de Euler (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 9: Ecuación de Euler
- **Prerequisites:** C-01
- **Recommended Modalities:** proof_dag, adversarial_break, open_symbolic
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 9)

#### Description & Cognitive Model
Condición necesaria de primer orden para un extremo local del problema básico variacional: $F_x - \frac{d}{dt}F_{\dot{x}} = 0$ y su desarrollo $F_x - F_{\dot{x}x}\dot{x} - F_{\dot{x}\dot{x}}\ddot{x} - F_{\dot{x}t} = 0$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Signo positivo en Euler | conceptual_swap | high | $F_x + \frac{d}{dt}F_{\dot{x}} = 0$ | Aplique el signo negativo en $F_x - \frac{d}{dt}F_{\dot{x}} = 0$, resultado de integrar por partes la primera variación del funcional. |
| `D-C02-02` | Omite derivada total respecto a t | conceptual_swap | high | $F_x - F_{\dot{x}} = 0$ | Derive totalmente $F_{\dot{x}}[x(t),\dot{x}(t),t]$ respecto al tiempo $t$ mediante regla de la cadena antes de restarla de $F_x$. |
| `D-C02-03` | Desarrollo incompleto de cadena | conceptual_swap | high | $F_x - F_{\dot{x}\dot{x}}\ddot{x} = 0$ | Expanda $\frac{d}{dt}F_{\dot{x}}$ incluyendo las tres dependencias de $F_{\dot{x}}(x,\dot{x},t)$: $F_{\dot{x}x}\dot{x} + F_{\dot{x}\dot{x}}\ddot{x} + F_{\dot{x}t}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | El integrando $F(x,\dot{x},t)$ es de clase $C^2$ y los extremos $x(t_0)=x_0, x(t_1)=x_1$ son fijos | Sin suavidad $C^2$ no existen las derivadas parciales mixtas ni la ecuación diferencial de segundo orden. | - |

---

### [C-03] Condición de Legendre (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 10: Condición de Legendre
- **Prerequisites:** C-02
- **Recommended Modalities:** adversarial_break, multiple_select, fill_in_the_blank
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 10)

#### Description & Cognitive Model
Condición necesaria de segundo orden sobre la curvatura respecto a $\dot{x}$: $F_{\dot{x}\dot{x}}[x^*(t),\dot{x}(t),t]\le 0$ para máximo local y $F_{\dot{x}\dot{x}}\ge 0$ para mínimo local en todo $t\in[t_0,t_1]$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Deriva respecto a x en lugar de x punto | conceptual_swap | high | $F_{xx} \le 0$ para máximo local | Recuerde que la condición de Legendre evalúa la segunda derivada parcial respecto a la velocidad $\dot{x}$ ($F_{\dot{x}\dot{x}}$), no respecto al estado $x$. |
| `D-C03-02` | Invierte desigualdad de Legendre | conceptual_swap | high | $F_{\dot{x}\dot{x}} \ge 0$ para máximo local | Verifique el signo de la segunda variación: concavidad en $\dot{x}$ ($F_{\dot{x}\dot{x}}\le 0$) corresponde a máximo local y $F_{\dot{x}\dot{x}}\ge 0$ a mínimo local. |
| `D-C03-03` | Confunde Legendre con suficiencia | conceptual_swap | high | $F_{\dot{x}\dot{x}}<0$ garantiza máximo global | Distinga que Legendre es únicamente condición necesaria local; la optimalidad global exige analizar la concavidad o convexidad conjunta de $F$ en $(x,\dot{x})$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | $x^*(t)$ satisface previamente la ecuación de Euler en $[t_0,t_1]$ | Sin cumplir la condición de primer orden, el signo de $F_{\dot{x}\dot{x}}$ no identifica un extremo. | - |

---

### [C-04] Condición de Suficiencia y Hessiano (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 11: Condición de Suficiencia y Hessiano
- **Prerequisites:** C-02, C-03
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 11)

#### Description & Cognitive Model
Suficiencia de máximo (mínimo) global cuando $F(x,\dot{x},t)$ es cóncava (convexa) en $(x,\dot{x})$ para cada $t\in[t_0,t_1]$, verificada mediante el hessiano $H_F$ semidefinido negativo (positivo)

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Confunde semidefinida negativa con convexa | conceptual_swap | high | $H_F$ semidefinida negativa implica función convexa | Corrija la equivalencia: una matriz hessiana semidefinida negativa ($F_{xx}\le 0, F_{\dot{x}\dot{x}}\le 0, \det H_F\ge 0$) implica concavidad (máximo global), no convexidad. |
| `D-C04-02` | Invierte signo del determinante hessiano | conceptual_swap | high | $\det(H_F)<0$ para función cóncava | Recuerde la regla de menores principales en dimensión 2: tanto en concavidad como en convexidad el determinante hessiano $\det(H_F)$ debe ser no negativo ($\ge 0$). |
| `D-C04-03` | Omite verificar $F_{xx}$ y $F_{\dot{x}\dot{x}}$ | conceptual_swap | high | Solo $\det(H_F)\ge 0$ basta para concavidad | Compruebe también el signo de los elementos diagonales ($F_{xx}\le 0$ y $F_{\dot{x}\dot{x}}\le 0$ para concavidad), pues $\det(H_F)>0$ también ocurre en matrices definidas positivas. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | La concavidad o convexidad de $F$ en $(x,\dot{x})$ se cumple para todo $t\in[t_0,t_1]$ | Si el signo del hessiano cambia dentro de $[t_0,t_1]$, la condición global de suficiencia falla. | - |

---

### [C-05] Casos Particulares de Euler (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 18: Casos Particulares de Euler
- **Prerequisites:** C-02
- **Recommended Modalities:** concept_matching, adversarial_break, multiple_select
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 18)

#### Description & Cognitive Model
Simplificaciones de la ecuación de Euler cuando $F$ omite $x$ ($F_{\dot{x}}=c$), omite $\dot{x}$ ($F_x=0$) o es autónoma en $(x,\dot{x})$ cumpliendo la identidad de Beltrami $F-\dot{x}F_{\dot{x}}=C$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Confunde caso sin x | conceptual_swap | high | $F_x=0 \Rightarrow F_{\dot{x}}=0$ | Al integrar $\frac{d}{dt}F_{\dot{x}}=0$ respecto al tiempo aparece una constante arbitraria $c$, no necesariamente cero. |
| `D-C05-02` | Signo en Beltrami | conceptual_swap | high | $F+\dot{x}F_{\dot{x}}=C$ | Al derivar $F(x,\dot{x})$ y sustituir $F_x=\frac{d}{dt}F_{\dot{x}}$ se obtiene $\frac{d}{dt}(F-\dot{x}F_{\dot{x}})=0$, con signo negativo. |
| `D-C05-03` | Caso sin x punto | conceptual_swap | high | $F_{\dot{x}}=0 \Rightarrow \dot{x}=0$ | Cuando $F$ no depende de $\dot{x}$, la ecuación de Euler se reduce a la condición algebraica $F_x=0$ para hallar $x(t)$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Integrando $F(x,\dot{x},t)$ de clase $C^2$ en sus argumentos | Sin diferenciabilidad de segundo orden no puede aplicarse la ecuación de Euler ni derivarse Beltrami. | - |
| `A-C05-02` | - | Autonomía temporal $\frac{\partial F}{\partial t}=0$ explícita en el caso de Beltrami | Si $F$ depende explícitamente de $t$, la cantidad $F-\dot{x}F_{\dot{x}}$ no se conserva constante. | - |

---

### [Hab-01] Resolución de EDO y Casos de Euler (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 14: Resolución de EDO de Euler
- **Prerequisites:** C-02, C-05
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 14), `01_optimizacion_dinamica.pdf` (page 20)

#### Description & Cognitive Model
Planteamiento y resolución analítica de la ecuación diferencial de Euler con condiciones de contorno fijas $x(t_0)=x_0, x(t_1)=x_1$, incluyendo integración directa cuando falta $x$, compatibilidad cuando falta $\dot{x}$ y uso de Beltrami $F-\dot{x}F_{\dot{x}}=C$.

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Error de signo en EDO | skipped_step | high | $\ddot{x}+x=0 \Rightarrow x(t)=c_1\cos t + c_2\sin t$ | Aplique el signo menos en $F_x - \frac{d}{dt}F_{\dot{x}}=0$: $2x - 2\ddot{x}=0 \Rightarrow \ddot{x}-x=0$, cuyas raíces son reales ($m=\pm 1$). |
| `D-Hab01-07` | Olvida segunda constante | skipped_step | high | $-2\dot{x}=c \Rightarrow x(t)=ct$ | Despeje $\dot{x}=c_1$ e integre dos veces el sistema para obtener $x(t)=c_1 t+c_2$ antes de imponer las dos fronteras. |
| `D-Hab01-02` | Olvida factor 2 al integrar | skipped_step | high | $b-\frac{d}{dt}(2a\dot{x})=0 \Rightarrow \ddot{x}=\frac{b}{a}$ | Conserve el factor $2$ proveniente de derivar $a\dot{x}^2$ respecto a $\dot{x}$: $F_{\dot{x}}=2a\dot{x} \Rightarrow \ddot{x}=\frac{b}{2a}$ y tras integrar dos veces aparece $\frac{b}{4a}t^2$. |
| `D-Hab01-08` | Ignora incompatibilidad | skipped_step | high | $x(t)=-t$ siempre alcanza el mínimo | Cuando $F$ no depende de $\dot{x}$ no hay constantes libres; verifique si $x(t)=-t$ satisface $x(0)=a$ y $x(1)=b$. |
| `D-Hab01-03` | Omite factor 1/2 en segunda integración | conceptual_swap | high | $\ddot{x}=\frac{b}{2a} \Rightarrow x(t)=\frac{b}{2a}t^2+c_1 t+c_2$ | Recuerde que al integrar $\dot{x}=\frac{b}{2a}t+c_1$ respecto a $t$, la antiderivada de $t$ es $\frac{t^2}{2}$, generando el coeficiente $\frac{b}{4a}$. |
| `D-Hab01-09` | Deriva mal F respecto x | conceptual_swap | high | $F_x=t+x=0$ | Aplique la regla de la cadena en $(t+x)^2$ para obtener $F_x=2(t+x)=0$ aunque la raíz coincida en $x=-t$. |
| `D-Hab01-04` | No impone condición inicial x(0) | conceptual_swap | high | $c_2=0$ por defecto en $x(0)=1$ | Sustituya ambos extremos $t=t_0$ y $t=t_1$ en la solución general $x(t)=c_1 e^{-t}+c_2 e^t$ para resolver el sistema $2\times 2$ de constantes. |
| `D-Hab01-10` | Aplica Beltrami con t | conceptual_swap | high | $t^2-\dot{x}^2-\dot{x}(-2\dot{x})=C$ | Verifique primero que $F$ no dependa explícitamente de $t$; en $t^2-\dot{x}^2$ falta $x$, por lo que aplica $F_{\dot{x}}=c$. |
| `D-Hab01-05` | Confunde raíces repetidas | conceptual_swap | high | $m^2-1=0 \Rightarrow x(t)=(c_1+c_2 t)e^t$ | Observe que $m^2-1=0$ tiene dos raíces reales distintas $m_1=-1$ y $m_2=1$, por lo que la base homogénea es $c_1 e^{-t}+c_2 e^t$. |
| `D-Hab01-06` | Error de signo al despejar c1 | conceptual_swap | high | $x(4)=4 \Rightarrow c_1=\frac{b}{a}-\frac{1}{2}$ | Despeje cuidadosamente $4=\frac{b}{4a}(16)+4c_1+2 \Rightarrow 4c_1=2-\frac{4b}{a} \Rightarrow c_1=\frac{1}{2}-\frac{b}{a}$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Las condiciones de frontera $x(t_0)=x_0$ y $x(t_1)=x_1$ son fijas y compatibles | Sin dos condiciones de frontera independientes quedan constantes arbitrarias sin determinar. | - |
| `A-Hab01-02` | - | Condiciones de frontera fijas $x(t_0)=x_0$ y $x(t_1)=x_1$ | Sin ambos extremos fijos, las constantes de integración requieren condiciones de transversalidad. | - |

---

### [Hab-02] Verificación de Optimalidad Local y Global (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 15: Verificación de Optimalidad Local y Global
- **Prerequisites:** C-03, C-04, Hab-01
- **Recommended Modalities:** open_symbolic, adversarial_break, unstructured_model
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 15)

#### Description & Cognitive Model
Evaluación conjunta de la condición de Legendre $F_{\dot{x}\dot{x}}$ y el hessiano $H_F$ para clasificar extremales como mínimos o máximos locales y globales, incluyendo casos semidefinidos como $F=bx+a\dot{x}^2+ct$ ($a<0$)

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Omite factor 2 en entrada $H_F$(2,2) | skipped_step | high | $H_F=\begin{bmatrix}0 & 0\\ 0 & a\end{bmatrix}$ para $F=bx+a\dot{x}^2+ct$ | Calcule consistentemente la segunda derivada parcial $F_{\dot{x}\dot{x}}=\frac{\partial}{\partial \dot{x}}(2a\dot{x})=2a$ tanto en Legendre como en la entrada $(2,2)$ de $H_F$. |
| `D-Hab02-02` | Etiqueta semidefinida negativa como convexa | skipped_step | high | $H_F$ semidefinida negativa implica $F$ convexa | Verifique que cuando $a<0$, $H_F=\text{diag}(0,2a)$ es semidefinida negativa, lo que implica concavidad de $F$ y garantiza un máximo global. |
| `D-Hab02-03` | Calcula mal el determinante de $H_F$ | conceptual_swap | high | $\det\begin{bmatrix}2 & 0\\ 0 & 2\end{bmatrix}=2$ | Calcule el determinante $2\times 2$ multiplicando los elementos de la diagonal principal y restando el producto cruzado: $2\cdot 2 - 0\cdot 0 = 4$. |
| `D-Hab02-04` | Concluye mínimo global con a negativo | conceptual_swap | high | $F_{\dot{x}\dot{x}}=2a<0 \Rightarrow \text{mínimo global}$ | Recuerde que una segunda derivada negativa ($2a<0$) indica curvatura cóncava hacia abajo, correspondiente a un máximo y nunca a un mínimo. |
| `D-Hab02-05` | Aplica criterio estricto al caso semidefinido | conceptual_swap | high | Como $F_{xx}=0$, $F$ no es cóncava | Aplique el criterio de semidefinición negativa ($F_{xx}\le 0, F_{\dot{x}\dot{x}}\le 0, \det H_F\ge 0$), el cual permite ceros en la diagonal y en el determinante. |
| `D-Hab02-06` | Omite verificar cruce mixto $F_x_xdot$ | conceptual_swap | high | Asume $F_{x\dot{x}}=1$ en $F=x^2+\dot{x}^2$ | Observe que $x^2+\dot{x}^2$ es aditivamente separable en $x$ y $\dot{x}$, por lo que las derivadas parciales mixtas $F_{x\dot{x}}=F_{\dot{x}x}$ son cero. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | En el segundo ejemplo, los parámetros satisfacen $a,b,c\in\mathbb{R}$ con $a<0$ | Si $a>0$, el hessiano pasa a ser semidefinido positivo (convexo) y el problema de maximización carece de máximo finito. | - |

---

### [C-08] Modelado Económico Variacional e Inversión (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 27: Modelado Económico Variacional
- **Prerequisites:** C-05, C-01
- **Recommended Modalities:** unstructured_model, adversarial_break, multiple_select, invariant_canvas
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 27), `02_Set_Problem_Calculo_de_variaciones.pdf` (page 2)

#### Description & Cognitive Model
Formulación de funcionales dinámicos en economía: monopolio dinámico de Evans, tradeoff inflación-desempleo de Taylor e inversión intertemporal descontada $\int_0^T e^{-rt}[aK-\frac{b}{2}K^2-\frac{c}{2}\dot{K}^2]\,dt$ con concavidad conjunta.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Signo en brecha producto | conceptual_swap | high | $y_f-y=\frac{\dot{\pi}}{\beta j}$ | De $\dot{\pi}=j(p-\pi)$ se tiene $p-\pi=\frac{\dot{\pi}}{j}$, y como $p-\pi=-\beta(y_f-y)$, resulta $y_f-y=-\frac{\dot{\pi}}{\beta j}$. |
| `D-C08-04` | Omite factor de descuento | conceptual_swap | high | $c\ddot{K} - bK = -a$ | Aplique la regla del producto al derivar $-ce^{-rt}\dot{K}$ respecto a $t$, generando el término adicional $+rce^{-rt}\dot{K}$. |
| `D-C08-02` | Omite pi en p | conceptual_swap | high | $p=\frac{\dot{\pi}}{j}$ | Despeje completamente $p-\pi=\frac{\dot{\pi}}{j} \Rightarrow p=\frac{\dot{\pi}}{j}+\pi$ antes de elevarlo al cuadrado en $\lambda(\pi,\dot{\pi})$. |
| `D-C08-05` | Signo erróneo en descuento | conceptual_swap | high | $c\ddot{K} + rc\dot{K} - bK = -a$ | Revise los signos: $\frac{d}{dt}(-ce^{-rt}\dot{K}) = e^{-rt}(-c\ddot{K} + rc\dot{K})$, que al restarse de $F_K$ da $+c\ddot{K} - rc\dot{K}$. |
| `D-C08-03` | Demanda estática en Evans | conceptual_swap | high | $q=a-bp(t)$ sin $\dot{p}(t)$ | El componente $h\dot{p}(t)$ introduce la derivada temporal en el integrando $\pi(t)=pq(p,\dot{p})-C(q)$, haciendo el problema dinámico. |
| `D-C08-06` | Confunde inversión bruta | conceptual_swap | high | $I(t) = \dot{K}(t) + \delta K(t)$ | Verifique el enunciado del problema: la inversión neta coincide exactamente con la variación temporal del capital $I(t)=\dot{K}(t)$. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C08-01` | - | Parámetros positivos $a,b,\alpha,\beta,\gamma>0$ y velocidad de ajuste $0<j\le 1$ | Si $j=0$ las expectativas quedan congeladas ($\dot{\pi}=0$) y no puede reducirse la inflación esperada. | - |
| `A-C08-02` | - | Tasa de descuento nula en ambos modelos de horizonte finito | Un factor de descuento $e^{-\rho t}$ introduciría dependencia explícita en $t$ modificando la ecuación de Euler. | - |
| `A-C08-03` | - | Parámetros estrictamente positivos $a>0, b>0, c>0, r>0$ | Si $b\le 0$ o $c\le 0$ se pierde la concavidad estricta conjunta del integrando. | - |

---

### [Hab-05] Solución de Desinflación Óptima (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 29: Solución de Desinflación Óptima
- **Prerequisites:** C-08, Hab-01
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 29)

#### Description & Cognitive Model
Derivación de la EDO de Euler $(1+\beta^2\alpha)\ddot{\pi}-\beta^2 j^2\alpha\pi=0$ en el modelo de Taylor, cálculo de raíces $r=\pm\frac{\beta j\sqrt{\alpha}}{\sqrt{1+\beta^2\alpha}}$, constantes de frontera y verificación de $H_F\succ 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Error en derivada total | skipped_step | high | $\frac{d}{dt}F_{\dot{\pi}}=2\alpha\frac{\dot{\pi}}{j}$ sin $\ddot{\pi}$ | Derive cada término de $F_{\dot{\pi}}=\frac{2\dot{\pi}}{(\beta j)^2}+\frac{2\alpha\pi}{j}+\frac{2\alpha\dot{\pi}}{j^2}$ respecto a $t$ para obtener términos en $\ddot{\pi}$ y $\dot{\pi}$. |
| `D-Hab05-02` | Relación c1 y c2 errónea | conceptual_swap | high | $c_1=c_2-\pi_0$ | De la condición inicial $\pi(0)=c_1+c_2=\pi_0$ se despeja $c_1=\pi_0-c_2$, manteniendo positivo $\pi_0$. |
| `D-Hab05-03` | Raíces complejas erróneas | conceptual_swap | high | $r=\pm i\frac{\beta j\sqrt{\alpha}}{\sqrt{1+\beta^2\alpha}}$ | En $r^2(1+\beta^2\alpha)-\beta^2 j^2\alpha=0$ el término independiente es negativo, por lo que $r^2>0$ y las raíces son reales opuestas. |
| `D-Hab05-04` | Olvida frontera T | skipped_step | high | Deja $c_1, c_2$ libres sin imponer $\pi(T)=0$ | Sustituya $c_1=\pi_0-c_2$ en $\pi(T)=0$ para despejar $c_2=\frac{\pi_0}{1-e^{-2r_1 T}}$ y $c_1=\frac{\pi_0}{1-e^{2r_1 T}}$. |
| `D-Hab05-05` | Omite término cruzado $H_F$ | conceptual_swap | high | $H_{12}=0$ en el hessiano de $\lambda(\pi,\dot{\pi})$ | Calcule la derivada mixta de $\alpha(\frac{\dot{\pi}}{j}+\pi)^2$ para incluir $\frac{2\alpha}{j}$ fuera de la diagonal de $H_F$. |
| `D-Hab05-06` | Cancela mal 2alpha*pidot/j | conceptual_swap | high | Deja $4\alpha\frac{\dot{\pi}}{j}$ en la EDO de Euler | Al igualar $F_\pi=\frac{d}{dt}F_{\dot{\pi}}$, el término $2\alpha\frac{\dot{\pi}}{j}$ aparece en ambos miembros y se cancela exactamente. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | Inflación inicial $\pi(0)=\pi_0 \neq 0$ y meta terminal $\pi(T)=0$ en horizonte $T>0$ | Si $T\to\infty$ el coeficiente $c_1\to 0$ y la solución colapsa a la rama estable $c_2 e^{-r_1 t}$. | - |

---

### [Hab-06] Trayectoria Óptima de Contaminación (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Trayectoria Óptima de Contaminación
- **Prerequisites:** C-01
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `02_Set_Problem_Calculo_de_variaciones.pdf` (page 3)

#### Description & Cognitive Model
Resolución variacional de $\min \int_0^T [\frac{a}{2}P^2 + \frac{b}{2}\dot{P}^2]\,dt$ con $P(0)=P_0$, $P(T)=P_T$ y verificación de mínimo global

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Raíces imaginarias | skipped_step | high | $P(t) = C_1 \cos(\sqrt{a/b}\,t) + C_2 \sin(\sqrt{a/b}\,t)$ | Verifique el signo en Euler-Lagrange: $F_P - \frac{d}{dt}F_{\dot{P}} = aP - b\ddot{P} = 0$, cuya ecuación característica tiene raíces reales $\pm\sqrt{a/b}$. |
| `D-Hab06-02` | Invierte razón a/b | skipped_step | high | $P(t) = C_1 e^{\sqrt{b/a}\,t} + C_2 e^{-\sqrt{b/a}\,t}$ | Despeje $\ddot{P} = (a/b)P$ dividiendo el coeficiente del daño $a$ entre el coeficiente del costo de ajuste $b$. |
| `D-Hab06-03` | Olvida raíz cuadrada | conceptual_swap | high | $P(t) = C_1 e^{(a/b)t} + C_2 e^{-(a/b)t}$ | Resuelva la ecuación característica cuadrática $\lambda^2 - a/b = 0$ extrayendo la raíz cuadrada $\lambda = \pm\sqrt{a/b}$. |
| `D-Hab06-04` | Factor de descuento espurio | conceptual_swap | high | $b\ddot{P} - rb\dot{P} - aP = 0$ | Lea el funcional sin descuento del Problema 7: al no existir $e^{-rt}$, no aparece ningún término proporcional a $\dot{P}$. |
| `D-Hab06-05` | Solución lineal sin daño | conceptual_swap | high | $P(t) = P_0 + \frac{P_T - P_0}{T}t$ | Incluya el término de daño ambiental $F_P = aP$ en Euler-Lagrange; la solución lineal solo sería válida si $a=0$. |
| `D-Hab06-06` | Asume máximo por signo | conceptual_swap | high | $F_{PP}=a>0$ implica máximo | Recuerde que una matriz Hessiana definida positiva ($F_{PP}=a>0, F_{\dot{P}\dot{P}}=b>0$) garantiza convexidad estricta y mínimo global único. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Condiciones de frontera no negativas $P_0, P_T \ge 0$ y $P(t) \ge 0$ en $[0,T]$ | Niveles negativos de contaminación carecen de sentido físico y violan la restricción. | - |

---

### [C-12] Planteamiento de Control Óptimo (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 1: Planteamiento de Control Óptimo
- **Prerequisites:** H-01, C-02
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `03_Teoria_de_control_optimo___teoria (1).pdf` (page 1)

#### Description & Cognitive Model
Formulación del problema de control óptimo con ecuación de estado $\dot{x}(t)=f(x(t),u(t),t)$, control admisible $u(t)\in\Omega$ continuo por tramos y funcional de Bolza $J=\int_{t_0}^{t_1}F(x,u,t)dt+S[x(t_1)]$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C12-01` | Exige control diferenciable | conceptual_swap | high | $u(t)$ debe ser continua y diferenciable en todo $[t_0,t_1]$ | Recuerde que el control óptimo solo requiere continuidad por tramos, permitiendo un número finito de discontinuidades. |
| `D-C12-02` | Estado discontinuo | conceptual_swap | high | $x(t)$ presenta saltos en los puntos de discontinuidad de $u(t)$ | La trayectoria de estado $x(t)$ es continua y diferenciable por tramos: las discontinuidades de $u(t)$ generan esquinas en $x(t)$, no saltos. |
| `D-C12-03` | Confunde Mayer y Lagrange | conceptual_swap | high | El funcional de Mayer integra $F(x,u,t)$ y omite $S[x(t_1)]$ | Distinga las formas del funcional de Bolza: Mayer fija $F=0$ conservando $S[x(t_1)]$, mientras Lagrange fija $S=0$ conservando la integral. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C12-01` | - | El conjunto de control $\Omega$ es compacto y convexo con discontinuidades finitas en $u(t)$ | Sin compacidad o con saltos infinitos, el control deja de ser admisible y la trayectoria de estado pierde continuidad. | - |

---

### [PRE-01] Principio del Máximo de Pontryagin y Hamiltoniano (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Principio del Máximo y Hamiltoniano
- **Prerequisites:** C-12
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `04_opt_din_3.pdf` (page 3), `03_Teoria_de_control_optimo___teoria (1).pdf` (page 3), `05_Control Optimo Apuntes.pdf` (page 2)

#### Description & Cognitive Model
Formulación del Hamiltoniano $H(x,u,\lambda,t)=F(x,u,t)+\lambda(t)f(x,u,t)$, condiciones necesarias de primer orden del Principio del Máximo ($H_u=0$ o $\max_{u\in\Omega} H$, $H_x=-\dot{\lambda}$, $H_\lambda=\dot{x}$) y su equivalencia con la Ecuación de Euler.

#### Fused Distractor Models (7)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-PRE01-01` | Signo positivo en adjunta | conceptual_swap | high | $\frac{\partial H}{\partial x}=\dot{\lambda}$ | Aplique el signo negativo en la ecuación de coestado $\frac{\partial H}{\partial x}=-\dot{\lambda}$ derivada de integrar por partes la restricción dinámica. |
| `D-PRE01-04` | Signo en coestado | conceptual_swap | high | $H_x=\dot{\lambda}$ | Aplique el signo negativo en la ecuación de movimiento de la variable de coestado: $H_x=\frac{\partial H}{\partial x}=-\dot{\lambda}$. |
| `D-PRE01-02` | Deriva respecto a lambda | conceptual_swap | high | $\frac{\partial H}{\partial \lambda}=-\dot{\lambda}$ | Distinga las condiciones: $\frac{\partial H}{\partial x}=-\dot{\lambda}$ rige el coestado, mientras $\frac{\partial H}{\partial \lambda}=\dot{x}$ recupera la ecuación de estado. |
| `D-PRE01-05` | Fuerza Hu=0 lineal | conceptual_swap | high | Si $H$ es lineal en $u$, la solución óptima cumple $H_u=0$ | Cuando $H$ es lineal respecto a $u$ sobre $\Omega=[u_1,u_2]$, $H_u$ no se anula y la maximización produce una solución de esquina. |
| `D-PRE01-03` | Omite restricción en H | conceptual_swap | high | $H=F(x,u,t)+\lambda x$ | Multiplique la variable de coestado $\lambda$ por la tasa de cambio $\dot{x}=f(x,u,t)$ completa, nunca por el nivel de la variable de estado $x$. |
| `D-PRE01-06` | Omite multiplicador dinámico | conceptual_swap | high | $\lambda$ es una constante fija en todo $[t_0,t_1]$ | La variable de coestado $\lambda(t)$ es el equivalente dinámico del multiplicador de Lagrange y evoluciona continuamente según $-\dot{\lambda}=H_x$. |
| `D-PRE01-07` | Signo errado en Euler | conceptual_swap | high | $\frac{\partial F}{\partial K}+\frac{d}{dt}\left(\frac{\partial F}{\partial \dot{K}}\right)=0$ | Aplique la resta en la Ecuación de Euler: $\frac{\partial F}{\partial K}-\frac{d}{dt}\left(\frac{\partial F}{\partial \dot{K}}\right)=0$, cuidando el signo al derivar respecto al tiempo. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-PRE01-01` | - | La variable de coestado $\lambda^*(t)$ es continua con primeras derivadas continuas en $[t_0,t_1]$ | Si $\lambda^*(t)$ carece de continuidad, el sistema canónico deja de caracterizar la trayectoria óptima. | - |
| `A-PRE01-02` | - | Soluciones interiores diferenciables en el control $u(t)$ y trayectoria $K(t)$ | Sin interioridad ni diferenciabilidad fallan las condiciones de primer orden $\frac{\partial \mathcal{H}}{\partial u}=0$ y Euler. | - |
| `A-PRE01-03` | - | Despeje directo del control $u$ desde $\dot{K}=f(K,u,t)$ para aplicar Euler | Si el control no puede despejarse de la ecuación de movimiento, debe usarse el Hamiltoniano. | - |

---

### [C-06] Condición de Estado Terminal Libre (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 21: Transversalidad Estado Final Libre
- **Prerequisites:** C-05, PRE-01
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 21), `04_opt_din_3.pdf` (page 8), `06_Problemas_teoria_de_control.pdf` (page 1)

#### Description & Cognitive Model
Anulación del precio sombra terminal $\lambda(T)=\left.\frac{\partial S}{\partial x}\right|_{t=T}=0$ y de la derivada variacional $\left.\frac{\partial F}{\partial \dot{x}}\right|_{t=T}=0$ cuando la variable de estado $x(T)$ carece de restricción final fija.

#### Fused Distractor Models (9)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Anula estado final | conceptual_swap | high | $x(t_1)=0$ | Un estado final libre no significa que valga cero, sino que su variación arbitraria exige anular $F_{\dot{x}}$ en $t=t_1$. |
| `D-C06-04` | Iguala estado final a cero | conceptual_swap | high | $x(T)=0$ | No confunda estado final libre con estado final nulo: la libertad terminal anula el precio sombra $\lambda(T)=0$, no necesariamente el nivel $x(T)$. |
| `D-C06-05` | Signo ecuación coestado | conceptual_swap | high | $\dot{\lambda}=\mathcal{H}_x$ | Recuerde la condición adjunta de Pontryagin: la variación del precio sombra satisface $\dot{\lambda}=-\partial\mathcal{H}/\partial x$. |
| `D-C06-02` | Usa condición de Caso II | conceptual_swap | high | $\left.\left(F-\dot{x}F_{\dot{x}}\right)\right|_{t=t_1}=0$ | Distinga el parámetro libre: si varía $x(t_1)$ con $t_1$ fijo, la condición es $\left.F_{\dot{x}}\right|_{t=t_1}=0$. |
| `D-C06-06` | Anula control terminal | conceptual_swap | high | $u(T)=0$ | Aplique la condición de transversalidad sobre el multiplicador $\lambda(T)=0$; el valor de $u(T)$ se deduce después desde $\frac{\partial H}{\partial u}=0$. |
| `D-C06-07` | Estado final nulo | conceptual_swap | high | $x(T)=0$ en horizonte libre | Cuando el valor final de la variable de estado es libre y no tiene valor residual, la transversalidad exige $\lambda(T)=0$ y no $x(T)=0$. |
| `D-C06-03` | Signo Legendre invertido | conceptual_swap | high | $\frac{\partial^2 F}{\partial \dot{x}^2}>0$ para máximo | Para maximizar, la condición de Legendre requiere $\frac{\partial^2 F}{\partial \dot{x}^2}<0$ (y $>0$ para minimizar). |
| `D-C06-08` | Signo erróneo al despejar c2 | conceptual_swap | high | $1=c_2+\frac{1}{4}c_1^{-1}$ | Verifique los signos al evaluar $x(t)=t-\frac{1}{4}(-t+c_1)^{-1}+c_2$ en $t=0$: resulta $1=c_2-\frac{1}{4}c_1^{-1}$, lo que implica $c_2=\frac{5}{4}$ cuando $c_1=1$. |
| `D-C06-09` | Minimización mal signada | conceptual_swap | high | $\mathcal{H}=C(x,u)+\lambda g(x,u)$ al maximizar | Al transformar un problema de minimización de costos al principio del máximo, introduzca $-C(x,u)$ como pago instantáneo antes de maximizar $\mathcal{H}$. |

#### Formal Mathematical Assumptions (4)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Horizonte temporal $t_1$ fijo con estado inicial $x(t_0)=x_0$ dado | Si $t_1$ fuera libre, se requeriría además la condición sobre el hamiltoniano variacional en $t_1$. | - |
| `A-C06-02` | - | Concavidad o convexidad conjunta de $F$ en $(x,\dot{x})$ para suficiencia global | Sin concavidad (máximo) o convexidad (mínimo) conjunta, el extremal solo se garantiza como óptimo local. | - |
| `A-C06-03` | - | Estado final $x(T)$ irrestricto en horizonte finito $[0,T]$ sin función de valor residual $S(x(T),T)$ | Si $x(T)$ tuviera restricción $x(T)\ge x_{\min}$, la condición cambiaría a holgura complementaria $\lambda(T)(x(T)-x_{\min})=0$. | - |
| `A-C06-04` | - | Horizonte finito $[0,T]$ sin descuento temporal y valor residual nulo | Con descuento $\rho>0$ o valor residual $S(x(T))$ cambian $\dot{\lambda}$ y $\lambda(T)$. | - |

---

### [C-07] Optimización de Horizonte Temporal $t_1$ (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 24: Transversalidad Instante Final Libre
- **Prerequisites:** C-05, PRE-01
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 24), `04_opt_din_3.pdf` (page 10)

#### Description & Cognitive Model
Determinación del tiempo óptimo de parada $t_1^*$ cuando el horizonte es endógeno mediante la identidad energética $F-\dot{x}F_{\dot{x}}=0$ o la ecuación hamiltoniana $H(x^*,u^*,\lambda^*,t_1)+\partial S/\partial t|_{t=t_1}=0$ con frontera $x(t_1)=x_1$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Anula solo F en t1 | conceptual_swap | high | $\left.F\right|_{t=t_1}=0$ | Al variar $t_1$ con $x(t_1)=x_1$ fijo, el desplazamiento horizontal añade $-\dot{x}F_{\dot{x}}$ en la condición de transversalidad. |
| `D-C07-04` | Anula coestado en t1 | conceptual_swap | high | $\lambda(t_1)=0$ | Cuando $x(t_1)$ está fijo pero $t_1$ es libre, la transversalidad exige $H(t_1)=0$ (si $S=0$), nunca $\lambda(t_1)=0$. |
| `D-C07-02` | Usa condición de Caso I | conceptual_swap | high | $\left.\frac{\partial F}{\partial \dot{x}}\right|_{t=t_1}=0$ | Como $x(t_1)=x_1$ está fijado y $t_1$ es libre, corresponde usar $\left.(F-\dot{x}F_{\dot{x}})\right|_{t=t_1}=0$ para hallar $t_1$. |
| `D-C07-05` | Signo erróneo en c1*t1 | conceptual_swap | high | $c_1 t_1 = 2$ | Despeje con cuidado $5-4=-\frac{c_1}{2}t_1$: se obtiene $1=-\frac{c_1}{2}t_1$, es decir $c_1 t_1=-2$, consistente con $t_1=1$ y $c_1=-2$. |
| `D-C07-03` | Signo positivo en $F_xdot$ | conceptual_swap | high | $\left.\left(F+\dot{x}\frac{\partial F}{\partial \dot{x}}\right)\right|_{t=t_1}=0$ | El hamiltoniano variacional que se anula en $t_1$ cuando el instante final es libre lleva signo menos: $F-\dot{x}F_{\dot{x}}=0$. |
| `D-C07-06` | Evalúa H en t=0 | conceptual_swap | high | $H(x^*,u^*,\lambda^*,0)=0$ | Evalúe el Hamiltoniano en el instante final libre $t=t_1$, pues el beneficio marginal de extender el horizonte se mide al cierre del programa. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Estado inicial $x(t_0)=x_0$ y estado final $x(t_1)=x_1$ ambos fijos | Si $x(t_1)$ también fuera libre, ambas condiciones de transversalidad deberían cumplirse simultáneamente. | - |
| `A-C07-02` | - | Horizonte terminal $t_1>0$ elegible libremente con estado final $x(t_1)$ prefijado | Si $t_1$ estuviera fijo de antemano, $H(t_1)$ no tendría por qué anularse en el óptimo. | - |

---

### [Hab-04] Optimización con Frontera Libre (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 22: Optimización con Frontera Libre
- **Prerequisites:** C-06, C-07
- **Recommended Modalities:** open_symbolic, adversarial_break, unstructured_model
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 22)

#### Description & Cognitive Model
Cálculo completo de extremales, constantes y tiempo terminal $t_1$ en problemas con estado o instante final libre, verificando optimalidad local (Legendre) y global mediante el hessiano $H_F$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Evalúa transversalidad en t0 | skipped_step | high | $t+2\dot{x}|_{t=0}=0$ | La transversalidad rige en el extremo libre $t=t_1$ (por ejemplo $t=2$), mientras en $t=t_0$ rige $x(t_0)=x_0$. |
| `D-Hab04-02` | Olvida condición final x(t1) | skipped_step | high | Deja $t_1$ sin determinar tras hallar $c_1=0$ | En Caso II use la condición de transversalidad para fijar la constante $c_1$ y luego $x(t_1)=x_1$ para despejar $t_1=\sqrt{60}$. |
| `D-Hab04-03` | Error en hessiano $H_F$ | conceptual_swap | high | Confunde semidefinida negativa con convexa | Recuerde que $H_F$ semidefinida negativa implica concavidad (máximo global), mientras semidefinida positiva implica convexidad (mínimo global). |
| `D-Hab04-04` | Error algebraico en $3xdot^2$ | conceptual_swap | high | $3\dot{x}^2+x-\dot{x}(6\dot{x})=3\dot{x}^2+x$ | Agrupe correctamente $3\dot{x}^2-6\dot{x}^2=-3\dot{x}^2$ antes de sustituir $\dot{x}(t_1)$ y $x(t_1)$ en la transversalidad. |
| `D-Hab04-05` | Raíz negativa de t1 | conceptual_swap | high | $t_1=-\sqrt{60}$ | Como el horizonte temporal parte en $t_0=0$ hacia adelante, seleccione la raíz positiva $t_1=\sqrt{60}>0$. |
| `D-Hab04-06` | Omite suficiencia global | conceptual_swap | high | Concluye óptimo global solo con Legendre | La condición de Legendre solo garantiza óptimo local; construya el hessiano $H_F$ respecto a $(x,\dot{x})$ para probar globalidad. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Horizonte positivo $t_1 > t_0$ en problemas de instante terminal libre | Elegir $t_1 \le t_0$ carece de sentido físico-económico en la integral de acumulación. | - |

---

### [C-11] Reducción Variacional e Identidades Dinámicas (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Reducción Variacional con Control
- **Prerequisites:** C-01, PRE-01
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select, concept_matching
- **Evidence Citations:** `02_Set_Problem_Calculo_de_variaciones.pdf` (page 4), `05_Control Optimo Apuntes.pdf` (page 3)

#### Description & Cognitive Model
Distinción entre variables de estado (stock como $K(t)$ o $G(t)$) y control (flujo como $C(t)$ o $u(t)$), identidades macroeconómicas $I=\dot{K}=rK-C$ y sustitución de la ecuación dinámica en el funcional variacional.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C11-01` | No cancela término cruzado | conceptual_swap | high | $b\ddot{G} - (r+2\delta)b\dot{G} - aG = -p$ | Expanda $\frac{d}{dt}F_{\dot{G}}$ con cuidado: el término $+b\delta\dot{G}$ se cancela exactamente con $-b\delta\dot{G}$ proveniente de $F_G$. |
| `D-C11-04` | Confunde stock con flujo | conceptual_swap | high | $C(t)$ es estado y $K(t)$ es control | Identifique la variable de estado como aquella cuya derivada temporal aparece en la restricción ($\dot{K}$ o $\dot{G}$) y el control como la variable elegida en cada instante. |
| `D-C11-02` | Sustituye u incorrectamente | conceptual_swap | high | $u(t) = \dot{G}(t) - \delta G(t)$ | Despeje el control desde $\dot{G} = u - \delta G$ sumando la depreciación: $u(t) = \dot{G}(t) + \delta G(t)$. |
| `D-C11-05` | Confunde inversión neta y bruta | conceptual_swap | high | $I^{\text{BRUTO}}=\dot{K}$ | Sume la depreciación $\delta K$ a la inversión neta $\dot{K}$ para obtener la inversión bruta: $I^{\text{BRUTO}}=\dot{K}+\delta K=S$. |
| `D-C11-03` | Omite efecto de depreciación | conceptual_swap | high | $b\ddot{G} - rb\dot{G} - aG = -p$ | Considere la contribución de $\delta$ tanto en $F_G$ como en $\frac{d}{dt}F_{\dot{G}}$, lo que añade $-b\delta(r+\delta)G$. |
| `D-C11-06` | Invierte signo en acumulación | conceptual_swap | high | $\dot{K}=C-rK$ | El ahorro o inversión neta $\dot{K}$ equivale al ingreso $rK$ menos el consumo $C$, por lo que $\dot{K}=rK-C$ y $I+C=rK$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C11-01` | - | Control sin restricción de no negatividad $u(t) \in \mathbb{R}$ o $q(t) \in \mathbb{R}$ | Si el control estuviera acotado, podrían activarse soluciones de esquina fuera de Euler-Lagrange. | - |
| `A-C11-02` | - | Economía cerrada sin gobierno donde el ahorro iguala la inversión $S=I$ | Si hay sector externo o gasto público, la identidad $S+C=Y$ deja de cumplirse directamente. | - |

---

### [Hab-07] Crecimiento y Daño Ambiental (Euler-Ramsey) (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Crecimiento y Daño Ambiental
- **Prerequisites:** C-08, C-11, PRE-01
- **Recommended Modalities:** open_symbolic, unstructured_model, adversarial_break, proof_dag
- **Evidence Citations:** `02_Set_Problem_Calculo_de_variaciones.pdf` (page 5), `05_Control Optimo Apuntes.pdf` (page 6)

#### Description & Cognitive Model
Aplicación de la Ecuación de Euler sobre $F(K,\dot{K},t)=e^{-\rho t}(\ln C-\frac{\theta}{2}K^2)$ con $C=AK^\alpha-\dot{K}-\delta K$ para derivar la regla de Euler-Ramsey $\frac{\dot{C}}{C}=\alpha A K^{\alpha-1}-\delta-\rho-\theta KC$ y verificar concavidad estricta.

#### Fused Distractor Models (9)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Omite daño ambiental en Euler | skipped_step | high | $\frac{\dot{C}}{C} = \alpha A K^{\alpha-1} - \delta - \rho$ | Incluya la derivada del daño ambiental $-\theta K$ en $F_K$ y multiplique por $C$ al despejar $\dot{C}/C$, obteniendo $-\theta K C$. |
| `D-Hab07-07` | Omite regla del cociente temporal | skipped_step | high | $\frac{d}{dt}\left(-e^{-\rho t}\frac{1}{C}\right)=\rho e^{-\rho t}\frac{1}{C}$ | Recuerde que $C$ depende del tiempo $t$, por lo que al derivar $-e^{-\rho t}C^{-1}$ debe incluir el término con $\dot{C}$ mediante la regla del cociente. |
| `D-Hab07-02` | Falta factor C en daño | skipped_step | high | $\frac{\dot{C}}{C} = \alpha A K^{\alpha-1} - \delta - \rho - \theta K$ | Al igualar $\frac{\alpha AK^{\alpha-1}-\delta}{C} - \theta K = \frac{\rho}{C} + \frac{\dot{C}}{C^2}$ y multiplicar por $C$, el término $-\theta K$ se convierte en $-\theta K C$. |
| `D-Hab07-08` | Omite depreciación en g(K) | skipped_step | high | $g(K)=A\alpha K^{\alpha-1}$ | Al derivar $C=AK^\alpha-\dot{K}-\delta K$ respecto a $K$, incluya la tasa de depreciación para obtener $g(K)=A\alpha K^{\alpha-1}-\delta$. |
| `D-Hab07-03` | Signo erróneo en utilidad | conceptual_swap | high | $F_{\dot{K}} = +e^{-\rho t}\frac{1}{C}$ | Aplique la regla de la cadena sobre $\ln(AK^\alpha - \delta K - \dot{K})$: la derivada respecto a $\dot{K}$ aporta un factor $-1$. |
| `D-Hab07-09` | Error de signo en daño ambiental | conceptual_swap | high | $\frac{\dot{C}}{C}=g(K)+\theta KC-\rho$ | La desutilidad $-\frac{\theta}{2}K^2$ aporta $-\theta K$ en $\frac{\partial F}{\partial K}$, que tras multiplicar por $C$ aparece como $-\theta KC$ en $\frac{\dot{C}}{C}$. |
| `D-Hab07-04` | Signo erróneo en $C_dot$ | conceptual_swap | high | $\frac{d}{dt}\left(-\frac{e^{-\rho t}}{C}\right) = e^{-\rho t}\left(\frac{\rho}{C} - \frac{\dot{C}}{C^2}\right)$ | Derive $-C^{-1}$ usando $\frac{d}{dt}(-C^{-1}) = +C^{-2}\dot{C}$ antes de combinar con la derivada de $e^{-\rho t}$. |
| `D-Hab07-05` | Confunde función de producción | conceptual_swap | high | $\frac{\dot{C}}{C} = AK^{\alpha-1} - \delta - \rho - \theta KC$ | Calcule correctamente la productividad marginal del capital como $\frac{\partial Y}{\partial K} = \alpha A K^{\alpha-1}$. |
| `D-Hab07-06` | Descarta concavidad global | conceptual_swap | high | $U(C)=\ln C$ no es cóncava en $(K,\dot{K})$ | Observe que $C(K,\dot{K})=AK^\alpha-\delta K-\dot{K}$ es cóncava para $0<\alpha<1$ y $\ln(\cdot)$ es creciente y cóncava, preservando la concavidad. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Consumo y capital estrictamente positivos $C(t) > 0$ y $K(t) > 0$ con $0<\alpha<1$ | Si $C(t) \le 0$ el logaritmo $\ln C$ deja de estar definido en los reales. | - |
| `A-Hab07-02` | - | Consumo positivo $C(t)>0$ y productividad marginal decreciente con $\alpha\in(0,1)$ | Si $C\le 0$, $\ln C$ se indefine y no es posible dividir por $C$ ni por $C^2$. | - |

---

### [Hab-08] Suficiencia de Mangasarian y Extremos Fijos (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Mangasarian y Ecuación de Euler
- **Prerequisites:** PRE-01
- **Recommended Modalities:** open_symbolic, proof_dag, unstructured_model, fill_in_the_blank
- **Evidence Citations:** `03_Teoria_de_control_optimo___teoria (1).pdf` (page 5), `04_opt_din_3.pdf` (page 4)

#### Description & Cognitive Model
Resolución de problemas de control óptimo con extremos fijos mediante EDO adjunta y de estado, derivación de Euler desde el Hamiltoniano y verificación de suficiencia global con la matriz hessiana de Mangasarian $H_H^e$.

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | Invierte concavidad máxima | skipped_step | high | $H_H^e$ definida positiva garantiza un máximo | Verifique el criterio de Mangasarian: $H_H^e$ definida negativa (cóncava) garantiza máximo y definida positiva (convexa) garantiza mínimo. |
| `D-Hab08-07` | Invierte signo exponencial | skipped_step | high | $c(t)=\frac{e^{-(r-\delta)t}}{c_1}$ | Reste correctamente los exponentes en el cociente: $\frac{e^{-\delta t}}{e^{-rt}}=e^{(r-\delta)t}$ antes de sustituir el control en la ecuación de estado. |
| `D-Hab08-02` | Hessiana solo en u | skipped_step | high | $H_H^e$ deriva únicamente respecto al control $u$ | La matriz hessiana de Mangasarian $H_H^e(x^*,u^*,\lambda,t)$ se construye respecto tanto a la variable de estado $x$ como al control $u$. |
| `D-Hab08-08` | Confunde constante en EDO | skipped_step | high | $k(t)=\frac{e^{(r-\delta)t}}{\delta c_1}+c_1 e^{rt}$ | Asigne una segunda constante independiente $c_2$ al resolver la ecuación diferencial de estado, reservando $c_1$ exclusivamente para el coestado $\lambda(t)$. |
| `D-Hab08-03` | Omite cambio u=xdot | conceptual_swap | high | En cálculo de variaciones $f(x,u,t)=F(x,u,t)$ | Traduzca el problema variacional definiendo $u=\dot{x}$, de modo que la ecuación de movimiento sea $f(x,u,t)=u$ y $H=F+\lambda u$. |
| `D-Hab08-09` | Criterio de concavidad invertido | conceptual_swap | high | $H_F$ semidefinida negativa en minimización | Verifique el sentido del problema en Mangasarian: $H_F$ debe ser semidefinida positiva (convexa) para minimizar y semidefinida negativa (cóncava) para maximizar. |
| `D-Hab08-04` | Signo erróneo lambda | conceptual_swap | high | $H_u=F_u+\lambda=0 \Rightarrow \lambda=F_u$ | Al despejar de $F_u+\lambda=0$, conserve el signo negativo $\lambda=-F_u$ antes de derivar respecto al tiempo en la ecuación de coestado. |
| `D-Hab08-10` | Omite solución particular | conceptual_swap | high | $x(t)=c_2 e^t$ | Sume la solución particular $x_p(t)=ae^{-t}$ a la complementaria $c_2e^t$ cuando el término de control $u(t)$ vuelve no homogénea la ecuación de estado. |
| `D-Hab08-05` | Omite derivada total | conceptual_swap | high | $-\dot{\lambda}=F_u$ en lugar de $\frac{dF_u}{dt}$ | Diferencie $\lambda=-F_u$ respecto al tiempo para obtener $-\dot{\lambda}=\frac{dF_u}{dt}$ y sustituir en $F_x=-\dot{\lambda}$. |
| `D-Hab08-11` | Aplica condición inicial en t=1 | conceptual_swap | high | $x(1)=c_2+\frac{c_1}{4}$ | Evalúe $e^t$ y $e^{-t}$ en el instante correcto: $t=0$ da $1$, mientras $t=1$ produce $e$ y $e^{-1}$ al plantear el sistema para $(c_1,c_2)$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab08-01` | - | La función $F(x,\dot{x},t)$ es no lineal y suficientemente diferenciable en $(x,u)$ | Si $F$ es lineal en $u=\dot{x}$, la condición $H_u=0$ no determina $\lambda=-F_u$ y falla la reducción a Euler. | - |
| `A-Hab08-02` | - | Diferenciabilidad y convexidad/concavidad conjunta de $H$ en $(x,u)$ para suficiencia de Mangasarian | Sin concavidad/convexidad conjunta, los puntos estacionarios solo son candidatos necesarios y no óptimos globales. | - |

---

### [Hab-09] Hamiltoniano en Valor Corriente y Transversalidad (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 6: Valor Corriente y Transversalidad
- **Prerequisites:** PRE-01
- **Recommended Modalities:** fill_in_the_blank, open_symbolic, unstructured_model, proof_dag
- **Evidence Citations:** `03_Teoria_de_control_optimo___teoria (1).pdf` (page 6), `04_opt_din_3.pdf` (page 12)

#### Description & Cognitive Model
Transformación del Hamiltoniano en valor presente $H=e^{-\rho t}F+\lambda f$ al Hamiltoniano en valor corriente $\mathcal{H}=F+mf$ con $m=\lambda e^{\rho t}$, ecuación adjunta $\frac{\partial\mathcal{H}}{\partial x}=-\dot{m}+\rho m$ y condiciones de transversalidad.

#### Fused Distractor Models (9)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab09-01` | Omite término rho m | skipped_step | high | $\frac{\partial\mathcal{H}}{\partial x}=-\dot{m}$ | Al derivar $\lambda=me^{-\rho t}$ respecto al tiempo surge $-\rho m e^{-\rho t}$, por lo que la ecuación de coestado corriente es $\frac{\partial\mathcal{H}}{\partial x}=-\dot{m}+\rho m$. |
| `D-Hab09-07` | Omite término rho*m | conceptual_swap | high | $\frac{\partial \mathcal{H}}{\partial k}=-\dot{m}$ | Recuerde que al definir $m=\lambda e^{\rho t}$, la regla del producto introduce el término $+\rho m$: $\frac{\partial \mathcal{H}}{\partial k}=-\dot{m}+\rho m$. |
| `D-Hab09-02` | Signo erróneo rho m | skipped_step | high | $\frac{\partial\mathcal{H}}{\partial x}=-\dot{m}-\rho m$ | Como $\dot{\lambda}=(\dot{m}-\rho m)e^{-\rho t}$ y $H_x=-\dot{\lambda}$, al multiplicar por $e^{\rho t}$ el término $+\rho m$ queda positivo. |
| `D-Hab09-08` | Incluye descuento en H corriente | conceptual_swap | high | $\mathcal{H}=u(c)e^{-\rho t}+m\dot{k}$ | Elimine el factor de descuento $e^{-\rho t}$ de la utilidad instantánea al trabajar con el Hamiltoniano en tiempo corriente $\mathcal{H}$. |
| `D-Hab09-03` | Invierte definición m | conceptual_swap | high | $m=\lambda e^{-\rho t}$ | Para pasar de valor presente a valor corriente multiplique por $e^{\rho t}$: $\mathcal{H}=e^{\rho t}H=F+(\lambda e^{\rho t})f$, luego $m=\lambda e^{\rho t}$. |
| `D-Hab09-09` | Signo erróneo en rho*m | conceptual_swap | high | $\dot{m}=-m(f'-\delta+\rho)$ | Despeje $\dot{m}$ desde $m(f'-\delta)=-\dot{m}+\rho m$: al pasar $-\dot{m}$ y $m(f'-\delta)$ se obtiene $\dot{m}=-m(f'-\delta-\rho)$. |
| `D-Hab09-04` | Transversalidad estado libre | conceptual_swap | high | $\left.\frac{dS}{dx}\right|_{t=t_1}+\lambda(t_1)=0$ | Para estado final libre con término de salvamento $S[x(t_1)]$, la condición de transversalidad iguala $\left.\frac{dS}{dx}\right|_{t=t_1}=\lambda(t_1)$. |
| `D-Hab09-05` | Omite dS/dt1 | conceptual_swap | high | $H(x^*(t_1),u^*(t_1),\lambda^*(t_1),t_1^*)=0$ aun con $S[x(t_1),t_1]$ | Cuando $S$ depende explícitamente de $t_1$, la condición de instante final libre exige $H(t_1^*)+\left.\frac{dS}{dt_1}\right|_{t=t_1}=0$. |
| `D-Hab09-06` | Confunde H y calH | conceptual_swap | high | $\lambda(t_1)=0$ implica $m(t_1)=0$ solo si $\rho=0$ | Como $e^{-\rho t_1}>0$ para todo $t_1$ finito, $\lambda(t_1)=m(t_1)e^{-\rho t_1}=0$ es equivalente a $m(t_1)=0$ y $H(t_1)=0 \Rightarrow \mathcal{H}(t_1)=0$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab09-01` | - | El factor de descuento $e^{-\rho t}$ es estrictamente positivo para todo $t\in[t_0,t_1]$ | Si el factor de descuento se anulara, la equivalencia entre $H(t_1)=0$ y $\mathcal{H}(t_1)=0$ dejaría de cumplirse. | - |
| `A-Hab09-02` | - | Descuento exponencial constante a tasa $\rho>0$ con variable de coestado corriente $m(t)=\lambda(t)e^{\rho t}$ | Con tasa de descuento variable en el tiempo, el factor $\rho$ deja de ser constante en la ecuación adjunta. | - |

---

### [C-14] Control Óptimo en Horizonte Infinito (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 7: Control Óptimo en Horizonte Infinito
- **Prerequisites:** PRE-01, Hab-09
- **Recommended Modalities:** adversarial_break, multiple_select, concept_matching
- **Evidence Citations:** `03_Teoria_de_control_optimo___teoria (1).pdf` (page 7)

#### Description & Cognitive Model
Extensión del problema de control óptimo al horizonte temporal infinito $\max\int_{t_0}^{+\infty}F(x,u,t)dt$ con condiciones de transversalidad asintóticas para instante libre, meta asintótica fija y estado final libre

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C14-01` | Evalúa en t1 finito | conceptual_swap | high | En horizonte infinito se exige $\lambda(t_1)=0$ en un $t_1$ fijo | Al tender el horizonte a $+\infty$, las condiciones de transversalidad se expresan mediante límites asintóticos $\lim_{t\to\infty}\lambda(t)=0$. |
| `D-C14-02` | Confunde meta asintótica | conceptual_swap | high | En estado final fijo se cumple $\lim_{t\to\infty}\lambda(t)=0$ | Cuando el estado final está fijo como meta asintótica, la condición es $\lim_{t\to\infty}x(t)=x_o$ con $x_o\in\mathbb{R}$, no $\lim_{t\to\infty}\lambda(t)=0$. |
| `D-C14-03` | Omite límite en H | conceptual_swap | high | Para instante final libre en horizonte infinito basta $H_u=0$ | La condición de transversalidad para instante final libre en horizonte infinito requiere explícitamente que $\lim_{t\to\infty}H(x,u,t)=0$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C14-01` | - | La integral impropia $\int_{t_0}^{+\infty}F(x,u,t)dt$ converge a lo largo de la trayectoria admisible | Si la integral objetivo diverge para controles admisibles, el criterio de optimalidad queda mal definido. | - |

---

### [Hab-11] Ecuación de Euler y Regla de Oro RCK (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 13: Ecuación de Euler y Regla de Oro RCK
- **Prerequisites:** Hab-09
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `04_opt_din_3.pdf` (page 13)

#### Description & Cognitive Model
Derivación de la ecuación dinámica del consumo $\dot{c}=-\frac{u'(c)}{u''(c)}(f'(k)-\delta-\rho)$ en el modelo Ramsey-Cass-Koopmans y cálculo del capital estacionario $k^*=(f')^{-1}(\delta+\rho)$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab11-01` | Omite signo negativo en Euler | skipped_step | high | $\dot{c}=\frac{u'}{u''}(f'-\delta-\rho)$ | Conserve el signo negativo de $\dot{m}=-m(f'-\delta-\rho)$ al sustituir $m=u'$ y $\dot{m}=u''\dot{c}$, pues como $u''<0$, $-\frac{u'}{u''}>0$. |
| `D-Hab11-02` | Invierte razón de derivadas | skipped_step | high | $\dot{c}=-\frac{u''}{u'}(f'-\delta-\rho)$ | Despeje $\dot{c}$ de $u''\dot{c}=-u'(f'-\delta-\rho)$ dividiendo ambos lados por $u''$, lo que ubica a $u'$ en el numerador y a $u''$ en el denominador. |
| `D-Hab11-03` | Confunde regla de oro simple | conceptual_swap | high | $f'(k^*)=\delta$ | Incluya la tasa de preferencia intertemporal $\rho$ en la condición $\dot{c}=0$: el consumo estacionario exige $f'(k^*)=\delta+\rho$. |
| `D-Hab11-04` | Resta delta y rho | conceptual_swap | high | $f'(k^*)=\delta-\rho$ | Sume ambas tasas $\delta+\rho$ al igualar $f'-\delta-\rho=0$; tanto la depreciación como la impaciencia elevan el rendimiento marginal requerido. |
| `D-Hab11-05` | No deriva u'(c) respecto a t | conceptual_swap | high | $u'(c)=\dot{m}$ | Aplique la regla de la cadena respecto al tiempo $t$ sobre $u'(c(t))=m(t)$ para obtener $u''(c)\dot{c}=\dot{m}$ antes de sustituir. |
| `D-Hab11-06` | Omite depreciación en $k_dot$ | conceptual_swap | high | $\dot{k}=f(k)-c$ | Reste la depreciación física $\delta k$ de la producción neta consumida: la acumulación neta es $\dot{k}=f(k)-\delta k-c$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab11-01` | - | Utilidad $u(c)$ doblemente diferenciable con $u'>0, u''<0$ y producción $f(k)$ estrictamente cóncava con $f(0)=0$ | Si $u''=0$ (utilidad lineal), la ecuación de Euler colapsa a soluciones de esquina. | - |

---

### [C-18] Diagrama de Fases, Isoclinas y Estado Estacionario (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 14: Diagrama de Fases y Transversalidad RCK
- **Prerequisites:** Hab-11, Hab-07
- **Recommended Modalities:** invariant_canvas, adversarial_break, multiple_select
- **Evidence Citations:** `04_opt_din_3.pdf` (page 14), `05_Control Optimo Apuntes.pdf` (page 7)

#### Description & Cognitive Model
Análisis cualitativo mediante isoclinas ($\dot{c}=0,\ \dot{k}=0$ o $\dot{C}=0,\ \dot{K}=0$), separación de equilibrios estacionarios triviales e interiores, trayectoria de punto de silla $(k^{**},c^{**})$ y transversalidad asintótica.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C18-01` | Invierte signo de $c_dot$ | conceptual_swap | high | $\dot{c}>0$ para $k>k^{**}$ | Recuerde la concavidad de $f$: para $k>k^{**}$ se cumple $f'(k)<\delta+\rho$, por lo que $\dot{c}<0$ y el consumo decrece. |
| `D-C18-04` | Descarta solución trivial C=0 | conceptual_swap | high | Solo resuelve $g(K)-\theta KC-\rho=0$ | Como $\dot{C}=C(g(K)-\theta KC-\rho)=0$ es un producto, debe analizar por separado el caso trivial $C=0$ y el caso interior $C\neq 0$. |
| `D-C18-02` | Invierte signo de $k_dot$ | conceptual_swap | high | $\dot{k}>0$ arriba de $\dot{k}=0$ | Observe que por encima de la isoclina $\dot{k}=0$, el consumo supera al producto neto $f(k)-\delta k$, haciendo que $\dot{k}<0$. |
| `D-C18-05` | Invierte cociente en K trivial | conceptual_swap | high | $K=\left(\frac{A}{\delta}\right)^{\frac{1}{\alpha-1}}$ | De $AK^\alpha=\delta K$ con $K\neq 0$ se obtiene $K^{\alpha-1}=\frac{\delta}{A}$, por lo que $K=\left(\frac{\delta}{A}\right)^{\frac{1}{\alpha-1}}$. |
| `D-C18-03` | Supone estabilidad global | conceptual_swap | high | Cualquier $c(0)$ converge a $(k^{**},c^{**})$ | Reconozca la dinámica de punto de silla: solo existe una trayectoria estable única que conduce a $(k^{**},c^{**})$ sin violar la transversalidad ni agotar el capital. |
| `D-C18-06` | Error en isoclina de consumo | conceptual_swap | high | $C=\frac{A\alpha K^{\alpha-1}-\delta+\rho}{\theta K}$ | Al igualar $g(K)-\theta KC-\rho=0$, despeje $\theta KC=g(K)-\rho$, lo que da $C=\frac{A\alpha K^{\alpha-1}-\delta-\rho}{\theta K}$ con $-\rho$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C18-01` | - | Condiciones de transversalidad $\lim_{t\to\infty}\lambda(t)k(t)e^{-\rho t}=0$ y $\lim_{t\to\infty}\mathcal{H}(t)e^{-\rho t}=0$ | Sin transversalidad, trayectorias explosivas o de sobreacumulación ineficiente no podrían descartarse. | - |
| `A-C18-02` | - | Parámetros positivos $A,\delta,\theta,\rho>0$ y capital estacionario no nulo $K\neq 0$ | Si $\theta=0$ o $K=0$, la isoclina interior $C=\frac{g(K)-\rho}{\theta K}$ presenta división por cero. | - |

---

### [Hab-12] Modelo Dinámico de Contaminación (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 16: Modelo Dinámico de Contaminación
- **Prerequisites:** C-06
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `04_opt_din_3.pdf` (page 16)

#### Description & Cognitive Model
Optimización del modelo de contaminación con $C=\alpha L$, $P'=C^2-\gamma P$ y $P(T)$ libre: obtención de la trayectoria adjunta $\lambda^*(t)=\frac{\theta}{\rho+\gamma}e^{-\rho t}[e^{-(\rho+\gamma)(T-t)}-1]\le 0$ y consumo óptimo $C^*(t)$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab12-01` | Precio sombra positivo | skipped_step | high | $\lambda^*(t)>0$ | Verifique el signo económico y algebraico: como $e^{-(\rho+\gamma)(T-t)}-1\le 0$ para $t\le T$, resulta $\lambda^*(t)\le 0$, reflejando que la contaminación es un mal. |
| `D-Hab12-02` | Signo erróneo en adjunta | skipped_step | high | $\dot{\lambda}=-\theta e^{-\rho t}-\gamma\lambda$ | Aplique $\frac{\partial H}{\partial P}=-\theta e^{-\rho t}-\gamma\lambda=-\dot{\lambda}$, lo que al multiplicar por $-1$ da $\dot{\lambda}=\theta e^{-\rho t}+\gamma\lambda$. |
| `D-Hab12-03` | Sustituye mal L en U | conceptual_swap | high | $U=\ln C-\frac{\beta}{\alpha}C^2-\theta P$ | Eleve al cuadrado toda la relación $L=C/\alpha$ dentro de $\beta L^2$, obteniendo el término $\frac{\beta}{\alpha^2}C^2$ en la función objetivo. |
| `D-Hab12-04` | Exponente positivo en C*(t) | conceptual_swap | high | $C^*(t)=[\frac{2\beta}{\alpha^2}+\frac{2\theta}{\rho+\gamma}(1-e^{-(\rho+\gamma)(T-t)})]^{1/2}$ | Despeje $C^2$ del denominador en $\frac{1}{C}e^{-\rho t}=[\frac{2\beta}{\alpha^2}e^{-\rho t}-2\lambda]C$ tomando el exponente $-1/2$. |
| `D-Hab12-05` | Omite factor e^(rho*t) | conceptual_swap | high | $C=[\frac{2\beta}{\alpha^2}-2\lambda]^{-1/2}$ | Multiplique ambos términos de $\frac{1}{C}e^{-\rho t}=(\frac{2\beta}{\alpha^2}e^{-\rho t}-2\lambda)C$ por $e^{\rho t}$ antes de despejar $C(t)$. |
| `D-Hab12-06` | Ignora transversalidad $P_T$ libre | conceptual_swap | high | $c_1=0$ | Imponga $\lambda(T)=c_1 e^{\gamma T}-\frac{\theta}{\rho+\gamma}e^{-\rho T}=0$ por ser $P(T)$ libre para hallar $c_1=\frac{\theta}{\rho+\gamma}e^{-(\rho+\gamma)T}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab12-01` | - | Parámetros positivos $\alpha>0$, $\gamma>0$, $\beta>0$, $\theta>0$ con estado terminal $P(T)$ libre | Si $P(T)$ estuviera acotado por un estándar ambiental máximo, $\lambda(T)$ sería estrictamente negativo si la cota es activa. | - |

---

### [Hab-13] Resolución de Control Óptimo Cuadrático Lineal (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Resolución de Control Óptimo por Hamiltoniano
- **Prerequisites:** PRE-01, C-06
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `05_Control Optimo Apuntes.pdf` (page 4), `06_Problemas_teoria_de_control.pdf` (page 1)

#### Description & Cognitive Model
Resolución de problemas cuadráticos lineales de control óptimo (incluyendo inversión óptima en publicidad $\dot{x}=u-0.5x$ con beneficio $4x-u^2$ y $\lambda(2)=0$), hallando $\lambda(t)$, $u^*(t)$ y $x(t)=x_c(t)+x_p(t)$.

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab13-01` | Omite signo negativo en coestado | skipped_step | high | $\dot{\lambda}=\lambda\Rightarrow \lambda(t)=c_1 e^t$ | Al aplicar $\frac{\partial \mathcal{H}}{\partial x}=-\dot{\lambda}$ con $\mathcal{H}=u^2+\lambda(x+u)$, resulta $\lambda=-\dot{\lambda}$, cuya solución es $\lambda(t)=c_1 e^{-t}$. |
| `D-Hab13-07` | Omite depreciación marca | skipped_step | high | $\dot{x}=u$ y $\dot{\lambda}=-4$ | Incorpore la pérdida natural del $50\%$ anual en la ley de movimiento $\dot{x}=u-0.5x$, pues altera tanto $x(t)$ como $\dot{\lambda}$. |
| `D-Hab13-02` | Olvida solución particular | skipped_step | high | $x(t)=c_2 e^t$ | La EDO $\dot{x}=x-\frac{c_1}{2}e^{-t}$ es no homogénea; sume a $x_c(t)=c_2 e^t$ la solución particular $x_p(t)=Ae^{-t}$ con $A=\frac{c_1}{4}$. |
| `D-Hab13-08` | Factor dos en control | skipped_step | high | $u^*(t)=\lambda(t)$ | Derive correctamente el término cuadrático $-u^2$ en $\mathcal{H}_u=-2u+\lambda=0$ para obtener $u^*(t)=\lambda(t)/2$. |
| `D-Hab13-03` | Error en coeficiente particular | conceptual_swap | high | $A=-\frac{c_1}{4}$ o $A=\frac{c_1}{2}$ | Al sustituir $x_p=Ae^{-t}$ y $\dot{x}_p=-Ae^{-t}$ en $\dot{x}=x-\frac{c_1}{2}e^{-t}$, queda $-A=A-\frac{c_1}{2}\Rightarrow 2A=\frac{c_1}{2}\Rightarrow A=\frac{c_1}{4}$. |
| `D-Hab13-09` | Signo en adjunta | conceptual_swap | high | $\dot{\lambda}=-4-0.5\lambda$ | Calcule $\dot{\lambda}=-\mathcal{H}_x=-(4-0.5\lambda)=-4+0.5\lambda$ cuidando el doble signo negativo de la depreciación. |
| `D-Hab13-04` | Invierte signo de control | conceptual_swap | high | $u(t)=+\frac{\lambda}{2}$ | En $\mathcal{H}=u^2+\lambda x+\lambda u$, la condición $\frac{\partial \mathcal{H}}{\partial u}=2u+\lambda=0$ implica $u=-\frac{\lambda}{2}=-\frac{c_1}{2}e^{-t}$. |
| `D-Hab13-10` | Transversalidad en t=0 | conceptual_swap | high | $\lambda(0)=0$ | La condición de transversalidad para estado final libre se evalúa en $T=2$ ($\lambda(2)=0$), mientras $x(0)=1$ fija el estado inicial. |
| `D-Hab13-05` | Aplica fronteras antes de tiempo | conceptual_swap | high | Fija $c_1$ usando solo $x(0)=1$ | Determine las dos constantes $c_1$ y $c_2$ al final resolviendo simultáneamente el sistema $x(0)=1$ y $x(1)=2$. |
| `D-Hab13-11` | Inversión constante | conceptual_swap | high | $u^*(t)=4$ | La cercanía del horizonte final reduce el valor marginal $\lambda(t)$ hasta anularlo en $t=2$, haciendo decreciente la inversión óptima. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab13-01` | - | Condiciones de frontera dadas en ambos extremos $x(0)=x_0$ y $x(T)=x_T$ | Sin condición terminal $x(T)$ se requiere condición de transversalidad $\lambda(T)=0$. | - |
| `A-Hab13-02` | - | Inversión publicitaria no negativa $u(t)\ge 0$ con $\lambda(t)\ge 0$ en $[0,2]$ | Si $\lambda(t)<0$, la restricción $u\ge 0$ se activaría en $u^*=0$. | - |

---

### [Hab-16] Control Cuadrático Aplicado (Inventarios y Seguridad) (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 1: Planificación Producción e Inventarios
- **Prerequisites:** C-06
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, adversarial_break, unstructured_model
- **Evidence Citations:** `06_Problemas_teoria_de_control.pdf` (page 1), `06_Problemas_teoria_de_control.pdf` (page 2)

#### Description & Cognitive Model
Minimización intertemporal de costos cuadráticos en planificación de producción e inventarios ($\dot{x}=u-5$) y seguridad pública ($\dot{x}=4-x-u$) con $x\ge 0$, $u\ge 0$ y condición de transversalidad libre $\lambda(2)=0$.

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab16-01` | Omite factor un medio | skipped_step | high | $\mathcal{H}=-x^2-(u-5)^2+\lambda(u-5)$ | Incluya la mitad del cuadrado tanto en el costo de inventario $\frac{1}{2}x^2$ como en el de ajuste $\frac{1}{2}(u-5)^2$. |
| `D-Hab16-07` | Signo del control en estado | skipped_step | high | $\dot{x}=4-x+u$ | Cada unidad de intervención reduce el ritmo de cambio del índice de delincuencia en una unidad, por lo que ingresa como $-u$. |
| `D-Hab16-02` | Desviación respecto a cero | skipped_step | high | Costo de ajuste $\frac{1}{2}u^2$ | El costo de ajuste penaliza la desviación respecto a cinco unidades anuales, por lo que corresponde a $\frac{1}{2}(u-5)^2$. |
| `D-Hab16-08` | Signo de la relación u y lambda | skipped_step | high | $u^*(t)=\lambda(t)$ | Al maximizar $-(x+\frac{1}{2}u^2)+\lambda(4-x-u)$, la condición $\mathcal{H}_u=-u-\lambda=0$ da $u^*(t)=-\lambda(t)\ge 0$ con $\lambda(t)\le 0$. |
| `D-Hab16-03` | Signo de demanda | conceptual_swap | high | $\dot{x}=u+5$ | El inventario aumenta con la producción $u$ y disminuye con las ventas constantes $5$, dando $\dot{x}=u-5$. |
| `D-Hab16-04` | Fuerza inventario final nulo | conceptual_swap | high | $x(2)=0$ como meta obligatoria | El enunciado indica que no existe obligación de mantener una cantidad específica al final; use $\lambda(2)=0$ y $x(2)=\operatorname{sech}(2)>0$. |
| `D-Hab16-09` | Ecuación adjunta sin signo | conceptual_swap | high | $\dot{\lambda}=-1-\lambda$ | Con pago instantáneo $-x-\frac{1}{2}u^2$, $\mathcal{H}_x=-1-\lambda$, luego $\dot{\lambda}=-\mathcal{H}_x=1+\lambda$ con $\lambda(2)=0$. |
| `D-Hab16-05` | Signo de EDO segundo orden | conceptual_swap | high | $\ddot{x}=-x$ | Al maximizar $-\frac{1}{2}x^2-\frac{1}{2}(u-5)^2+\lambda(u-5)$, resulta $\dot{\lambda}=x$ y $\dot{x}=\lambda$, generando $\ddot{x}=x$ con hiperbólicas. |
| `D-Hab16-10` | Intervención creciente al final | conceptual_swap | high | $u^*(t)=e^{t-2}-1$ o creciente | Como $\lambda(2)=0$, el beneficio marginal de reducir la delincuencia cae a cero al final del horizonte, haciendo $u^*(t)=1-e^{t-2}$ decreciente. |
| `D-Hab16-06` | Confunde signo coestado | conceptual_swap | high | $\lambda(t)>0$ y $u^*(t)>5$ | Dado que el inventario $x(t)>0$ genera costo, su precio sombra $\lambda(t)=-\sinh(2-t)/\cosh(2)$ es negativo y $u^*(t)<5$ para reducir stock. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab16-01` | - | No negatividad de inventario $x(t)\ge 0$ y producción $u(t)\ge 0$ en $[0,2]$ | Verifica que $x^*(t)=\cosh(2-t)/\cosh(2)>0$ y $u^*(t)=5-\sinh(2-t)/\cosh(2)>0$ son interiores. | - |
| `A-Hab16-02` | - | No negatividad del índice $x(t)\ge 0$ y de la intervención $u(t)\ge 0$ en $[0,2]$ | Con $x(0)=5$ y $\dot{x}=4-x-u$, $x^*(t)$ permanece estrictamente positivo en $[0,2]$. | - |

---

### [C-23] Estado Final Fijo y Permisos (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 1: Estado Final Fijo y Permisos
- **Prerequisites:** C-06
- **Recommended Modalities:** adversarial_break, multiple_select, open_symbolic
- **Evidence Citations:** `06_Problemas_teoria_de_control.pdf` (page 1)

#### Description & Cognitive Model
Contraste entre estado libre ($\lambda(T)=0$) y agotamiento exacto de permisos ($x(3)=0$) en $\dot{x}=2-u$ con $\mathcal{H}=12u-u^2+\lambda(2-u)$, donde $\dot{\lambda}=0$ da $u^*=4$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C23-01` | Aplica transversalidad libre | conceptual_swap | high | $\lambda(3)=0$ pese a $x(3)=0$ | Cuando el estado final está fijado en $x(3)=0$, $\lambda(3)$ queda libre y se determina mediante la condición de frontera $x(3)=0$. |
| `D-C23-02` | Omite flujo de entrada | conceptual_swap | high | $\dot{x}=-u$ | Incluya la recepción continua de dos permisos adicionales por año en la ecuación de estado: $\dot{x}=2-u$ con $x(0)=6$. |
| `D-C23-03` | Emisión sin restricción terminal | conceptual_swap | high | $u^*(t)=6$ con $\lambda=0$ | Emitir $u=6$ agotaría los permisos antes del tercer año ($\dot{x}=-4$); el precio sombra $\bar{\lambda}=4$ raciona las emisiones a $u^*=4$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C23-01` | - | Meta terminal exacta $x(3)=0$ con $x(t)\ge 0$ y $u(t)\ge 0$ en $[0,3]$ | Si el agotamiento no fuera obligatorio, $\lambda(3)=0$ implicaría $u^*=6$ hasta agotar el stock. | - |

---
