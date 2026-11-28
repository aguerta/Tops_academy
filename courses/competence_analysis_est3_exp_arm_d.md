# Cognitive Task Analysis (CTA): Estadistica 3 Test K4

- **Course ID:** `estadistica_3_test_k4`
- **Macro-Competency:** Dominio y aplicación analítica integral de Estadistica 3 Test K4
- **Structure:** 23 total competencies (0 Facts, 13 Concepts, 10 Skills) with 102 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Sigma-Álgebra Generada y Minimalidad | Concept | Evaluate | Unidad 3: Sigma-Álgebra Generada y Minimalidad | - | 3 |
| `Hab-01` | Particiones Atómicas y Conteo de Eventos | Skill | Evaluate | Unidad 3: Particiones Atómicas y Conteo de Eventos | C-01 | 6 |
| `C-02` | Álgebra de Borel y Generadores Equivalentes | Concept | Evaluate | Unidad 4: Álgebra de Borel y Generadores Equivalentes | C-01 | 3 |
| `C-03` | Medibilidad por Preimágenes y Lema del Generador | Concept | Evaluate | Unidad 5: Medibilidad por Preimágenes y Lema del Generador | C-01, C-02 | 3 |
| `Hab-02` | Criterio Operativo y Composición Borel-Medible | Skill | Evaluate | Unidad 5: Criterio Operativo y Composición Borel-Medible | C-02, C-03 | 6 |
| `Hab-03` | Constancia sobre Átomos y Procesos Adaptados | Skill | Evaluate | Unidad 6: Constancia sobre Átomos y Procesos Adaptados | Hab-01, C-03 | 6 |
| `C-04` | Esperanza Condicional y Propiedades Algebraicas | Concept | Evaluate | Unidad 2: Esperanza Condicional y Propiedades Algebraicas | C-03 | 4 |
| `Hab-04` | Ley de Adam y Descomposición Iterada | Skill | Evaluate | Unidad 3: Ley de Adam y Descomposición Iterada | C-04 | 6 |
| `C-05` | Proyección Ortogonal y Optimalidad en L2 | Concept | Evaluate | Unidad 4: Proyección Ortogonal y Optimalidad en L2 | Hab-04 | 4 |
| `Hab-05` | Varianza Condicional y Ley de Eve | Skill | Evaluate | Unidad 4: Varianza Condicional y Ley de Eve | Hab-04, C-05 | 6 |
| `Hab-06` | Modelos Jerárquicos Beta-Binomial y Poisson-Binomial | Skill | Evaluate | Unidad 5: Modelos Jerárquicos Beta-Binomial y Poisson-Binomial | Hab-05 | 6 |
| `C-06` | Propiedad Torre, Filtraciones y Martingalas | Concept | Evaluate | Unidad 6: Propiedad Torre, Filtraciones y Martingalas | Hab-04, Hab-03 | 4 |
| `C-07` | Proceso Estocástico, Espacio Parametral y Trayectorias | Concept | Analyze | Unidad 1: Proceso Estocástico, Espacio Parametral y Trayectorias | C-03 | 3 |
| `C-08` | Propiedad de Markov en Tiempo Discreto | Concept | Evaluate | Unidad 4: Propiedad de Markov en Tiempo Discreto | C-07 | 3 |
| `C-09` | Incrementos Independientes, Estacionariedad y Procesos de Lévy | Concept | Evaluate | Unidad 5: Incrementos Independientes, Estacionariedad y Procesos de Lévy | C-07 | 3 |
| `C-10` | Martingalas a Tiempo Discreto | Concept | Evaluate | Unidad 5: Martingalas a Tiempo Discreto | C-07, C-04 | 3 |
| `C-11` | Caminata Aleatoria Simple y Momentos | Concept | Evaluate | Unidad 8: Caminata Aleatoria Simple y Momentos | C-08 | 3 |
| `Hab-07` | Cálculo de Probabilidades de Transición en n Pasos | Skill | Evaluate | Unidad 10: Cálculo de Probabilidades de Transición en n Pasos | C-11 | 6 |
| `C-12` | Recurrencia y Retorno al Origen en Caminatas Aleatorias | Concept | Evaluate | Unidad 12: Recurrencia y Retorno al Origen en Caminatas Aleatorias | C-11, Hab-07 | 3 |
| `Hab-08` | Función Generadora de Primer Retorno al Origen | Skill | Analyze | Unidad 14: Función Generadora de Primer Retorno al Origen | C-12 | 6 |
| `C-13` | Ecuación en Diferencias de la Ruina del Jugador | Concept | Evaluate | Unidad 17: Ecuación en Diferencias de la Ruina del Jugador | C-11 | 3 |
| `Hab-09` | Cálculo de la Probabilidad de Ruina del Jugador | Skill | Evaluate | Unidad 18: Cálculo de la Probabilidad de Ruina del Jugador | C-13 | 6 |
| `Hab-10` | Duración Esperada del Juego hasta la Ruina | Skill | Evaluate | Unidad 20: Duración Esperada del Juego hasta la Ruina | C-13, Hab-09 | 6 |

---

## Detailed Competency Specifications

### [C-01] Sigma-Álgebra Generada y Minimalidad (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Sigma-Álgebra Generada y Minimalidad
- **Prerequisites:** None
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `01_measure_theory_bridge.pdf` (page 3)

#### Description & Cognitive Model
Definición de la menor $\sigma$-álgebra $\sigma(\mathcal{C}) := \bigcap_{\Sigma \supseteq \mathcal{C}} \Sigma$ que contiene a $\mathcal{C}$ como estructura de eventos decidibles e información observable.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Potencia automática | conceptual_swap | high | $\sigma(\mathcal{C}) = \mathcal{P}(\Omega)$ | Recuerde que $\sigma(\mathcal{C})$ es la intersección de todas las $\sigma$-álgebras que contienen a $\mathcal{C}$, por lo que conserva la menor resolución posible. |
| `D-C01-02` | Unión en lugar de intersección | conceptual_swap | high | $\sigma(\mathcal{C}) = \bigcup_{\Sigma \supseteq \mathcal{C}} \Sigma$ | Use la intersección de todas las $\sigma$-álgebras que contienen a $\mathcal{C}$; la unión de $\sigma$-álgebras ni siquiera garantiza cerradura bajo uniones. |
| `D-C01-03` | Confunde cerradura finita | conceptual_swap | high | $\mathcal{C} \cup \mathcal{C}^c$ ya es $\sigma$-álgebra | Verifique los tres axiomas de $\sigma$-álgebra: pertenencia del espacio total, cerradura bajo complementos y cerradura bajo uniones numerables. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | El espacio muestral $\Omega$ es no vacío y $\mathcal{C} \subseteq \mathcal{P}(\Omega)$ | Sin $\mathcal{P}(\Omega)$ como cota superior, la familia de $\sigma$-álgebras que contienen a $\mathcal{C}$ no estaría bien definida. | - |

---

### [Hab-01] Particiones Atómicas y Conteo de Eventos (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Particiones Atómicas y Conteo de Eventos
- **Prerequisites:** C-01
- **Recommended Modalities:** open_symbolic, unstructured_model, adversarial_break
- **Evidence Citations:** `01_measure_theory_bridge.pdf` (page 3)

#### Description & Cognitive Model
Construcción de átomos disjuntos mediante intersecciones booleanas para colecciones finitas y cálculo exacto de cardinalidad $|\sigma(\{A_1,\dots,A_k\})| = 2^k$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Fórmula directa sin partición | skipped_step | high | $|\sigma(\mathcal{C})| = 2^{|\mathcal{C}|}$ | Descomponga primero la colección generadora en átomos no vacíos, disjuntos dos a dos y exhaustivos antes de contar $|\sigma(\mathcal{C})| = 2^k$. |
| `D-Hab01-02` | Incluye átomos vacíos | skipped_step | high | Cuenta $\emptyset$ como átomo adicional en $k$ | Excluya las intersecciones vacías al listar los átomos; solo los bloques no vacíos generan uniones distintas en la $\sigma$-álgebra finita. |
| `D-Hab01-03` | Omite el complemento exterior | conceptual_swap | high | Olvida el bloque $\Omega \setminus \bigcup C_i$ | Incluya siempre el complemento de la unión de generadores si es no vacío, pues la partición atómica debe cubrir todo el espacio muestral $\Omega$. |
| `D-Hab01-04` | Cardinalidad no potencia de dos | conceptual_swap | high | $|\sigma(\mathcal{C})|$ puede ser impar o $3, 5, 6$ | Verifique que toda $\sigma$-álgebra finita está en biyección con $\mathcal{P}(\{1,\dots,k\})$ sobre sus $k$ átomos, por lo que su tamaño siempre es $2^k$. |
| `D-Hab01-05` | Átomos no indivisibles | conceptual_swap | high | Subconjunto propio de un átomo está en $\sigma(\mathcal{C})$ | Recuerde que los átomos son eventos indivisibles: ningún subconjunto propio no vacío de un átomo $A_j$ pertenece a $\sigma(\{A_1,\dots,A_k\})$. |
| `D-Hab01-06` | Suma cardinalidades en vez de exponenciar | conceptual_swap | high | $|\sigma(\{A_1,\dots,A_k\})| = 2k$ | Cuente todos los subconjuntos de índices $J \subseteq \{1,\dots,k\}$ para formar uniones de átomos; existen $2^k$ elecciones posibles y no $2k$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Los bloques $\{A_1,\dots,A_k\}$ son no vacíos, disjuntos y exhaustivos | Si se solapan o no cubren $\Omega$, el conteo $2^k$ sobre $\mathcal{C}$ falla. | - |

---

### [C-02] Álgebra de Borel y Generadores Equivalentes (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Álgebra de Borel y Generadores Equivalentes
- **Prerequisites:** C-01
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `01_measure_theory_bridge.pdf` (page 4)

#### Description & Cognitive Model
Estructura de la $\sigma$-álgebra de Borel $\mathcal{B}(\mathbb{R}) := \sigma(\mathcal{O}_{\mathbb{R}})$, insuficiencia topológica de los abiertos y equivalencia con rayos $\{(-\infty,x]\}$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Abiertos forman sigma-álgebra | conceptual_swap | high | $\mathcal{O}_{\mathbb{R}}$ ya es una $\sigma$-álgebra | Compruebe que el complemento de un abierto no siempre es abierto y la intersección numerable de abiertos puede producir un conjunto cerrado puntual. |
| `D-C02-02` | Borel igual a potencia de R | conceptual_swap | high | $\mathcal{B}(\mathbb{R}) = \mathcal{P}(\mathbb{R})$ | Distinga uniones numerables de no numerables: una $\sigma$-álgebra solo cierra bajo uniones numerables, por lo que $\mathcal{B}(\mathbb{R}) \subsetneq \mathcal{P}(\mathbb{R})$. |
| `D-C02-03` | Rayos insuficientes | conceptual_swap | high | $\sigma(\{(-\infty, x]\}) \subsetneq \mathcal{B}(\mathbb{R})$ | Construya intervalos abiertos $(a,b)$ como unión numerable de $(a, b - 1/n]$ y cada abierto como unión de intervalos con extremos racionales. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | $\mathbb{R}$ está dotado de su topología estándar $\mathcal{O}_{\mathbb{R}}$ | Sin la topología estándar, los intervalos abiertos y rayos no generan los mismos borelianos. | - |

---

### [C-03] Medibilidad por Preimágenes y Lema del Generador (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Medibilidad por Preimágenes y Lema del Generador
- **Prerequisites:** C-01, C-02
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `01_measure_theory_bridge.pdf` (page 5)

#### Description & Cognitive Model
Caracterización de mapas $(\mathcal{F}\text{--}\Sigma_N)$-medibles mediante preimágenes $X^{-1}(B) \in \mathcal{F}$ y reducción al conjunto generador $\mathcal{E}$ por el Lema de Schuller.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Usa imagen directa | conceptual_swap | high | $X$ medible $\Leftrightarrow \forall A \in \mathcal{F}, X(A) \in \Sigma_N$ | Verifique con la preimagen $X^{-1}$: la imagen directa no preserva intersecciones ni complementos cuando $X$ no es inyectiva, mientras $X^{-1}$ conmuta con todo. |
| `D-C03-02` | Dependencia de la probabilidad P | conceptual_swap | high | La medibilidad requiere especificar $\mathbb{P}$ | Separe la estructura medible de la medida: la medibilidad de $X$ solo depende de las $\sigma$-álgebras $\mathcal{F}$ de partida y $\Sigma_N$ de llegada. |
| `D-C03-03` | Verifica solo un generador parcial | conceptual_swap | high | Basta que $X^{-1}(A) \in \mathcal{F}$ para algún $A \in \mathcal{E}$ | Aplique el Lema del Generador sobre toda la familia generadora $\mathcal{E}$ para garantizar que la $\sigma$-álgebra de conjuntos buenos contenga a $\sigma(\mathcal{E})$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | $\Sigma_N = \sigma(\mathcal{E})$ está generada por $\mathcal{E} \subseteq \mathcal{P}(N)$ | Si $\mathcal{E}$ no genera toda $\Sigma_N$, verificar $X^{-1}(A) \in \mathcal{F}$ en $\mathcal{E}$ no garantiza medibilidad. | - |

---

### [Hab-02] Criterio Operativo y Composición Borel-Medible (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Criterio Operativo y Composición Borel-Medible
- **Prerequisites:** C-02, C-03
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, adversarial_break
- **Evidence Citations:** `01_measure_theory_bridge.pdf` (page 5)

#### Description & Cognitive Model
Verificación de $\mathcal{F}$-medibilidad de variables aleatorias reales mediante $\{X \le x\} \in \mathcal{F}$ y preservación bajo composición con funciones continuas $g(X)$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Exige verificar todo boreliano | skipped_step | high | Debe probarse $X^{-1}(B) \in \mathcal{F}$ para todo $B \in \mathcal{B}(\mathbb{R})$ a mano | Reduzca la verificación a los eventos de umbral $\{X \le x\} = X^{-1}((-\infty, x]) \in \mathcal{F}$ para todo $x \in \mathbb{R}$, usando el Lema del Generador. |
| `D-Hab02-02` | Rechaza composición continua | skipped_step | high | $g(X)$ puede no ser $\mathcal{F}$-medible aunque $g$ sea continua | Aplique que toda función continua $g : \mathbb{R} \to \mathbb{R}$ es Borel-medible y la composición de mapas medibles conserva la $\mathcal{F}$-medibilidad. |
| `D-Hab02-03` | Confunde dirección de composición | conceptual_swap | high | $X \circ g$ tiene las mismas preimágenes que $g \circ X$ | Desarrolle la preimagen compuesta paso a paso como $(g \circ X)^{-1}(C) = X^{-1}(g^{-1}(C))$, verificando primero $g^{-1}(C) \in \Sigma_N$. |
| `D-Hab02-04` | Exige diferenciabilidad de g | conceptual_swap | high | $g$ debe ser derivable en todo punto para que $g(X)$ sea medible | Recuerde que basta la continuidad topológica de $g$ para que $g^{-1}(U)$ sea abierto y, por ende, boreliano; no se requiere derivabilidad. |
| `D-Hab02-05` | Restringe x a enteros o positivos | conceptual_swap | high | Basta comprobar $\{X \le x\} \in \mathcal{F}$ solo para $x \ge 0$ | Verifique la pertenencia de $\{X \le x\}$ a $\mathcal{F}$ para todo $x \in \mathbb{R}$, pues los rayos generadores de $\mathcal{B}(\mathbb{R})$ recorren toda la recta real. |
| `D-Hab02-06` | Usa igualdad puntual en lugar de rayo | conceptual_swap | high | $\{X = x\} \in \mathcal{F}\ \forall x$ basta en $\mathbb{R}$ | Note que los singletons no generan $\mathcal{B}(\mathbb{R})$ bajo uniones numerables; utilice los rayos $(-\infty, x]$ o intervalos abiertos como generadores válidos. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | La función $g : \mathbb{R} \to \mathbb{R}$ es continua en la topología estándar | Si $g$ no es continua ni Borel-medible, $g(X)$ podría dejar de ser $\mathcal{F}$-medible. | - |

---

### [Hab-03] Constancia sobre Átomos y Procesos Adaptados (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 6: Constancia sobre Átomos y Procesos Adaptados
- **Prerequisites:** Hab-01, C-03
- **Recommended Modalities:** unstructured_model, open_symbolic, adversarial_break
- **Evidence Citations:** `01_measure_theory_bridge.pdf` (page 6)

#### Description & Cognitive Model
Evaluación de $\mathcal{F}$-medibilidad en espacios finitos mediante constancia de $X$ en cada átomo $A_j$ y verificación de adaptabilidad $\sigma(X_t) \subseteq \mathcal{F}_t$ en filtraciones.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Constancia global en lugar de atómica | skipped_step | high | $X$ debe ser constante en todo $\Omega$ para ser medible | Permita que $X$ tome valores distintos entre átomos diferentes; solo se exige que $X(\omega_1) = X(\omega_2)$ dentro de un mismo átomo $A_j$. |
| `D-Hab03-02` | Ignora variación intra-átomo | skipped_step | high | Si $\sigma(X)$ tiene menos elementos que $\mathcal{F}$, entonces $X$ es medible | Evalúe $X$ en todos los escenarios de cada átomo $A_j$: si existen $\omega_1, \omega_2 \in A_j$ con $X(\omega_1) \neq X(\omega_2)$, entonces $X$ no es $\mathcal{F}$-medible. |
| `D-Hab03-03` | Confunde medibilidad en filtración futura | conceptual_swap | high | $X_{t+1}$ siempre es $\mathcal{F}_t$-medible en una filtración | Verifique en cada instante $t$ que $\sigma(X_t) \subseteq \mathcal{F}_t$; una variable futura $X_{t+1}$ que rompe átomos de $\mathcal{F}_t$ no es $\mathcal{F}_t$-medible. |
| `D-Hab03-04` | Filtración decreciente | conceptual_swap | high | $\mathcal{F}_0 \supseteq \mathcal{F}_1 \supseteq \dots$ es una filtración | Asegure que la información crece con el tiempo ($\mathcal{F}_s \subseteq \mathcal{F}_t$ para $s \le t$), refinando cada átomo al observar nuevos eventos. |
| `D-Hab03-05` | Independencia de la sigma-álgebra | conceptual_swap | high | Si $X$ es $\mathcal{P}(\Omega)$-medible, es $\mathcal{F}$-medible para cualquier $\mathcal{F}$ | Recuerde que la medibilidad depende de la $\sigma$-álgebra de partida $\mathcal{F}$: al reducir la resolución de los átomos, una función puede dejar de ser medible. |
| `D-Hab03-06` | Identifica sigma(X) con F | conceptual_swap | high | Si $X$ es $\mathcal{F}$-medible entonces $\sigma(X) = \mathcal{F}$ | Distinga contención de igualdad: ser $\mathcal{F}$-medible equivale a $\sigma(X) \subseteq \mathcal{F}$, pues una función constante tiene $\sigma(X) = \{\emptyset, \Omega\}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | $\mathcal{F} = \sigma(\{A_1,\dots,A_k\})$ está generada por una partición finita | En espacios infinitos no atómicos la caracterización por átomos finitos no aplica directamente. | - |

---

### [C-04] Esperanza Condicional y Propiedades Algebraicas (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 2: Esperanza Condicional y Propiedades Algebraicas
- **Prerequisites:** C-03
- **Recommended Modalities:** unstructured_model, adversarial_break, multiple_select
- **Evidence Citations:** `02_stat110_lec27_conditional_expectation.pdf` (page 2)

#### Description & Cognitive Model
Definición de $\mathbb{E}[Y \mid X] = g(X)$ como variable aleatoria $\sigma(X)$-medible, linealidad, sacar lo conocido e independencia sin reciprocidad.

#### Fused Distractor Models (4)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Confunde con constante | conceptual_swap | high | $\mathbb{E}[Y \mid X] \in \mathbb{R}$ constante | Distinga que condicionar en un evento produce una constante, pero condicionar en una variable aleatoria $X$ genera una función aleatoria $\sigma(X)$-medible. |
| `D-C04-02` | Recíproco independencia | conceptual_swap | high | $\mathbb{E}[Y \mid X] = \mathbb{E}[Y] \Rightarrow X \perp Y$ | Recuerde que la igualdad de medias condicionales no implica independencia estocástica, pues pueden existir dependencias en momentos pares o en la varianza. |
| `D-C04-03` | Saca variable desconocida | conceptual_swap | high | $\mathbb{E}[h(Y)X \mid X] = h(Y)\mathbb{E}[X \mid X]$ | Aplique la propiedad de sacar lo conocido únicamente a funciones medibles de la variable condicionante $X$, nunca a funciones de la variable aleatoria $Y$. |
| `D-C04-04` | Omite integrabilidad P2 | conceptual_swap | high | $\mathbb{E}[h(X)Y \mid X] = h(X)\mathbb{E}[Y \mid X]$ siempre | Verifique siempre que tanto $Y$ como el producto $h(X)Y$ pertenezcan a $L^1$ antes de extraer $h(X)$ fuera de la esperanza condicional dada $X$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | $Y \in L^1$ ($\mathbb{E}[|Y|] < \infty$) en el espacio $(\Omega, \mathcal{F}, \mathbb{P})$ | Si $\mathbb{E}[|Y|] = \infty$, la esperanza condicional $\mathbb{E}[Y \mid X]$ puede no existir. | - |
| `A-C04-02` | - | Integrabilidad del producto $h(X)Y \in L^1$ para sacar lo conocido | Sin integrabilidad del producto no es válido extraer $h(X)$ de $\mathbb{E}[h(X)Y \mid X]$. | - |

---

### [Hab-04] Ley de Adam y Descomposición Iterada (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Ley de Adam y Descomposición Iterada
- **Prerequisites:** C-04
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, proof_dag
- **Evidence Citations:** `02_stat110_lec27_conditional_expectation.pdf` (page 3)

#### Description & Cognitive Model
Cálculo de esperanzas incondicionales mediante iteración $\mathbb{E}[\mathbb{E}[Y \mid X]] = \mathbb{E}[Y]$ eligiendo una variable auxiliar estratégica.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Invierte orden iterado | skipped_step | high | $\mathbb{E}[\mathbb{E}[Y \mid X]] = \mathbb{E}[X]$ | Recuerde que al promediar $\mathbb{E}[Y \mid X]$ sobre la distribución de $X$ se recupera la esperanza incondicional de $Y$, no la de la variable condicionante. |
| `D-Hab04-02` | Deja X sin promediar | skipped_step | high | $\mathbb{E}[\mathbb{E}[Y \mid X]] = g(X)$ | Aplique el operador de esperanza exterior completo sobre $g(X)$ mediante LOTUS para obtener un escalar determinista igual a $\mathbb{E}[Y]$. |
| `D-Hab04-03` | Confunde con evento | conceptual_swap | high | $\mathbb{E}[\mathbb{E}[Y \mid X]] = \mathbb{E}[Y \mid X=x]$ | Pondere cada valor condicional $g(x)$ por la probabilidad o densidad marginal de $X$ antes de sumar o integrar sobre todo el soporte de $X$. |
| `D-Hab04-04` | Exige segundo momento | conceptual_swap | high | Requiere $Y \in L^2$ para la Ley de Adam | Distinga los supuestos: la Ley de Adam solo requiere integrabilidad absoluta $Y \in L^1$ para intercambiar sumas o integrales por Fubini, no $Y \in L^2$. |
| `D-Hab04-05` | Omite factor marginal | conceptual_swap | high | $\sum_x \sum_y y\mathbb{P}(Y=y \mid X=x)$ | Multiplique cada esperanza condicional $\mathbb{E}[Y \mid X=x]$ por la probabilidad marginal $\mathbb{P}(X=x)$ para reconstruir la distribución conjunta. |
| `D-Hab04-06` | Aplica regla producto mal | conceptual_swap | high | $\mathbb{P}(Y=y \mid X=x)\mathbb{P}(Y=y)$ | Use la regla del producto correcta $\mathbb{P}(Y=y \mid X=x)\mathbb{P}(X=x) = \mathbb{P}(X=x, Y=y)$ antes de intercambiar el orden de sumación. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | $Y \in L^1$ ($\mathbb{E}[|Y|] < \infty$) para convergencia absoluta | Sin $Y \in L^1$ falla el intercambio de sumas o el Teorema de Fubini en la demostración. | - |

---

### [C-05] Proyección Ortogonal y Optimalidad en L2 (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Proyección Ortogonal y Optimalidad en L2
- **Prerequisites:** Hab-04
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `02_stat110_lec27_conditional_expectation.pdf` (page 4)

#### Description & Cognitive Model
Interpretación geométrica de $\mathbb{E}[Y \mid X]$ como proyección ortogonal en $L^2$ que minimiza el error cuadrático medio $\mathbb{E}[(Y - h(X))^2]$.

#### Fused Distractor Models (4)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Restringe a lineal | conceptual_swap | high | Solo minimiza MSE entre $h(X) = aX + b$ | Distinga que la esperanza condicional minimiza el error cuadrático medio sobre todas las funciones medibles $h(X) \in L^2$, lineales o no lineales. |
| `D-C05-02` | Signo término cruzado | conceptual_swap | high | $\mathbb{E}[(Y-\hat{Y})(\hat{Y}-h(X))] \neq 0$ | Aplique la ortogonalidad del residuo $Y - \mathbb{E}[Y \mid X]$ frente a toda función $\tilde{h}(X) = \mathbb{E}[Y \mid X] - h(X)$ para anular el producto cruzado. |
| `D-C05-03` | Aplica L2 a Cauchy | conceptual_swap | high | Usa proyección $L^2$ cuando $\mathbb{E}[Y^2] = \infty$ | Verifique que $Y$ y $h(X)$ pertenezcan a $L^2$, pues si el producto interno $\mathbb{E}[Y^2]$ diverge la geometría de proyección ortogonal deja de aplicarse. |
| `D-C05-04` | Correlación residual | conceptual_swap | high | $\operatorname{Cov}(Y - \mathbb{E}[Y \mid X], h(X)) \neq 0$ | Como el residuo $Y - \mathbb{E}[Y \mid X]$ tiene media cero por la Ley de Adam y es ortogonal a $h(X)$, su covarianza con cualquier $h(X) \in L^2$ es cero. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | $Y \in L^2$ y $h(X) \in L^2$ ($\mathbb{E}[Y^2] < \infty$, $\mathbb{E}[h(X)^2] < \infty$) | Si $\mathbb{E}[Y^2] = \infty$, la distancia MSE y el producto interno en $L^2$ divergen. | - |

---

### [Hab-05] Varianza Condicional y Ley de Eve (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Varianza Condicional y Ley de Eve
- **Prerequisites:** Hab-04, C-05
- **Recommended Modalities:** open_symbolic, proof_dag, adversarial_break
- **Evidence Citations:** `02_stat110_lec27_conditional_expectation.pdf` (page 4)

#### Description & Cognitive Model
Definición y cálculo de $\operatorname{Var}(Y \mid X) = \mathbb{E}[Y^2 \mid X] - (\mathbb{E}[Y \mid X])^2$ y descomposición EVVE $\operatorname{Var}(Y) = \mathbb{E}[\operatorname{Var}(Y \mid X)] + \operatorname{Var}(\mathbb{E}[Y \mid X])$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Omite barra exterior | skipped_step | high | $\operatorname{Var}(Y \mid X) = \mathbb{E}[(Y - \mathbb{E}[Y \mid X])^2]$ | Incluya siempre el condicionamiento exterior $\mid X$ en la varianza condicional para obtener una variable aleatoria $\sigma(X)$-medible y no su promedio escalar. |
| `D-Hab05-02` | Solo toma esperanza Var | skipped_step | high | $\operatorname{Var}(Y) = \mathbb{E}[\operatorname{Var}(Y \mid X)]$ | Sume la variabilidad entre grupos $\operatorname{Var}(\mathbb{E}[Y \mid X])$ a la variabilidad intra-grupo $\mathbb{E}[\operatorname{Var}(Y \mid X)]$ según la fórmula EVVE. |
| `D-Hab05-03` | Invierte operadores EVVE | conceptual_swap | high | $\operatorname{Var}(Y) = \operatorname{Var}(\operatorname{Var}(Y \mid X)) + \mathbb{E}[\mathbb{E}[Y \mid X]]$ | Use la mnemotecnia EVVE ($\mathbb{E}[\operatorname{Var}] + \operatorname{Var}[\mathbb{E}]$) para asegurar que ambos sumandos tengan unidades cuadráticas homogéneas. |
| `D-Hab05-04` | Resta media en lugar cuadrado | conceptual_swap | high | $\operatorname{Var}(Y \mid X) = \mathbb{E}[Y^2 \mid X] - \mathbb{E}[Y \mid X]$ | Eleve al cuadrado la esperanza condicional $\mathbb{E}[Y \mid X]$ al restarla de $\mathbb{E}[Y^2 \mid X]$ tras expandir $(Y - \mathbb{E}[Y \mid X])^2$ y sacar lo conocido. |
| `D-Hab05-05` | Confunde E[Var] con Var(Y) | conceptual_swap | high | $\mathbb{E}[(Y - \mathbb{E}[Y \mid X])^2] = \operatorname{Var}(Y)$ | Recuerde que $\mathbb{E}[(Y - \mathbb{E}[Y \mid X])^2] = \mathbb{E}[\operatorname{Var}(Y \mid X)]$ representa solo la variabilidad intra-grupo, menor o igual que $\operatorname{Var}(Y)$. |
| `D-Hab05-06` | Omite L2 en EVVE | conceptual_swap | high | Aplica EVVE con $\mathbb{E}[Y^2] = \infty$ | Exija segundo momento finito $Y \in L^2$ antes de aplicar la Ley de Eve, pues si $\mathbb{E}[Y^2] = \infty$ los términos cuadráticos de la identidad divergen. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | $Y \in L^2$ ($\mathbb{E}[Y^2] < \infty$) para existencia de varianzas | Si $\mathbb{E}[Y^2] = \infty$, ni $\operatorname{Var}(Y)$ ni la Ley de Eve están bien definidas. | - |

---

### [Hab-06] Modelos Jerárquicos Beta-Binomial y Poisson-Binomial (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Modelos Jerárquicos Beta-Binomial y Poisson-Binomial
- **Prerequisites:** Hab-05
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `02_stat110_lec27_conditional_expectation.pdf` (page 5)

#### Description & Cognitive Model
Resolución de momentos incondicionales en modelos jerárquicos Beta-Binomial y adelgazamiento Poisson-Binomial mediante las leyes de Adam y Eve.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Olvida n al cuadrado | skipped_step | high | $\operatorname{Var}(nQ) = n\operatorname{Var}(Q)$ | Extraiga las constantes multiplicativas elevadas al cuadrado al calcular $\operatorname{Var}(\mathbb{E}[X \mid Q]) = \operatorname{Var}(nQ) = n^2\operatorname{Var}(Q)$. |
| `D-Hab06-02` | Confunde E[Q(1-Q)] | skipped_step | high | $\mathbb{E}[Q(1-Q)] = \mathbb{E}[Q](1-\mathbb{E}[Q])$ | Calcule $\mathbb{E}[Q(1-Q)]$ integrando contra la densidad Beta o usando $\mathbb{E}[Q] - \mathbb{E}[Q^2]$, ya que $\mathbb{E}[Q^2] \neq (\mathbb{E}[Q])^2$ cuando $\operatorname{Var}(Q) > 0$. |
| `D-Hab06-03` | Omite Var(N) en adelgazamiento | conceptual_swap | high | $\operatorname{Var}(X) = \mathbb{E}[Np(1-p)]$ | Sume el término $\operatorname{Var}(\mathbb{E}[X \mid N]) = \operatorname{Var}(Np) = p^2\lambda$ al término $\lambda p(1-p)$ para recuperar $\operatorname{Var}(X) = \lambda p$. |
| `D-Hab06-04` | Fija Q como constante | conceptual_swap | high | $\operatorname{Var}(X) = n\mu(1-\mu)$ | Reconozca que la sobredispersión Beta-Binomial añade el término $n^2\operatorname{Var}(Q)$ sobre el promedio binomial, reflejando la incertidumbre en $Q$. |
| `D-Hab06-05` | Error identidad Gamma | conceptual_swap | high | $\Gamma(a+b+2) = (a+b)\Gamma(a+b)$ | Aplique recursivamente $\Gamma(z+1) = z\Gamma(z)$ dos veces para obtener $\Gamma(a+b+2) = (a+b+1)(a+b)\Gamma(a+b)$ antes de cancelar. |
| `D-Hab06-06` | Saca p sin cuadrado | conceptual_swap | high | $\operatorname{Var}(Np) = p\operatorname{Var}(N)$ | Aplique la propiedad cuadrática $\operatorname{Var}(pN) = p^2\operatorname{Var}(N) = p^2\lambda$ para que al sumar $\lambda p(1-p)$ se cancelen los términos en $p^2$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Parámetros positivos $a,b > 0$, $\lambda > 0$ y $p \in (0,1)$ | Fuera de estos rangos las distribuciones Beta, Binomial o Poisson no están bien definidas. | - |

---

### [C-06] Propiedad Torre, Filtraciones y Martingalas (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 6: Propiedad Torre, Filtraciones y Martingalas
- **Prerequisites:** Hab-04, Hab-03
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `02_stat110_lec27_conditional_expectation.pdf` (page 6)

#### Description & Cognitive Model
Extensión a $\sigma$-álgebras finitas mediante promedios por átomo, Propiedad Torre $\mathbb{E}[\mathbb{E}[Y \mid \mathcal{F}_t] \mid \mathcal{F}_s] = \mathbb{E}[Y \mid \mathcal{F}_s]$ y martingalas.

#### Fused Distractor Models (4)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Domina sigma grande | conceptual_swap | high | $\mathbb{E}[\mathbb{E}[Y \mid \mathcal{F}_t] \mid \mathcal{F}_s] = \mathbb{E}[Y \mid \mathcal{F}_t]$ | Recuerde que en la Propiedad Torre domina siempre la $\sigma$-álgebra más pequeña $\mathcal{F}_s \subseteq \mathcal{F}_t$, porque contiene menos información. |
| `D-C06-02` | Variable no constante en átomo | conceptual_swap | high | $\mathbb{E}[Y \mid \mathcal{F}](\omega)$ varía dentro de $A_j$ | Verifique que una variable $\mathcal{F}$-medible debe ser constante en cada átomo $A_j$ de la partición que genera a $\mathcal{F}$, tomando allí el promedio $\mathbb{E}[Y \mid A_j]$. |
| `D-C06-03` | Olvida adaptabilidad martingala | conceptual_swap | high | Basta $\mathbb{E}[X_n] = \mathbb{E}[X_0]$ para ser martingala | Exija las tres condiciones de martingala respecto a $\{\mathcal{F}_n\}$: adaptabilidad a $\mathcal{F}_n$, integrabilidad $X_n \in L^1$ y $\mathbb{E}[X_{n+1} \mid \mathcal{F}_n] = X_n$. |
| `D-C06-04` | Invierte inclusión filtración | conceptual_swap | high | Aplica Torre con $\mathcal{F}_t \subseteq \mathcal{F}_s$ dando $\mathcal{F}_s$ | Compruebe la dirección de la filtración antes de reducir la esperanza iterada: cualquiera sea el orden de condicionamiento, prevalece la $\sigma$-álgebra menos fina. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Filtración $\mathcal{F}_s \subseteq \mathcal{F}_t$, $Y \in L^1$ y átomos con $\mathbb{P}(A_j) > 0$ | Sin $Y \in L^1$ o sin átomos de probabilidad positiva no existen los promedios condicionales. | - |

---

### [C-07] Proceso Estocástico, Espacio Parametral y Trayectorias (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 1: Proceso Estocástico, Espacio Parametral y Trayectorias
- **Prerequisites:** C-03
- **Recommended Modalities:** concept_matching, multiple_select, adversarial_break
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 1)

#### Description & Cognitive Model
Caracterización de un proceso estocástico $\{X_t:t\in T\}$ sobre $(\Omega,\mathscr{F},P)$ como función $X:T\times\Omega\to S$, distinguiendo variable aleatoria $\omega\mapsto X_t(\omega)$ de trayectoria $t\mapsto X_t(\omega)$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Confunde trayectoria con variable | conceptual_swap | high | Fijar $t$ define una trayectoria determinista | Distinga las secciones de $X(t,\omega)$: fijar $t$ da la variable aleatoria $\omega\mapsto X_t(\omega)$, mientras que fijar $\omega$ genera la trayectoria temporal. |
| `D-C07-02` | Intercambia T y S | conceptual_swap | high | El índice $t$ pertenece al espacio de estados $S$ | Identifique el espacio parametral $T$ como conjunto de índices temporales y el espacio de estados $S$ como el conjunto donde las variables $X_t$ toman valores. |
| `D-C07-03` | Asume independencia global | conceptual_swap | high | Las variables $\{X_t:t\in T\}$ son siempre independientes | Recuerde que las variables aleatorias de un proceso estocástico presentan en general estructuras de dependencia temporal y no son necesariamente independientes. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Espacio de estados $S$ dotado de $\sigma$-álgebra $S\cap\mathscr{B}(\mathbb{R})$ | Sin una $\sigma$-álgebra en $S$, el mapeo $\omega\mapsto X_t(\omega)$ no es medible como variable aleatoria. | - |

---

### [C-08] Propiedad de Markov en Tiempo Discreto (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Propiedad de Markov en Tiempo Discreto
- **Prerequisites:** C-07
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 4)

#### Description & Cognitive Model
Condición de independencia condicional del futuro respecto al pasado dado el presente: $P(X_{n+1}=x_{n+1}\mid X_0=x_0,\dots,X_n=x_n)=P(X_{n+1}=x_{n+1}\mid X_n=x_n)$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Confunde con independencia | conceptual_swap | high | $P(X_{n+1}=x_{n+1}\mid X_n=x_n)=P(X_{n+1}=x_{n+1})$ | Conserve el estado presente $X_n=x_n$ en el condicionamiento: la propiedad de Markov descarta la historia pasada $X_0,\dots,X_{n-1}$, pero mantiene la dependencia en $X_n$. |
| `D-C08-02` | Retiene estado inicial | conceptual_swap | high | Depende de $(X_0=x_0, X_n=x_n)$ | Aplique la pérdida de memoria completa sobre toda la trayectoria previa hasta $n-1$, de modo que solo el último estado observado $X_n=x_n$ resume la información relevante. |
| `D-C08-03` | Asume igualdad de trayectorias | conceptual_swap | high | $X_{n+1}=X_n$ casi seguramente | Distinga la igualdad de probabilidades condicionales de transición de una igualdad entre variables aleatorias: el proceso puede cambiar de estado aleatoriamente. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C08-01` | - | Evento condicionante pasado-presente con probabilidad positiva | Si $P(X_0=x_0,\dots,X_n=x_n)=0$, la probabilidad condicional clásica no está definida. | - |

---

### [C-09] Incrementos Independientes, Estacionariedad y Procesos de Lévy (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Incrementos Independientes, Estacionariedad y Procesos de Lévy
- **Prerequisites:** C-07
- **Recommended Modalities:** multiple_select, adversarial_break, concept_matching
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 5)

#### Description & Cognitive Model
Propiedades de incrementos independientes sobre intervalos disjuntos, estacionariedad estricta y de incrementos $X_{t+h}-X_{s+h}\stackrel{d}{=}X_t-X_s$, que definen un proceso de Lévy a tiempo continuo.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Confunde estacionariedad con incrementos | conceptual_swap | high | Todo proceso estacionario tiene incrementos independientes | Separe ambos conceptos: la estacionariedad exige invarianza distribucional ante desplazamientos $h>0$, mientras que los incrementos independientes exigen independencia en intervalos disjuntos. |
| `D-C09-02` | Confunde igualdad en distribución | conceptual_swap | high | $X_{t+h}-X_{s+h}=X_t-X_s$ punto a punto | Verifique que la estacionariedad de incrementos establece igualdad en distribución de probabilidad y no igualdad trayectoria por trayectoria. |
| `D-C09-03` | Omite condición en Lévy | conceptual_swap | high | Proceso de Lévy solo requiere incrementos independientes | Incluya ambas condiciones conjuntas para caracterizar un proceso de Lévy a tiempo continuo: incrementos independientes e incrementos estacionarios. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | Espacio parametral continuo $T=[0,\infty)$ y partición ordenada $0\le t_1<\dots<t_n$ | Sin orden estricto de tiempos, los intervalos se traslapan y los incrementos pierden independencia. | - |

---

### [C-10] Martingalas a Tiempo Discreto (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Martingalas a Tiempo Discreto
- **Prerequisites:** C-07, C-04
- **Recommended Modalities:** adversarial_break, multiple_select, proof_dag
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 5)

#### Description & Cognitive Model
Proceso $\{X_n:n=0,1,\dots\}$ que modela un juego justo mediante la esperanza condicional $E(X_{n+1}\mid X_0=x_0,\dots,X_n=x_n)=x_n$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C10-01` | Confunde con media constante | conceptual_swap | high | $E(X_{n+1})=E(X_n)$ implica propiedad de martingala | Exija la condición más fuerte sobre toda la historia observada: la esperanza condicional dado $(X_0,\dots,X_n)$ debe coincidir con $X_n$, no basta igualar medias marginales. |
| `D-C10-02` | Iguala con Markov | conceptual_swap | high | Toda cadena de Markov es una martingala | Distinguir ambas propiedades: Markov elimina dependencia del pasado en la distribución condicional, mientras que la martingala fija el valor esperado condicional en el estado presente. |
| `D-C10-03` | Descarta historia previa | conceptual_swap | high | $E(X_{n+1}\mid X_n=x_n)=x_n$ basta sin condicionar en $X_0,\dots,X_{n-1}$ | Incluya toda la historia pasada $(X_0,\dots,X_n)$ en el condicionamiento de la esperanza futura para verificar la definición general de martingala. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C10-01` | - | Integrabilidad de $X_n$ para todo $n\ge 0$ | Si $E(|X_n|)=\infty$, la esperanza condicional puede no estar definida. | - |

---

### [C-11] Caminata Aleatoria Simple y Momentos (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 8: Caminata Aleatoria Simple y Momentos
- **Prerequisites:** C-08
- **Recommended Modalities:** unstructured_model, adversarial_break, multiple_select
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 8)

#### Description & Cognitive Model
Caminata aleatoria simple sobre $\mathbb{Z}$ definida por $X_n=X_0+\sum_{i=1}^n\xi_i$ con $\xi_i$ i.i.d. ($P(\xi=1)=p$, $P(\xi=-1)=q=1-p$), cuya esperanza es $E(X_n)=n(p-q)$ y varianza $\mathrm{Var}(X_n)=4npq$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C11-01` | Varianza sin factor 4 | conceptual_swap | high | $\mathrm{Var}(X_n)=npq$ | Calcule $\mathrm{Var}(\xi)=E(\xi^2)-(E(\xi))^2=1-(p-q)^2=4pq$ antes de sumar $n$ variables independientes, pues cada paso toma valores $\pm 1$ de amplitud $2$. |
| `D-C11-02` | Media sin signo q | conceptual_swap | high | $E(X_n)=np$ | Sume ambos resultados posibles del paso $\xi\in\{+1,-1\}$ ponderados por sus probabilidades para obtener $E(\xi)=p-q$ y $E(X_n)=n(p-q)$. |
| `D-C11-03` | Confunde máximo de varianza | conceptual_swap | high | La varianza es máxima cuando $p\to 1$ | Analice $4np(1-p)$ como función cuadrática en $p\in(0,1)$: su máximo ocurre en la caminata simétrica $p=q=1/2$, donde $\mathrm{Var}(X_n)=n$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C11-01` | - | Pasos $\xi_1,\xi_2,\dots$ independientes e idénticamente distribuidos con $p+q=1$ | Si los pasos están correlacionados, la varianza ya no es la suma $n\,\mathrm{Var}(\xi)$. | - |

---

### [Hab-07] Cálculo de Probabilidades de Transición en n Pasos (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 10: Cálculo de Probabilidades de Transición en n Pasos
- **Prerequisites:** C-11
- **Recommended Modalities:** fill_in_the_blank, open_symbolic, unstructured_model
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 10)

#### Description & Cognitive Model
Determinación de $P(X_n=x\mid X_0=y)=\binom{n}{\frac{1}{2}(n+x-y)}p^{\frac{1}{2}(n+x-y)}q^{\frac{1}{2}(n-x+y)}$ cuando $-n\le x-y\le n$ y $n, x-y$ comparten paridad.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Ignora restricción de paridad | skipped_step | high | Aplica la fórmula binomial aunque $n$ y $x-y$ tengan distinta paridad | Verifique primero que $|x-y|\le n$ y que $n$ y $x-y$ sean ambos pares o ambos impares; en cualquier otro caso la probabilidad de transición es exactamente cero. |
| `D-Hab07-02` | Usa x en lugar de x-y | skipped_step | high | Sustituye $\frac{1}{2}(n+x)$ cuando $X_0=y\neq 0$ | Traslade el proceso mediante $Z_n=X_n-y$ para usar el desplazamiento neto $x-y$ en lugar de la posición absoluta $x$ cuando $X_0=y$. |
| `D-Hab07-03` | Olvida coeficiente binomial | conceptual_swap | high | $P(X_n=x\mid X_0=y)=p^{\frac{1}{2}(n+x-y)}q^{\frac{1}{2}(n-x+y)}$ | Multiplique la probabilidad de una trayectoria específica por $\binom{n}{\frac{1}{2}(n+x-y)}$, que cuenta todas las formas de elegir los pasos a la derecha. |
| `D-Hab07-04` | Intercambia exponentes p y q | conceptual_swap | high | Asigna potencia $\frac{1}{2}(n-x+y)$ a $p$ | Recuerde que $R_n=\frac{1}{2}(n+X_n-y)$ cuenta los pasos positivos con probabilidad $p$, mientras que $L_n=\frac{1}{2}(n-X_n+y)$ cuenta los pasos negativos con probabilidad $q$. |
| `D-Hab07-05` | Omite factor 1/2 en exponente | conceptual_swap | high | Usa $n+x-y$ directamente como número de éxitos | Sume ambas ecuaciones lineales $R_n+L_n=n$ y $R_n-L_n=x-y$ y divida entre $2$ para obtener el número entero de pasos a la derecha $R_n$. |
| `D-Hab07-06` | Asume soporte fuera de [-n,n] | conceptual_swap | high | Evalúa probabilidad positiva para $|x-y|>n$ | Acote el desplazamiento máximo en $n$ pasos unitarios a $|x-y|\le n$; ningún estado fuera de ese intervalo puede alcanzarse en $n$ transiciones. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Igualdad de paridad entre $n$ y $x-y$ con $-n\le x-y\le n$ | Si $n$ y $x-y$ tienen distinta paridad, $\frac{1}{2}(n+x-y)$ no es entero y la probabilidad es $0$. | - |

---

### [C-12] Recurrencia y Retorno al Origen en Caminatas Aleatorias (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 12: Recurrencia y Retorno al Origen en Caminatas Aleatorias
- **Prerequisites:** C-11, Hab-07
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 12)

#### Description & Cognitive Model
Análisis de la probabilidad de eventual regreso al origen $1-|p-q|$ en caminatas simples sobre $\mathbb{Z}$, estableciendo certeza de retorno si $p=q=1/2$ con tiempo promedio infinito y retorno no seguro si $p\neq q$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C12-01` | Tiempo promedio finito | conceptual_swap | high | Si $p=q=1/2$, el tiempo promedio de regreso es finito | Distinga recurrencia segura de tiempo esperado finito: aunque la probabilidad total de retorno sea unitaria cuando $p=1/2$, la derivada $\lim_{t\nearrow 1}G'(t)=\infty$ muestra que el tiempo promedio de regreso es infinito. |
| `D-C12-02` | Certeza en caso asimétrico | conceptual_swap | high | La caminata regresa con probabilidad $1$ para todo $p\in(0,1)$ | Evalúe $1-|p-q|$: cuando $p\neq 1/2$, la deriva no nula hace $|p-q|>0$ y la probabilidad de retorno eventual al origen es estrictamente menor que $1$. |
| `D-C12-03` | Confunde pn con fk | conceptual_swap | high | La probabilidad de regreso eventual es $\sum_{n=0}^\infty p_n$ | Sume las probabilidades de primer retorno $f_k$ (eventos disjuntos), nunca $p_n$, pues $p_n$ incluye múltiples visitas previas al origen y su serie puede divergir. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C12-01` | - | Caminata aleatoria simple en $\mathbb{Z}$ sin estados absorbentes ni fronteras | En caminatas con barreras absorbentes el proceso puede quedar atrapado sin regresar jamás al origen. | - |

---

### [Hab-08] Función Generadora de Primer Retorno al Origen (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 14: Función Generadora de Primer Retorno al Origen
- **Prerequisites:** C-12
- **Recommended Modalities:** open_symbolic, proof_dag, fill_in_the_blank
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 14)

#### Description & Cognitive Model
Derivación de la función generadora $G(t)=\sum_{k=0}^\infty f_k t^k=1-(1-4pqt^2)^{1/2}$ a partir de la descomposición $p_n=\sum_{k=0}^n f_k p_{n-k}$ y la identidad $\sum_{n=0}^\infty p_n t^n=(1-4pqt^2)^{-1/2}$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | Olvida término p0=1 | skipped_step | high | $\sum_{n=0}^\infty p_n t^n=G(t)\sum_{n=0}^\infty p_n t^n$ | Separe el término $n=0$ ($p_0=1$) en la suma $\sum_{n=1}^\infty p_n t^n=(\sum_{n=0}^\infty p_n t^n)-1$ antes de despejar $G(t)$. |
| `D-Hab08-02` | Signo erróneo en raíz | skipped_step | high | $G(t)=1+(1-4pqt^2)^{1/2}$ | Despeje $G(t)=1-\frac{1}{\sum_{n=0}^\infty p_n t^n}$ usando $(1-4pqt^2)^{-1/2}$ en el denominador, lo que produce el signo negativo en $1-(1-4pqt^2)^{1/2}$. |
| `D-Hab08-03` | Omite paridad de pn | conceptual_swap | high | Escribe $\sum_{n=0}^\infty p_n t^n=\sum_{n=0}^\infty \binom{2n}{n}p^n q^n t^n$ | Recuerde que $p_n$ solo es no nulo en tiempos pares $2n$, por lo que cada término aporta potencia $t^{2n}$ y genera el argumento $4pqt^2$. |
| `D-Hab08-04` | Factor 4 incorrecto | conceptual_swap | high | $G(t)=1-(1-pqt^2)^{1/2}$ | Conserve el factor $4^n$ de la identidad $\binom{2n}{n}=(-4)^n\binom{-1/2}{n}$ al agrupar $(-4pqt^2)^n$ dentro de la expansión binomial $(1+u)^{-1/2}$. |
| `D-Hab08-05` | Exponente negativo en G(t) | conceptual_swap | high | $G(t)=1-(1-4pqt^2)^{-1/2}$ | Divida la ecuación $((1-4pqt^2)^{-1/2}-1)=G(t)(1-4pqt^2)^{-1/2}$ entre $(1-4pqt^2)^{-1/2}$ para cambiar el exponente a $+1/2$. |
| `D-Hab08-06` | Evalúa Lema de Abel en t=0 | conceptual_swap | high | Calcula $\sum f_n=G(0)$ | Tome el límite radial $\lim_{t\nearrow 1}G(t)$ mediante el lema de Abel para sumar todos los coeficientes $\sum_{n=0}^\infty f_n$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab08-01` | - | Radio de convergencia $|4pqt^2|<1$ para $|t|<1$ | Para $|t|\ge 1$ cuando $p=q=1/2$, la serie binomial $(1-t^2)^{-1/2}$ diverge. | - |

---

### [C-13] Ecuación en Diferencias de la Ruina del Jugador (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 17: Ecuación en Diferencias de la Ruina del Jugador
- **Prerequisites:** C-11
- **Recommended Modalities:** unstructured_model, adversarial_break, multiple_select
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 17)

#### Description & Cognitive Model
Formulación del problema de la ruina del jugador sobre $\{0,1,\dots,N\}$ con estados absorbentes $0$ y $N$, mediante la ecuación en diferencias homogénea $u_k=pu_{k+1}+qu_{k-1}$ y condiciones de frontera $u_0=1, u_N=0$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C13-01` | Invierte condiciones de frontera | conceptual_swap | high | $u_0=0$ y $u_N=1$ | Verifique la definición de $u_k=P(X_\tau=0\mid X_0=k)$: si inicia sin capital ($k=0$) la ruina es segura ($u_0=1$), y si alcanza el total $N$ gana el juego ($u_N=0$). |
| `D-C13-02` | Invierte índices con p y q | conceptual_swap | high | $u_k=qu_{k+1}+pu_{k-1}$ | Condicione sobre la primera apuesta: el jugador sube a $k+1$ si gana (probabilidad $p$) y baja a $k-1$ si pierde (probabilidad $q$). |
| `D-C13-03` | Agrega término constante +1 | conceptual_swap | high | $u_k=1+pu_{k+1}+qu_{k-1}$ | Distinga probabilidades de eventos ($u_k$ homogénea) de tiempos esperados ($m_k$ no homogénea con $+1$ por el paso transcurrido). |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C13-01` | - | Estados $0$ y $N$ absorbentes y tiempo de paro $\tau$ finito casi seguramente | Sin absorción en $0$ y $N$, la caminata no termina y las condiciones de frontera pierden sentido. | - |

---

### [Hab-09] Cálculo de la Probabilidad de Ruina del Jugador (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 18: Cálculo de la Probabilidad de Ruina del Jugador
- **Prerequisites:** C-13
- **Recommended Modalities:** fill_in_the_blank, open_symbolic, unstructured_model
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 18)

#### Description & Cognitive Model
Resolución de la ecuación de ruina $u_k=pu_{k+1}+qu_{k-1}$ para obtener $u_k=\frac{N-k}{N}$ si $p=\frac{1}{2}$ y $u_k=\frac{(q/p)^k-(q/p)^N}{1-(q/p)^N}$ si $p\neq\frac{1}{2}$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab09-01` | Usa fórmula asimétrica en p=1/2 | skipped_step | high | Evalúa $\frac{1-1}{1-1}$ directamente cuando $p=1/2$ | Aplique la rama simétrica $u_k=(N-k)/N$ cuando $p=1/2$, pues la suma parcial $S_k=\sum_{j=0}^k (q/p)^j$ vale $k+1$ y no la fórmula geométrica. |
| `D-Hab09-02` | Invierte razón p/q | skipped_step | high | Usa $(p/q)^k$ en lugar de $(q/p)^k$ en la fórmula de $u_k$ | Verifique que $u_{k+1}-u_k=(q/p)(u_k-u_{k-1})$ genera potencias de $q/p$; si $p>q$, $q/p<1$ y la probabilidad de ruina decrece más rápido. |
| `D-Hab09-03` | Confunde ruina con victoria | conceptual_swap | high | $u_k=\frac{k}{N}$ para $p=1/2$ | Recuerde que $u_k$ decrece con el capital inicial $k$: a mayor $k$, menor probabilidad de ruina, cumpliendo $u_0=1$ y $u_N=0$ mediante $(N-k)/N$. |
| `D-Hab09-04` | Omite término (q/p)^N en numerador | conceptual_swap | high | $u_k=\frac{1-(q/p)^k}{1-(q/p)^N}$ | Calcule $1-\frac{S_{k-1}}{S_{N-1}}$ con $S_{k-1}=\frac{1-(q/p)^k}{1-q/p}$, lo cual produce $\frac{(q/p)^k-(q/p)^N}{1-(q/p)^N}$ y satisface ambas fronteras. |
| `D-Hab09-05` | Índice desplazado en S | conceptual_swap | high | Sustituye $S_k/S_N$ en lugar de $S_{k-1}/S_{N-1}$ | Cuente los términos sumados desde $u_2-u_1$ hasta $u_k-u_{k-1}$: son $k-1$ diferencias que suman $S_{k-1}-1$, generando el índice $k-1$. |
| `D-Hab09-06` | Asume insensibilidad cerca de 1/2 | conceptual_swap | high | Supone que $u_k$ varía linealmente con $p$ cerca de $1/2$ | Observe que para $N$ grande la función $u_k(p)$ presenta una transición muy pronunciada en torno a $p=1/2$, pasando rápidamente de casi $1$ a casi $0$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab09-01` | - | Capital inicial $k\in\{0,1,\dots,N\}$ y probabilidades $p,q>0$ con $p+q=1$ | Si $p=0$ o $q=0$, la razón $q/p$ o su inverso queda indefinida y la ruina o victoria es determinista. | - |

---

### [Hab-10] Duración Esperada del Juego hasta la Ruina (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 20: Duración Esperada del Juego hasta la Ruina
- **Prerequisites:** C-13, Hab-09
- **Recommended Modalities:** unstructured_model, open_symbolic, fill_in_the_blank
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 20)

#### Description & Cognitive Model
Cálculo del número esperado de apuestas hasta la absorción $m_k$ resolviendo $m_k=1+pm_{k+1}+qm_{k-1}$ con $m_0=m_N=0$: $m_k=k(N-k)$ si $p=q$ y $m_k=\frac{1}{q-p}\left(k-N\frac{1-(q/p)^k}{1-(q/p)^N}\right)$ si $p\neq q$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab10-01` | Omite +1 en ecuación | skipped_step | high | $m_k=pm_{k+1}+qm_{k-1}$ | Sume $1$ por la apuesta que debe realizarse en el paso actual antes de pasar a $k+1$ o $k-1$ al condicionar la esperanza del tiempo restante. |
| `D-Hab10-02` | Signo invertido en q-p | skipped_step | high | $m_k=\frac{1}{p-q}\left(k-N\frac{1-(q/p)^k}{1-(q/p)^N}\right)$ | Verifique el signo de $m_k>0$ para $0<k<N$: el denominador correcto es $q-p$ junto con $k-N\frac{1-(q/p)^k}{1-(q/p)^N}$, asegurando positividad tanto si $p>q$ como si $p<q$. |
| `D-Hab10-03` | Confunde frontera con $u_0$=1 | conceptual_swap | high | Impone $m_0=1$ y $m_N=0$ | Fije $m_0=0$ y $m_N=0$, pues cuando la fortuna inicial ya está en un estado absorbente no se realiza ninguna apuesta adicional. |
| `D-Hab10-04` | Máximo en extremos | conceptual_swap | high | El tiempo esperado $m_k$ es máximo en $k=1$ o $k=N-1$ | Analice la parábola $m_k=k(N-k)$ en el caso justo $p=1/2$: alcanza su máximo $(N/2)^2$ en el punto medio $k=N/2$, donde ambos jugadores tienen igual capital. |
| `D-Hab10-05` | Usa rama asimétrica en p=q | conceptual_swap | high | Evalúa $\frac{1}{q-p}$ en $p=q=1/2$ | Emplee la expresión simétrica $m_k=k(N-k)$ cuando $p=q=1/2$, obtenida al tomar $S_k=k+1$ en la suma telescópica. |
| `D-Hab10-06` | Omite factor N en fracción | conceptual_swap | high | $m_k=\frac{1}{q-p}\left(k-\frac{1-(q/p)^k}{1-(q/p)^N}\right)$ | Multiplique la fracción $\frac{1-(q/p)^k}{1-(q/p)^N}$ por $N$ para que se cumpla la condición de frontera $m_N=\frac{1}{q-p}(N-N\cdot 1)=0$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab10-01` | - | Finitud casi segura del tiempo de absorción $\tau$ y condiciones $m_0=m_N=0$ | Si el juego no tuviera absorción segura, la esperanza de duración podría divergir. | - |

---
