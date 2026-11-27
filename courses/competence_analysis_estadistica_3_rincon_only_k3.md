# Cognitive Task Analysis (CTA): Estadistica 3 Rincon Only K3

- **Course ID:** `estadistica_3_rincon_only_k3`
- **Macro-Competency:** Dominio y aplicación analítica integral de Estadistica 3 Rincon Only K3
- **Structure:** 11 total competencies (1 Facts, 6 Concepts, 4 Skills) with 45 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Proceso Estocástico y Trayectorias | Concept | Evaluate | Unidad 1: Proceso Estocástico y Trayectorias | - | 3 |
| `C-02` | Propiedad de Markov y Martingalas | Concept | Evaluate | Unidad 4: Propiedad de Markov y Martingalas | C-01 | 3 |
| `C-03` | Incrementos y Procesos de Lévy y Gaussianos | Concept | Evaluate | Unidad 5: Incrementos y Procesos de Lévy y Gaussianos | C-01 | 3 |
| `H-01` | Caminata Aleatoria Simple en Enteros | Fact | Understand | Unidad 7: Caminata Aleatoria Simple en Enteros | C-02 | 3 |
| `Hab-01` | Esperanza y Varianza de Caminata Aleatoria | Skill | Evaluate | Unidad 8: Esperanza y Varianza de Caminata Aleatoria | H-01 | 6 |
| `Hab-02` | Distribución de Transición en n Pasos | Skill | Evaluate | Unidad 10: Distribución de Transición en n Pasos | H-01 | 6 |
| `C-04` | Retorno Eventual al Origen y Dicotomía Simétrica | Concept | Evaluate | Unidad 12: Retorno Eventual al Origen y Dicotomía Simétrica | Hab-02 | 3 |
| `C-05` | Planteamiento de la Ruina del Jugador | Concept | Analyze | Unidad 16: Planteamiento de la Ruina del Jugador | H-01 | 3 |
| `Hab-03` | Resolución de Probabilidad de Ruina del Jugador | Skill | Evaluate | Unidad 17: Resolución de Probabilidad de Ruina del Jugador | C-05 | 6 |
| `C-06` | Sensibilidad y Asimetría en Ruina del Jugador | Concept | Evaluate | Unidad 19: Sensibilidad y Asimetría en Ruina del Jugador | Hab-03 | 3 |
| `Hab-04` | Duración Esperada antes de la Ruina | Skill | Evaluate | Unidad 20: Duración Esperada antes de la Ruina | C-05, Hab-03 | 6 |

---

## Detailed Competency Specifications

### [C-01] Proceso Estocástico y Trayectorias (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 1: Proceso Estocástico y Trayectorias
- **Prerequisites:** None
- **Recommended Modalities:** unstructured_model, adversarial_break, multiple_select
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 1)

#### Description & Cognitive Model
Definición formal de proceso estocástico $\{X_t : t \in T\}$ sobre $(\Omega, \mathscr{F}, P)$ distinguiendo espacio parametral $T$, espacio de estados $S$, variables aleatorias y trayectorias.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Confunde trayectoria con variable | conceptual_swap | high | $t \mapsto X_t(\omega)$ es una variable aleatoria | Fije $\omega \in \Omega$ para obtener una función determinista del tiempo (trayectoria) y fije $t \in T$ para obtener una variable aleatoria. |
| `D-C01-02` | Exige independencia total | conceptual_swap | high | $X_t$ y $X_s$ siempre son independientes | Recuerde que un proceso estocástico modela evolución con estructura de dependencia temporal entre sus variables aleatorias. |
| `D-C01-03` | Confunde espacio parametral y de estados | conceptual_swap | high | $T$ es el conjunto de valores de $X_t$ | Distinga el conjunto parametral $T$ que indexa el tiempo del espacio de estados $S$ donde toman valores las variables aleatorias. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Base dada por un espacio de probabilidad $(\Omega, \mathscr{F}, P)$ y una $\sigma$-álgebra en $S$ | Sin $\sigma$-álgebra asociada a $S$ no es posible definir eventos medibles $(X_t \in A)$ ni probabilidades. | - |

---

### [C-02] Propiedad de Markov y Martingalas (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Propiedad de Markov y Martingalas
- **Prerequisites:** C-01
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 4)

#### Description & Cognitive Model
Caracterización de procesos de Markov mediante independencia condicional del pasado dado el presente y de martingalas a tiempo discreto mediante esperanza condicional constante.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Confunde Markov con independencia | conceptual_swap | high | $P(X_{n+1}=x_{n+1}\mid X_n=x_n) = P(X_{n+1}=x_{n+1})$ | La propiedad de Markov descarta la historia pasada $X_0,\dots,X_{n-1}$ dado $X_n$, pero mantiene la dependencia respecto al presente $X_n$. |
| `D-C02-02` | Confunde martingala con proceso constante | conceptual_swap | high | $X_{n+1} = X_n$ casi seguramente | Una martingala exige que el promedio condicional futuro $E(X_{n+1}\mid X_0,\dots,X_n)$ sea $X_n$, permitiendo fluctuaciones aleatorias. |
| `D-C02-03` | Asume equivalencia Markov-Martingala | conceptual_swap | high | Todo proceso de Markov es una martingala | Verifique por separado la estructura de transición condicional de Markov y la igualdad de esperanza condicional que define un juego justo. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | Existencia de la esperanza $E(|X_n|) < \infty$ para definir la martingala | Si las variables no son integrables, la esperanza condicional $E(X_{n+1}\mid X_0,\dots,X_n)$ no está bien definida. | - |

---

### [C-03] Incrementos y Procesos de Lévy y Gaussianos (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Incrementos y Procesos de Lévy y Gaussianos
- **Prerequisites:** C-01
- **Recommended Modalities:** adversarial_break, multiple_select, concept_matching
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 5)

#### Description & Cognitive Model
Definición de incrementos independientes, estacionariedad estricta, incrementos estacionarios y su combinación en procesos de Lévy y procesos Gaussianos a tiempo continuo.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Confunde estacionariedad con incrementos estacionarios | conceptual_swap | high | $X_{t+h} \stackrel{d}{=} X_t \Leftrightarrow X_{t+h}-X_{s+h} \stackrel{d}{=} X_t-X_s$ | Distinga la invariancia temporal de las distribuciones finito-dimensionales del proceso respecto a la invariancia de sus diferencias $X_t-X_s$. |
| `D-C03-02` | Incluye tiempos solapados en incrementos | conceptual_swap | high | $X_{t_2}-X_{t_1}$ y $X_{t_3}-X_{t_1}$ son independientes para $t_1 < t_2 < t_3$ | Aplique la independencia de incrementos exclusivamente sobre intervalos de tiempo disjuntos $0 \le t_1 < t_2 < \dots < t_n$. |
| `D-C03-03` | Reduce Lévy a un solo requisito | conceptual_swap | high | Incrementos independientes implican proceso de Lévy | Verifique simultáneamente ambas condiciones: un proceso de Lévy requiere tanto incrementos independientes como incrementos estacionarios. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | Espacio parametral continuo $T=[0,\infty)$ con orden temporal $0 \le t_1 < t_2 < \dots < t_n$ | Sin intervalos ordenados y disjuntos no se garantiza la descomposición aditiva de desplazamientos independientes. | - |

---

### [H-01] Caminata Aleatoria Simple en Enteros (Fact)

- **Bloom Level:** Understand
- **Session:** Unidad 7: Caminata Aleatoria Simple en Enteros
- **Prerequisites:** C-02
- **Recommended Modalities:** fill_in_the_blank, multiple_select, concept_matching
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 7)

#### Description & Cognitive Model
Definición de caminata aleatoria simple sobre $\mathbb{Z}$ con probabilidades homogéneas $p$ a la derecha y $q=1-p$ a la izquierda mediante suma de pasos i.i.d. $\xi_i \in \{+1,-1\}$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Asume pasos dependientes | conceptual_swap | high | $\xi_i$ depende de la posición previa $X_{i-1}$ | En una caminata aleatoria simple, los pasos $\xi_1, \xi_2, \dots$ son independientes e idénticamente distribuidos con $P(\xi=+1)=p$. |
| `D-H01-02` | Permite permanencia sin especificarla | conceptual_swap | high | $P(X_{n+1}=i \mid X_n=i) > 0$ con $p+q=1$ | Cuando $p+q=1$ en la caminata simple, el proceso siempre avanza a $i+1$ o retrocede a $i-1$ sin probabilidad de permanencia. |
| `D-H01-03` | Olvida restricción de suma unitaria | conceptual_swap | high | $p$ y $q$ pueden sumar distinto de $1$ | Asegure que las probabilidades de transición hacia $+1$ y $-1$ formen una distribución válida cumpliendo $p+q=1$. |

---

### [Hab-01] Esperanza y Varianza de Caminata Aleatoria (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 8: Esperanza y Varianza de Caminata Aleatoria
- **Prerequisites:** H-01
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, adversarial_break
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 8)

#### Description & Cognitive Model
Cálculo analítico de la esperanza $E(X_n)=n(p-q)$ y la varianza $\operatorname{Var}(X_n)=4npq$ para $X_0=0$, junto con su interpretación de deriva y dispersión máxima simétrica.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Confunde varianza con segundo momento | skipped_step | high | $\operatorname{Var}(\xi) = E(\xi^2) = 1$ | Reste el cuadrado de la media $E(\xi)=p-q$ al segundo momento $E(\xi^2)=1$ para obtener $\operatorname{Var}(\xi)=1-(p-q)^2=4pq$. |
| `D-Hab01-02` | Aplica factor cuadrático en n | skipped_step | high | $\operatorname{Var}(X_n) = 4n^2 pq$ | Use la aditividad de la varianza para variables independientes $\xi_i$: la suma de $n$ varianzas iguales produce factor lineal $n$. |
| `D-Hab01-03` | Omite factor 4 en varianza | conceptual_swap | high | $\operatorname{Var}(X_n) = npq$ | Note que $\xi_i \in \{-1, +1\}$ tiene amplitud $2$, por lo que su varianza es $4$ veces la de una Bernoulli con parámetro $p$. |
| `D-Hab01-04` | Suma probabilidades en esperanza | conceptual_swap | high | $E(X_n) = n(p+q) = n$ | Multiplique cada valor del paso ($+1$ y $-1$) por su probabilidad respectiva antes de sumar: $E(\xi)=(+1)p + (-1)q = p-q$. |
| `D-Hab01-05` | Asume varianza nula si p=q | conceptual_swap | high | Si $p=q=1/2$, entonces $\operatorname{Var}(X_n)=0$ | Distinga tendencia media nula de dispersión: en el caso simétrico $p=q=1/2$, la varianza $\operatorname{Var}(X_n)=n$ alcanza su máximo. |
| `D-Hab01-06` | Olvida multiplicar por n | conceptual_swap | high | $E(X_n) = p-q$ | Sume las esperanzas de los $n$ pasos independientes $\sum_{i=1}^n E(\xi_i)$ para obtener la esperanza acumulada $n(p-q)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Condición inicial fija $X_0=0$ e independencia mutua de los pasos $\xi_1,\dots,\xi_n$ | Si $X_0 \neq 0$ aleatorio o los pasos son dependientes, cambian la media y aparecen covarianzas en la varianza. | - |

---

### [Hab-02] Distribución de Transición en n Pasos (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 10: Distribución de Transición en n Pasos
- **Prerequisites:** H-01
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 10)

#### Description & Cognitive Model
Deducción y cálculo de $P(X_n=x \mid X_0=y)$ mediante conteo de pasos a la derecha $R_n=\frac{1}{2}(n+X_n-y)$ y verificación de restricciones de paridad y alcance $-n \le x-y \le n$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Ignora paridad entre pasos y posición | skipped_step | high | $P(X_n=x \mid X_0=0) > 0$ para todo $x \in [-n, n]$ | Verifique que $n$ y $x-y$ tengan la misma paridad antes de aplicar el coeficiente binomial, pues $\frac{1}{2}(n+x-y)$ debe ser entero. |
| `D-Hab02-02` | Usa desplazamiento directo sin dividir por 2 | skipped_step | high | $R_n = n + x - y$ | Resuelva simultáneamente $R_n - L_n = x-y$ y $R_n + L_n = n$ para hallar $R_n = \frac{1}{2}(n+x-y)$ pasos hacia la derecha. |
| `D-Hab02-03` | Intercambia exponentes de p y q | conceptual_swap | high | $p^{\frac{1}{2}(n-x+y)} q^{\frac{1}{2}(n+x-y)}$ | Asocie $p$ al número de pasos a la derecha $R_n=\frac{1}{2}(n+x-y)$ y $q$ al número de pasos a la izquierda $L_n=\frac{1}{2}(n-x+y)$. |
| `D-Hab02-04` | Omite restricción de alcance máximo | conceptual_swap | high | Aplica la fórmula para $|x-y| > n$ | Compruebe que $|x-y| \le n$, pues en $n$ pasos unitarios la distancia recorrida desde $y$ nunca excede $n$ unidades. |
| `D-Hab02-05` | Usa denominador 2n en simétrica | conceptual_swap | high | $P(X_n=x \mid X_0=0) = \binom{n}{\frac{1}{2}(n+x)} \frac{1}{2n}$ | Recuerde que existen $2^n$ trayectorias equiprobables de longitud $n$, por lo que la probabilidad simétrica divide entre $2^n$. |
| `D-Hab02-06` | Olvida trasladar el origen y | conceptual_swap | high | $P(X_n=x \mid X_0=y) = P(X_n=x \mid X_0=0)$ | Defina el proceso desplazado $Z_n = X_n - y$ para reducir la transición de $y$ a $x$ al cálculo equivalente desde $0$ hasta $x-y$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Estados enteros $x, y \in \mathbb{Z}$, tiempo entero $n \ge 0$ e independencia de incrementos $\xi_i$ | Si el desplazamiento no es entero o los pasos no son independientes, la distribución de $R_n$ deja de ser binomial. | - |

---

### [C-04] Retorno Eventual al Origen y Dicotomía Simétrica (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 12: Retorno Eventual al Origen y Dicotomía Simétrica
- **Prerequisites:** Hab-02
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 12)

#### Description & Cognitive Model
Análisis de la probabilidad de retorno eventual $1-|p-q|$ mediante ecuación de renovación $p_n=\sum_{k=0}^n f_k p_{n-k}$ y función generadora $G(t)=1-(1-4pqt^2)^{1/2}$, contrastando certeza y tiempo medio infinito.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Asume retorno seguro si p distinto de q | conceptual_swap | high | $\sum_{n=0}^{\infty} f_n = 1$ para todo $p \in (0,1)$ | Evalúe el límite $1-|p-q|$: únicamente cuando $p=q=1/2$ la probabilidad de eventual regreso al origen es igual a $1$. |
| `D-C04-02` | Asume tiempo medio finito si retorno es seguro | conceptual_swap | high | $p=1/2 \Rightarrow \sum_{n=0}^{\infty} n f_n < \infty$ | Derive $G(t)=1-(1-t^2)^{1/2}$ y evalúe $\lim_{t \nearrow 1} G'(t)$ para constatar que en el caso simétrico el tiempo esperado es infinito. |
| `D-C04-03` | Confunde retorno $p_n$ con primer retorno $f_n$ | conceptual_swap | high | $p_n = f_n$ para todo $n \ge 1$ | Distinga $p_n=P(X_n=0\mid X_0=0)$ de la probabilidad de primer retorno $f_n$, relacionadas por la convolución $p_n = \sum_{k=0}^n f_k p_{n-k}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | Inicio en el origen $X_0=0$, convención $p_0=1, f_0=0$ y radio de convergencia $|t|<1$ | Sin $|t|<1$ la expansión binomial de $(1-4pqt^2)^{-1/2}$ diverge y no aplica el lema de Abel. | - |

---

### [C-05] Planteamiento de la Ruina del Jugador (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 16: Planteamiento de la Ruina del Jugador
- **Prerequisites:** H-01
- **Recommended Modalities:** unstructured_model, adversarial_break, multiple_select
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 16)

#### Description & Cognitive Model
Modelado del problema de la ruina del jugador sobre $\{0,1,\dots,N\}$ con estados absorbentes $0$ y $N$, tiempo de paro $\tau = \min\{n\ge 0: X_n=0 \text{ o } X_n=N\}$ y ecuaciones en diferencias.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Invierte condiciones de frontera de ruina | conceptual_swap | high | $u_0 = 0$ y $u_N = 1$ | Verifique que el estado $0$ representa la ruina del jugador A ($u_0=1$) y el estado $N$ representa su victoria total ($u_N=0$). |
| `D-C05-02` | Omite término independiente en duración | conceptual_swap | high | $m_k = p m_{k+1} + q m_{k-1}$ | Sume la unidad $+1$ correspondiente a la apuesta recién realizada antes de condicionar sobre el resultado siguiente: $m_k = 1 + p m_{k+1} + q m_{k-1}$. |
| `D-C05-03` | Trata fronteras como reflejantes | conceptual_swap | high | Desde $0$ o $N$ la caminata puede regresar a $1$ o $N-1$ | Considere $0$ y $N$ como estados absorbentes donde el juego termina en el instante $\tau$ y la cadena jamás los abandona. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Capital total constante $N \ge 2$, apuestas unitarias sin empates ($p+q=1$) y $\tau < \infty$ c.s. | Si hay empates o capital ilimitado, cambian las transiciones y la finitud casi segura del tiempo de absorción $\tau$. | - |

---

### [Hab-03] Resolución de Probabilidad de Ruina del Jugador (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 17: Resolución de Probabilidad de Ruina del Jugador
- **Prerequisites:** C-05
- **Recommended Modalities:** open_symbolic, proof_dag, fill_in_the_blank
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 17)

#### Description & Cognitive Model
Resolución de la ecuación en diferencias $u_k = p u_{k+1} + q u_{k-1}$ con $u_0=1, u_N=0$ mediante diferencias sucesivas y sumas geométricas $S_k$ para casos simétrico y asimétrico.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Invierte razón q/p a p/q | skipped_step | high | $u_k = \frac{(p/q)^k - (p/q)^N}{1 - (p/q)^N}$ | Reescriba $u_k = p u_{k+1} + q u_{k-1}$ como $u_{k+1}-u_k = (q/p)(u_k-u_{k-1})$ para identificar la razón geométrica correcta $q/p$. |
| `D-Hab03-02` | Aplica fórmula asimétrica en p=1/2 | skipped_step | high | Evalúa $\frac{1^k - 1^N}{1 - 1^N}$ cuando $p=1/2$ | Distinga el caso $p=1/2$ donde $S_k = k+1$ es lineal, obteniendo la solución recta $u_k = (N-k)/N$ en lugar de una forma indeterminada. |
| `D-Hab03-03` | Invierte numerador k/N en p=1/2 | conceptual_swap | high | $u_k = \frac{k}{N}$ para $p=1/2$ | Compruebe las condiciones de frontera: $k/N$ es la probabilidad de ganar ($1-u_k$), mientras la probabilidad de ruina es $(N-k)/N$. |
| `D-Hab03-04` | Trunca mal la suma $S_k$ | conceptual_swap | high | $S_k = \frac{1-(q/p)^k}{1-(q/p)}$ | Cuente los $k+1$ sumandos desde $j=0$ hasta $j=k$ en $S_k = 1 + (q/p) + \dots + (q/p)^k$ para fijar el exponente $k+1$. |
| `D-Hab03-05` | Omite término constante 1 en $u_k$ | conceptual_swap | high | $u_k = \frac{(q/p)^k}{1 - (q/p)^N}$ | Imponga la condición de frontera $u_N=0$ al despejar $u_1-1 = -1/S_{N-1}$, lo cual garantiza que el numerador se anule en $k=N$. |
| `D-Hab03-06` | Confunde índice $S_{k-1}$ con $S_k$ | conceptual_swap | high | $u_k = 1 - \frac{S_k}{S_{N-1}}$ | Sume exactamente desde $u_2-u_1$ hasta $u_k-u_{k-1}$ para obtener factor $S_{k-1}-1$, de modo que $u_k = 1 - S_{k-1}/S_{N-1}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | Probabilidades no degeneradas $p \in (0,1)$, $q=1-p$ y condiciones de frontera $u_0=1, u_N=0$ | Si $p=0$ o $p=1$, no existe razón $q/p$ finita no nula y la solución es determinista ($u_k=1$ o $u_k=0$ para $0<k<N$). | - |

---

### [C-06] Sensibilidad y Asimetría en Ruina del Jugador (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 19: Sensibilidad y Asimetría en Ruina del Jugador
- **Prerequisites:** Hab-03
- **Recommended Modalities:** adversarial_break, multiple_select, unstructured_model
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 19)

#### Description & Cognitive Model
Interpretación cualitativa de $u_k$ frente al capital inicial $k$, el capital total $N$ y la probabilidad $p$: ruina casi segura frente a adversarios muy ricos y alta sensibilidad cerca de $p=1/2$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Cree que juego justo protege capital pequeño | conceptual_swap | high | Si $p=1/2$, entonces $u_k \approx 1/2$ aunque $k \ll N$ | Evalúe $u_k=(N-k)/N$ cuando $k \ll N$: aun en un juego justo ($p=1/2$), jugar contra un adversario mucho más rico lleva a ruina casi segura. |
| `D-C06-02` | Asume variación lineal respecto a p | conceptual_swap | high | $u_k$ cambia a tasa constante en todo $p \in (0,1)$ | Observe el comportamiento de $u_k$ como función de $p$: es casi constante lejos de $1/2$ y cambia abruptamente en una vecindad de $p=1/2$. |
| `D-C06-03` | Asume concavidad única para todo p | conceptual_swap | high | $u_k$ como función de $k$ siempre es convexa | Compare las curvas de $u_k$ respecto a $k$: son convexas cuando $p>1/2$, lineales en $p=1/2$ y cóncavas cuando $p<1/2$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Capital total $N$ fijo y comparación asintótica de $k$ relativo a $N$ con $p \in (0,1)$ | Si $N$ no es grande frente a $k$, desaparece el régimen asintótico $k \ll N$ y la transición cerca de $p=1/2$ es más suave. | - |

---

### [Hab-04] Duración Esperada antes de la Ruina (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 20: Duración Esperada antes de la Ruina
- **Prerequisites:** C-05, Hab-03
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 20)

#### Description & Cognitive Model
Resolución de la ecuación en diferencias no homogénea $m_k = 1 + p m_{k+1} + q m_{k-1}$ con $m_0=m_N=0$ para hallar la duración promedio $m_k$ y su máximo $(N/2)^2$ en el juego justo simétrico.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Signo invertido en factor 1/(q-p) | skipped_step | high | $m_k = \frac{1}{p-q}\left(k - N\frac{1-(q/p)^k}{1-(q/p)^N}\right)$ | Verifique la positividad de $m_k$: cuando $q>p$, $\frac{1-(q/p)^k}{1-(q/p)^N} < k/N$ y el factor debe ser $1/(q-p)$ para que $m_k > 0$. |
| `D-Hab04-02` | Usa fórmula homogénea de ruina | skipped_step | high | $m_k = k(1-u_k)$ para todo $p \neq 1/2$ | Recuerde que la ecuación de $m_k$ es no homogénea con término $+1$, generando la expresión $\frac{1}{q-p}[k - N(1-u_k)]$ cuando $p \neq q$. |
| `D-Hab04-03` | Error de frontera $m_0$ = 1 | conceptual_swap | high | Impone $m_0 = 1$ al despejar $m_1$ | Note que si el jugador inicia en $0$ o en $N$, el juego ya terminó y requiere cero apuestas, por lo que $m_0=0$ y $m_N=0$. |
| `D-Hab04-04` | Omite N multiplicando el cociente | conceptual_swap | high | $m_k = \frac{1}{q-p}\left(k - \frac{1-(q/p)^k}{1-(q/p)^N}\right)$ | Evalúe la condición $m_N=0$: para que el paréntesis se anule en $k=N$, el cociente unitario debe multiplicarse por $N$. |
| `D-Hab04-05` | Confunde máximo con $N^2$/2 | conceptual_swap | high | La duración máxima promedio es $\frac{N^2}{2}$ | Sustituya $k=N/2$ en $m_k = k(N-k)$ cuando $p=1/2$ para obtener $(N/2)(N-N/2) = (N/2)^2 = N^2/4$. |
| `D-Hab04-06` | Trunca suma en $m_1$ a k-2 | conceptual_swap | high | $m_1 = \frac{1}{S_{N-1}}\frac{1}{p}\sum_{i=0}^{k-2} S_i$ | Al imponer $m_N=0$ en la ecuación sumada hasta $N$, el límite superior de la suma que determina $m_1$ es $N-2$ y no $k-2$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Condiciones absorbentes $m_0=m_N=0$, $p \in (0,1)$ y finitud del tiempo esperado de absorción | Si alguno de los estados extremos no fuera absorbente, el juego podría no terminar en tiempo esperado finito. | - |

---
