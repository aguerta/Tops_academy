# Cognitive Task Analysis (CTA): Mateco 4 Test K3

- **Course ID:** `mateco_4_test_k3`
- **Macro-Competency:** Dominio y aplicación analítica integral de Mateco 4 Test K3
- **Structure:** 27 total competencies (0 Facts, 12 Concepts, 15 Skills) with 175 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Funcional de Trayectoria Continua | Concept | Evaluate | Unidad 5: Funcional de Trayectoria Continua | - | 3 |
| `C-02` | Frontera Fija y Puntos Finales Libres | Concept | Analyze | Unidad 6: Frontera Fija y Puntos Finales Libres | C-01 | 3 |
| `C-12` | Formulación de Control Óptimo y Funcionales de Bolza, Mayer y Lagrange | Concept | Understand | Unidad 8: Funcionales de Lagrange, Mayer y Bolza | C-01 | 6 |
| `PRE-01` | Principio del Máximo de Pontryagin (Control Interior) | Concept | Understand | Unidad 3: Principio del Máximo | C-12 | 9 |
| `C-03` | Ecuación de Euler de Primer Orden | Concept | Evaluate | Unidad 9: Ecuación de Euler de Primer Orden | C-01, C-02 | 3 |
| `C-04` | Condición Necesaria de Legendre | Concept | Evaluate | Unidad 10: Condición Necesaria de Legendre | C-03 | 3 |
| `C-05` | Condiciones Variacionales de Segundo Orden y Suficiencia Hessiana | Concept | Evaluate | Unidad 12: Suficiencia Global vía Hessiano | C-03, C-04 | 8 |
| `Hab-01` | Resolución de Euler con Frontera Fija | Skill | Evaluate | Unidad 14: Resolución de Euler con Frontera Fija | C-03 | 6 |
| `Hab-02` | Diagnóstico Integral de Optimalidad | Skill | Evaluate | Unidad 17: Diagnóstico Integral de Optimalidad | Hab-01, C-04, C-05 | 6 |
| `C-07` | Casos Particulares de Euler e Identidad de Beltrami | Concept | Analyze | Unidad 18: Casos Particulares de Euler sin x o sin x-punto | C-05 | 5 |
| `C-09` | Formulación del Monopolio Dinámico de Evans | Concept | Analyze | Unidad 27: Formulación del Monopolio Dinámico de Evans | C-05 | 3 |
| `Hab-05` | Optimización del Tradeoff Inflación-Desempleo | Skill | Evaluate | Unidad 28: Optimización del Tradeoff Inflación-Desempleo | C-05, C-07 | 6 |
| `Hab-06` | Inversión Óptima con Costos de Ajuste Convexos | Skill | Evaluate | Unidad 2: Inversión Óptima con Costos de Ajuste Convexos | C-05 | 6 |
| `Hab-07` | Control Óptimo de Contaminación sin Descuento | Skill | Evaluate | Unidad 3: Control Óptimo de Contaminación sin Descuento | C-05 | 6 |
| `C-11` | Reducción Variacional de Sistemas con Dinámica Lineal | Concept | Evaluate | Unidad 4: Reducción Variacional de Sistemas con Dinámica Lineal | C-05 | 3 |
| `Hab-08` | Crecimiento Óptimo con Utilidad Logarítmica y Daño Ambiental | Skill | Evaluate | Unidad 5: Crecimiento Óptimo con Utilidad Logarítmica y Daño Ambiental | C-05, C-11, PRE-01 | 9 |
| `C-13` | Principio del Máximo con Control Acotado y Mangasarian | Concept | Evaluate | Unidad 3: Principio del Máximo de Pontryagin y Mangasarian | C-12, PRE-01 | 7 |
| `Hab-09` | Deducción de Euler y Transversalidad Terminal en Control Óptimo | Skill | Evaluate | Unidad 5: Deducción de Euler y Transversalidad Terminal | C-13, PRE-01 | 9 |
| `Hab-03` | Resolución Variacional y de Control con Transversalidad Libre | Skill | Evaluate | Unidad 21: Resolución con Estado Final Libre | C-05, C-07, Hab-09 | 10 |
| `Hab-10` | Hamiltoniano en Valor Corriente y Modelo RCK | Skill | Evaluate | Unidad 6: Formulación con Factor de Descuento en Valor Corriente | C-13, PRE-01 | 9 |
| `C-14` | Transversalidad Asintótica en Horizonte Infinito | Concept | Analyze | Unidad 7: Transversalidad Asintótica en Horizonte Infinito | C-13 | 3 |
| `Hab-11` | Resolución de Control Óptimo Lineal-Cuadrático con Extremos Fijos | Skill | Evaluate | Unidad 4: Control Óptimo Básico | PRE-01 | 10 |
| `Hab-13` | Análisis de Isoclinas y Estado Estacionario | Skill | Evaluate | Unidad 13: Dinámica RCK e Isoclinas | Hab-10, Hab-08 | 10 |
| `Hab-14` | Control Óptimo de Contaminación con Utilidad Logarítmica | Skill | Evaluate | Unidad 17: Modelo de Contaminación | Hab-09, Hab-10 | 6 |
| `Hab-16` | Inversión Óptima en Publicidad y Acumulación con Depreciación | Skill | Evaluate | Unidad 5: Modelado de Publicidad y Acumulación | PRE-01 | 10 |
| `Hab-19` | Control Óptimo de Costos Cuadráticos con Restricciones de No Negatividad | Skill | Evaluate | Unidad 1: Planificación de Producción e Inventarios Cuadráticos | PRE-01 | 10 |
| `Hab-20` | Asignación de Permisos de Emisión con Meta Final | Skill | Evaluate | Unidad 1: Asignación de Permisos de Emisión con Meta Final | PRE-01 | 6 |

---

## Detailed Competency Specifications

### [C-01] Funcional de Trayectoria Continua (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Funcional de Trayectoria Continua
- **Prerequisites:** None
- **Recommended Modalities:** unstructured_model, adversarial_break, multiple_select
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 5)

#### Description & Cognitive Model
Un funcional $V[y]=\int_0^T F[t,y(t),y'(t)]\,dt$ asigna un número real a cada trayectoria admisible $y(t)$ según tiempo, estado y pendiente.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Confunde funcional con función | conceptual_swap | high | $F(t,y,y')$ es el funcional | Distinga el integrando puntual $F[t,y(t),y'(t)]$ del funcional $V[y]$, que mapea toda la trayectoria a un escalar. |
| `D-C01-02` | Omite la pendiente en el integrando | conceptual_swap | high | $V[y]=\int_0^T F[t,y(t)]\,dt$ | Incluya la derivada $y'(t)=\frac{dy}{dt}$ en $F$, pues la dirección del arco distingue trayectorias que parten del mismo punto. |
| `D-C01-03` | Optimiza un valor puntual | conceptual_swap | high | $\max_y F(t_0,y(t_0),y'(t_0))$ | Recuerde que la optimización dinámica busca la función completa $y(t)$ sobre $[0,T]$ que extremiza la suma integral. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | La trayectoria $y(t)$ es diferenciable a trozos en $[0,T]$ | Sin $y'(t)$ bien definida no puede evaluarse el integrando $F[t,y(t),y'(t)]$. | - |

---

### [C-02] Frontera Fija y Puntos Finales Libres (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 6: Frontera Fija y Puntos Finales Libres
- **Prerequisites:** C-01
- **Recommended Modalities:** multiple_select, adversarial_break, concept_matching
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 6)

#### Description & Cognitive Model
Distinción entre horizonte y estado terminal fijos frente a problemas con estado final libre ($t=T$ fijo) o instante final libre ($y(T)=Z$ fijo).

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Confunde estado e instante libre | conceptual_swap | high | Estado final libre implica $T$ variable | Identifique qué coordenada permanece fija: en estado final libre $t=T$ es fijo y varía $y(T)$; en instante libre varía $T$. |
| `D-C02-02` | Impone ambos extremos fijos | conceptual_swap | high | Siempre se cumple $y(T)=Z$ y $T$ fijo | Reconozca que liberar $y(T)$ o $T$ exige sustituir la condición de frontera fija por una condición de transversalidad. |
| `D-C02-03` | Libera condición inicial | conceptual_swap | high | $y(0)=A$ también es libre | Mantenga fijo el estado inicial $y(0)=A$ del problema variacional estándar al analizar la libertad del extremo terminal. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | El estado inicial $y(t_0)=x_0$ está dado y fijo | Sin punto de partida fijo la trayectoria carece de anclaje inicial. | - |

---

### [C-12] Formulación de Control Óptimo y Funcionales de Bolza, Mayer y Lagrange (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 8: Funcionales de Lagrange, Mayer y Bolza
- **Prerequisites:** C-01
- **Recommended Modalities:** concept_matching, multiple_select, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 8), `03_Teoria_de_control_optimo___teoria (1).pdf` (page 1)

#### Description & Cognitive Model
Formulación del sistema dinámico $\dot{x}(t)=f(x(t),u(t),t)$ con control admisible $u(t)\in\Omega$ y clasificación de funcionales objetivo en formas equivalentes de Lagrange (integral), Mayer (terminal) y Bolza (mixta).

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C12-01` | Invierte Mayer y Lagrange | conceptual_swap | high | Mayer es $\int_0^T F\,dt$ | Asocie Lagrange exclusivamente con el término integral acumulado y Mayer con la valoración terminal $G(T,y(T))$. |
| `D-C12-02` | Exige diferenciabilidad global en u | conceptual_swap | high | $u(t)$ debe ser continua y diferenciable en todo $[t_0,t_1]$ | Permita discontinuidades de salto finito en el control admisible $u(t)$ mientras la trayectoria de estado $x(t)$ permanezca continua con esquinas en esos instantes. |
| `D-C12-03` | Omite término terminal en Bolza | conceptual_swap | high | Bolza es $\int_0^T F\,dt$ | Recuerde que la forma de Bolza combina el flujo acumulado integral de Lagrange con el término de estado final de Mayer. |
| `D-C12-04` | Estado discontinuo en saltos de control | conceptual_swap | high | $x(t)$ presenta saltos donde $u(t)$ es discontinua | Recuerde que la ecuación de estado integra el control por tramos, por lo que $x(t)$ es continua en todo $[t_0,t_1]$ y solo pierde diferenciabilidad formando esquinas. |
| `D-C12-05` | Usa valor inicial en Mayer | conceptual_swap | high | $V[y]=G(0,y(0))$ | Evalúe la función de Mayer en el horizonte terminal $T$ y el estado final $y(T)$, pues mide el resultado al cierre. |
| `D-C12-06` | Confunde funcional de Mayer y Lagrange | conceptual_swap | high | Mayer conserva $F\neq 0$ y Lagrange conserva $S\neq 0$ | Distinga las reducciones del funcional de Bolza: el funcional de Mayer anula la integral intermedia ($F=0$) y el de Lagrange anula el valor terminal ($S=0$). |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C12-01` | - | Control admisible $u(t)\in\Omega$ continuo por tramos y acotado en un conjunto compacto y convexo $\Omega$ | Si el control toma valores infinitos o sale de $\Omega$, la trayectoria deja de ser admisible y puede no existir óptimo. | - |
| `A-C12-02` | - | Continuidad de la trayectoria de estado $x(t)$ usando el valor terminal de cada tramo como condición inicial del siguiente | Sin continuidad de $x(t)$ en los puntos de conmutación, el funcional objetivo y la dinámica quedan mal definidos. | - |

---

### [PRE-01] Principio del Máximo de Pontryagin (Control Interior) (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 3: Principio del Máximo
- **Prerequisites:** C-12
- **Recommended Modalities:** fill_in_the_blank, multiple_select, concept_matching, unstructured_model
- **Evidence Citations:** `04_opt_din_3.pdf` (page 3), `05_Control Optimo Apuntes.pdf` (page 2), `06_Problemas_teoria_de_control.pdf` (page 1)

#### Description & Cognitive Model
Formulación del Hamiltoniano $H(x,u,\lambda,t)=F(x,u,t)+\lambda f(x,u,t)$ y condiciones necesarias del Principio del Máximo para control interior: $\partial H/\partial u=0$, $\partial H/\partial x=-\dot{\lambda}$ y $\dot{x}=f(x,u,t)$, junto con la interpretación económica del precio sombra $\lambda(t)$.

#### Fused Distractor Models (9)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-PRE01-01` | Signo coestado | conceptual_swap | high | $\frac{\partial H}{\partial x}=\dot{\lambda}$ | Recuerde que la ecuación de coestado exige el signo negativo: la derivada respecto al estado iguala a menos la tasa de cambio del multiplicador. |
| `D-PRE01-02` | Omite restricción dinámica | conceptual_swap | high | $H=f(x,u,t)$ | Incorpore siempre la ecuación de movimiento multiplicada por el coestado $\lambda$ dentro del Hamiltoniano para acoplar control y estado. |
| `D-PRE01-04` | Deriva respecto al estado en optimización | conceptual_swap | high | $\frac{\partial\mathcal{H}}{\partial x}=0$ | Distinga la variable de control (flujo elegible con derivada nula) de la variable de estado (stock sujeto a la ecuación adjunta). |
| `D-PRE01-05` | Transversalidad errónea con estado fijo | conceptual_swap | high | $\lambda(T)=0\text{ siempre}$ | Distinga entre estado terminal libre, que exige $\lambda(T)=0$ sin valor residual, y estado terminal fijo, donde $\lambda(T)$ queda libre. |
| `D-PRE01-03` | Deriva respecto a estado en control | conceptual_swap | high | $\frac{\partial H}{\partial x}=0$ | Distinga la condición estática del control $\partial H/\partial u=0$ de la ecuación dinámica del coestado $\partial H/\partial x=-\dot{\lambda}$. |
| `D-PRE01-06` | Omite restricción dinámica en Hamiltoniano | conceptual_swap | high | $\mathcal{H}=F(x,u,t)+\lambda x$ | Acople el multiplicador de coestado a la tasa de cambio temporal del estado $f(x,u,t)$ y nunca al nivel acumulado del stock. |
| `D-PRE01-07` | Descuento espurio en Hamiltoniano | conceptual_swap | high | $H=e^{-\rho t}F+\lambda f$ | Verifique si el problema carece de descuento temporal antes de multiplicar el integrando por factores exponenciales. |
| `D-PRE01-08` | Confunde stock con control | conceptual_swap | high | $\max_{x(t)} \mathcal{H}$ | Identifique primero qué variable posee derivada temporal en la restricción (estado) para optimizar únicamente respecto al flujo de control. |
| `D-PRE01-09` | Confusión de coestado con control | conceptual_swap | high | $\lambda(t)=u^*(t)$ | Interprete la variable de coestado como el valor marginal del estado sobre el objetivo óptimo, no como la variable de decisión. |

#### Formal Mathematical Assumptions (4)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-PRE01-01` | - | Diferenciabilidad continua de $F(x,u,t)$ y $f(x,u,t)$ respecto a $(x,u)$ | Sin suavidad interior no rige la condición de primer orden $\frac{\partial\mathcal{H}}{\partial u}=0$. | - |
| `A-PRE01-02` | - | Solución interior en el conjunto de controles admisibles $u(t)$ | En soluciones de esquina la derivada parcial respecto al control puede no anularse. | - |
| `A-PRE01-03` | - | Diferenciabilidad de $F(x,u)$ y $f(x,u)$ respecto a $(x,u)$ | Sin diferenciabilidad no aplican las condiciones de primer orden ni la ecuación de coestado. | - |
| `A-PRE01-04` | - | Ausencia de descuento temporal y valor terminal $S(x(T))=0$ | Si hubiera descuento o valor residual, cambiarían el Hamiltoniano y la condición de transversalidad. | - |

---

### [C-03] Ecuación de Euler de Primer Orden (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 9: Ecuación de Euler de Primer Orden
- **Prerequisites:** C-01, C-02
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 9)

#### Description & Cognitive Model
Condición necesaria de primer orden $F_x - \frac{d}{dt}F_{\dot{x}}=0$ (desarrollada como $F_x - F_{\dot{x}x}\dot{x} - F_{\dot{x}\dot{x}}\ddot{x} - F_{\dot{x}t}=0$) para un óptimo local.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Omite derivada total temporal | conceptual_swap | high | $F_x - F_{\dot{x}} = 0$ | Aplique el operador derivada total $\frac{d}{dt}$ sobre $F_{\dot{x}}[x(t),\dot{x}(t),t]$ antes de restar de $F_x$. |
| `D-C03-02` | Invierte signo de la ecuación | conceptual_swap | high | $F_x + \frac{d}{dt}F_{\dot{x}} = 0$ | Verifique el signo negativo entre $F_x$ y $\frac{d}{dt}F_{\dot{x}}$ proveniente de la integración por partes en la primera variación. |
| `D-C03-03` | Deriva parcialmente respecto a t | conceptual_swap | high | $F_x - F_{\dot{x}t} = 0$ | Expanda $\frac{d}{dt}F_{\dot{x}}$ con la regla de la cadena completa: $F_{\dot{x}x}\dot{x} + F_{\dot{x}\dot{x}}\ddot{x} + F_{\dot{x}t}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | $F(x,\dot{x},t)$ es de clase $C^2$ y $x^*(t)\in C^2[t_0,t_1]$ | Sin derivabilidad continua de segundo orden no existen las derivadas parciales de Euler. | - |

---

### [C-04] Condición Necesaria de Legendre (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 10: Condición Necesaria de Legendre
- **Prerequisites:** C-03
- **Recommended Modalities:** adversarial_break, multiple_select, open_symbolic
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 10)

#### Description & Cognitive Model
Condición necesaria de segundo orden: $F_{\dot{x}\dot{x}}[x^*(t),\dot{x}^*(t),t]\le 0$ para máximo local y $F_{\dot{x}\dot{x}}\ge 0$ para mínimo local en todo $t\in[t_0,t_1]$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Invierte desigualdad de Legendre | conceptual_swap | high | $F_{\dot{x}\dot{x}}\ge 0$ para máximo local | Recuerde la concavidad en $\dot{x}$: $F_{\dot{x}\dot{x}}\le 0$ corresponde a máximo local y $F_{\dot{x}\dot{x}}\ge 0$ a mínimo local. |
| `D-C04-02` | Deriva respecto a x en lugar de xdot | conceptual_swap | high | Evalúa $F_{xx}\le 0$ como condición de Legendre | Calcule la segunda derivada parcial exclusivamente respecto a la velocidad $\dot{x}$, pues Legendre controla perturbaciones rápidas. |
| `D-C04-03` | Confunde necesidad con suficiencia | conceptual_swap | high | $F_{\dot{x}\dot{x}}<0$ garantiza máximo global | Considere que Legendre junto con Euler solo garantizan un óptimo local; la globalidad exige concavidad o convexidad global. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | La trayectoria $x^*(t)$ ya satisface la ecuación de Euler | Evaluar $F_{\dot{x}\dot{x}}$ fuera de una extremal de Euler no identifica candidatos a óptimo. | - |

---

### [C-05] Condiciones Variacionales de Segundo Orden y Suficiencia Hessiana (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 12: Suficiencia Global vía Hessiano
- **Prerequisites:** C-03, C-04
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 12), `01_optimizacion_dinamica.pdf` (page 17), `02_Set_Problem_Calculo_de_variaciones.pdf` (page 1)

#### Description & Cognitive Model
Criterio necesario de Legendre $F_{\dot{x}\dot{x}}\le 0$ (o $\ge 0$) y teorema de suficiencia global mediante la concavidad o convexidad conjunta de $F(x,\dot{x},t)$ (o $e^{-rt}F$) vía matriz hessiana $H_F$.

#### Fused Distractor Models (8)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Omite verificar $F_xdot_xdot$ cuando $F_xx$=0 | conceptual_swap | high | $F_{xx}\le 0$ y $\det(H_F)\ge 0$ basta siempre | Cuando $F_{xx}=0$ y $\det(H_F)=0$, verifique también el signo de $F_{\dot{x}\dot{x}}$ para distinguir semidefinida negativa de positiva. |
| `D-C05-04` | Signo invertido Legendre | conceptual_swap | high | $\frac{\partial^2 F}{\partial \dot{x}^2}>0$ para máximo local | Verifique el signo de la segunda derivada respecto a $\dot{x}$: negativa corresponde a concavidad y máximo local, positiva a mínimo local. |
| `D-C05-05` | Omite derivada total temporal | conceptual_swap | high | $L_x - L_{\dot{x}} = 0$ | Aplique el operador derivada total temporal $\frac{d}{dt}L_{\dot{x}}$ incluyendo la dependencia explícita de $t$ y de $\dot{x}(t)$. |
| `D-C05-02` | Confunde definida negativa con convexa | conceptual_swap | high | $H_F$ semidefinida negativa implica convexa | Relacione matriz hessiana semidefinida negativa con concavidad (máximo global) y semidefinida positiva con convexidad (mínimo global). |
| `D-C05-06` | Confunde signo de Legendre | conceptual_swap | high | $L_{\dot{x}\dot{x}} \ge 0$ para máximo | Recuerde que la concavidad en $\dot{x}$ para un máximo exige $L_{\dot{x}\dot{x}} \le 0$, mientras que un mínimo requiere $L_{\dot{x}\dot{x}} \ge 0$. |
| `D-C05-03` | Exige concavidad estricta para máximo global | conceptual_swap | high | Si $\det(H_F)=0$ falla la suficiencia | Aplique el teorema con concavidad/convexidad débil: basta que $H_F$ sea semidefinida para garantizar el óptimo global. |
| `D-C05-07` | Omite derivada cruzada | conceptual_swap | high | Basta $\partial^2 F/\partial x^2 \le 0$ y $\partial^2 F/\partial \dot{x}^2 \le 0$ | Evalúe el determinante completo del hessiano $H_F$, incluyendo las derivadas cruzadas, para confirmar que el segundo menor principal sea no negativo. |
| `D-C05-08` | Solo Legendre sin Hessiana | conceptual_swap | high | $L_{\dot{x}\dot{x}} < 0$ garantiza máximo global | Verifique la concavidad o convexidad conjunta en $(x,\dot{x})$ mediante la matriz Hessiana completa del integrando antes de afirmar optimalidad global. |

#### Formal Mathematical Assumptions (4)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | La concavidad o convexidad en $(x,\dot{x})$ se cumple para todo $t\in[t_0,t_1]$ | Si el signo del hessiano cambia en algún subintervalo de $t$, no se garantiza optimalidad global. | - |
| `A-C05-02` | - | El integrando $F(x,\dot{x},t)$ es dos veces continuamente diferenciable en $(x,\dot{x})$ | Sin diferenciabilidad de segundo orden no existen la condición de Legendre ni la matriz hessiana $H_F$. | - |
| `A-C05-03` | - | Trayectorias admisibles suficientemente regulares $x \in C^2([0,T])$ | Sin regularidad $C^2$ no existe $\ddot{x}$ en Euler-Lagrange. | - |
| `A-C05-04` | - | Condiciones de frontera fijas $x(0)=x_0$ y $x(T)=x_T$ compatibles | Si son incompatibles con restricciones de dominio, no hay trayectoria admisible. | - |

---

### [Hab-01] Resolución de Euler con Frontera Fija (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 14: Resolución de Euler con Frontera Fija
- **Prerequisites:** C-03
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 14)

#### Description & Cognitive Model
Deducción y solución de la ecuación diferencial $F_x - \frac{d}{dt}F_{\dot{x}}=0$ determinando las constantes de integración mediante $x(t_0)=x_0$ y $x(t_1)=x_1$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Confunde derivada total con parcial | skipped_step | high | $\frac{d}{dt}F_{\dot{x}} = F_{\dot{x}t}$ | Recuerde que $\dot{x}(t)$ depende de $t$; al derivar $F_{\dot{x}}$ respecto a $t$ aparecen términos con $\ddot{x}(t)$. |
| `D-Hab01-02` | Signo erróneo en polinomio característico | skipped_step | high | $m^2 + 1 = 0$ cuando $\ddot{x}-x=0$ | Sustituya $x=e^{mt}$ en $\ddot{x}-\alpha^2 x=0$ preservando el signo negativo para obtener raíces reales $\pm\alpha$. |
| `D-Hab01-03` | Omite segunda constante al integrar | conceptual_swap | high | $\ddot{x}=k \Rightarrow x(t)=\frac{k}{2}t^2 + c_1$ | Incorpore dos constantes independientes $c_1 t + c_2$ al integrar una ecuación diferencial de segundo orden. |
| `D-Hab01-04` | Factor erróneo al integrar $t^2$ | conceptual_swap | high | $\int k t\,dt = k t^2$ | Aplique la regla de la potencia en cada integración sucesiva: $\iint k\,dt\,dt = \frac{k}{2}t^2 + c_1 t + c_2$. |
| `D-Hab01-05` | Deja constantes sin resolver | conceptual_swap | high | $x^*(t)=c_1 e^{-t}+c_2 e^t$ sin evaluar frontera | Resuelva el sistema lineal $2\times 2$ con las dos condiciones de frontera para hallar los valores únicos de $c_1$ y $c_2$. |
| `D-Hab01-06` | Despeja mal coeficiente de t | conceptual_swap | high | Error de signo al despejar $c_1$ con $x(t_1)$ | Sustituya primero $t=t_0$ para fijar una relación y luego evalúe $t=t_1$ verificando que ambas fronteras se cumplan. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Las condiciones de frontera $x(t_0)=x_0$ y $x(t_1)=x_1$ son compatibles | Sin dos condiciones de frontera independientes las constantes $c_1,c_2$ quedan indeterminadas. | - |

---

### [Hab-02] Diagnóstico Integral de Optimalidad (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 17: Diagnóstico Integral de Optimalidad
- **Prerequisites:** Hab-01, C-04, C-05
- **Recommended Modalities:** open_symbolic, adversarial_break, unstructured_model
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 17)

#### Description & Cognitive Model
Evaluación conjunta de la ecuación de Euler, condición de Legendre ($F_{\dot{x}\dot{x}}$) y matriz hessiana $H_F$ para clasificar óptimos locales y globales.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Omite factor 2 en segunda derivada de $axdot^2$ | skipped_step | high | $\frac{\partial^2}{\partial \dot{x}^2}(a\dot{x}^2)=a$ | Derive dos veces el término cuadrático $a\dot{x}^2$ respecto a $\dot{x}$: la primera derivada es $2a\dot{x}$ y la segunda es $2a$. |
| `D-Hab02-02` | Invierte signos de menores principales | skipped_step | high | $F_{xx}<0$ y $\det(H_F)<0$ para definida negativa | Recuerde que los menores principales alternan signo: en $2\times 2$ definida negativa el primero es $<0$ y el determinante es $>0$. |
| `D-Hab02-03` | Ignora derivadas cruzadas en $H_F$ | conceptual_swap | high | Asume siempre $F_{x\dot{x}}=0$ | Calcule explícitamente la derivada mixta $F_{x\dot{x}}$ antes de evaluar el determinante $\det(H_F)=F_{xx}F_{\dot{x}\dot{x}}-(F_{x\dot{x}})^2$. |
| `D-Hab02-04` | Confunde mínimo con máximo tras Legendre | conceptual_swap | high | $F_{\dot{x}\dot{x}}<0$ clasifica mínimo local | Verifique el sentido de la desigualdad de Legendre: $F_{\dot{x}\dot{x}}\le 0$ corresponde a máximo y $F_{\dot{x}\dot{x}}\ge 0$ a mínimo. |
| `D-Hab02-05` | No verifica consistencia local-global | conceptual_swap | high | Legendre negativo pero concluye mínimo global | Compruebe la coherencia entre Legendre y el hessiano: todo máximo global en $(x,\dot{x})$ debe satisfacer $F_{\dot{x}\dot{x}}\le 0$. |
| `D-Hab02-06` | Evalua $H_F$ solo en t=$t_0$ | conceptual_swap | high | Verifica $H_F$ únicamente en el punto inicial | Verifique las condiciones de signo sobre $H_F$ para todo $t\in[t_0,t_1]$ y en todo el dominio de $(x,\dot{x})$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | La extremal candidata $x^*(t)$ satisface Euler y las condiciones de frontera | Sin satisfacer Euler y la frontera, las pruebas de segundo orden no certifican ningún óptimo. | - |

---

### [C-07] Casos Particulares de Euler e Identidad de Beltrami (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 18: Casos Particulares de Euler sin x o sin x-punto
- **Prerequisites:** C-05
- **Recommended Modalities:** adversarial_break, multiple_select, open_symbolic, proof_dag
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 18), `01_optimizacion_dinamica.pdf` (page 19)

#### Description & Cognitive Model
Primeras integrales y reducciones de la ecuación de Euler: ausencia de $x$ ($F_{\dot{x}}=c$), ausencia de $\dot{x}$ ($F_x=0$) e identidad de Beltrami $F-\dot{x}F_{\dot{x}}=C$ en sistemas autónomos sin dependencia explícita de $t$.

#### Fused Distractor Models (5)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Anula derivada en vez de igualar a constante | conceptual_swap | high | Si $\partial F/\partial x=0$ entonces $\partial F/\partial \dot{x}=0$ | Al integrar $\frac{d}{dt}\left(\frac{\partial F}{\partial \dot{x}}\right)=0$ respecto al tiempo aparece una constante arbitraria $c$, no necesariamente cero. |
| `D-C07-04` | Signo positivo en Beltrami | conceptual_swap | high | $F + \dot{x}\frac{\partial F}{\partial \dot{x}} = C$ | Derive la identidad usando la regla del producto: $\frac{dF}{dt}=\frac{d}{dt}\left(\dot{x}\frac{\partial F}{\partial \dot{x}}\right)$ implica restar ambos términos. |
| `D-C07-02` | Fuerza condiciones en caso algebraico | conceptual_swap | high | Siempre existe solución para $\partial F/\partial x=0$ con frontera arbitraria | Compruebe si la trayectoria algebraica obtenida de $\partial F/\partial x=0$ satisface las condiciones de frontera dadas; si no, no existe extremal admisible. |
| `D-C07-05` | Aplica con t explícito | conceptual_swap | high | $F - \dot{x}\frac{\partial F}{\partial \dot{x}} = C$ incluso si $\partial F/\partial t \neq 0$ | Verifique primero que $\partial F/\partial t = 0$ explícitamente; de lo contrario, la derivada total $\frac{d}{dt}\left(F-\dot{x}\frac{\partial F}{\partial \dot{x}}\right)$ iguala $\partial F/\partial t \neq 0$. |
| `D-C07-03` | Integra respecto a x | conceptual_swap | high | Si falta $\dot{x}$, se resuelve $\partial F/\partial \dot{x}=c$ | Distinga cuál variable está ausente en $F$: si falta $\dot{x}$, el término temporal desaparece y la ecuación de Euler colapsa a $\partial F/\partial x=0$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Condiciones de frontera fijas $x(t_0)=x_0$ y $x(t_1)=x_1$ en $[t_0,t_1]$ | Cuando falta $\dot{x}$, condiciones de frontera incompatibles con $\partial F/\partial x=0$ dejan el problema sin solución. | - |
| `A-C07-02` | - | Ausencia de dependencia temporal explícita en el integrando: $\frac{\partial F}{\partial t}=0$ | Si $t$ aparece explícitamente en $F$, $F-\dot{x}\frac{\partial F}{\partial \dot{x}}$ deja de ser constante a lo largo del extremal. | - |

---

### [C-09] Formulación del Monopolio Dinámico de Evans (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 27: Formulación del Monopolio Dinámico de Evans
- **Prerequisites:** C-05
- **Recommended Modalities:** unstructured_model, adversarial_break, multiple_select
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 27)

#### Description & Cognitive Model
Planteamiento variacional del monopolio dinámico $\max \int_{t_0}^{t_1} [pq(p,\dot{p}) - C(q)]\,dt$ con demanda dependiente de la tasa de cambio del precio $q=a-bp(t)+h\dot{p}(t)$, costos cuadráticos $C(q)=\alpha q^2+\beta q+\gamma$ y descuento nulo

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Trata q como variable de estado | conceptual_swap | high | Optimiza respecto a $q$ y $\dot{q}$ ignorando $p(t)$ y $\dot{p}(t)$ | Sustituya $q=a-bp(t)+h\dot{p}(t)$ dentro de $pq-C(q)$ para expresar el funcional únicamente en términos del precio $p(t)$ y su derivada $\dot{p}(t)$. |
| `D-C09-02` | Omite efecto especulativo | conceptual_swap | high | Fija $h=0$ reduciendo el problema a estático | Conserve el término $h\dot{p}(t)$ con $h\neq 0$, pues la sensibilidad de la demanda a la variación del precio es lo que vuelve dinámico el problema. |
| `D-C09-03` | Confunde costo con ingreso | conceptual_swap | high | Maximiza $\int_{t_0}^{t_1} [pq + C(q)]\,dt$ | Formule el beneficio instantáneo como ingreso total $pq(p,\dot{p})$ menos el costo total cuadrático $C(q)=\alpha q^2+\beta q+\gamma$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | Parámetros positivos $a,b,\alpha,\beta,\gamma > 0$, $h\neq 0$, tasa de descuento nula y precios frontera $p(t_0)=p_0, p(t_1)=p_1$ | Si $h=0$, desaparece $\dot{p}(t)$ y el problema degenera en optimización estática sin dinámica de precios. | - |

---

### [Hab-05] Optimización del Tradeoff Inflación-Desempleo (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 28: Optimización del Tradeoff Inflación-Desempleo
- **Prerequisites:** C-05, C-07
- **Recommended Modalities:** open_symbolic, unstructured_model, adversarial_break
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 28)

#### Description & Cognitive Model
Minimización del costo social $\int_0^T \left[\left(\frac{\dot{\pi}}{\beta j}\right)^2 + \alpha\left(\frac{\dot{\pi}}{j}+\pi\right)^2\right]\,dt$ derivada de la curva de Phillips y expectativas adaptativas, resolviendo $(1+\beta^2\alpha)\ddot{\pi}-\beta^2 j^2\alpha\pi=0$ con $\pi(0)=\pi_0, \pi(T)=0$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Error al sustituir brecha de producto | skipped_step | high | Sustituye $(y_f-y)=\frac{\dot{\pi}}{\beta j}$ con signo o factor invertido $(\beta j \dot{\pi})$ | Despeje $p=\pi+\frac{\dot{\pi}}{j}$ de $\dot{\pi}=j(p-\pi)$ y reemplace en $p=-\beta(y_f-y)+\pi$ para obtener $y_f-y=-\frac{\dot{\pi}}{\beta j}$. |
| `D-Hab05-02` | Signo positivo en EDO de Euler | skipped_step | high | $(1+\beta^2\alpha)\ddot{\pi} + \beta^2 j^2\alpha\pi = 0$ generando raíces imaginarias | Revise el signo al igualar $F_\pi = \frac{d}{dt}F_{\dot{\pi}}$: los términos cruzados en $\dot{\pi}$ se cancelan y resulta $(1+\beta^2\alpha)\ddot{\pi}-\beta^2 j^2\alpha\pi=0$ con raíces reales. |
| `D-Hab05-03` | Omite término j en raíces | conceptual_swap | high | $r = \pm \frac{\beta\sqrt{\alpha}}{\sqrt{1+\beta^2\alpha}}$ | Multiplique toda la ecuación de Euler por $\beta^2 j^2$ al despejar los denominadores para conservar el coeficiente $\beta^2 j^2\alpha$ en el término en $\pi$. |
| `D-Hab05-04` | Error en constante c1 | conceptual_swap | high | Asume $c_1 = c_2 - \pi_0$ en la sustitución de frontera | De la condición inicial $\pi(0)=c_1+c_2=\pi_0$ despeje correctamente $c_1=\pi_0-c_2$ antes de sustituir en la condición final $\pi(T)=0$. |
| `D-Hab05-05` | Omite término cruzado en hessiano | conceptual_swap | high | Coloca ceros fuera de la diagonal de $H_F$ | Calcule la derivada mixta de $\alpha\left(\frac{\dot{\pi}}{j}+\pi\right)^2$, que aporta $\frac{2\alpha}{j}$ fuera de la diagonal, manteniendo $\det(H_F)=\frac{4\alpha}{(\beta j)^2}>0$. |
| `D-Hab05-06` | Confunde máximo con mínimo | conceptual_swap | high | Exige $\partial^2 F/\partial \dot{\pi}^2 < 0$ para el costo social | Al tratarse de una minimización de costo social, la condición de Legendre exige $\frac{2}{(\beta j)^2}+\frac{2\alpha}{j^2}>0$ y $H_F$ definida positiva. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | Ajuste de expectativas $0 < j \le 1$, ponderación $\alpha > 0$, pendiente $\beta > 0$ y metas $\pi(0)=\pi_0, \pi(T)=0$ | Si $j=0$ o $\beta=0$, el cociente $\frac{\dot{\pi}}{\beta j}$ se indetermina y la trayectoria óptima colapsa. | - |

---

### [Hab-06] Inversión Óptima con Costos de Ajuste Convexos (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 2: Inversión Óptima con Costos de Ajuste Convexos
- **Prerequisites:** C-05
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `02_Set_Problem_Calculo_de_variaciones.pdf` (page 2)

#### Description & Cognitive Model
Resolución del problema $\max \int_0^T e^{-rt}(aK - \frac{b}{2}K^2 - \frac{c}{2}\dot{K}^2)dt$ mediante Euler-Lagrange, ecuación característica $\lambda^2 - r\lambda - \frac{b}{c}=0$ y verificación de máximo global único

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Omite término de descuento en derivada | skipped_step | high | $c\ddot{K} - bK = -a$ | Aplique la regla del producto al calcular $\frac{d}{dt}(-ce^{-rt}\dot{K})$, lo que introduce el término de descuento $+r\dot{K}$ tras simplificar $e^{-rt}$. |
| `D-Hab06-02` | Signo erróneo en término de descuento | skipped_step | high | $\ddot{K} + r\dot{K} - \frac{b}{c}K = -\frac{a}{c}$ | Revise los signos en $L_K - \frac{d}{dt}L_{\dot{K}}=0$: como $L_{\dot{K}}=-ce^{-rt}\dot{K}$, al restar $\frac{d}{dt}L_{\dot{K}}$ resulta $+c\ddot{K}-cr\dot{K}$. |
| `D-Hab06-03` | Estado estacionario invertido | conceptual_swap | high | $K^* = \frac{b}{a}$ | Resuelva la solución particular constante $-\frac{b}{c}K^* = -\frac{a}{c}$, donde el beneficio marginal neto nulo $a - bK^* = 0$ da $K^* = a/b$. |
| `D-Hab06-04` | Ecuación característica sin término lineal | conceptual_swap | high | $\lambda^2 - \frac{b}{c} = 0$ | Incluya la raíz del término $-r\dot{K}$ en la ecuación característica $\lambda^2 - r\lambda - b/c = 0$ para obtener raíces asimétricas por el descuento. |
| `D-Hab06-05` | Hessiana positiva en maximización | conceptual_swap | high | $L_{KK} = b > 0$ y $L_{\dot{K}\dot{K}} = c > 0$ | Evalúe la Hessiana sobre el integrando completo $e^{-rt}(aK - \frac{b}{2}K^2 - \frac{c}{2}\dot{K}^2)$, cuyos elementos diagonales son $-be^{-rt}<0$ y $-ce^{-rt}<0$. |
| `D-Hab06-06` | Confunde inversión neta con stock | conceptual_swap | high | $C(\dot{K}) = \frac{c}{2}K^2$ | Distinga el beneficio operativo que depende del stock $K(t)$ del costo de ajuste que penaliza la velocidad de cambio $I(t)=\dot{K}(t)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Parámetros positivos $a>0$, $b>0$, $c>0$ y tasa de descuento $r>0$ | Si $b\le 0$ o $c\le 0$, falla la concavidad estricta y la existencia de máximo único. | - |

---

### [Hab-07] Control Óptimo de Contaminación sin Descuento (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Control Óptimo de Contaminación sin Descuento
- **Prerequisites:** C-05
- **Recommended Modalities:** open_symbolic, adversarial_break, multiple_select
- **Evidence Citations:** `02_Set_Problem_Calculo_de_variaciones.pdf` (page 3)

#### Description & Cognitive Model
Minimización del costo social acumulado $\int_0^T (\frac{a}{2}P^2 + \frac{b}{2}\dot{P}^2)dt$ sujeto a $P(0)=P_0$, $P(T)=P_T$ y $P(t)\ge 0$, verificando convexidad estricta y unicidad

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Signo erróneo en Euler-Lagrange | skipped_step | high | $\ddot{P} + \frac{a}{b}P = 0$ | Sustituya $L_P = aP$ y $\frac{d}{dt}L_{\dot{P}} = b\ddot{P}$ en $L_P - \frac{d}{dt}L_{\dot{P}} = 0$ para obtener $\ddot{P} - \frac{a}{b}P = 0$ con exponenciales reales. |
| `D-Hab07-02` | Confunde raíces exponenciales con trigonométricas | skipped_step | high | $P(t) = A\cos(\omega t) + B\sin(\omega t)$ | Verifique que la ecuación característica $\lambda^2 - \frac{a}{b} = 0$ con $a,b>0$ tiene raíces reales $\pm\sqrt{a/b}$, por lo que la solución es hiperbólica o exponencial. |
| `D-Hab07-03` | Invierte razón de parámetros | conceptual_swap | high | $\ddot{P} - \frac{b}{a}P = 0$ | Divida toda la ecuación $aP - b\ddot{P} = 0$ entre el coeficiente de $\ddot{P}$, que es el parámetro de costo de ajuste $b$, para obtener $a/b$. |
| `D-Hab07-04` | Omite restricción de no negatividad | conceptual_swap | high | Cualquier $P_0, P_T \in \mathbb{R}$ es admisible | Compruebe explícitamente tras hallar la trayectoria óptima que $P(t) \ge 0$ se cumple en todo $[0,T]$ cuando $P_0, P_T \ge 0$. |
| `D-Hab07-05` | Interpreta mínimo como máximo | conceptual_swap | high | $L_{\dot{P}\dot{P}} = b > 0$ implica máximo | Recuerde que $H = \mathrm{diag}(a, b)$ definida positiva implica convexidad estricta del costo social y garantiza un mínimo global único. |
| `D-Hab07-06` | Introduce tasa de descuento inexistente | conceptual_swap | high | $\ddot{P} - r\dot{P} - \frac{a}{b}P = 0$ | Verifique el planteamiento del problema: el costo social acumulado se integra sin factor de descuento exponencial ($r=0$). |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Parámetros de daño y ajuste positivos $a>0$, $b>0$ con $P_0, P_T \ge 0$ | Si $a\le 0$ o $b\le 0$, se pierde la convexidad estricta del costo social. | - |

---

### [C-11] Reducción Variacional de Sistemas con Dinámica Lineal (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Reducción Variacional de Sistemas con Dinámica Lineal
- **Prerequisites:** C-05
- **Recommended Modalities:** unstructured_model, adversarial_break, multiple_select
- **Evidence Citations:** `02_Set_Problem_Calculo_de_variaciones.pdf` (page 4)

#### Description & Cognitive Model
Sustitución de la variable de control ($u(t)=\dot{G}+\delta G$ o $q(t)=E-\dot{x}-\delta x$) en problemas con tasa de depreciación $\delta>0$ y descuento $r>0$, cancelando términos cruzados en Euler-Lagrange y verificando $\det H > 0$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C11-01` | Error al despejar el control | conceptual_swap | high | $q(t) = E + \dot{x} + \delta x$ | Despeje cuidadosamente la variable de control desde la ecuación de movimiento: si $\dot{x}=E-q-\delta x$, entonces $q = E - \dot{x} - \delta x$. |
| `D-C11-02` | No cancela término cruzado en EDO | conceptual_swap | high | $\ddot{G} - (r - 2\delta)\dot{G} - \dots = 0$ | Verifique que en $L_G - \frac{d}{dt}L_{\dot{G}}=0$ el término $-b\delta\dot{G}$ de $L_G$ se cancela exactamente con $+b\delta\dot{G}$ proveniente de $-\frac{d}{dt}L_{\dot{G}}$. |
| `D-C11-03` | Omite términos cruzados en la Hessiana | conceptual_swap | high | $H = \mathrm{diag}(L_{xx}, L_{\dot{x}\dot{x}})$ | Calcule la derivada cruzada mixta $L_{x\dot{x}} = \pm e^{-rt}b\delta \ne 0$ y evalúe $\det H = L_{xx}L_{\dot{x}\dot{x}} - (L_{x\dot{x}})^2 = e^{-2rt}ab > 0$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C11-01` | - | Control sin restricción de no negatividad ($u(t), q(t) \in \mathbb{R}$) para solución interior | Restricciones activas sobre el control invalidan Euler-Lagrange interior. | - |
| `A-C11-02` | - | Tasa de depreciación $\delta > 0$ y parámetros cuadráticos $a, b > 0$ | Si $a \le 0$ o $b \le 0$, el determinante Hessiano $e^{-2rt}ab$ deja de ser positivo. | - |

---

### [Hab-08] Crecimiento Óptimo con Utilidad Logarítmica y Daño Ambiental (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Crecimiento Óptimo con Utilidad Logarítmica y Daño Ambiental
- **Prerequisites:** C-05, C-11, PRE-01
- **Recommended Modalities:** open_symbolic, proof_dag, unstructured_model, adversarial_break
- **Evidence Citations:** `02_Set_Problem_Calculo_de_variaciones.pdf` (page 5), `05_Control Optimo Apuntes.pdf` (page 6)

#### Description & Cognitive Model
Derivación de la ecuación de Euler y del sistema dinámico $(\dot{K},\dot{C})$ para $F(K,\dot{K},t)=e^{-\rho t}(\ln C-\frac{\theta}{2}K^2)$ con $C=AK^\alpha-\dot{K}-\delta K$, obteniendo $\dot{C}/C=g(K)-\theta KC-\rho$ y verificando concavidad estricta.

#### Fused Distractor Models (9)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | Omite daño ambiental en regla de Keynes-Ramsey | skipped_step | high | $\frac{\dot{C}}{C} = \alpha AK^{\alpha-1} - \delta - \rho$ | Incluya la derivada del daño ambiental $-\theta K$ en $L_K$; al multiplicar toda la ecuación por $C$ aparece el término corrector $-\theta K C$ que frena la acumulación. |
| `D-Hab08-07` | Omite regla de la cadena en derivada temporal | conceptual_swap | high | $\frac{d}{dt}\left(\frac{-e^{-\rho t}}{C}\right)=\frac{\rho e^{-\rho t}}{C}$ | Aplique la regla del cociente y la regla de la cadena al derivar respecto al tiempo, pues el consumo óptimo $C(t)$ depende de $t$. |
| `D-Hab08-02` | Deriva mal el logaritmo respecto a $K_dot$ | skipped_step | high | $L_{\dot{K}} = e^{-\rho t}\frac{1}{C}$ | Aplique la regla de la cadena sobre $\ln(AK^\alpha - \delta K - \dot{K})$: como $\frac{\partial C}{\partial \dot{K}} = -1$, resulta $L_{\dot{K}} = -e^{-\rho t}/C$. |
| `D-Hab08-08` | Omite desutilidad del capital en Euler | conceptual_swap | high | $\frac{\dot{C}}{C}=g(K)-\rho$ | Incluya la derivada parcial del daño ambiental respecto al stock en $\frac{\partial F}{\partial K}$ antes de despejar la tasa de crecimiento del consumo. |
| `D-Hab08-03` | Error en derivada temporal de 1/C | conceptual_swap | high | $\frac{d}{dt}\left(-\frac{e^{-\rho t}}{C}\right) = e^{-\rho t}\left(\frac{\dot{C}}{C} + \frac{\rho}{C}\right)$ | Derive $C(t)^{-1}$ respecto al tiempo obteniendo $-C^{-2}\dot{C}$, lo cual produce $\dot{C}/C^2$ antes de multiplicar por $C$ para hallar $\dot{C}/C$. |
| `D-Hab08-04` | Intenta hallar solución cerrada elemental | conceptual_swap | high | $K(t) = c_1 e^{\lambda_1 t} + c_2 e^{\lambda_2 t}$ | Reconozca que la no linealidad de $AK^\alpha$ y $\ln C$ impide soluciones elementales cerradas, por lo que el óptimo se caracteriza con el sistema $(\dot{K}, \dot{C})$. |
| `D-Hab08-09` | Confunde productividad neta con bruta | conceptual_swap | high | $g(K)=A\alpha K^{\alpha-1}$ | Reste la tasa de depreciación del capital a la productividad marginal bruta al evaluar el rendimiento neto del stock. |
| `D-Hab08-05` | Evalúa consumo no positivo | conceptual_swap | high | $C(t) \le 0$ es admisible en el óptimo | Exija $C(t) = AK^\alpha - \delta K - \dot{K} > 0$ y $K(t) > 0$ en todo $[0,T]$ para que la función de utilidad logarítmica esté bien definida. |
| `D-Hab08-06` | Signo erróneo de Legendre en utilidad logarítmica | conceptual_swap | high | $L_{\dot{K}\dot{K}} = \frac{e^{-\rho t}}{C^2} > 0$ | Aplique el doble signo negativo: $\frac{\partial}{\partial \dot{K}}(-e^{-\rho t}C^{-1}) = e^{-\rho t}C^{-2}\frac{\partial C}{\partial \dot{K}} = -e^{-\rho t}/C^2 < 0$. |

#### Formal Mathematical Assumptions (4)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab08-01` | - | Elasticidad $0<\alpha<1$, $A>0$, $\theta>0$, $\rho>0$, $\delta\ge 0$ | Si $\alpha \ge 1$, la función de producción deja de ser estrictamente cóncava. | - |
| `A-Hab08-02` | - | Dominio estricto $K(t)>0$ y $C(t)=AK^\alpha-\delta K-\dot{K}>0$ | Si $C(t)\le 0$, el integrando logarítmico $\ln C$ no está definido en $\mathbb{R}$. | - |
| `A-Hab08-03` | - | Consumo estrictamente positivo $C(t)>0$ y factor de descuento $e^{-\rho t}\neq 0$ | Si $C\le 0$ la función de utilidad logarítmica $\ln C$ deja de estar definida. | - |
| `A-Hab08-04` | - | Despeje biyectivo del control $C=AK^\alpha-\dot{K}-\delta K$ en el funcional | Si el control no es despejable en términos de $(K,\dot{K})$, no aplica directamente la Ecuación de Euler. | - |

---

### [C-13] Principio del Máximo con Control Acotado y Mangasarian (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Principio del Máximo de Pontryagin y Mangasarian
- **Prerequisites:** C-12, PRE-01
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `03_Teoria_de_control_optimo___teoria (1).pdf` (page 3), `04_opt_din_3.pdf` (page 6)

#### Description & Cognitive Model
Condiciones necesarias del Principio del Máximo sobre $u\in\Omega$ ($H_x=-\dot{\lambda}$, $H_\lambda=\dot{x}$) combinadas con el criterio suficiente de optimalidad global de Mangasarian mediante la matriz hessiana del Hamiltoniano respecto a $(x,u)$.

#### Fused Distractor Models (7)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C13-01` | Aplica siempre Hu=0 en problemas lineales | conceptual_swap | high | $H_u=0$ determina el óptimo incluso si $H$ es lineal en $u$ | Verifique si $H$ es lineal en $u$ sobre $\Omega=[u_1,u_2]$: al no depender $H_u$ del control, la maximización exige solución de esquina en los extremos de $\Omega$. |
| `D-C13-05` | Invierte concavidad y convexidad | conceptual_swap | high | $H_F$ convexa implica máximo | Recuerde que una matriz Hessiana semidefinida positiva corresponde a convexidad (mínimo global) y semidefinida negativa a concavidad (máximo global). |
| `D-C13-02` | Invierte ecuaciones del sistema canónico | conceptual_swap | high | $H_x=\dot{x}$ y $H_\lambda=-\dot{\lambda}$ | Identifique que $H_\lambda=\frac{\partial H}{\partial\lambda}=f(x,u,t)=\dot{x}$ gobierna la variable de estado, mientras $H_x=-\dot{\lambda}$ determina la evolución del coestado. |
| `D-C13-06` | Solo evalúa segunda derivada en u | conceptual_swap | high | Usa solo $\partial^2 H/\partial u^2$ | Construya la matriz Hessiana conjunta $H_F$ respecto tanto al estado $x$ como al control $u$ para verificar la suficiencia global de Mangasarian. |
| `D-C13-03` | Signo erróneo en la ecuación de coestado | conceptual_swap | high | $H_x=\dot{\lambda}$ en lugar de $H_x=-\dot{\lambda}$ | Mantenga el signo negativo en la ecuación adjunta $H_x=-\dot{\lambda}$ del sistema canónico de Pontryagin para preservar la optimalidad de primer orden. |
| `D-C13-07` | Confunde necesidad con suficiencia | conceptual_swap | high | Mangasarian es condición necesaria | Distinga que el Principio del Máximo brinda condiciones necesarias, mientras que Mangasarian aporta suficiencia global mediante la curvatura de $H$. |
| `D-C13-04` | Confunde concavidad y convexidad de Mangasarian | conceptual_swap | high | $H^e_H$ definida positiva garantiza máximo y definida negativa garantiza mínimo | Aplique la condición suficiente de Mangasarian correctamente: $H^e_H(x^*,u^*,\lambda,t)$ cóncava (definida negativa) certifica máximo y convexa (definida positiva) certifica mínimo. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C13-01` | - | Variable de coestado $\lambda^*(t)$ continua y con primeras derivadas continuas en todo $[t_0,t_1]$ | Sin regularidad $C^1$ del coestado, el sistema canónico $H_x=-\dot{\lambda}$ no queda bien definido puntualmente. | - |
| `A-C13-02` | - | Concavidad o convexidad conjunta de $H(x,u,\lambda,t)$ en $(x,u)$ evaluada mediante la matriz hessiana $H^e_H$ | Sin verificación de segundo orden de Mangasarian, un punto que satisface Pontryagin puede no ser óptimo global. | - |
| `A-C13-03` | - | El dominio de control es convexo y $H$ es dos veces diferenciable en $(x,u)$ | Sin concavidad o convexidad conjunta de $H$, el punto crítico podría ser solo local. | - |

---

### [Hab-09] Deducción de Euler y Transversalidad Terminal en Control Óptimo (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Deducción de Euler y Transversalidad Terminal
- **Prerequisites:** C-13, PRE-01
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, proof_dag, adversarial_break
- **Evidence Citations:** `03_Teoria_de_control_optimo___teoria (1).pdf` (page 5), `04_opt_din_3.pdf` (page 8)

#### Description & Cognitive Model
Traducción del cálculo de variaciones a control óptimo ($u=\dot{x}$) y aplicación de condiciones de transversalidad en horizonte fijo $[0,T]$ con estado final libre ($\lambda(T)=\partial S/\partial x|_{t=T}=0$) o instante final libre.

#### Fused Distractor Models (9)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab09-01` | Signo positivo en multiplicador de variaciones | skipped_step | high | $H_u=F_u+\lambda=0\Rightarrow\lambda=F_u$ | Despeje con signo negativo $\lambda=-F_u$ de $H_u=F_u+\lambda=0$ antes de derivar respecto al tiempo y sustituir en la ecuación de coestado $F_x=-\dot{\lambda}$. |
| `D-Hab09-07` | Fija el estado en vez del coestado | conceptual_swap | high | $x(T)=0$ | Cuando el estado terminal $x(T)$ es libre, la condición de transversalidad restringe al multiplicador $\lambda(T)$ y no al valor físico de $x(T)$. |
| `D-Hab09-02` | Omite derivada total respecto al tiempo en Euler | skipped_step | high | $F_x-F_{\dot{x}}=0$ | Aplique la derivada total temporal $-\dot{\lambda}=\frac{dF_u}{dt}=\frac{dF_{\dot{x}}}{dt}$ al sustituir $\lambda=-F_u$ en $F_x=-\dot{\lambda}$ para obtener la ecuación de Euler. |
| `D-Hab09-08` | Evalúa transversalidad en t=0 | conceptual_swap | high | $\lambda(0)=0$ | Aplique la condición de transversalidad en el extremo libre $t=T$, ya que en $t=0$ el estado inicial $x(0)$ está dado como condición de contorno. |
| `D-Hab09-03` | Fuerza coestado nulo con valor terminal S distinto de cero | conceptual_swap | high | $\lambda(t_1)=0$ aunque exista función de rescate $S[x(t_1)]$ | Evalúe la derivada marginal de la función terminal cuando el estado final es libre: $\left.\frac{dS}{dx}\right|_{t=t_1}=\lambda(t_1)$, que solo se anula si $S=0$. |
| `D-Hab09-09` | Usa condición de tiempo libre | conceptual_swap | high | $H(T)=0$ | Distinga entre estado final libre ($\lambda(T)=0$) e instante final libre ($H(T)=0$ cuando no hay función de valor residual $S$). |
| `D-Hab09-04` | Olvida derivada parcial de S respecto a t1 | conceptual_swap | high | $H(x^*(t_1),u^*(t_1),\lambda^*(t_1),t_1^*)=0$ con $S[x(t_1),t_1]$ | Sume la contribución temporal directa de la función terminal en la transversalidad de instante final libre: $H(t_1)+\left.\frac{dS}{dt_1}\right|_{t=t_1}=0$. |
| `D-Hab09-05` | Aplica transversalidad de estado libre a problema con x(t1) fijo | conceptual_swap | high | Impone $\lambda(t_1)=S'(x(t_1))$ cuando $x(t_1)=x_1$ está fijado | Verifique primero si el estado final $x(t_1)$ es libre antes de imponer $\lambda(t_1)=\left.\frac{dS}{dx}\right|_{t_1}$; si $x(t_1)=x_1$ es dato, la condición de borde recae sobre $x$. |
| `D-Hab09-06` | Intercambia condiciones de estado libre e instante libre | conceptual_swap | high | Usa $H(t_1)=0$ para estado final libre y $\lambda(t_1)=0$ para instante libre | Asocie cada libertad terminal con su multiplicador conjugado: el estado final libre restringe al coestado $\lambda(t_1)$ y el instante final libre restringe al Hamiltoniano $H(t_1)$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab09-01` | - | No linealidad de $F(x,\dot{x},t)$ en $\dot{x}$ para la reducción desde Pontryagin a la ecuación de Euler | Si $F$ es lineal en $u=\dot{x}$, la condición $H_u=0$ no permite despejar $\lambda=-F_u$ de forma interior. | - |
| `A-Hab09-02` | - | El horizonte temporal $T$ es fijo y no existe restricción terminal sobre $x(T)$ | Si $x(T)$ está fijo, no aplica $\lambda(T)=0$ sino la condición de frontera $x(T)=x_T$. | - |

---

### [Hab-03] Resolución Variacional y de Control con Transversalidad Libre (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 21: Resolución con Estado Final Libre
- **Prerequisites:** C-05, C-07, Hab-09
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model, adversarial_break
- **Evidence Citations:** `01_optimizacion_dinamica.pdf` (page 21), `01_optimizacion_dinamica.pdf` (page 24), `04_opt_din_3.pdf` (page 10)

#### Description & Cognitive Model
Determinación de trayectorias óptimas y horizontes terminales mediante condiciones de transversalidad para estado final libre ($\partial F/\partial \dot{x}|_{t_1}=0$) e instante final libre ($F-\dot{x}F_{\dot{x}}|_{t_1}=0$ y $H(t_1)+\partial S/\partial t|_{t_1}=0$).

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Transversalidad en t0 | skipped_step | high | $\left.\frac{\partial F}{\partial \dot{x}}\right|_{t=t_0}=0$ | Aplique la condición de transversalidad en el extremo donde el estado es libre ($t=t_1$), mientras en $t=t_0$ se impone la condición inicial dada $x(t_0)=x_0$. |
| `D-Hab03-07` | Usa condición de estado libre | skipped_step | high | $\left.\frac{\partial F}{\partial \dot{x}}\right|_{t=t_1}=0$ cuando $t_1$ es libre | Cuando el estado final $x(t_1)=x_1$ está fijo y el tiempo $t_1$ es libre, la condición de transversalidad es $\left.\left(F-\dot{x}\frac{\partial F}{\partial \dot{x}}\right)\right|_{t=t_1}=0$. |
| `D-Hab03-08` | Aplica transversalidad de estado libre | skipped_step | high | $\lambda(t_1)=0$ | Dado que $x(t_1)$ está fijo y el tiempo terminal $t_1$ es libre, debe anularse el Hamiltoniano aumentado en $t_1$ y no el coestado. |
| `D-Hab03-02` | Anula el estado final | skipped_step | high | $x(t_1)=0$ cuando $x(t_1)$ es libre | No iguale el estado $x(t_1)$ a cero cuando es libre; la optimización fija el valor marginal $\left.\frac{\partial F}{\partial \dot{x}}\right|_{t=t_1}=0$ en la frontera. |
| `D-Hab03-09` | Anula solo el integrando | skipped_step | high | $\left.F\right|_{t=t_1}=0$ al optimizar $t_1$ | Incluya el término $-\dot{x}\frac{\partial F}{\partial \dot{x}}$ en la condición de transversalidad de tiempo libre para capturar el ajuste de la trayectoria al variar $t_1$. |
| `D-Hab03-10` | Signo erróneo al evaluar H(t1) | skipped_step | high | $t_1^2+u^2+\lambda u$ sin sustituir $u^*=-\lambda/2$ | Sustituya las trayectorias óptimas $x^*(t_1)$, $u^*(t_1)$ y $\lambda^*(t_1)$ dentro de $H$ antes de resolver la ecuación para el instante óptimo $t_1$. |
| `D-Hab03-03` | Usa condición de tiempo libre | conceptual_swap | high | $\left.\left(F-\dot{x}\frac{\partial F}{\partial \dot{x}}\right)\right|_{t=t_1}=0$ para estado libre | Distinga los casos de frontera: si $t_1$ es fijo y $x(t_1)$ libre, la condición correcta es $\left.\frac{\partial F}{\partial \dot{x}}\right|_{t=t_1}=0$, sin el término $F$. |
| `D-Hab03-11` | Acepta tiempo terminal negativo | conceptual_swap | high | $t_1<0$ | Descarte raíces temporales negativas al resolver la ecuación cuadrática de transversalidad, pues el horizonte económico exige $t_1>0$. |
| `D-Hab03-04` | Anula derivada primera del estado | conceptual_swap | high | $\dot{x}(t_1)=0$ siempre que $x(t_1)$ sea libre | Calcule primero la derivada parcial $\frac{\partial F}{\partial \dot{x}}$ del integrando antes de evaluar en $t=t_1$, pues puede incluir términos en $x$ o $t$. |
| `D-Hab03-12` | Descarta raíz positiva de t1 | conceptual_swap | high | Acepta $t_1 < t_0$ al despejar la ecuación cuadrática final | Al resolver la ecuación final para el horizonte $t_1$, seleccione la raíz real que satisfaga $t_1 > t_0$ acorde al dominio temporal del problema. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | Instante final $t_1$ fijo con estado inicial $x(t_0)=x_0$ dado y $x(t_1)$ sin restricción | Si $x(t_1)$ estuviera fijo, desaparecería la condición $\left.\partial F/\partial \dot{x}\right|_{t=t_1}=0$. | - |
| `A-Hab03-02` | - | Estados inicial $x(t_0)=x_0$ y final $x(t_1)=x_1$ fijos con horizonte $t_1 > t_0$ libre | Si $t_1$ fuera fijo, el sistema quedaría sobredeterminado al agregar la transversalidad de tiempo libre. | - |
| `A-Hab03-03` | - | El instante final $t_1>0$ es una variable de elección libre con $x(t_1)$ fijo | Si $t_1$ estuviera fijo, sobraría la ecuación $H(t_1)+\partial S/\partial t=0$. | - |

---

### [Hab-10] Hamiltoniano en Valor Corriente y Modelo RCK (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 6: Formulación con Factor de Descuento en Valor Corriente
- **Prerequisites:** C-13, PRE-01
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model, adversarial_break
- **Evidence Citations:** `03_Teoria_de_control_optimo___teoria (1).pdf` (page 6), `04_opt_din_3.pdf` (page 12)

#### Description & Cognitive Model
Transformación del Hamiltoniano en valor presente $H=e^{-\rho t}F+\lambda f$ al Hamiltoniano en valor corriente $\mathcal{H}=F+mf$ con $m=\lambda e^{\rho t}$, coestado $\partial\mathcal{H}/\partial x=-\dot{m}+\rho m$ y formulación en el modelo Ramsey-Cass-Koopmans.

#### Fused Distractor Models (9)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab10-01` | Omite el término rho*m en el coestado corriente | skipped_step | high | $\frac{\partial\mathcal{H}}{\partial x}=-\dot{m}$ | Aplique la regla del producto al derivar $m=\lambda e^{\rho t}$, lo que introduce el término adicional de descuento $\rho m$ en $\frac{\partial\mathcal{H}}{\partial x}=-\dot{m}+\rho m$. |
| `D-Hab10-07` | Omite término de descuento en coestado | conceptual_swap | high | $\frac{\partial \mathcal{H}}{\partial k}=-\dot{m}$ | Al trabajar con el Hamiltoniano en tiempo corriente $\mathcal{H}$, debe sumar $\rho m$ al lado derecho de la ecuación de coestado por el factor de descuento. |
| `D-Hab10-02` | Signo invertido en el término de descuento del coestado | skipped_step | high | $\frac{\partial\mathcal{H}}{\partial x}=-\dot{m}-\rho m$ | Verifique el signo sustituyendo $\dot{m}=\dot{\lambda}e^{\rho t}+\rho m$ y $\frac{\partial\mathcal{H}}{\partial x}=-e^{\rho t}\dot{\lambda}$, de donde resulta $\frac{\partial\mathcal{H}}{\partial x}=-\dot{m}+\rho m$. |
| `D-Hab10-08` | Incluye descuento dentro de H corriente | conceptual_swap | high | $\mathcal{H}=e^{-\rho t}u(c)+m\dot{k}$ | Distinga el Hamiltoniano en valor presente (que incluye $e^{-\rho t}$) del Hamiltoniano en tiempo corriente $\mathcal{H}$ (que factoriza el descuento en $m$). |
| `D-Hab10-03` | Cambio de variable con exponente negativo | conceptual_swap | high | $m=\lambda e^{-\rho t}$ | Multiplique por $e^{\rho t}$ (exponente positivo) al definir el coestado corriente $m=\lambda e^{\rho t}$ porque $\mathcal{H}=e^{\rho t}H$ reescala todo el Hamiltoniano. |
| `D-Hab10-09` | Olvida depreciación en acumulación | conceptual_swap | high | $\dot{k}=f(k)-c$ | Reste el desgaste físico $\delta k$ además del consumo $c$ al expresar la acumulación neta de capital $\dot{k}=f(k)-\delta k-c$. |
| `D-Hab10-04` | Descuenta doblemente la función intermedia F en H corriente | conceptual_swap | high | $\mathcal{H}=e^{-\rho t}F+mf$ | Recuerde que multiplicar $H=e^{-\rho t}F+\lambda f$ por $e^{\rho t}$ cancela el factor de descuento en $F$, dejando $\mathcal{H}=F(x,u,t)+mf(x,u,t)$. |
| `D-Hab10-05` | Aplica transversalidad m(t1)=0 olvidando el factor exponencial | conceptual_swap | high | $\lambda(t_1)=m(t_1)=0$ sin el factor $e^{-\rho t_1}$ | Exprese la condición de estado final libre desde el valor presente $\lambda(t_1)=m(t_1)e^{-\rho t_1}=0$ antes de concluir la anulación en valor corriente. |
| `D-Hab10-06` | No multiplica H por exp(rho*t1) en instante final libre | conceptual_swap | high | Impone $H(t_1)=0$ con una expresión distinta a $\mathcal{H}(t_1)=0$ | Use la equivalencia $H(t_1)=0\Rightarrow e^{\rho t_1}H(t_1)=\mathcal{H}(t_1)=0$ para expresar correctamente la transversalidad de instante final libre en valor corriente. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab10-01` | - | Tasa de descuento constante $\rho$ en el factor exponencial $e^{-\rho t}$ del funcional objetivo | Si la tasa de descuento varía con el tiempo, $\dot{m}$ incorpora $\dot{\rho}$ y no se reduce a $-\dot{m}+\rho m$. | - |
| `A-Hab10-02` | - | Utilidad $u(c)$ con $u'>0, u''<0$ y producción $f(k)$ estrictamente cóncava con $f(0)=0$ | Sin concavidad estricta no se garantiza trayectoria única hacia el estado estacionario. | - |

---

### [C-14] Transversalidad Asintótica en Horizonte Infinito (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 7: Transversalidad Asintótica en Horizonte Infinito
- **Prerequisites:** C-13
- **Recommended Modalities:** adversarial_break, multiple_select, concept_matching
- **Evidence Citations:** `03_Teoria_de_control_optimo___teoria (1).pdf` (page 7)

#### Description & Cognitive Model
Extensión del Principio del Máximo de Pontryagin a problemas de horizonte infinito $\max\int_{t_0}^{+\infty}F(x,u,t)dt$ distinguiendo las condiciones de transversalidad asintóticas para instante final libre ($\lim_{t\to\infty}H=0$), estado final fijo o meta asintótica ($\lim_{t\to\infty}x(t)=x_0$) y estado final libre ($\lim_{t\to\infty}\lambda(t)=0$)

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C14-01` | Aplica transversalidad de coestado en meta asintótica fija | conceptual_swap | high | Impone $\lim_{t\to\infty}\lambda(t)=0$ cuando $\lim_{t\to\infty}x(t)=x_0$ es fijo | Distinga el régimen terminal: cuando existe una meta asintótica fija $\lim_{t\to\infty}x(t)=x_0\in\mathbb{R}$, la condición de borde recae sobre $x(t)$ y no sobre $\lambda(t)\to 0$. |
| `D-C14-02` | Confunde meta asintótica con condición inicial x0 | conceptual_swap | high | $\lim_{t\to\infty}x(t)=x(t_0)$ obligatoriamente | Diferencie el dato inicial $x(t_0)=x_0$ de la constante real prefijada en la meta asintótica $\lim_{t\to\infty}x(t)=x_o$ cuando el estado final es fijo en horizonte infinito. |
| `D-C14-03` | Anula el Hamiltoniano para todo t en lugar del límite | conceptual_swap | high | $H(x,u,t)=0$ para todo $t\in[t_0,\infty)$ en instante final libre | Aplique la condición de transversalidad únicamente en el límite asintótico $\lim_{t\to\infty}H(x,u,t)=0$, nunca como identidad puntual para todo $t$ finito. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C14-01` | - | Convergencia del funcional integral impropio $\int_{t_0}^{+\infty}F(x,u,t)dt$ en el horizonte infinito | Si la integral diverge para las trayectorias admisibles, el criterio de optimalidad directa deja de ser bien definido. | - |

---

### [Hab-11] Resolución de Control Óptimo Lineal-Cuadrático con Extremos Fijos (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Control Óptimo Básico
- **Prerequisites:** PRE-01
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `04_opt_din_3.pdf` (page 4), `05_Control Optimo Apuntes.pdf` (page 4)

#### Description & Cognitive Model
Resolución completa de problemas de control óptimo lineal-cuadrático con extremos fijos $(x(0),x(T))$ mediante el Principio del Máximo, integrando las EDO de coestado y estado para hallar $x^*(t)$, $u^*(t)$ y $\lambda^*(t)$.

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab11-01` | Omite solución particular | skipped_step | high | $x(t)=c_2 e^t$ | Sume la solución particular a la complementaria antes de imponer las condiciones inicial y final de la ecuación diferencial lineal. |
| `D-Hab11-07` | Signo erróneo en exponente del coestado | skipped_step | high | $\lambda(t)=c_1 e^t$ | Verifique el signo al despejar $\dot{\lambda}=-\frac{\partial\mathcal{H}}{\partial x}$ antes de integrar la ecuación diferencial homogénea del coestado. |
| `D-Hab11-02` | Constantes sin contorno | skipped_step | high | $c_1$ y $c_2$ indeterminadas | Utilice ambas condiciones de frontera, inicial y final, para formar un sistema cerrado que determine de forma única las constantes de integración. |
| `D-Hab11-08` | Signo positivo al despejar el control | skipped_step | high | $u(t)=+\frac{\lambda}{2}$ | Mantenga el signo negativo al trasladar el término de coestado en la condición de primer orden respecto al control óptimo. |
| `D-Hab11-03` | Coestado con signo positivo | conceptual_swap | high | $\lambda(t)=c_1 e^t$ | Verifique el signo en $\dot{\lambda}=-\partial H/\partial x$ antes de integrar la ecuación diferencial del multiplicador de Lagrange. |
| `D-Hab11-04` | No sustituye control en estado | conceptual_swap | high | $\dot{x}=x+u$ sin despejar $u$ | Exprese primero el control óptimo $u^*(t)$ en función del coestado $\lambda(t)$ y sustitúyalo en la ecuación de movimiento del estado. |
| `D-Hab11-09` | Error en coeficiente indeterminado | conceptual_swap | high | $x_p(t)=\frac{c_1}{2}e^{-t}$ | Derive explícitamente la forma propuesta $x_p(t)$ y sustituya tanto $x_p$ como $\dot{x}_p$ en la EDO para igualar coeficientes. |
| `D-Hab11-05` | Error coeficiente particular | conceptual_swap | high | $a=-c_1/2$ | Derive correctamente el término exponencial propuesto en la solución particular y agrupe los términos semejantes antes de despejar el coeficiente. |
| `D-Hab11-10` | Evalúa frontera antes de integrar estado | conceptual_swap | high | $u(0)=x(0)$ | Determine las constantes de integración del coestado y del estado al final del procedimiento usando las condiciones de frontera dadas. |
| `D-Hab11-06` | Confunde orden de integración | conceptual_swap | high | Integra $x(t)$ antes de $\lambda(t)$ | Resuelva secuencialmente: primero la ecuación de coestado $\lambda(t)$, luego el control óptimo $u(t)$ y finalmente la trayectoria del estado $x(t)$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab11-01` | - | La función objetivo es diferenciable y la ecuación de estado es lineal en $(x,u)$ | Si no es diferenciable, no aplican las condiciones de primer orden clásicas. | - |
| `A-Hab11-02` | - | Condiciones de frontera fijas en ambos extremos $x(0)=x_0$ y $x(T)=x_T$ | Sin dos condiciones de frontera quedan indeterminadas las constantes $(c_1,c_2)$. | - |

---

### [Hab-13] Análisis de Isoclinas y Estado Estacionario (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 13: Dinámica RCK e Isoclinas
- **Prerequisites:** Hab-10, Hab-08
- **Recommended Modalities:** open_symbolic, unstructured_model, adversarial_break, multiple_select
- **Evidence Citations:** `04_opt_din_3.pdf` (page 13), `05_Control Optimo Apuntes.pdf` (page 7)

#### Description & Cognitive Model
Determinación de isoclinas $\dot{c}=0$ y $\dot{k}=0$ y estados estacionarios en modelos dinámicos de crecimiento (RCK estándar y con daño ambiental), separando equilibrios triviales e interiores y evaluando estabilidad de punto de silla.

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab13-01` | Signo invertido en ecuación de Euler | skipped_step | high | $\dot{c}=\frac{u'}{u''}(f'-\delta-\rho)$ | Combine $u''(c)\dot{c}=\dot{m}$ con $\dot{m}=-m(f'-\delta-\rho)$ y $u'=m$ para preservar el signo negativo que asegura $\dot{c}>0$ cuando $f'>\delta+\rho$. |
| `D-Hab13-07` | Descarta solución trivial al dividir por C | skipped_step | high | $g(K)-\theta KC-\rho=0$ | Factorice $\dot{C}=C(g(K)-\theta KC-\rho)=0$ y evalúe por separado la rama trivial $C=0$ y la rama interior $C\neq 0$. |
| `D-Hab13-02` | Estado estacionario sin descuento | skipped_step | high | $f'(k^*)=\delta$ | Recuerde que en el modelo RCK la regla de oro modificada incorpora la tasa de preferencia intertemporal $\rho$ además de la depreciación $\delta$. |
| `D-Hab13-08` | Invierte exponente en capital trivial | skipped_step | high | $K=\left(\frac{\delta}{A}\right)^{\alpha-1}$ | Agrupe las potencias del capital como $K^{\alpha-1}=\frac{\delta}{A}$ y eleve ambos lados al recíproco $\frac{1}{\alpha-1}$. |
| `D-Hab13-03` | Isoclina $k_dot$=0 sin depreciación | conceptual_swap | high | $c=f(k)$ | Reste la depreciación $\delta k$ de la producción $f(k)$ para obtener la curva cóncava en forma de campana de la isoclina $\dot{k}=0$. |
| `D-Hab13-09` | Omite producto por K en denominador de isoclina | conceptual_swap | high | $C=\frac{g(K)-\rho}{\theta}$ | Divida por todo el coeficiente $\theta K$ (con $K\neq 0$) al aislar el consumo en la isoclina interior de $\dot{C}=0$. |
| `D-Hab13-04` | Confunde estabilidad global con punto de silla | conceptual_swap | high | Cualquier trayectoria converge a $(k^*,c^*)$ | Analice las flechas de fase en los cuatro cuadrantes alrededor de $(k^*,c^*)$ para identificar la estructura de punto de silla con una única senda convergente. |
| `D-Hab13-10` | Confunde isoclina de capital con producto | conceptual_swap | high | $C=AK^\alpha$ | Recuerde que en estado estacionario $\dot{K}=0$ parte del producto debe reponer la depreciación $\delta K$ del capital. |
| `D-Hab13-05` | Omite transversalidad en horizonte infinito | conceptual_swap | high | Usa $\lambda(T)=0$ finito | En horizonte infinito, reemplace la condición terminal finita por $\lim_{t\to\infty}\lambda(t)k(t)e^{-\rho t}=0$ para descartar trayectorias explosivas. |
| `D-Hab13-11` | Omite rho en isoclina del consumo | conceptual_swap | high | $C=\frac{A\alpha K^{\alpha-1}-\delta}{\theta K}$ | Incluya la tasa de preferencia temporal $\rho$ junto a la depreciación al igualar la tasa de crecimiento del consumo a cero. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab13-01` | - | Se cumplen las condiciones de Inada y $\lim_{t\to\infty}H(t)e^{-\rho t}=0$ | Sin transversalidad asintótica, la familia podría sobreacumular capital ineficientemente. | - |
| `A-Hab13-02` | - | Parámetros positivos $A,\delta,\rho,\theta>0$ y elasticidad $\alpha\in(0,1)$ | Si $\alpha=1$ desaparece la curvatura necesaria para un equilibrio interior finito. | - |

---

### [Hab-14] Control Óptimo de Contaminación con Utilidad Logarítmica (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 17: Modelo de Contaminación
- **Prerequisites:** Hab-09, Hab-10
- **Recommended Modalities:** open_symbolic, unstructured_model, fill_in_the_blank
- **Evidence Citations:** `04_opt_din_3.pdf` (page 17)

#### Description & Cognitive Model
Resolución del problema de control óptimo de contaminación con dinámica $P'=C^2-\gamma P$, utilidad $U=\ln C-\frac{\beta}{\alpha^2}C^2-\theta P$ y estado final libre $P(T)=P_T$, hallando $\lambda^*(t)$ y el consumo óptimo $C^*(t)$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab14-01` | Signo erróneo en EDO del coestado | skipped_step | high | $\dot{\lambda}=-\theta e^{-\rho t}-\gamma\lambda$ | Calcule $\partial H/\partial P=-\theta e^{-\rho t}-\gamma\lambda$ e iguálelo a $-\dot{\lambda}$ para obtener $\dot{\lambda}-\gamma\lambda=\theta e^{-\rho t}$. |
| `D-Hab14-02` | Omite sustitución laboral en utilidad | skipped_step | high | Mantiene $L^2$ en lugar de $C^2/\alpha^2$ | Utilice la relación tecnológica $C(t)=\alpha L(t)$ para expresar la desutilidad del trabajo $\beta L^2$ exclusivamente en términos del control $C$. |
| `D-Hab14-03` | Exponente incorrecto al despejar C | conceptual_swap | high | $C^*=\left[\frac{2\beta}{\alpha^2}-2\lambda e^{\rho t}\right]^{1/2}$ | Agrupe los términos en $C$ al resolver $\partial H/\partial C=0$ y note que $C^2$ queda en el denominador, produciendo el exponente $-1/2$. |
| `D-Hab14-04` | Ignora transversalidad de $P_T$ libre | conceptual_swap | high | Deja $c_1$ sin determinar | Aplique la condición de transversalidad $\lambda(T)=0$ por ser $P(T)$ libre para determinar la constante $c_1$ de la trayectoria del coestado. |
| `D-Hab14-05` | Error en denominador de solución particular | conceptual_swap | high | Usa $\gamma-\rho$ en vez de $\rho+\gamma$ | Al sustituir $A e^{-\rho t}$ en $\dot{\lambda}-\gamma\lambda=\theta e^{-\rho t}$, sume los coeficientes $(-\rho-\gamma)A=\theta$ para obtener $A=-\theta/(\rho+\gamma)$. |
| `D-Hab14-06` | Mezcla reglas de tiempo corriente y presente | conceptual_swap | high | Usa $-\dot{\lambda}+\rho\lambda$ en $H$ con $e^{-\rho t}$ | Verifique si el Hamiltoniano incluye el factor $e^{-\rho t}$: si está en valor presente, la regla de coestado es $\partial H/\partial P=-\dot{\lambda}$ sin el término $+\rho\lambda$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab14-01` | - | Los parámetros tecnológicos y ambientales $\alpha, \beta, \gamma, \theta, \rho$ son estrictamente positivos | Si $\gamma\le 0$ o $\alpha\le 0$, la dinámica de polución o consumo pierde sentido económico. | - |

---

### [Hab-16] Inversión Óptima en Publicidad y Acumulación con Depreciación (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Modelado de Publicidad y Acumulación
- **Prerequisites:** PRE-01
- **Recommended Modalities:** unstructured_model, open_symbolic, multiple_select, adversarial_break
- **Evidence Citations:** `05_Control Optimo Apuntes.pdf` (page 5), `06_Problemas_teoria_de_control.pdf` (page 1)

#### Description & Cognitive Model
Planteamiento del Hamiltoniano $\mathcal{H}=4x-u^2+\lambda(u-0.5x)$ y resolución completa de la trayectoria óptima de reconocimiento de marca $x^*(t)$ e inversión en publicidad $u^*(t)$ con depreciación y estado final libre.

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab16-01` | Invierte rol de estado y control | skipped_step | high | $\dot{a}=G-0.5a$ | Distinga el stock acumulado que sufre depreciación u olvido (variable de estado) del flujo elegido instantáneamente (variable de control). |
| `D-Hab16-07` | Omite depreciación del reconocimiento | skipped_step | high | $\dot{x}=u$ | Incluya la depreciación natural del stock de reconocimiento restando el producto de la tasa de desgaste por el estado vigente. |
| `D-Hab16-02` | Omite depreciación en ecuación de estado | skipped_step | high | $\dot{G}=a$ | Incorpore la tasa de depreciación proporcional al stock en la ley de movimiento para reflejar el deterioro temporal del activo. |
| `D-Hab16-08` | Signo erróneo en coestado lineal | skipped_step | high | $\dot{\lambda}=4+0.5\lambda$ | Recuerde que la ecuación de coestado lleva signo negativo frente a la derivada parcial del Hamiltoniano respecto al estado. |
| `D-Hab16-03` | Error de signo en derivada del coestado | conceptual_swap | high | $-0.5\lambda=+\dot{\lambda}$ | Derive todos los términos dependientes del estado tanto en el beneficio instantáneo como en la dinámica antes de igualar a $-\dot{\lambda}$. |
| `D-Hab16-09` | Despeje incorrecto del control | conceptual_swap | high | $u^*(t)=\lambda(t)$ | Derive el término cuadrático del costo publicitario con su exponente completo antes de igualar a cero para despejar el control. |
| `D-Hab16-04` | Olvida factor cuadrático al optimizar control | conceptual_swap | high | $-a+\lambda=0$ | Aplique correctamente la regla de la potencia al derivar el costo cuadrático de ajuste respecto a la variable de control. |
| `D-Hab16-10` | Fija estado final en cero | conceptual_swap | high | $x(2)=0$ | Cuando el estado final es libre y no tiene valor residual, la condición terminal recae sobre el coestado y no sobre el estado. |
| `D-Hab16-05` | Aplica ingreso lineal como ahorro sin descuento | conceptual_swap | high | $\dot{K}=rK+C$ | Recuerde que el consumo detrae recursos de la inversión bruta, por lo que entra con signo negativo en la acumulación del capital. |
| `D-Hab16-11` | Usa beneficio lineal en control | conceptual_swap | high | $H=4x-u+\lambda(u-0.5x)$ | Verifique la forma funcional cuadrática del costo de inversión antes de construir el Hamiltoniano y aplicar condiciones de primer orden. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab16-01` | - | Costo convexo cuadrático en el control y tasa de depreciación constante | Sin convexidad del costo no existe solución interior única para la inversión óptima. | - |
| `A-Hab16-02` | - | No negatividad de la inversión publicitaria $u(t)\ge 0$ | Si $\lambda(t)<0$ sería necesario truncar el control óptimo en cero en lugar de usar la fórmula interior. | - |
| `A-Hab16-03` | - | Concavidad estricta del Hamiltoniano en el control $u$ | Sin $\partial^2 H/\partial u^2<0$ la condición de primer orden no garantiza máximo. | - |

---

### [Hab-19] Control Óptimo de Costos Cuadráticos con Restricciones de No Negatividad (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 1: Planificación de Producción e Inventarios Cuadráticos
- **Prerequisites:** PRE-01
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, adversarial_break, unstructured_model
- **Evidence Citations:** `06_Problemas_teoria_de_control.pdf` (page 1), `06_Problemas_teoria_de_control.pdf` (page 2)

#### Description & Cognitive Model
Minimización de costos cuadráticos en horizonte finito $[0,2]$ con estado final libre $x(2)$ y restricciones $u\ge 0$, $x\ge 0$ mediante Pontryagin en modelos de producción-inventarios y asignación a seguridad pública.

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab19-01` | Maximiza en vez de minimizar | skipped_step | high | $H=-\frac{1}{2}x^2-\frac{1}{2}(u-5)^2+\lambda(u-5)$ con $\dot{\lambda}=-x$ | Mantenga consistencia entre la convención elegida para el funcional objetivo y los signos de la condición de optimalidad y del coestado. |
| `D-Hab19-07` | Omite decaimiento natural del índice | skipped_step | high | $\dot{x}=4-u$ | Incorpore la tasa anual de disminución natural proporcional al nivel vigente del índice dentro de la ecuación de estado. |
| `D-Hab19-02` | Omite ventas en ecuación de inventario | skipped_step | high | $\dot{x}=u$ | Reste el flujo constante de ventas a la tasa de producción al formular la dinámica de acumulación del inventario. |
| `D-Hab19-08` | Signo erróneo en intervención sobre estado | skipped_step | high | $\dot{x}=4-x+u$ | Verifique que cada unidad de intervención pública reduce el ritmo de crecimiento del índice, entrando con signo negativo. |
| `D-Hab19-03` | Omite desviación en costo de ajuste | conceptual_swap | high | $\frac{1}{2}u^2$ | Exprese el costo de ajuste como la mitad del cuadrado de la diferencia entre producción y nivel de referencia. |
| `D-Hab19-09` | Coestado con signo invertido en minimización | conceptual_swap | high | $\dot{\lambda}=1-\lambda$ | Aplique $\dot{\lambda}=-\partial H/\partial x$ con los signos exactos del costo instantáneo y de la ecuación de estado. |
| `D-Hab19-04` | Despeje invertido del control | conceptual_swap | high | $u^*(t)=5+\lambda(t)$ | Despeje con cuidado el control desde la derivada del Hamiltoniano de minimización respecto a la tasa de producción. |
| `D-Hab19-05` | Raíces trigonométricas en EDO de segundo orden | conceptual_swap | high | $\ddot{x}+x=0$ | Verifique el signo al derivar la ecuación de estado y sustituir la dinámica del coestado para obtener funciones hiperbólicas. |
| `D-Hab19-06` | Impone inventario final nulo | conceptual_swap | high | $x(2)=0$ | Dado que el inventario final es libre y sin valor residual, utilice la condición de transversalidad sobre el coestado terminal. |
| `D-Hab19-10` | Fija meta terminal de delincuencia nula | conceptual_swap | high | $x(2)=0$ | Al no existir meta terminal obligatoria ni costo final, el estado terminal es libre y la condición de transversalidad anula el coestado final. |

#### Formal Mathematical Assumptions (4)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab19-01` | - | Trayectoria interior no negativa $x(t)\ge 0$ y $u(t)\ge 0$ | Si el control o el estado tocaran cero, activarían restricciones de desigualdad y multiplicadores adicionales. | - |
| `A-Hab19-02` | - | Convexidad estricta del Hamiltoniano en $(x,u)$ | Garantiza que la solución estacionaria corresponda a un mínimo global del costo total. | - |
| `A-Hab19-03` | - | No negatividad del índice de delincuencia y de la intervención $x(t)\ge 0,\;u(t)\ge 0$ | Si el índice alcanzara cero antes del final, se requeriría analizar restricciones de estado activas. | - |
| `A-Hab19-04` | - | Ausencia de meta final obligatoria y de costo terminal adicional | Permite aplicar la condición de transversalidad estándar $\lambda(T)=0$ sobre el coestado final. | - |

---

### [Hab-20] Asignación de Permisos de Emisión con Meta Final (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 1: Asignación de Permisos de Emisión con Meta Final
- **Prerequisites:** PRE-01
- **Recommended Modalities:** unstructured_model, open_symbolic, multiple_select
- **Evidence Citations:** `06_Problemas_teoria_de_control.pdf` (page 1)

#### Description & Cognitive Model
Maximización de $\int_0^3 (12u-u^2)\,dt$ sujeto a $\dot{x}=2-u$, $x(0)=6$, $x(3)=0$, $u\ge 0$ y $x\ge 0$, identificando trayectoria constante de emisiones y coestado constante no nulo.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab20-01` | Impone coestado terminal nulo | skipped_step | high | $\lambda(3)=0$ | Cuando la restricción terminal fija el nivel exacto del estado final, la variable de coestado terminal queda libre y puede ser no nula. |
| `D-Hab20-02` | Omite dotación continua en estado | skipped_step | high | $\dot{x}=-u$ | Sume el flujo continuo de permisos otorgados por unidad de tiempo antes de restar las emisiones instantáneas. |
| `D-Hab20-03` | Signo invertido en coestado | conceptual_swap | high | $u^*(t)=6+\frac{\lambda(t)}{2}$ | Observe que las emisiones reducen el stock de permisos, por lo que el coestado entra con signo negativo al derivar respecto al control. |
| `D-Hab20-04` | Emisiones máximas miopes | conceptual_swap | high | $u^*(t)=6$ | Recuerde que la escasez intertemporal de permisos introduce un precio sombra positivo que modera la tasa óptima de emisión. |
| `D-Hab20-05` | Error en balance acumulado de permisos | conceptual_swap | high | $\int_0^3 u(t)\,dt=x(0)$ | Sume la dotación acumulada a lo largo de todo el horizonte al stock inicial para determinar el presupuesto total de permisos. |
| `D-Hab20-06` | Supone coestado dependiente del tiempo | conceptual_swap | high | $\dot{\lambda}=-\lambda$ | Verifique que ni el beneficio instantáneo ni la ecuación de movimiento dependen del stock de permisos, por lo que el coestado es constante. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab20-01` | - | Disponibilidad no negativa de permisos $x(t)\ge 0$ en todo el horizonte | Con trayectoria constante lineal entre extremos positivos y cero, la restricción de no negatividad se satisface automáticamente. | - |
| `A-Hab20-02` | - | Concavidad estricta del beneficio instantáneo en $u$ | Asegura que suavizar las emisiones de manera constante maximice el beneficio total. | - |

---
