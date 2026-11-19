# Cognitive Task Analysis (CTA): Mateco 4 Optimizacion Plus

- **Course ID:** `mateco_4_optimizacion_plus`
- **Macro-Competency:** Dominio y aplicación analítica integral de Mateco 4 Optimizacion Plus
- **Structure:** 30 total competencies (1 Facts, 16 Concepts, 13 Skills) with 208 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Principio del Máximo y Hamiltoniano | Concept | Understand | Unidad 2: Principio del Máximo y Hamiltoniano | - | 10 |
| `C-02` | Identidades Macroeconómicas de Acumulación | Concept | Understand | Unidad 3: Identidades Macroeconómicas de Acumulación | C-01 | 6 |
| `Hab-01` | Resolución de Control Óptimo Lineal | Skill | Apply | Unidad 4: Resolución de Control Óptimo Lineal | C-01 | 10 |
| `Hab-02` | Derivación por Ecuación de Euler | Skill | Apply | Unidad 6: Derivación por Ecuación de Euler | C-01, C-02 | 6 |
| `Hab-03` | Estado Estacionario, Isoclinas y Diagrama de Fases | Skill | Analyze | Unidad 7: Análisis de Estado Estacionario e Isoclinas | Hab-02 | 10 |
| `C-04` | Condición Suficiente de Mangasarian | Concept | Evaluate | Unidad 4: Condición Suficiente de Mangasarian | C-01 | 10 |
| `C-05` | Condiciones de Transversalidad (Estado y Tiempo Libre) | Concept | Understand | Unidad 8: Condiciones de Transversalidad (Estado y Tiempo Libre) | C-01 | 6 |
| `Hab-05` | Cálculo de Trayectorias con Frontera Libre | Skill | Apply | Unidad 10: Cálculo de Trayectorias con Frontera Libre | C-05, C-01 | 10 |
| `C-06` | Hamiltoniano en Tiempo Corriente (Modelo RCK) | Concept | Understand | Unidad 12: Hamiltoniano en Tiempo Corriente (Modelo RCK) | C-01 | 6 |
| `Hab-07` | Optimización Dinámica en Modelo de Contaminación | Skill | Apply | Unidad 16: Optimización Dinámica en Modelo de Contaminación | C-01, C-05 | 6 |
| `C-07` | Forma Funcional y Trayectorias | Concept | Understand | Unidad 5: Forma Funcional y Trayectorias | - | 6 |
| `H-01` | Puntos Finales y Transversalidad | Fact | Remember | Unidad 6: Puntos Finales y Transversalidad | C-07 | 6 |
| `C-08` | Funcionales Lagrange Mayer Bolza | Concept | Understand | Unidad 8: Funcionales Lagrange Mayer Bolza | C-07 | 6 |
| `C-09` | Ecuación de Euler | Concept | Understand | Unidad 9: Ecuación de Euler | C-08 | 6 |
| `C-10` | Condición de Legendre | Concept | Understand | Unidad 10: Condición de Legendre | C-09 | 6 |
| `C-11` | Suficiencia y Criterio Hessiano | Concept | Analyze | Unidad 11: Suficiencia y Criterio Hessiano | C-09 | 6 |
| `Hab-08` | Resolución de Euler con EDO | Skill | Apply | Unidad 14: Resolución de Euler con EDO | C-09, C-10, C-11 | 10 |
| `C-12` | Casos Particulares sin x o dx/dt | Concept | Understand | Unidad 18: Casos Particulares sin x o dx/dt | C-09 | 6 |
| `C-13` | Identidad de Beltrami | Concept | Understand | Unidad 19: Identidad de Beltrami | C-12 | 6 |
| `Hab-10` | Resolución de Casos Particulares | Skill | Apply | Unidad 20: Resolución de Casos Particulares | C-12, C-13 | 6 |
| `C-14` | Transversalidad: Estado Final Libre | Concept | Understand | Unidad 21: Transversalidad: Estado Final Libre | C-12 | 6 |
| `Hab-11` | Extremales con Estado Final Libre | Skill | Apply | Unidad 22: Extremales con Estado Final Libre | C-14 | 6 |
| `C-15` | Transversalidad: Instante Final Libre | Concept | Understand | Unidad 24: Transversalidad: Instante Final Libre | C-13, C-14 | 6 |
| `Hab-12` | Extremales con Horizonte Libre | Skill | Apply | Unidad 25: Extremales con Horizonte Libre | C-15 | 6 |
| `Hab-13` | Modelado Económico Variacional | Skill | Analyze | Unidad 28: Modelado Económico Variacional | C-12, Hab-10 | 6 |
| `C-16` | Principio del Máximo de Pontryagin | Concept | Understand | Unidad 1: Principio del Máximo de Pontryagin | C-01 | 6 |
| `Hab-14` | Aplicaciones de Control Óptimo con Estado Libre | Skill | Apply | Unidad 1: Inversión Óptima en Publicidad | C-16 | 10 |
| `Hab-16` | Utilización Óptima de Permisos de Emisión | Skill | Apply | Unidad 1: Utilización Óptima de Permisos de Emisión | C-16 | 6 |
| `C-17` | Planteamiento de Control Óptimo | Concept | Understand | Unidad 1: Planteamiento de Control Óptimo | C-01, C-07 | 6 |
| `Hab-19` | Hamiltoniano en Valor Corriente | Skill | Apply | Unidad 6: Hamiltoniano en Valor Corriente | C-01, Hab-05 | 6 |

---

## Detailed Competency Specifications

### [C-01] Principio del Máximo y Hamiltoniano (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 2: Principio del Máximo y Hamiltoniano
- **Prerequisites:** None
- **Evidence Citations:** `Control Optimo Apuntes.pdf` (page 2), `opt_din_3.pdf` (page 3), `Teoria_de_control_optimo___teoria (1).pdf` (page 3)

#### Description & Cognitive Model
Formulación del Hamiltoniano $\mathcal{H}(x,u,\lambda,t)=F(x,u,t)+\lambda f(x,u,t)$ distinguiendo estado (stock) y control (flujo) mediante las condiciones $\frac{\partial\mathcal{H}}{\partial u}=0$, $\frac{\partial\mathcal{H}}{\partial x}=-\dot{\lambda}$ y $\dot{x}=f(x,u,t)$

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Signo coestado | conceptual_swap | high | $\frac{\partial\mathcal{H}}{\partial x}=\dot{\lambda}$ | Recuerde el signo negativo en la ecuación adjunta: la derivada respecto al estado iguala a $-\dot{\lambda}$. |
| `D-C01-07` | Signo en coestado | conceptual_swap | high | $H_x=\dot{\lambda}$ | En el sistema canónico la ecuación del coestado lleva signo menos: $H_x=-\dot{\lambda}$, es decir $\dot{\lambda}=-H_x$. |
| `D-C01-02` | Deriva en control | conceptual_swap | high | $\frac{\partial\mathcal{H}}{\partial u}=-\dot{\lambda}$ | Separe las condiciones: la optimización respecto al control $u$ se iguala a cero y la del estado $x$ a $-\dot{\lambda}$. |
| `D-C01-08` | Deriva respecto a x | conceptual_swap | high | $\frac{\partial H}{\partial x}=0$ | Solo el control $u$ satisface $\partial H/\partial u=0$; el estado $x$ evoluciona según $\partial H/\partial x=-\dot{\lambda}$. |
| `D-C01-09` | Multiplica F por lambda | conceptual_swap | high | $H=\lambda F + f$ | La variable de coestado $\lambda(t)$ multiplica a la restricción dinámica $f(x,u,t)$, formando $H=F+\lambda f$. |
| `D-C01-03` | Confunde stock-flujo | conceptual_swap | high | Trata $u(t)$ como estado | Identifique como variable de estado aquella cuya derivada temporal aparece en la restricción dinámica. |
| `D-C01-10` | Omite restricción | conceptual_swap | high | $H=F(x,u,t)$ | Incorpore siempre la ecuación de transición $\dot{x}=f$ multiplicada por el coestado $\lambda$ dentro del Hamiltoniano. |
| `D-C01-11` | Fuerza Hu=0 en esquina | conceptual_swap | high | $H_u=0\text{ siempre}$ | Si $H$ es lineal en $u$ o el óptimo cae en la frontera de $\Omega$, $H_u=0$ no aplica y debe maximizar $H$ en los extremos. |
| `D-C01-04` | Omite multiplicador | conceptual_swap | high | $\mathcal{H}=F(x,u,t)+f(x,u,t)$ | Multiplique siempre la ecuación de movimiento $f(x,u,t)$ por la variable de coestado dinámica $\lambda(t)$. |
| `D-C01-12` | Coestado constante | conceptual_swap | high | $\lambda(t)=c_1$ | El coestado $\lambda(t)$ solo es constante si $H$ no depende explícitamente del estado $x$; resuelva $\dot{\lambda}=-\partial H/\partial x$. |

#### Formal Mathematical Assumptions (4)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Existencia de solución interior en $u(t)$ y diferenciabilidad de $F$ y $f$ | Sin interioridad o suavidad no aplica la condición de primer orden $\partial_u\mathcal{H}=0$. | - |
| `A-C01-02` | - | Diferenciabilidad continua de $F$ y $f$ respecto a $(x,u)$ | Sin suavidad no aplican condiciones de primer orden. | - |
| `A-C01-03` | - | Control interior en el conjunto admisible | En frontera se requieren condiciones de holgura. | - |
| `A-C01-04` | - | Las funciones $F$ y $f$ son diferenciables en $x$ y el coestado $\lambda^*(t)$ es $C^1([t_0,t_1])$ | Sin diferenciabilidad en $x$ no existe el sistema canónico $H_x=-\dot{\lambda}$. | - |

---

### [C-02] Identidades Macroeconómicas de Acumulación (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 3: Identidades Macroeconómicas de Acumulación
- **Prerequisites:** C-01
- **Evidence Citations:** `Control Optimo Apuntes.pdf` (page 3)

#### Description & Cognitive Model
Relación entre producto, consumo, ahorro e inversión neta y bruta en modelos dinámicos mediante $I=\dot{K}=rK-C$, $S+C=Y$ e $I^{\text{BRUTO}}=\dot{K}+\delta K$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Confunde neta-bruta | conceptual_swap | high | $I^{\text{BRUTO}}=\dot{K}$ | Distinga inversión neta ($\dot{K}$) de inversión bruta: esta última incluye la reposición por depreciación $\delta K$. |
| `D-C02-02` | Signo depreciación | conceptual_swap | high | $I^{\text{BRUTO}}=\dot{K}-\delta K$ | Sume la depreciación $\delta K$ a la inversión neta $\dot{K}$ pues la inversión bruta cubre desgaste más acumulación. |
| `D-C02-03` | Omite consumo | conceptual_swap | high | $S=Y$ | Recuerde la identidad de cuentas nacionales $Y=C+S$: el ahorro es el ingreso residual tras descontar el consumo. |
| `D-C02-04` | Ahorro igual neta | conceptual_swap | high | $S=\dot{K}$ cuando $\delta>0$ | En economías con depreciación $\delta K$, el ahorro financia la inversión bruta ($S=I^{\text{BRUTO}}=\dot{K}+\delta K$). |
| `D-C02-05` | Confunde producto | conceptual_swap | high | $Y=rK-C$ | Identifique $Y=rK$ como el producto total de la economía; al restarle el consumo $C$ se obtiene la inversión $\dot{K}$. |
| `D-C02-06` | Tasa descuento | conceptual_swap | high | Confunde $\delta$ descuento con depreciación | Separe el rol de cada parámetro según el modelo: en el problema 1 $\delta$ descuenta utilidad y en el 4 deprecia capital. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | Economía cerrada sin gobierno ni sector externo ($Y=C+I^{\text{BRUTO}}$) | Si hay gasto público o balanza comercial, cambia la identidad ahorro-inversión. | - |

---

### [Hab-01] Resolución de Control Óptimo Lineal (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 4: Resolución de Control Óptimo Lineal
- **Prerequisites:** C-01
- **Evidence Citations:** `Control Optimo Apuntes.pdf` (page 4), `opt_din_3.pdf` (page 4)

#### Description & Cognitive Model
Integración del sistema coestado-estado en problemas con EDO lineal no homogénea $\dot{x}=ax+b(t)$ usando $x(t)=x_c(t)+x_p(t)$ y ajuste de constantes $(c_1,c_2)$ con condiciones de frontera

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Omite particular | skipped_step | high | $x(t)=c_2 e^{at}$ | Sume siempre la solución particular $x_p(t)$ obtenida por coeficientes indeterminados al término homogéneo $x_c(t)$. |
| `D-Hab01-07` | Omite particular | skipped_step | high | $x(t)=c_2 e^t$ | Al sustituir $u(t)$ en $\dot{x}=f$, resuelva tanto la solución complementaria como la particular antes de aplicar fronteras. |
| `D-Hab01-02` | Ansatz erróneo | skipped_step | high | $x_p(t)=A e^{t}$ para $b(t)=k e^{-t}$ | Elija la solución particular con el mismo exponente del término no homogéneo $b(t)$ para igualar coeficientes. |
| `D-Hab01-08` | Error exponente coestado | skipped_step | high | $\dot{\lambda}=-\lambda \Rightarrow \lambda=c_1 e^t$ | Integre $\dot{\lambda}=-a\lambda$ manteniendo el signo negativo en el exponente: $\lambda(t)=c_1 e^{-at}$. |
| `D-Hab01-03` | Signo al derivar xp | conceptual_swap | high | $\frac{d}{dt}(Ae^{-t})=Ae^{-t}$ | Aplique la regla de la cadena al derivar $Ae^{-t}$: el signo negativo baja y resulta $-Ae^{-t}$. |
| `D-Hab01-09` | Fija c2 igual a x(0) | conceptual_swap | high | $c_2=x(0)$ directamente | Evalúe la solución general completa $x(0)=x_c(0)+x_p(0)$ para despejar $c_2$ en función de $c_1$. |
| `D-Hab01-04` | Frontera prematura | conceptual_swap | high | Fija $c_1$ antes de hallar $x(t)$ | Determine ambas constantes $(c_1,c_2)$ al final imponiendo las condiciones dadas sobre el estado $x(0)$ y $x(T)$. |
| `D-Hab01-10` | Olvida sustituir u(t) | conceptual_swap | high | Integra $\dot{x}=x$ con $u=0$ | Reemplace el control óptimo $u^*(t)$ en función de $\lambda(t)$ dentro de la ecuación de estado antes de integrarla. |
| `D-Hab01-05` | Signo coestado en min | conceptual_swap | high | $\lambda(t)=c_1 e^t$ en $\dot{\lambda}=-\lambda$ | Integre $\dot{\lambda}=-\lambda$ conservando el signo negativo en el exponente para obtener $\lambda(t)=c_1 e^{-t}$. |
| `D-Hab01-11` | Invierte frontera final | conceptual_swap | high | $x(0)=x(T)$ en sistema | Aplique la condición inicial en $t=0$ y la condición terminal en $t=T$ para formar el sistema lineal en $c_1,c_2$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Condiciones de frontera fijas $x(0)=x_0$ y $x(T)=x_T$ conocidas | Sin dos condiciones de frontera no se determinan de forma única $c_1$ y $c_2$. | - |
| `A-Hab01-02` | - | Condiciones de frontera $x(0)=x_0$ y $x(T)=x_T$ conocidas | Sin ambos extremos el sistema queda indeterminado. | - |

---

### [Hab-02] Derivación por Ecuación de Euler (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 6: Derivación por Ecuación de Euler
- **Prerequisites:** C-01, C-02
- **Evidence Citations:** `Control Optimo Apuntes.pdf` (page 6)

#### Description & Cognitive Model
Eliminación del control $C=AK^{\alpha}-\dot{K}-\delta K$ en el integrando $F(K,\dot{K},t)$ y aplicación de $\frac{\partial F}{\partial K}-\frac{d}{dt}\left(\frac{\partial F}{\partial \dot{K}}\right)=0$ para deducir $\frac{\dot{C}}{C}=g(K)-\theta KC-\rho$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Olvida regla cadena | skipped_step | high | $\frac{\partial \ln C}{\partial K}=0$ | Recuerde que $C=AK^{\alpha}-\dot{K}-\delta K$ depende de $K$; derive $\ln C$ respecto a $K$ multiplicando por $g(K)$. |
| `D-Hab02-02` | Signo en dF/dKdot | skipped_step | high | $\frac{\partial F}{\partial \dot{K}}=+e^{-\rho t}\frac{1}{C}$ | Al derivar $C=AK^{\alpha}-\dot{K}-\delta K$ respecto a $\dot{K}$ surge un $-1$ que hace negativo a $\partial_{\dot{K}}F$. |
| `D-Hab02-03` | Omite producto en d/dt | conceptual_swap | high | $\frac{d}{dt}\left(-\frac{e^{-\rho t}}{C}\right)=e^{-\rho t}\frac{\dot{C}}{C^2}$ | Aplique la regla del producto/cociente en el tiempo $t$: tanto $e^{-\rho t}$ como $C(t)$ varían con $t$. |
| `D-Hab02-04` | Signo de theta K | conceptual_swap | high | $\frac{\dot{C}}{C}=g(K)+\theta KC-\rho$ | Conserve el signo negativo de la desutilidad $-\frac{\theta}{2}K^2$: el daño ambiental reduce el crecimiento del consumo. |
| `D-Hab02-05` | Omite multiplicar C | conceptual_swap | high | $\frac{\dot{C}}{C}=g(K)-\theta K-\rho$ | Al multiplicar toda la ecuación de Euler simplificada por $C$, el término $-\theta K$ pasa a ser $-\theta KC$. |
| `D-Hab02-06` | Confunde g(K) | conceptual_swap | high | $g(K)=A\alpha K^{\alpha-1}$ sin $-\delta$ | Incluya la depreciación en la productividad marginal neta del capital: $g(K)=A\alpha K^{\alpha-1}-\delta$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Posibilidad de despejar el control $C$ en función de $(K,\dot{K})$ | Si el control no es despejable de $\dot{K}$, se requiere el Principio del Máximo. | - |

---

### [Hab-03] Estado Estacionario, Isoclinas y Diagrama de Fases (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 7: Análisis de Estado Estacionario e Isoclinas
- **Prerequisites:** Hab-02
- **Evidence Citations:** `Control Optimo Apuntes.pdf` (page 7), `opt_din_3.pdf` (page 13)

#### Description & Cognitive Model
Obtención de isoclinas $\dot{C}=0$ y $\dot{K}=0$ en modelos de crecimiento óptimo (Ramsey-Cass-Koopmans), análisis cualitativo del diagrama de fases y condición de transversalidad.

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Ignora caso trivial | skipped_step | high | Divide por $C$ asumiendo $C\neq 0$ | Factorice $\dot{C}=C(g(K)-\theta KC-\rho)=0$ y evalúe por separado la rama trivial $C=0$ y la rama interior. |
| `D-Hab03-07` | Confunde con Regla de Oro | skipped_step | high | $c'=0 \Rightarrow f'(k)=\delta$ | La regla de Keynes-Ramsey modificada por impaciencia $\rho>0$ exige $f'(k^*)=\delta+\rho$ en el estado estacionario. |
| `D-Hab03-02` | Exponente invertido | skipped_step | high | $K=(\delta/A)^{\alpha-1}$ | Al despejar $K^{\alpha-1}=\delta/A$ desde $AK^{\alpha}=\delta K$, eleve ambos lados a la potencia recíproca $\frac{1}{\alpha-1}$. |
| `D-Hab03-08` | Isoclina k'=0 lineal | skipped_step | high | $\dot{k}=0 \Rightarrow c=f(k)$ | Al igualar $\dot{k}=f(k)-\delta k-c=0$, despeje el consumo estacionario como $c=f(k)-\delta k$ (curva acampanada). |
| `D-Hab03-03` | Omite theta K | conceptual_swap | high | $C=A\alpha K^{\alpha-1}-\delta-\rho$ | Despeje $C$ de $g(K)-\rho=\theta KC$ dividiendo el numerador completo entre $\theta K$ con $K\neq 0$. |
| `D-Hab03-09` | Invierte flechas de c | conceptual_swap | high | $k<k^* \Rightarrow c'<0$ | Como $f$ es cóncava, para $k<k^*$ se cumple $f'(k)>\delta+\rho$, lo que implica $c'>0$ (consumo creciente). |
| `D-Hab03-04` | Signo rho en isoclina | conceptual_swap | high | $C=\frac{g(K)+\rho}{\theta K}$ | Pase $\theta KC$ o $\rho$ respetando los signos de $\frac{\dot{C}}{C}=g(K)-\theta KC-\rho=0$, donde $\rho$ resta a $g(K)$. |
| `D-Hab03-10` | Invierte flechas de k | conceptual_swap | high | Por encima de $\dot{k}=0$ sube $k$ | Si $c>f(k)-\delta k$ (por encima de la isoclina $\dot{k}=0$), el consumo excede la producción neta y $\dot{k}<0$. |
| `D-Hab03-05` | Confunde isoclina K | conceptual_swap | high | $\dot{K}=0 \Rightarrow C=AK^{\alpha}+\delta K$ | Despeje $C$ desde $AK^{\alpha}-C-\delta K=0$: el consumo estacionario es el producto menos la depreciación $\delta K$. |
| `D-Hab03-11` | Omite $e^{-rho t}$ en límite | conceptual_swap | high | $\lim_{t\to\infty} m(t)k(t)=0$ sin descuento | En tiempo corriente la transversalidad en horizonte infinito es $\lim_{t\to\infty} m(t)k(t)e^{-\rho t}=0$ (con $m=\lambda$). |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | Parámetros positivos $A>0$, $\delta>0$, $\theta>0$, $\rho>0$ y $\alpha\in(0,1)$ | Si $\theta=0$ o $\alpha\ge 1$, cambia la existencia o unicidad del equilibrio interior. | - |
| `A-Hab03-02` | - | Condiciones de Inada sobre $f(k)$ para existencia de $k^*>0$ | Sin ellas puede no existir corte interior. | - |

---

### [C-04] Condición Suficiente de Mangasarian (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Condición Suficiente de Mangasarian
- **Prerequisites:** C-01
- **Evidence Citations:** `opt_din_3.pdf` (page 4), `Teoria_de_control_optimo___teoria (1).pdf` (page 5)

#### Description & Cognitive Model
Evaluación de la matriz hessiana $H_F$ respecto a $(x,u)$ para verificar semidefinición negativa en máximos globales o positiva en mínimos globales

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Criterio invertido | conceptual_swap | high | $H_F$ semidefinida positiva implica máximo | Una matriz $H_F$ semidefinida positiva indica convexidad (mínimo global); para máximos globales exija concavidad ($H_F \le 0$). |
| `D-C04-07` | Invierte concavidad | conceptual_swap | high | $H_H^e\text{ convexa }\Rightarrow\text{ máximo}$ | Para garantizar un máximo, $H_H^e$ debe ser cóncava (definida negativa); si es convexa (definida positiva) garantiza un mínimo. |
| `D-C04-02` | Solo segunda derivada u | conceptual_swap | high | $\frac{\partial^2 H}{\partial u^2}<0$ basta | Verifique la concavidad o convexidad conjunta en $(x,u)$ evaluando todos los menores principales de la hessiana $H_F$. |
| `D-C04-08` | Hessiana solo en u | conceptual_swap | high | $H_{uu}\le 0\text{ basta}$ | La condición de Mangasarian exige evaluar la matriz hessiana conjunta $H_H^e$ respecto a estado $x$ y control $u$. |
| `D-C04-03` | Confunde signo det | conceptual_swap | high | $|H_F|<0$ para concavidad | En una matriz $2\times 2$ semidefinida negativa se cumple $H_{xx}\le 0$, $H_{uu}\le 0$ y determinante $H_{xx}H_{uu}-H_{xu}^2\ge 0$. |
| `D-C04-09` | Signo en Euler | conceptual_swap | high | $F_x+\frac{dF_{\dot{x}}}{dt}=0$ | De $H_u=F_u+\lambda=0$ y $H_x=-\dot{\lambda}$ se obtiene $\lambda=-F_u \Rightarrow -\dot{\lambda}=\frac{dF_u}{dt}$, dando resta $F_x-\frac{dF_{\dot{x}}}{dt}=0$. |
| `D-C04-04` | Exige definida estricta | conceptual_swap | high | Si $|H_F|=0$ no hay óptimo | El teorema de Mangasarian solo requiere semidefinición (concavidad o convexidad débil), por lo que $|H_F|=0$ es válido. |
| `D-C04-10` | Omite derivada total | conceptual_swap | high | $F_x-F_{\dot{x}}=0$ | Al sustituir $\lambda=-F_u$ en $F_x=-\dot{\lambda}$, debe aplicar la derivada temporal $\frac{d}{dt}F_u$ antes de volver a $\dot{x}=u$. |
| `D-C04-05` | Evalúa en x solamente | conceptual_swap | high | $H_{xx}\le 0$ basta para máximo | Construya la matriz completa $2\times 2$ con segundas derivadas respecto a $x$ y $u$ para validar la condición suficiente. |
| `D-C04-11` | Sustitución errónea u=x | conceptual_swap | high | $f(x,u,t)=x$ | Para traducir $\int F(x,\dot{x},t)\,dt$ a control óptimo se define $u=\dot{x}$, de modo que la ecuación de estado es $\dot{x}=u$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | Existencia de segundas derivadas parciales de $H$ en $(x,u)$ | Sin clase $C^2$ no se construye la hessiana $H_F$. | - |
| `A-C04-02` | - | La función $F(x,\dot{x},t)$ es no lineal en $\dot{x}$ y dos veces diferenciable | Si $F$ es lineal en $\dot{x}$, $H_u=0$ no determina $u$ y falla la reducción clásica a Euler. | - |

---

### [C-05] Condiciones de Transversalidad (Estado y Tiempo Libre) (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 8: Condiciones de Transversalidad (Estado y Tiempo Libre)
- **Prerequisites:** C-01
- **Evidence Citations:** `opt_din_3.pdf` (page 8)

#### Description & Cognitive Model
Condiciones de frontera óptimas para estado final libre $\lambda(T)=\partial S/\partial x|_T=0$ o instante final libre $H(t_1)+\partial S/\partial t|_{t_1}=0$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Estado final nulo | conceptual_swap | high | $x(T)=0$ si $x(T)$ es libre | Cuando el estado final es libre no se fija $x(T)=0$, sino que se anula el valor marginal del coestado: $\lambda(T)=0$. |
| `D-C05-02` | Tiempo libre sin H | conceptual_swap | high | $\lambda(t_1)=0$ con $t_1$ libre y $x(t_1)$ fijo | Si $x(t_1)$ es fijo y $t_1$ es libre, la transversalidad exige anular el Hamiltoniano evaluado en el óptimo: $H(t_1)=0$. |
| `D-C05-03` | Signo en transversalidad | conceptual_swap | high | $H(t_1)-\frac{\partial S}{\partial t}=0$ | La condición correcta para horizonte libre con función de rescate $S$ es la suma $H(x^*,u^*,\lambda^*,t_1)+\partial S/\partial t|_{t_1}=0$. |
| `D-C05-04` | Anula control final | conceptual_swap | high | $u(T)=0$ como transversalidad | La transversalidad actúa sobre el coestado $\lambda(T)$ o sobre el Hamiltoniano $H(t_1)$, nunca imponiendo $u(T)=0$ arbitrariamente. |
| `D-C05-05` | Omite derivada S | conceptual_swap | high | $\lambda(T)=S(x(T))$ | Iguale $\lambda(T)$ a la derivada parcial $\partial S/\partial x$ evaluada en $t=T$ (que es cero si no hay valor residual $S$). |
| `D-C05-06` | Tiempo final negativo | conceptual_swap | high | Acepta $t_1<0$ de $t_1^2=c_1^2/4$ | Como el horizonte temporal parte en $t=0$, seleccione siempre la raíz positiva $t_1>0$ al resolver la ecuación de transversalidad. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Ausencia de restricción terminal sobre $x(T)$ o sobre $t_1$ | Si ambos están fijos no aplica transversalidad. | - |

---

### [Hab-05] Cálculo de Trayectorias con Frontera Libre (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 10: Cálculo de Trayectorias con Frontera Libre
- **Prerequisites:** C-05, C-01
- **Evidence Citations:** `opt_din_3.pdf` (page 10), `Teoria_de_control_optimo___teoria (1).pdf` (page 5)

#### Description & Cognitive Model
Aplicación de condiciones de transversalidad en $T$ o $t_1$ para determinar $c_1$, $t_1^*$ y las trayectorias óptimas $x^*(t),u^*(t),\lambda^*(t)$

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Usa H(0)=0 | skipped_step | high | Evalúa $H(0)=0$ para hallar $t_1$ | La condición de transversalidad de tiempo libre debe evaluarse en el instante final $t=t_1$, sustituyendo $x^*,u^*,\lambda^*$. |
| `D-Hab05-07` | Iguala coestado a cero con rescate | skipped_step | high | $\lambda(t_1)=0\text{ con }S\neq 0$ | Cuando hay función de valor terminal $S[x(t_1)]$, el coestado final iguala la derivada $\left.\frac{dS}{dx}\right|_{t=t_1}$, no necesariamente cero. |
| `D-Hab05-02` | No sustituye u* en H | skipped_step | high | Deja $u$ sin reemplazar en $H(t_1)$ | Exprese $u^*(t_1)$ en función de $c_1$ antes de igualar $H(t_1)=0$ para obtener una ecuación algebraica en $(c_1,t_1)$. |
| `D-Hab05-08` | Signo menos en instante libre | conceptual_swap | high | $H(t_1)-\frac{dS}{dt_1}=0$ | La condición para instante final libre suma ambos términos: $H(x^*(t_1),u^*(t_1),\lambda^*(t_1),t_1^*)+\left.\frac{dS}{dt_1}\right|_{t=t_1}=0$. |
| `D-Hab05-03` | Fija c1=0 directo | conceptual_swap | high | $c_1=0$ cuando $\lambda(1)=-1+c_1=0$ | Evalúe $\lambda(T)$ con la expresión obtenida de la EDO (por ejemplo $-1+c_1=0 \Rightarrow c_1=1$) antes de sustituir en $c_2$. |
| `D-Hab05-09` | Confunde derivada espacial y temporal | skipped_step | high | $H(t_1)+\frac{dS}{dx}=0$ | Para estado final libre se deriva $S$ respecto a $x$ ($\frac{dS}{dx}=\lambda(t_1)$), mientras para instante final libre se deriva respecto a $t_1$. |
| `D-Hab05-04` | Error signo en c1*t1 | conceptual_swap | high | $5=-\frac{c_1}{2}t_1+4 \Rightarrow c_1 t_1=-2$ | Al pasar $4$ restando queda $1=-\frac{c_1}{2}t_1$, por lo que $c_1 t_1=-2$; verifique siempre el signo al multiplicar por $-2$. |
| `D-Hab05-10` | Evalúa en t0 | conceptual_swap | high | $\lambda(t_0)=\left.\frac{dS}{dx}\right|_{t=t_0}$ | Las condiciones de transversalidad reemplazan la condición de frontera faltante en el extremo terminal $t_1$, nunca en $t_0$. |
| `D-Hab05-05` | Olvida actualizar c2 | conceptual_swap | high | Deja $c_2$ sin usar $c_1^*$ | Una vez determinado $c_1^*$ por transversalidad, sustitúyalo en la relación de $x(0)$ para hallar el valor numérico de $c_2$. |
| `D-Hab05-11` | Anula H sin tiempo libre | conceptual_swap | high | $H(t_1)=0\text{ con }t_1\text{ fijo}$ | La anulación $H(t_1)+\frac{dS}{dt_1}=0$ solo aplica si el instante final $t_1$ es libre; si $t_1$ es fijo y $x(t_1)$ libre, use $\lambda(t_1)=S_x$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | Solución general previa de $\lambda(t)$ y $x(t)$ en términos de $c_1,c_2$ | Sin integración previa no se evalúa la frontera. | - |
| `A-Hab05-02` | - | La función terminal $S[x(t_1),t_1]$ es diferenciable en $x$ y en $t_1$ en el óptimo | Sin diferenciabilidad de $S$ no pueden formularse las derivadas de transversalidad en $t_1$. | - |

---

### [C-06] Hamiltoniano en Tiempo Corriente (Modelo RCK) (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 12: Hamiltoniano en Tiempo Corriente (Modelo RCK)
- **Prerequisites:** C-01
- **Evidence Citations:** `opt_din_3.pdf` (page 12)

#### Description & Cognitive Model
Formulación del Hamiltoniano $\mathcal{H}=u(c)+m(f(k)-\delta k-c)$ con coestado $m=\lambda e^{\rho t}$ y deducción de la regla de Keynes-Ramsey $c'=-(u'/u'')(f'-\delta-\rho)$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Omite descuento rho | conceptual_swap | high | $\frac{\partial \mathcal{H}}{\partial k}=-\dot{m}$ | En tiempo corriente la ecuación de coestado incorpora la tasa de descuento $\rho$: $\partial \mathcal{H}/\partial k = -\dot{m}+\rho m$. |
| `D-C06-02` | Signo errado en rho | conceptual_swap | high | $\dot{m}=-m(f'-\delta+\rho)$ | Al despejar $\dot{m}$ de $m(f'-\delta)=-\dot{m}+\rho m$, ambos $\delta$ y $\rho$ restan a $f'$: $\dot{m}=-m(f'-\delta-\rho)$. |
| `D-C06-03` | Incluye $e^{-rho t}$ en H | conceptual_swap | high | $\mathcal{H}=u(c)e^{-\rho t}+m\dot{k}$ | El Hamiltoniano en tiempo corriente factoriza el descuento $e^{-\rho t}$, dejando la utilidad sin descuento explícito. |
| `D-C06-04` | No deriva u'(c)=m | conceptual_swap | high | $u'(c)=0 \Rightarrow c'=0$ | Derive respecto al tiempo la condición $u'(c)=m$ usando regla de la cadena ($u''c'=m'$) para sustituir $m'$ y $m$. |
| `D-C06-05` | Signo en Keynes-Ramsey | conceptual_swap | high | $c'=\frac{u'}{u''}(f'-\delta-\rho)$ | Como $m'=-u'(f'-\delta-\rho)$ y $u''<0$, la ecuación resulta $c'=-(u'/u'')(f'-\delta-\rho)$ para que $f'>\delta+\rho \Rightarrow c'>0$. |
| `D-C06-06` | Omite depreciación delta | conceptual_swap | high | $\dot{k}=f(k)-c$ | La producción $f(k)$ se destina a consumo $c$ e inversión bruta $\dot{k}+\delta k$, por lo que $\dot{k}=f(k)-\delta k-c$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Utilidad instantánea con $u'>0, u''<0$ y producción $f''<0$ | Sin concavidad estricta falla la unicidad interior. | - |

---

### [Hab-07] Optimización Dinámica en Modelo de Contaminación (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 16: Optimización Dinámica en Modelo de Contaminación
- **Prerequisites:** C-01, C-05
- **Evidence Citations:** `opt_din_3.pdf` (page 16)

#### Description & Cognitive Model
Resolución del modelo ambiental con $P'=C^2-\gamma P$, cálculo de $\dot{\lambda}=\theta e^{-\rho t}+\gamma\lambda$, transversalidad $\lambda(T)=0$ y consumo óptimo $C^*(t)$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Signo errado en lambda punto | skipped_step | high | $\dot{\lambda}=-\theta e^{-\rho t}-\gamma\lambda$ | Como $\partial H/\partial P=-\theta e^{-\rho t}-\gamma\lambda=-\dot{\lambda}$, al multiplicar por $-1$ se obtiene $\dot{\lambda}=\theta e^{-\rho t}+\gamma\lambda$. |
| `D-Hab07-02` | Omite factor $e^{rho t}$ en C* | skipped_step | high | $C=[\frac{2\beta}{\alpha^2}-2\lambda]^{-1/2}$ | Al dividir toda la condición $\partial H/\partial C=0$ por $e^{-\rho t}$, el término $2\lambda C$ queda multiplicado por $e^{\rho t}$. |
| `D-Hab07-03` | Signo + en exponente C* | conceptual_swap | high | $C=[\frac{2\beta}{\alpha^2}-2\lambda e^{\rho t}]^{1/2}$ | Al factorizar $1/C=C(\frac{2\beta}{\alpha^2}-2\lambda e^{\rho t})$ se obtiene $C^2=[\dots]^{-1}$, por lo que $C=[\dots]^{-1/2}$. |
| `D-Hab07-04` | Fija lambda(0)=0 | conceptual_swap | high | $\lambda(0)=c_1-\frac{\theta}{\rho+\gamma}=0$ | Como el estado final $P(T)=P_T$ es libre y $P(0)=1$ es fijo, la condición de transversalidad se aplica en $T$: $\lambda(T)=0$. |
| `D-Hab07-05` | Error integrar EDO lambda | conceptual_swap | high | $\lambda(t)=c_1 e^{-\gamma t}-\frac{\theta}{\rho+\gamma}e^{-\rho t}$ | La ecuación $\dot{\lambda}-\gamma\lambda=\theta e^{-\rho t}$ tiene solución homogénea $c_1 e^{\gamma t}$ con exponente positivo $+\gamma t$. |
| `D-Hab07-06` | Ignora sustitución L=C/alpha | conceptual_swap | high | Mantiene $L^2$ sin sustituir en $H$ | Use la ecuación de consumo $C=\alpha L \Rightarrow L^2=C^2/\alpha^2$ para expresar la utilidad únicamente en función de $C$ y $P$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Parámetros positivos $\alpha,\beta,\gamma,\theta,\rho>0$ y $P(T)$ libre | Garantizan $\lambda^*(t)\le 0$ y consumo real positivo. | - |

---

### [C-07] Forma Funcional y Trayectorias (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 5: Forma Funcional y Trayectorias
- **Prerequisites:** None
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 5)

#### Description & Cognitive Model
Mapeo funcional $V[y]=\int_0^T F[t,y(t),y'(t)]dt$ que asigna un valor real a cada trayectoria admisible $y(t)$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Confunde con función | conceptual_swap | high | $V(t)=F(t,y,y')$ | Recuerde que un funcional toma una trayectoria completa $y(t)$ y la mapea a un escalar mediante la integral. |
| `D-C07-02` | Omite pendiente | conceptual_swap | high | $V[y]=\int_0^T F[t,y(t)]dt$ | Incluya $y'(t)=\frac{dy}{dt}$ en $F$, pues el valor de cada arco depende de su dirección inicial. |
| `D-C07-03` | Omite estado y(t) | conceptual_swap | high | $V[y]=\int_0^T F[t,y'(t)]dt$ | Mantenga el estado $y(t)$ dentro de $F$, ya que el arco parte del nivel de estado en cada etapa $t$. |
| `D-C07-04` | Suma discreta | conceptual_swap | high | $V[y]=\sum_{t=0}^T y(t)$ | Use la integral definida de $F[t,y(t),y'(t)]$ en tiempo continuo en lugar de sumar estados discretos. |
| `D-C07-05` | Invierte dominio | conceptual_swap | high | $V:\mathbb{R}\Rightarrow\mathcal{C}^1$ | Invierta el mapeo: el funcional parte del conjunto de trayectorias admisibles hacia la recta real. |
| `D-C07-06` | Límite indefinido | conceptual_swap | high | $V[y]=\int F[t,y,y']dt$ | Fije los límites $[0,T]$ en la integral para obtener un valor escalar único asociado a la trayectoria. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Trayectorias admisibles $y\in\mathcal{C}^1([0,T])$ | Sin diferenciabilidad continua no existe $y'(t)$ en cada arco. | - |

---

### [H-01] Puntos Finales y Transversalidad (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 6: Puntos Finales y Transversalidad
- **Prerequisites:** C-07
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 6)

#### Description & Cognitive Model
Distinción de frontera terminal: estado final libre con $t=T$ fijo frente a instante final libre con $y=Z$ fijo

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Invierte casos libres | conceptual_swap | high | $y(T)=Z$ es estado final libre | Distinga ambos casos: en estado final libre el tiempo $T$ está fijo y varía $y(T)$; en instante final libre varía $T$. |
| `D-H01-02` | Ambos extremos fijos | conceptual_swap | high | $t=T\text{ fijo y }y(T)=Z\text{ fijo}$ | Reconozca que en problemas con transversalidad al menos una coordenada final ($y(T)$ o $T$) queda libre. |
| `D-H01-03` | Confunde origen libre | conceptual_swap | high | $y(0)=A$ libre | Mantenga fijo el punto inicial $A$ y aplique la libertad terminal solo en el horizonte final. |
| `D-H01-04` | Exige y constante | conceptual_swap | high | $y(t)=Z,\;\forall t\in[0,T]$ | Aplique la condición $y=Z$ únicamente en el instante terminal $T$ cuando el horizonte es libre. |
| `D-H01-05` | Igualdad de pendientes | conceptual_swap | high | $y'(T)=0$ siempre | No fuerce $y'(T)=0$ como definición de frontera libre; la condición depende de la transversalidad. |
| `D-H01-06` | Tiempo negativo | conceptual_swap | high | $T<0$ en horizonte libre | Restrinja los instantes finales admisibles $T_1,T_2,T_3$ a valores positivos posteriores al inicio. |

---

### [C-08] Funcionales Lagrange Mayer Bolza (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 8: Funcionales Lagrange Mayer Bolza
- **Prerequisites:** C-07
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 8)

#### Description & Cognitive Model
Clasificación de objetivos dinámicos: Lagrange $\int_0^T Fdt$, Mayer $G(T,y(T))$ y Bolza $\int_0^T Fdt+G(T,y(T))$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Confunde Mayer-Lagrange | conceptual_swap | high | Mayer: $V[y]=\int_0^T Fdt$ | Asocie Lagrange a la integral $\int_0^T Fdt$ y Mayer exclusivamente a la función terminal $G(T,y(T))$. |
| `D-C08-02` | Omite G en Bolza | conceptual_swap | high | Bolza: $V[y]=\int_0^T Fdt$ | Sume la función terminal $G(T,y(T))$ a la integral de flujo para formar el problema de Bolza. |
| `D-C08-03` | Resta término terminal | conceptual_swap | high | Bolza: $\int_0^T Fdt-G(T,y(T))$ | Escriba Bolza como suma $\int_0^T Fdt+G(T,y(T))$; cualquier penalización se incorpora dentro de $G$. |
| `D-C08-04` | Mayer en t=0 | conceptual_swap | high | Mayer: $V[y]=G(0,y(0))$ | Evalúe $G$ en el horizonte final $(T,y(T))$, pues Mayer optimiza el estado terminal. |
| `D-C08-05` | Multiplica integral por G | conceptual_swap | high | Bolza: $G(T,y(T))\int_0^T Fdt$ | Combine ambos componentes del funcional de Bolza mediante adición y nunca mediante producto. |
| `D-C08-06` | Incluye y' en Mayer | conceptual_swap | high | Mayer: $V[y]=G(T,y(T),y'(T))$ | Defina el funcional de Mayer únicamente en términos del tiempo final $T$ y el estado final $y(T)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C08-01` | - | Función terminal $G(T,y(T))$ diferenciable | Permite expresar objetivos mixtos de flujo y stock final. | - |

---

### [C-09] Ecuación de Euler (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 9: Ecuación de Euler
- **Prerequisites:** C-08
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 9)

#### Description & Cognitive Model
Condición necesaria de primer orden $F_x-\frac{d}{dt}F_{\dot{x}}=0$ y su expansión $F_x-F_{\dot{x}x}\dot{x}-F_{\dot{x}\dot{x}}\ddot{x}-F_{\dot{x}t}=0$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Invierte signo Euler | conceptual_swap | high | $F_x+\frac{d}{dt}F_{\dot{x}}=0$ | Aplique el signo negativo en $F_x-\frac{d}{dt}F_{\dot{x}}=0$, proveniente de la integración por partes. |
| `D-C09-02` | Omite derivada total | conceptual_swap | high | $F_x-F_{\dot{x}}=0$ | Derive totalmente respecto al tiempo $t$ el término $F_{\dot{x}}[x(t),\dot{x}(t),t]$ antes de restarlo de $F_x$. |
| `D-C09-03` | Derivada parcial simple | conceptual_swap | high | $F_x-F_{\dot{x}t}=0$ | Aplique la regla de la cadena completa: $\frac{d}{dt}F_{\dot{x}}=F_{\dot{x}x}\dot{x}+F_{\dot{x}\dot{x}}\ddot{x}+F_{\dot{x}t}$. |
| `D-C09-04` | Intercambia x y $x_punto$ | conceptual_swap | high | $F_{\dot{x}}-\frac{d}{dt}F_x=0$ | Coloque la derivada parcial respecto al estado $F_x$ primero y derive respecto a $t$ la parcial $F_{\dot{x}}$. |
| `D-C09-05` | Signo positivo en cadena | conceptual_swap | high | $F_x+F_{\dot{x}x}\dot{x}+F_{\dot{x}\dot{x}}\ddot{x}+F_{\dot{x}t}=0$ | Distribuya el signo menos de $-\frac{d}{dt}F_{\dot{x}}$ a los tres términos de la regla de la cadena. |
| `D-C09-06` | Omite término $F_xt$ | conceptual_swap | high | $F_x-F_{\dot{x}x}\dot{x}-F_{\dot{x}\dot{x}}\ddot{x}=0$ | Incluya $-F_{\dot{x}t}$ en la forma desarrollada cuando $F$ dependa explícitamente de $t$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | $F\in\mathcal{C}^2$ y extremos fijos $x(t_0)=x_0,x(t_1)=x_1$ | Garantiza la existencia de $F_{\dot{x}x},F_{\dot{x}\dot{x}},F_{\dot{x}t}$ y variación nula en bordes. | - |

---

### [C-10] Condición de Legendre (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 10: Condición de Legendre
- **Prerequisites:** C-09
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 10)

#### Description & Cognitive Model
Condición necesaria de segundo orden $F_{\dot{x}\dot{x}}\le 0$ para máximo local y $F_{\dot{x}\dot{x}}\ge 0$ para mínimo local en $[t_0,t_1]$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C10-01` | Invierte desigualdad máx | conceptual_swap | high | $F_{\dot{x}\dot{x}}\ge 0$ para máximo | Recuerde que concavidad local en $\dot{x}$ para máximo requiere $F_{\dot{x}\dot{x}}\le 0$, y para mínimo $F_{\dot{x}\dot{x}}\ge 0$. |
| `D-C10-02` | Deriva respecto a x | conceptual_swap | high | $F_{xx}\le 0$ es Legendre | Calcule la segunda derivada parcial respecto a la velocidad $\dot{x}$ dos veces ($F_{\dot{x}\dot{x}}$), no respecto a $x$. |
| `D-C10-03` | Usa derivada mixta | conceptual_swap | high | $F_{x\dot{x}}\le 0$ es Legendre | Aplique únicamente $F_{\dot{x}\dot{x}}$ en la condición de Legendre; $F_{x\dot{x}}$ aparece en el Hessiano completo. |
| `D-C10-04` | Desigualdad estricta obligatoria | conceptual_swap | high | $F_{\dot{x}\dot{x}}<0$ siempre necesaria | Use desigualdad débil ($\le 0$ o $\ge 0$) en la condición necesaria de Legendre para todo $t\in[t_0,t_1]$. |
| `D-C10-05` | Evalúa solo en $t_0$ | conceptual_swap | high | $F_{\dot{x}\dot{x}}(t_0)\le 0$ basta | Verifique la condición de Legendre para todo $t\in[t_0,t_1]$ a lo largo de la trayectoria $x^*(t)$. |
| `D-C10-06` | Confunde suficiencia global | conceptual_swap | high | $F_{\dot{x}\dot{x}}\le 0\Rightarrow$ máximo global | Considere Legendre como condición necesaria de segundo orden; la suficiencia global exige concavidad conjunta. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C10-01` | - | Existencia de $F_{\dot{x}\dot{x}}$ continua en $[t_0,t_1]$ | Permite evaluar el signo de la segunda variación. | - |

---

### [C-11] Suficiencia y Criterio Hessiano (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 11: Suficiencia y Criterio Hessiano
- **Prerequisites:** C-09
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 11)

#### Description & Cognitive Model
Condición suficiente de óptimo global: concavidad (máximo) o convexidad (mínimo) de $F(x,\dot{x},t)$ vía menores principales de $H_F$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C11-01` | Invierte signo det($H_F$) | conceptual_swap | high | $F_{xx}<0$ y $\det(H_F)<0$ cóncava | Corrija el criterio de Sylvester: en $2\times 2$, definida negativa exige $F_{xx}<0$ y $\det(H_F)>0$. |
| `D-C11-02` | Solo diagonal negativa | conceptual_swap | high | $F_{xx}\le 0$ y $F_{\dot{x}\dot{x}}\le 0$ basta | Calcule el determinante completo $F_{xx}F_{\dot{x}\dot{x}}-(F_{x\dot{x}})^2\ge 0$ para garantizar semidefinición. |
| `D-C11-03` | Confunde cóncava-mínimo | conceptual_swap | high | $F$ cóncava $\Rightarrow$ mínimo global | Asocie concavidad (Hessiano semidefinido negativo) con máximo global y convexidad (semidefinido positivo) con mínimo global. |
| `D-C11-04` | Exige estricta para global | conceptual_swap | high | Semidefinida no da óptimo global | Aplique el teorema 1.3: basta concavidad o convexidad débil (semidefinida) para garantizar óptimo global. |
| `D-C11-05` | Omite condición de Euler | conceptual_swap | high | $H_F$ semidefinida $\Rightarrow x^*$ óptimo | Verifique primero que $x^*(t)$ cumpla Euler y condiciones de frontera antes de aplicar suficiencia por $H_F$. |
| `D-C11-06` | Asume $H_F$ asimétrica | conceptual_swap | high | $F_{x\dot{x}}\neq F_{\dot{x}x}$ en $\mathcal{C}^2$ | Aproveche la simetría de Schwarz ($F_{x\dot{x}}=F_{\dot{x}x}$) al armar el Hessiano $H_F$ de clase $\mathcal{C}^2$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C11-01` | - | $F$ de clase $\mathcal{C}^2$ en $(x,\dot{x})$ para cada $t\in[t_0,t_1]$ | Permite caracterizar concavidad y convexidad mediante $H_F$. | - |

---

### [Hab-08] Resolución de Euler con EDO (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 14: Resolución de Euler con EDO
- **Prerequisites:** C-09, C-10, C-11
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 14), `optimizacion_dinamica.pdf` (page 16)

#### Description & Cognitive Model
Aplicación de Euler para obtener la EDO de segundo orden, hallar raíces características y ajustar constantes de frontera

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | Error signo en EDO | skipped_step | high | $\ddot{x}+x=0$ | Reste correctamente $\frac{d}{dt}(2\dot{x})$ de $2x$: $2x-2\ddot{x}=0\Rightarrow \ddot{x}-x=0$. |
| `D-Hab08-07` | Integra una sola vez | skipped_step | high | $x(t)=\frac{b}{2a}t+c_1$ | Integre $\ddot{x}=\frac{b}{2a}$ dos veces para obtener el término cuadrático $\frac{b}{4a}t^2+c_1t+c_2$. |
| `D-Hab08-02` | Raíz característica doble | skipped_step | high | $m^2-1=0\Rightarrow m_1=m_2=1$ | Factorice $m^2-1=(m-1)(m+1)=0$ para obtener ambas raíces reales $m_1=-1$ y $m_2=1$. |
| `D-Hab08-08` | Error factor en integración | skipped_step | high | $x(t)=\frac{b}{2a}t^2+c_1t+c_2$ | Divida $\frac{b}{2a}$ entre $2$ al integrar $\frac{b}{2a}t$, obteniendo $\frac{b}{4a}t^2$. |
| `D-Hab08-03` | Omite constantes frontera | conceptual_swap | high | $x(t)=e^{-t}+e^t$ | Sustituya $x(0)=1$ y $x(1)=e$ en $c_1e^{-t}+c_2e^t$ para hallar $c_1=0$ y $c_2=1$. |
| `D-Hab08-09` | Confunde signo de a | conceptual_swap | high | $F_{\dot{x}\dot{x}}=2a>0$ con $a<0$ | Evalúe $2a<0$ usando la hipótesis $a<0$ para verificar la condición de Legendre de máximo. |
| `D-Hab08-04` | Solución trigonométrica | conceptual_swap | high | $x(t)=c_1\cos t+c_2\sin t$ | Use exponenciales reales $c_1e^{-t}+c_2e^t$ cuando las raíces características sean reales distintas. |
| `D-Hab08-10` | Diagonal errónea en $H_F$ | conceptual_swap | high | $F_{\dot{x}\dot{x}}=a$ en el Hessiano | Calcule $\frac{\partial^2 F}{\partial \dot{x}^2}=2a$ de manera consistente tanto en Legendre como en $H_F$. |
| `D-Hab08-05` | Olvida factor 2 en $F_xdot$ | conceptual_swap | high | $2x-\ddot{x}=0$ | Aplique la regla de la potencia en $F_{\dot{x}}=2\dot{x}$ antes de derivar respecto a $t$. |
| `D-Hab08-11` | Clasifica como convexa | conceptual_swap | high | $F_{xx}=0,\det(H_F)=0\Rightarrow$ convexa | Verifique todos los menores principales con $2a<0$: $H_F$ es semidefinida negativa, por lo que $F$ es cóncava. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab08-01` | - | Condiciones de frontera bien definidas $x(t_0)=x_0,x(t_1)=x_1$ | Determinan de forma única las constantes $c_1,c_2$ de la EDO. | - |
| `A-Hab08-02` | - | Parámetro $a<0$ y condiciones $x(0)=2,x(4)=4$ | Asegura concavidad del integrando y unicidad de la trayectoria. | - |

---

### [C-12] Casos Particulares sin x o dx/dt (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 18: Casos Particulares sin x o dx/dt
- **Prerequisites:** C-09
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 18)

#### Description & Cognitive Model
Simplificación de la ecuación de Euler cuando $F$ omite $x$ ($\frac{\partial F}{\partial \dot{x}}=c$) o $\dot{x}$ ($\frac{\partial F}{\partial x}=0$)

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C12-01` | Confunde derivada total | conceptual_swap | high | $\frac{\partial F}{\partial x}=0 \Rightarrow \frac{\partial F}{\partial \dot{x}}=0$ | Al integrar $\frac{\partial}{\partial t}(\frac{\partial F}{\partial \dot{x}})=0$ respecto a $t$ surge una constante $c$, no cero. |
| `D-C12-02` | Asume x constante | conceptual_swap | high | $F_x=0 \Rightarrow x(t)=c$ | La condición $F_x=0$ implica que $F_{\dot{x}}$ es constante, lo que aún requiere integrar respecto a $t$. |
| `D-C12-03` | Mantiene término nulo | conceptual_swap | high | $F_{\dot{x}}=0 \Rightarrow \frac{\partial F}{\partial x}-\ddot{x}=0$ | Si $F$ no depende de $\dot{x}$, entonces $F_{\dot{x}}=0$ y su derivada temporal también es nula, quedando $F_x=0$. |
| `D-C12-04` | Invierte casos | conceptual_swap | high | $F_{\dot{x}}=0 \Rightarrow \frac{\partial F}{\partial \dot{x}}=c$ | Cuando falta $\dot{x}$ la ecuación de Euler es puramente algebraica ($F_x=0$); la constante aparece cuando falta $x$. |
| `D-C12-05` | Omite condición de borde | conceptual_swap | high | $F_x=0$ siempre admite solución única | Una ecuación algebraica $F_x=0$ fija $x(t)$ sin constantes libres, pudiendo ser incompatible con los bordes. |
| `D-C12-06` | Deriva respecto a x | conceptual_swap | high | $\frac{\partial}{\partial x}\left[\frac{\partial F}{\partial \dot{x}}\right]=0$ | En la ecuación de Euler el operador exterior siempre deriva respecto al tiempo $t$, nunca respecto a $x$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C12-01` | - | Integrando $F \in C^2$ en sus argumentos | Sin diferenciabilidad de segundo orden no puede aplicarse Euler. | - |

---

### [C-13] Identidad de Beltrami (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 19: Identidad de Beltrami
- **Prerequisites:** C-12
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 19)

#### Description & Cognitive Model
Primera integral de Euler $F - \dot{x}\frac{\partial F}{\partial \dot{x}} = C$ válida cuando el integrando $F(x,\dot{x})$ es autónomo

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C13-01` | Signo positivo erróneo | conceptual_swap | high | $F + \dot{x}\frac{\partial F}{\partial \dot{x}} = C$ | Al agrupar $\frac{\partial}{\partial t}(F - \dot{x}F_{\dot{x}})=0$, el segundo término lleva signo negativo por regla del producto. |
| `D-C13-02` | Omite factor velocidad | conceptual_swap | high | $F - \frac{\partial F}{\partial \dot{x}} = C$ | Multiplique siempre $\frac{\partial F}{\partial \dot{x}}$ por $\dot{x}$ para compensar el término $\frac{\partial F}{\partial \dot{x}}\ddot{x}$ en $\frac{dF}{dt}$. |
| `D-C13-03` | Aplica con t explícito | conceptual_swap | high | Usa $F - \dot{x}F_{\dot{x}}=C$ si $F_t \neq 0$ | La identidad de Beltrami solo vale cuando $\frac{\partial F}{\partial t}=0$ explícitamente; si $t$ aparece en $F$, use Euler completa. |
| `D-C13-04` | Iguala a cero | conceptual_swap | high | $F - \dot{x}\frac{\partial F}{\partial \dot{x}} = 0$ | La anulación de la derivada temporal implica una constante arbitraria $C$, que solo es cero bajo transversalidad. |
| `D-C13-05` | Usa segunda derivada | conceptual_swap | high | $F - \ddot{x}\frac{\partial F}{\partial \dot{x}} = C$ | La identidad involucra la velocidad $\dot{x}$ multiplicando a $F_{\dot{x}}$, reduciendo el orden de la EDO a uno. |
| `D-C13-06` | Sustituye x por Fx | conceptual_swap | high | $F - x\frac{\partial F}{\partial x} = C$ | La transformación de Legendre en la identidad de Beltrami se realiza respecto a la velocidad $\dot{x}$, no respecto a $x$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C13-01` | - | Ausencia explícita del tiempo $\frac{\partial F}{\partial t}=0$ | Si $F$ depende de $t$, la cantidad $F-\dot{x}F_{\dot{x}}$ no se conserva. | - |

---

### [Hab-10] Resolución de Casos Particulares (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 20: Resolución de Casos Particulares
- **Prerequisites:** C-12, C-13
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 20)

#### Description & Cognitive Model
Cálculo de extremales en problemas sin $x$, sin $\dot{x}$ o autónomos verificando compatibilidad con $x(t_0)$ y $x(t_1)$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab10-01` | Olvida segunda constante | skipped_step | high | $x(t)=c_1 t$ al integrar $\dot{x}=c_1$ | Al integrar $\dot{x}=c_1$ respecto a $t$ debe añadir una segunda constante $c_2$ para ajustar las dos condiciones de borde. |
| `D-Hab10-02` | Fuerza bordes imposibles | skipped_step | high | Reporta $x(t)=-t$ aunque $x(0)\neq 0$ | Cuando $F_x=0$ fija $x(t)$ sin constantes libres, verifique si cumple $x(t_0)=x_0$ y $x(t_1)=x_1$ antes de concluir existencia. |
| `D-Hab10-03` | Error de signo en Fx | conceptual_swap | high | $F=(t+x)^2 \Rightarrow F_x=2(t-x)$ | Aplique la regla de la cadena correctamente: la derivada de $(t+x)^2$ respecto a $x$ es $2(t+x)$, dando $x(t)=-t$. |
| `D-Hab10-04` | Confunde constante c | conceptual_swap | high | $-2\dot{x}=c \Rightarrow \dot{x}=c$ y usa $c$ mal | Despeje primero $\dot{x}=-c/2=c_1$ e integre para obtener $x(t)=c_1 t+c_2$ antes de evaluar $x(0)=1$ y $x(1)=2$. |
| `D-Hab10-05` | Deriva F respecto a t | conceptual_swap | high | Calcula $\frac{d}{dt}[t^2-\dot{x}^2]=0$ | El integrando $F=t^2-\dot{x}^2$ depende explícitamente de $t$, por lo que debe usar el caso sin $x$ ($F_{\dot{x}}=c$), no Beltrami. |
| `D-Hab10-06` | Integra sin despejar | conceptual_swap | high | $F_{\dot{x}}=-2\dot{x}=c \Rightarrow x=-t^2+c$ | Como $F_{\dot{x}}=-2\dot{x}$ es constante, $\dot{x}$ es constante y su integral respecto a $t$ es lineal, no cuadrática. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab10-01` | - | Existencia de función admisible continua | Si la solución algebraica viola los extremos fijos, no existe óptimo. | - |

---

### [C-14] Transversalidad: Estado Final Libre (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 21: Transversalidad: Estado Final Libre
- **Prerequisites:** C-12
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 21)

#### Description & Cognitive Model
Condición de frontera natural $\left.\frac{\partial F}{\partial \dot{x}}\right|_{t=t_1}=0$ cuando $x(t_1)$ es libre en horizonte fijo $[t_0,t_1]$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C14-01` | Anula derivada en x | conceptual_swap | high | $\left.\frac{\partial F}{\partial x}\right|_{t=t_1}=0$ | La variación libre del estado terminal $x(t_1)$ anula el momento conjugado $\frac{\partial F}{\partial \dot{x}}$, no $\frac{\partial F}{\partial x}$. |
| `D-C14-02` | Evalúa en tiempo inicial | conceptual_swap | high | $\left.\frac{\partial F}{\partial \dot{x}}\right|_{t=t_0}=0$ | El estado inicial $x(t_0)=x_0$ está fijo; la condición de transversalidad solo se impone en el extremo libre $t=t_1$. |
| `D-C14-03` | Usa condición de t1 libre | conceptual_swap | high | $\left.(F-\dot{x}F_{\dot{x}})\right|_{t=t_1}=0$ | La expresión $F-\dot{x}F_{\dot{x}}=0$ corresponde a horizonte $t_1$ libre; cuando $t_1$ es fijo y $x(t_1)$ libre se usa $F_{\dot{x}}=0$. |
| `D-C14-04` | Fija estado final cero | conceptual_swap | high | $x(t_1)=0$ | Estado final libre significa que $x(t_1)$ no está restringido a cero ni a ningún valor previo; lo determina $F_{\dot{x}}|_{t_1}=0$. |
| `D-C14-05` | Invierte signo Legendre | conceptual_swap | high | $\frac{\partial^2 F}{\partial (\dot{x})^2}>0$ para máximo | Para maximizar $J(x)$, la condición necesaria de Legendre exige $F_{\dot{x}\dot{x}} \le 0$ (estricta $<0$), no positiva. |
| `D-C14-06` | Omite concavidad global | conceptual_swap | high | Euler y transversalidad bastan para máximo global | Las condiciones de primer orden y Legendre solo garantizan extremal o óptimo local; el máximo global requiere $F$ cóncava en $(x,\dot{x})$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C14-01` | - | Horizonte terminal $t_1$ fijo y conocido | Si $t_1$ también fuera libre, se requeriría una condición adicional. | - |

---

### [Hab-11] Extremales con Estado Final Libre (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 22: Extremales con Estado Final Libre
- **Prerequisites:** C-14
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 22)

#### Description & Cognitive Model
Resolución de problemas con $x(t_1)$ libre hallando constantes con $x(t_0)=x_0$ y $F_{\dot{x}}|_{t=t_1}=0$, y validando $H_F$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab11-01` | Evalúa antes de derivar | skipped_step | high | Sustituye $t=2$ antes de hallar $\dot{x}$ | Primero calcule la expresión simbólica de $\frac{\partial F}{\partial \dot{x}}$ en función de $t$ y $\dot{x}$, y luego evalúe en $t=2$. |
| `D-Hab11-02` | Error en constante c | skipped_step | high | $t+2\dot{x}=c \Rightarrow x(t)=-\frac{t^2}{2}+ct+c_1$ | Al despejar $\dot{x}=\frac{c-t}{2}$ e integrar, los coeficientes quedan divididos por $2$ y $4$, resultando $x(t)=-\frac{t^2}{4}+\frac{c}{2}t+c_1$. |
| `D-Hab11-03` | Hessiana mal ordenada | conceptual_swap | high | Pone $F_{\dot{x}\dot{x}}$ en entrada $(1,1)$ de $H_F$ | La matriz Hessiana $H_F$ ordena segundas derivadas respecto a $(x,\dot{x})$, colocando $F_{xx}=0$ en $(1,1)$ y $F_{\dot{x}\dot{x}}=2$ en $(2,2)$. |
| `D-Hab11-04` | Confunde mínimo y máximo | conceptual_swap | high | $F_{\dot{x}\dot{x}}=2>0 \Rightarrow$ máximo local | Una segunda derivada positiva $F_{\dot{x}\dot{x}}=2>0$ y $H_F$ semidefinida positiva corresponden a un mínimo, no a un máximo. |
| `D-Hab11-05` | Aplica x(2)=0 | conceptual_swap | high | Usa $x(2)=0$ para hallar $c$ | Como $x(2)$ es libre, no debe igualarlo a cero; use $t+2\dot{x}|_{t=2}=0$ para obtener $c=0$ y $x(t)=-t^2/4$. |
| `D-Hab11-06` | Omite constante c1 | conceptual_swap | high | $x(0)=0 \Rightarrow c=0$ | La condición inicial $x(0)=0$ determina la constante de integración $c_1=0$, mientras que $c=0$ proviene de la transversalidad. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab11-01` | - | Convexidad conjunta de $F$ en $(x,\dot{x})$ | Sin $H_F$ semidefinida positiva no se asegura mínimo global. | - |

---

### [C-15] Transversalidad: Instante Final Libre (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 24: Transversalidad: Instante Final Libre
- **Prerequisites:** C-13, C-14
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 24)

#### Description & Cognitive Model
Condición $\left.\left(F - \dot{x}\frac{\partial F}{\partial \dot{x}}\right)\right|_{t=t_1}=0$ cuando $t_1$ es libre y el estado terminal $x(t_1)=x_1$ está fijado

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C15-01` | Usa condición de x1 libre | conceptual_swap | high | $\left.\frac{\partial F}{\partial \dot{x}}\right|_{t=t_1}=0$ | Cuando $x(t_1)=x_1$ es fijo y $t_1$ es libre, la transversalidad anula el hamiltoniano/Beltrami $F-\dot{x}F_{\dot{x}}$, no solo $F_{\dot{x}}$. |
| `D-C15-02` | Signo positivo en F | conceptual_swap | high | $\left.\left(F + \dot{x}\frac{\partial F}{\partial \dot{x}}\right)\right|_{t=t_1}=0$ | La condición de transversalidad para tiempo terminal libre siempre resta $\dot{x}\frac{\partial F}{\partial \dot{x}}$ al integrando $F$. |
| `D-C15-03` | Evalúa en t0 | conceptual_swap | high | $\left.\left(F - \dot{x}\frac{\partial F}{\partial \dot{x}}\right)\right|_{t=t_0}=0$ | El instante inicial $t_0$ es fijo; la condición de transversalidad se evalúa exclusivamente en el instante libre $t=t_1$. |
| `D-C15-04` | Omite condición x(t1)=x1 | conceptual_swap | high | Solo usa $x(t_0)=x_0$ y transversalidad | Necesita las tres condiciones ($x(t_0)=x_0$, $x(t_1)=x_1$ y transversalidad en $t_1$) para determinar $c_1, c_2$ y el tiempo $t_1$. |
| `D-C15-05` | Asume t1 arbitrario | conceptual_swap | high | $F-\dot{x}F_{\dot{x}}=0$ para todo $t\in[t_0,t_1]$ | A diferencia de la identidad de Beltrami ($=C$ en todo $t$), la transversalidad solo exige que $F-\dot{x}F_{\dot{x}}$ sea cero en $t=t_1$. |
| `D-C15-06` | Confunde con Fx | conceptual_swap | high | $\left.\left(F - x\frac{\partial F}{\partial x}\right)\right|_{t=t_1}=0$ | El término de corrección por desplazamiento temporal involucra la velocidad $\dot{x}$ y el momento $F_{\dot{x}}$, no $xF_x$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C15-01` | - | Existencia de tiempo terminal positivo $t_1 > t_0$ | Una raíz negativa o compleja de $t_1$ carece de sentido temporal. | - |

---

### [Hab-12] Extremales con Horizonte Libre (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 25: Extremales con Horizonte Libre
- **Prerequisites:** C-15
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 25)

#### Description & Cognitive Model
Resolución del sistema formado por $x(t_0)=x_0$, $x(t_1)=x_1$ y $\left.(F-\dot{x}F_{\dot{x}})\right|_{t=t_1}=0$ para hallar $x(t)$ y $t_1$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab12-01` | Error al integrar x'' | skipped_step | high | $1-6\ddot{x}=0 \Rightarrow x(t)=\frac{t^2}{6}+c_1 t+c_2$ | Al integrar $\ddot{x}=\frac{1}{6}$ dos veces, primero obtiene $\dot{x}=\frac{t}{6}+c_1$ y luego $x(t)=\frac{t^2}{12}+c_1 t+c_2$. |
| `D-Hab12-02` | Fija t1=1 arbitrario | skipped_step | high | Sustituye $t_1=1$ en $x(t_1)=5$ | El horizonte $t_1$ es una incógnita del problema; manténgalo simbólico hasta despejar $c_1=0$ y resolver $t_1^2-60=0$. |
| `D-Hab12-03` | Signo en transversalidad | conceptual_swap | high | $3\dot{x}^2+x+\dot{x}(6\dot{x})=0 \Rightarrow 9\dot{x}^2+x=0$ | Debe restar $\dot{x}F_{\dot{x}}=6\dot{x}^2$ a $F=3\dot{x}^2+x$, obteniendo $-3\dot{x}^2+x=0$ evaluado en $t_1$. |
| `D-Hab12-04` | Acepta raíz negativa | conceptual_swap | high | $t_1^2=60 \Rightarrow t_1=-\sqrt{60}$ | Como el intervalo temporal inicia en $t_0=0$, el instante final $t_1$ debe ser positivo, eligiendo $t_1=\sqrt{60}$. |
| `D-Hab12-05` | Omite término x en F | conceptual_swap | high | Evalúa solo $3\dot{x}^2-\dot{x}(6\dot{x})=0$ | La condición evalúa el integrando completo $F=3\dot{x}^2+x$; al incluir $x(t_1)$ se cancelan los términos en $t_1^2$ y queda $-3c_1^2=0$. |
| `D-Hab12-06` | Concluye sin Hessiana | conceptual_swap | high | Solo verifica $\frac{\partial^2 F}{\partial \dot{x}^2}=6>0$ para global | La condición de Legendre ($6>0$) garantiza mínimo local; para mínimo global debe verificar $H_F$ semidefinida positiva. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab12-01` | - | Intervalo temporal no degenerado $t \in [0, t_1]$ con $t_1 > 0$ | Solo la raíz positiva $t_1=\sqrt{60}$ define un horizonte válido. | - |

---

### [Hab-13] Modelado Económico Variacional (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 28: Modelado Económico Variacional
- **Prerequisites:** C-12, Hab-10
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 28)

#### Description & Cognitive Model
Formulación del funcional $\lambda(\pi,\dot{\pi})=\left(\frac{\dot{\pi}}{\beta j}\right)^2+\alpha\left(\frac{\dot{\pi}}{j}+\pi\right)^2$ en desinflación y obtención de $\pi(t)$ óptima

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab13-01` | Despeja mal p | skipped_step | high | $\dot{\pi}=j(p-\pi) \Rightarrow p=\frac{\dot{\pi}}{j}-\pi$ | Al despejar $p$ de $\dot{\pi}=j(p-\pi)$ divida por $j$ y sume $\pi$, obteniendo $p=\frac{\dot{\pi}}{j}+\pi$. |
| `D-Hab13-02` | Invierte signo de Phillips | skipped_step | high | $p=-\beta(y_f-y)+\pi \Rightarrow y_f-y=\frac{\dot{\pi}}{\beta j}$ | Sustituya $p-\pi=\frac{\dot{\pi}}{j}$ en $p-\pi=-\beta(y_f-y)$ para obtener $(y_f-y)^2=\left(\frac{\dot{\pi}}{\beta j}\right)^2$. |
| `D-Hab13-03` | Omite término cruzado | conceptual_swap | high | $\frac{\partial F}{\partial \dot{\pi}}=2\frac{\dot{\pi}}{(\beta j)^2}+2\alpha\frac{\dot{\pi}}{j^2}$ | Al derivar $\alpha(\frac{\dot{\pi}}{j}+\pi)^2$ respecto a $\dot{\pi}$ no olvide el término cruzado $2\alpha\frac{\pi}{j}$ que luego se cancela en Euler. |
| `D-Hab13-04` | Raíces complejas erróneas | conceptual_swap | high | $(1+\beta^2\alpha)\ddot{\pi}-\beta^2 j^2\alpha\pi=0 \Rightarrow r=\pm i\omega$ | Como los coeficientes tienen signos opuestos, la ecuación característica $r^2(1+\beta^2\alpha)=\beta^2 j^2\alpha$ da raíces reales $r=\pm\frac{\beta j\sqrt{\alpha}}{\sqrt{1+\beta^2\alpha}}$. |
| `D-Hab13-05` | Usa fronteras erróneas | conceptual_swap | high | Impone $\pi(0)=0$ y $\pi(T)=\pi_0$ | El plan de desinflación parte de $\pi(0)=\pi_0$ y busca eliminar la inflación esperada al final del horizonte con $\pi(T)=0$. |
| `D-Hab13-06` | Confunde maximización | conceptual_swap | high | Busca $\max \int_0^T \lambda(\pi,\dot{\pi})dt$ | El funcional $\lambda(p,y)$ representa pérdidas por brecha de producto e inflación, por lo que el banco central minimiza la integral. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab13-01` | - | Parámetros positivos $\alpha, \beta > 0$ y velocidad de ajuste $0 < j \le 1$ | Garantiza que $H_F$ sea definida positiva y exista mínimo global único. | - |

---

### [C-16] Principio del Máximo de Pontryagin (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 1: Principio del Máximo de Pontryagin
- **Prerequisites:** C-01
- **Evidence Citations:** `Problemas_teoria_de_control.pdf` (page 1)

#### Description & Cognitive Model
Formulación del Hamiltoniano $H(x,u,\lambda)=f(x,u)+\lambda g(x,u)$, ecuación de coestado $\dot{\lambda}=-\partial H/\partial x$ y transversalidad $\lambda(T)=0$ con estado final libre

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C16-01` | Signo ecuación coestado | conceptual_swap | high | $\dot{\lambda}=\partial H/\partial x$ | Recuerde que la dinámica del coestado lleva signo negativo $\dot{\lambda}=-\partial H/\partial x$ en control óptimo sin descuento. |
| `D-C16-02` | Transversalidad errónea | conceptual_swap | high | $x(T)=0$ siempre | Distinga estado final libre, donde se impone $\lambda(T)=0$, de estado final fijo $x(T)=x_T$ sin condición previa en $\lambda(T)$. |
| `D-C16-03` | Omite coestado en H | conceptual_swap | high | $H=f(x,u)+g(x,u)$ | Multiplique la ecuación de movimiento $\dot{x}=g(x,u)$ por la variable de coestado $\lambda(t)$ al construir el Hamiltoniano. |
| `D-C16-04` | Condición de control | conceptual_swap | high | $\partial H/\partial x=0$ | Derive el Hamiltoniano respecto al control $u$, no respecto al estado $x$, para obtener la condición óptima $\partial H/\partial u=0$. |
| `D-C16-05` | Descuento espurio | conceptual_swap | high | $\dot{\lambda}=\rho\lambda-\partial H/\partial x$ | Verifique que el problema no tiene descuento temporal ($\rho=0$), por lo que la ecuación adjunta es $\dot{\lambda}=-\partial H/\partial x$. |
| `D-C16-06` | Coestado inicial nulo | conceptual_swap | high | $\lambda(0)=0$ | Aplique la condición inicial dada sobre el estado $x(0)=x_0$ y la transversalidad $\lambda(T)=0$ al final del horizonte. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C16-01` | - | Existencia de solución interior suave en $u(t)\ge 0$ sin factor de descuento ($\rho=0$) | Si el control alcanza la cota $u=0$, deben usarse multiplicadores de holgura complementaria. | - |

---

### [Hab-14] Aplicaciones de Control Óptimo con Estado Libre (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 1: Inversión Óptima en Publicidad
- **Prerequisites:** C-16
- **Evidence Citations:** `Problemas_teoria_de_control.pdf` (page 1), `Problemas_teoria_de_control.pdf` (page 2)

#### Description & Cognitive Model
Resolución de problemas aplicados de control óptimo (publicidad, inventarios y seguridad) con estado final libre $\lambda(T)=0$ mediante el Hamiltoniano y sistema coestado-estado.

#### Fused Distractor Models (10)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab14-01` | Signo depreciación | skipped_step | high | $\dot{x}=u+0.5x$ | Reste la depreciación natural del $50\%$ anual en la ecuación de estado: $\dot{x}=u-0.5x$ en lugar de sumarla. |
| `D-Hab14-07` | Omite signo minimizar | skipped_step | high | $H=\frac{1}{2}x^2+\frac{1}{2}(u-5)^2+\lambda(u-5)$ con $\dot{\lambda}=-\partial H/\partial x$ | Al minimizar costos, formule $H=-\frac{1}{2}x^2-\frac{1}{2}(u-5)^2+\lambda(u-5)$ o invierta el signo en $\partial H/\partial u=0$ para obtener $\dot{\lambda}=x$. |
| `D-Hab14-08` | Signo del control en EDO | skipped_step | high | $\dot{x}=4-x+u$ | Reste la intensidad de intervención $u$ porque cada unidad reduce el ritmo de cambio del índice: $\dot{x}=4-x-u$. |
| `D-Hab14-02` | Factor 2 en control | skipped_step | high | $u^*=2\lambda$ | Derive $-u^2$ correctamente: $\partial H/\partial u=-2u+\lambda=0 \Rightarrow u^*=\lambda/2$, no $2\lambda$. |
| `D-Hab14-09` | Demanda mal restada | skipped_step | high | $\dot{x}=u+5$ | Reste la demanda constante de cinco unidades anuales en la acumulación de inventario: $\dot{x}=u-5$. |
| `D-Hab14-10` | Signo en coestado | skipped_step | high | $\dot{\lambda}=-1-\lambda$ | Al maximizar $-J$ con $H=-x-\frac{1}{2}u^2+\lambda(4-x-u)$, calcule $\dot{\lambda}=-\partial H/\partial x=-(-1-\lambda)=1+\lambda$. |
| `D-Hab14-03` | Signo coestado | conceptual_swap | high | $\dot{\lambda}=4-0.5\lambda$ | Aplique $\dot{\lambda}=-\partial H/\partial x=-(4-0.5\lambda)=-4+0.5\lambda$ para obtener $\lambda(t)=8(1-e^{0.5(t-2)})$. |
| `D-Hab14-11` | Desviación sin 5 | conceptual_swap | high | $H=-\frac{1}{2}x^2-\frac{1}{2}u^2+\lambda(u-5)$ | Centre el costo de ajuste en la desviación respecto a cinco unidades anuales: $\frac{1}{2}(u-5)^2$, lo que da $u^*=5+\lambda$. |
| `D-Hab14-12` | Despeje de u con signo | conceptual_swap | high | $u^*=\lambda$ | Resuelva $\partial H/\partial u=-u-\lambda=0 \Rightarrow u^*=-\lambda$; como $\lambda(t)=e^{t-2}-1\le 0$, resulta $u^*(t)=1-e^{t-2}\ge 0$. |
| `D-Hab14-04` | Valor terminal fijo | conceptual_swap | high | $x(2)=0$ | Diferencie ausencia de valor residual, que implica $\lambda(2)=0$ con $x(2)$ libre, de una obligación de agotar el estado. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab14-01` | - | Tasa de depreciación continua constante $\delta=0.5$ y no negatividad $u(t)\ge 0$ verificada por $\lambda(t)\ge 0$ | Como $1-e^{0.5(t-2)}\ge 0$ en $[0,2]$, la restricción $u\ge 0$ no se satura. | - |
| `A-Hab14-02` | - | Restricciones de no negatividad $x(t)\ge 0$ y $u(t)\ge 0$ inactivas en $[0,2]$ | Como $x^*(t)>0$ y $u^*(t)=5+\lambda(t)>4$, no se activan cotas inferiores. | - |
| `A-Hab14-03` | - | Índice inicial $x(0)=5$ y tasa natural de reducción del $100\%$ anual sin cota activa en $x\ge 0$ | El término constante $4$ y $u^*\le 1$ mantienen $x^*(t)>0$ en $[0,2]$. | - |

---

### [Hab-16] Utilización Óptima de Permisos de Emisión (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 1: Utilización Óptima de Permisos de Emisión
- **Prerequisites:** C-16
- **Evidence Citations:** `Problemas_teoria_de_control.pdf` (page 1)

#### Description & Cognitive Model
Maximización de $\int_0^3 (12u-u^2)\,dt$ sujeta a $\dot{x}=2-u$, $x(0)=6$ y estado final fijo $x(3)=0$ mediante coestado constante $\dot{\lambda}=0$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab16-01` | Transversalidad nula | skipped_step | high | $\lambda(3)=0$ | Recuerde que la empresa debe agotar todos los permisos ($x(3)=0$ fijo), por lo que $\lambda(3)$ es libre y se determina con $x(3)=0$. |
| `D-Hab16-02` | Signo de emisiones | skipped_step | high | $\dot{x}=2+u$ | Reste las emisiones $u$ y sume la asignación continua de $2$ permisos por año: $\dot{x}=2-u$. |
| `D-Hab16-03` | Omite asignación anual | conceptual_swap | high | $\dot{x}=-u$ | Incluya los $2$ permisos adicionales por año en $\dot{x}=2-u$; así se dispone de $6+3(2)=12$ permisos en total y $u^*=4$. |
| `D-Hab16-04` | Derivada de control | conceptual_swap | high | $12-u-\lambda=0$ | Derive correctamente el término cuadrático: $\partial H/\partial u=12-2u-\lambda=0 \Rightarrow u^*=6-\lambda/2$. |
| `D-Hab16-05` | Coestado variable | conceptual_swap | high | $\dot{\lambda}=-\lambda$ | Verifique que $H$ no depende del estado $x$, por lo que $\dot{\lambda}=-\partial H/\partial x=0$ y $\lambda$ es constante. |
| `D-Hab16-06` | Emisión creciente | conceptual_swap | high | $u^*(t)=2t$ | Observe que el beneficio marginal es estrictamente cóncavo y $\lambda$ es constante, por lo que suavizar las emisiones en $u^*=4$ es óptimo. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab16-01` | - | Stock inicial $x(0)=6$ y flujo continuo de $2$ permisos anuales totalmente agotados en $T=3$ | La trayectoria $x^*(t)=6-2t$ verifica $x^*(t)\ge 0$ en todo $[0,3]$. | - |

---

### [C-17] Planteamiento de Control Óptimo (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 1: Planteamiento de Control Óptimo
- **Prerequisites:** C-01, C-07
- **Evidence Citations:** `Teoria_de_control_optimo___teoria (1).pdf` (page 1)

#### Description & Cognitive Model
Formulación dinámica con ecuación de estado $\dot{x}=f(x,u,t)$, control admisible $u(t)\in\Omega$ continuo a trozos y funcional objetivo $J=\int_{t_0}^{t_1} F(x,u,t)\,dt + S[x(t_1)]$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C17-01` | Control continuo global | conceptual_swap | high | $u(t)\in C^1([t_0,t_1])$ | Recuerde que un control admisible solo requiere ser continuo a trozos con saltos finitos, generando esquinas en $x(t)$. |
| `D-C17-02` | Estado discontinuo | conceptual_swap | high | $x(t)\text{ admite saltos}$ | La variable de estado $x(t)$ debe ser continua y diferenciable por tramos; las discontinuidades ocurren en $u(t)$. |
| `D-C17-03` | Omite valor terminal | conceptual_swap | high | $J=\int_{t_0}^{t_1} F(x,u,t)\,dt$ | En el funcional a lo Bolza debe sumar tanto la integral intermedia $F(x,u,t)$ como la función de rescate $S[x(t_1)]$. |
| `D-C17-04` | Confunde Mayer y Lagrange | conceptual_swap | high | $J=S[x(t_1)]\text{ con }S=0$ | El funcional a lo Mayer anula la integral ($F=0$) dejando $S[x(t_1)]$, mientras Lagrange anula $S=0$ dejando la integral. |
| `D-C17-05` | Omite conjunto de control | conceptual_swap | high | $u(t)\in\mathbb{R}\text{ siempre}$ | Incluya la restricción compacta y convexa $u(t)\in\Omega$, pues habilita soluciones de esquina ausentes en cálculo de variaciones. |
| `D-C17-06` | Confunde estado y control | conceptual_swap | high | $\dot{u}(t)=f(x,u,t)$ | La ecuación diferencial $\dot{x}=f(x,u,t)$ gobierna la evolución del estado $x(t)$ dada la elección del control $u(t)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C17-01` | - | El conjunto de controles admisibles $\Omega$ es compacto y convexo | Sin compacidad y convexidad de $\Omega$ pueden no existir soluciones óptimas o de esquina bien definidas. | - |

---

### [Hab-19] Hamiltoniano en Valor Corriente (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 6: Hamiltoniano en Valor Corriente
- **Prerequisites:** C-01, Hab-05
- **Evidence Citations:** `Teoria_de_control_optimo___teoria (1).pdf` (page 6)

#### Description & Cognitive Model
Resolución de problemas con factor de descuento $e^{-\rho t}$ usando $\mathcal{H}=F+mf$ ($m=\lambda e^{\rho t}$), ecuación $\frac{\partial\mathcal{H}}{\partial x}=-\dot{m}+\rho m$ y transversalidad en horizonte infinito

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab19-01` | Omite término rho m | skipped_step | high | $\frac{\partial\mathcal{H}}{\partial x}=-\dot{m}$ | Al cambiar $m=\lambda e^{\rho t}$, la derivada $\dot{\lambda}=e^{-\rho t}(\dot{m}-\rho m)$ introduce el término adicional $+\rho m$: $\mathcal{H}_x=-\dot{m}+\rho m$. |
| `D-Hab19-02` | Signo negativo en rho m | conceptual_swap | high | $\frac{\partial\mathcal{H}}{\partial x}=-\dot{m}-\rho m$ | Como $H=e^{-\rho t}\mathcal{H}$ y $H_x=-\dot{\lambda}=-e^{-\rho t}(\dot{m}-\rho m)$, al cancelar $e^{-\rho t}$ queda $\mathcal{H}_x=-\dot{m}+\rho m$. |
| `D-Hab19-03` | Descuenta f en valor corriente | skipped_step | high | $\mathcal{H}=e^{-\rho t}F+mf$ | El Hamiltoniano en valor corriente se define multiplicando $H$ por $e^{\rho t}$, eliminando el descuento de $F$: $\mathcal{H}=F+mf$. |
| `D-Hab19-04` | Cambio inverso de coestado | conceptual_swap | high | $m=\lambda e^{-\rho t}$ | Dado que $H=e^{-\rho t}F+\lambda f$ y $\mathcal{H}=e^{\rho t}H=F+(\lambda e^{\rho t})f$, el coestado corriente es $m=\lambda e^{\rho t}$. |
| `D-Hab19-05` | Transversalidad sin descuento en m | conceptual_swap | high | $\lim_{t\to\infty}m(t)=0\text{ siempre}$ | La condición de transversalidad en horizonte infinito con estado libre exige $\lim_{t\to\infty}\lambda(t)=\lim_{t\to\infty}m(t)e^{-\rho t}=0$, no $m(t)\to 0$. |
| `D-Hab19-06` | Confunde meta asintótica con libre | conceptual_swap | high | $\lim_{t\to\infty}x(t)=x_o\text{ y }\lim_{t\to\infty}\lambda(t)=0$ | La meta asintótica $\lim_{t\to\infty}x(t)=x_o$ corresponde a estado final fijo, mientras $\lim_{t\to\infty}\lambda(t)=0$ corresponde a estado final libre. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab19-01` | - | La integral descontada $\int_{t_0}^{\infty} e^{-\rho t}F(x,u,t)\,dt$ converge para $\rho>0$ | Sin convergencia de la integral en horizonte infinito no está bien definido el óptimo. | - |

---
