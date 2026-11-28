# Cognitive Task Analysis (CTA): Estadistica 3 Test K3

- **Course ID:** `estadistica_3_test_k3`
- **Macro-Competency:** Dominio y aplicación analítica integral de Estadistica 3 Test K3
- **Structure:** 22 total competencies (1 Facts, 13 Concepts, 8 Skills) with 94 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Sigma-Álgebra Generada y Minimalidad | Concept | Evaluate | Unidad 3: Sigma-Álgebra Generada y Minimalidad | - | 4 |
| `Hab-01` | Conteo de Átomos y Cardinalidad | Skill | Analyze | Unidad 3: Conteo de Átomos y Cardinalidad | C-01 | 6 |
| `C-02` | Álgebra de Borel y Generadores | Concept | Evaluate | Unidad 4: Álgebra de Borel y Generadores | C-01 | 4 |
| `C-03` | Medibilidad por Preimágenes y Generador | Concept | Evaluate | Unidad 5: Medibilidad por Preimágenes y Generador | C-02 | 4 |
| `Hab-02` | Verificación de Medibilidad sobre Átomos | Skill | Evaluate | Unidad 5: Verificación de Medibilidad sobre Átomos | Hab-01, C-03 | 6 |
| `C-04` | Filtraciones y Procesos Adaptados | Concept | Analyze | Unidad 6: Filtraciones y Procesos Adaptados | C-03, Hab-02 | 4 |
| `C-05` | Esperanza Condicional como Variable Aleatoria | Concept | Analyze | Unidad 2: Esperanza Condicional como Variable Aleatoria | C-03 | 3 |
| `C-06` | Ley de Adam y Estrategia de Iteración | Concept | Evaluate | Unidad 3: Ley de Adam y Estrategia de Iteración | C-05 | 3 |
| `C-07` | Proyección Ortogonal en L2 y Optimalidad MSE | Concept | Evaluate | Unidad 4: Proyección Ortogonal en L2 y Optimalidad MSE | C-05, C-06 | 3 |
| `C-08` | Varianza Condicional y Ley de Eve | Concept | Evaluate | Unidad 4: Varianza Condicional y Ley de Eve | C-06 | 3 |
| `Hab-03` | Cálculo Jerárquico con Adam y Eve | Skill | Evaluate | Unidad 5: Cálculo Jerárquico con Adam y Eve | C-06, C-08 | 6 |
| `Hab-04` | Esperanza Condicional en Sigma-Álgebras y Propiedad Torre | Skill | Evaluate | Unidad 6: Esperanza Condicional en Sigma-Álgebras y Propiedad Torre | C-06, C-04 | 6 |
| `H-01` | Definición de Proceso Estocástico | Fact | Understand | Unidad 1: Definición de Proceso Estocástico | C-03 | 3 |
| `C-09` | Propiedad de Markov | Concept | Evaluate | Unidad 4: Propiedad de Markov | H-01 | 3 |
| `C-10` | Incrementos Independientes y Estacionarios | Concept | Evaluate | Unidad 5: Incrementos Independientes y Estacionarios | H-01 | 3 |
| `C-11` | Condición de Martingala Discreta | Concept | Evaluate | Unidad 5: Condición de Martingala Discreta | H-01, C-05 | 3 |
| `C-12` | Caminata Aleatoria Simple en Enteros | Concept | Analyze | Unidad 8: Caminata Aleatoria Simple en Enteros | H-01, C-09 | 3 |
| `Hab-05` | Esperanza y Varianza de Caminata | Skill | Analyze | Unidad 8: Esperanza y Varianza de Caminata | C-12 | 6 |
| `Hab-06` | Distribución de Transición Binomial | Skill | Evaluate | Unidad 10: Distribución de Transición Binomial | C-12 | 6 |
| `C-13` | Recurrencia y Retorno al Origen | Concept | Evaluate | Unidad 12: Recurrencia y Retorno al Origen | Hab-06 | 3 |
| `Hab-07` | Probabilidad de Ruina del Jugador | Skill | Evaluate | Unidad 17: Probabilidad de Ruina del Jugador | C-09, C-12 | 6 |
| `Hab-08` | Duración Esperada Antes de Ruina | Skill | Evaluate | Unidad 20: Duración Esperada Antes de Ruina | Hab-07 | 6 |

---

## Detailed Competency Specifications

### [C-01] Sigma-Álgebra Generada y Minimalidad (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Sigma-Álgebra Generada y Minimalidad
- **Prerequisites:** None
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `01_measure_theory_bridge.pdf` (page 3)

#### Description & Cognitive Model
Definición de la sigma-álgebra generada $\sigma(\mathcal{C})$ como intersección de todas las sigma-álgebras sobre $\Omega$ que contienen a $\mathcal{C}$, y su propiedad de minimalidad

#### Fused Distractor Models (4)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Confunde colección con cierre | conceptual_swap | high | $\sigma(\mathcal{C}) = \mathcal{C}$ | Verifique si la colección generadora contiene el espacio muestral y es cerrada bajo complementos y uniones numerables antes de identificarla con su cierre. |
| `D-C01-02` | Maximilidad en vez de minimalidad | conceptual_swap | high | $\sigma(\mathcal{C}) = \mathcal{P}(\Omega)$ | Recuerde que la intersección produce la menor estructura que contiene a los generadores, no el conjunto potencia completo salvo que los átomos sean unitarios. |
| `D-C01-03` | Unión de sigma-álgebras | conceptual_swap | high | $\sigma(\mathcal{C}) = \bigcup_{\Sigma \supseteq \mathcal{C}} \Sigma$ | Note que la unión arbitraria de sigma-álgebras no preserva la cerradura bajo complementos ni uniones, mientras que la intersección siempre define una sigma-álgebra. |
| `D-C01-04` | Cardinalidad no potencia de dos | conceptual_swap | high | $|\mathcal{F}| = 2k$ o impar | Compruebe que toda sigma-álgebra finita se construye mediante subconjuntos de átomos disjuntos, por lo que su cardinalidad es necesariamente una potencia de dos. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | El conjunto $\Omega$ es no vacío y $\mathcal{C} \subseteq \mathcal{P}(\Omega)$ | Si $\Omega$ fuese vacío o $\mathcal{C}$ no fuese subcolección de partes, la familia de sigma-álgebras sobre $\Omega$ carecería de dominio válido. | - |
| `A-C01-02` | - | La familia $\{\Sigma \subseteq \mathcal{P}(\Omega) : \mathcal{C} \subseteq \Sigma\}$ es no vacía porque contiene a $\mathcal{P}(\Omega)$ | Sin un miembro garantizado como el conjunto potencia, la intersección de la familia quedaría indeterminada. | - |

---

### [Hab-01] Conteo de Átomos y Cardinalidad (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 3: Conteo de Átomos y Cardinalidad
- **Prerequisites:** C-01
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `01_measure_theory_bridge.pdf` (page 3)

#### Description & Cognitive Model
Construcción de los $k$ átomos indivisibles $\{A_1,\dots,A_k\}$ mediante intersecciones booleanas de generadores solapados y conteo exacto $|\sigma(\mathcal{C})| = 2^k$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Fórmula directa sobre generadores | skipped_step | high | $|\sigma(\mathcal{C})| = 2^{|\mathcal{C}|}$ | Descomponga primero los generadores solapados en bloques disjuntos no vacíos que cubran todo el espacio antes de elevar dos al número de átomos. |
| `D-Hab01-02` | Omite complemento residual | skipped_step | high | $\bigcup_{j} C_j = \Omega$ | Verifique si la unión de los generadores cubre el espacio muestral completo; si queda un resto no vacío, ese complemento forma un átomo adicional. |
| `D-Hab01-03` | Cuenta intersecciones vacías | conceptual_swap | high | Incluye $A_j = \emptyset$ como átomo | Descarte toda intersección booleana que resulte vacía, pues los átomos son por definición bloques observables no vacíos e indivisibles. |
| `D-Hab01-04` | Suma cardinales en vez de potencia | conceptual_swap | high | $|\sigma(\{A_1,\dots,A_k\})| = 2k$ | Cada evento decidible corresponde a un subconjunto de índices de átomos, lo que produce exactamente dos elevado al número de átomos. |
| `D-Hab01-05` | Aplica regla finita a infinito | conceptual_swap | high | $|\sigma(\mathcal{C})| = 2^{|\mathcal{C}|}$ en continuos | Restrinja la fórmula de cardinalidad finita únicamente a particiones de un número finito de bloques no vacíos y exhaustivos. |
| `D-Hab01-06` | Confunde átomo con evento unitario | conceptual_swap | high | Todo átomo es un singleton $\{\omega\}$ | Recuerde que un átomo es un bloque indivisible bajo la información disponible y puede agrupar múltiples escenarios indistinguibles. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Los átomos $A_1,\dots,A_k$ son no vacíos, disjuntos dos a dos y exhaustivos | Si falta disjunción o exhaustividad, las uniones de bloques no forman una sigma-álgebra de tamaño $2^k$. | - |

---

### [C-02] Álgebra de Borel y Generadores (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Álgebra de Borel y Generadores
- **Prerequisites:** C-01
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `01_measure_theory_bridge.pdf` (page 4)

#### Description & Cognitive Model
Construcción de la sigma-álgebra de Borel $\mathcal{B}(\mathbb{R}) := \sigma(\mathcal{O}_{\mathbb{R}})$, insuficiencia de $\mathcal{O}_{\mathbb{R}}$, equivalencia con rayos $(-\infty,x]$ y frontera $\mathcal{B}(\mathbb{R}) \subsetneq \mathcal{P}(\mathbb{R})$

#### Fused Distractor Models (4)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Abiertos forman sigma-álgebra | conceptual_swap | high | $\mathcal{O}_{\mathbb{R}}$ es sigma-álgebra | Compruebe que el complemento de un intervalo abierto es cerrado y que una intersección numerable de abiertos puede producir un punto aislado cerrado. |
| `D-C02-02` | Igualdad con partes de R | conceptual_swap | high | $\mathcal{B}(\mathbb{R}) = \mathcal{P}(\mathbb{R})$ | Recuerde que una sigma-álgebra solo exige cerradura bajo uniones numerables, por lo que uniones no numerables de puntos pueden salir de los borelianos. |
| `D-C02-03` | Insuficiencia de rayos cerrados | conceptual_swap | high | $\sigma(\{(-\infty,x]\}) \subsetneq \mathcal{B}(\mathbb{R})$ | Exprese cada intervalo abierto como unión numerable de diferencias de rayos cerrados para confirmar que ambas colecciones generan exactamente los mismos borelianos. |
| `D-C02-04` | Cerradura bajo unión no numerable | conceptual_swap | high | $\bigcup_{i \in I} B_i \in \mathcal{B}(\mathbb{R})$ arbitraria | Exija siempre que la familia de índices sea finita o numerable antes de concluir que la unión pertenece a la sigma-álgebra de Borel. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | La recta real $\mathbb{R}$ está dotada de la topología estándar $\mathcal{O}_{\mathbb{R}}$ | Al cambiar la topología base, cambia la colección de abiertos que genera los conjuntos medibles. | - |
| `A-C02-02` | - | Todo abierto real es unión numerable de intervalos abiertos con extremos racionales | Sin separabilidad racional de la recta real no se podría reducir $\sigma(\mathcal{O}_{\mathbb{R}})$ a intervalos con extremos racionales. | - |

---

### [C-03] Medibilidad por Preimágenes y Generador (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Medibilidad por Preimágenes y Generador
- **Prerequisites:** C-02
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `01_measure_theory_bridge.pdf` (page 5)

#### Description & Cognitive Model
Definición de mapa medible $X : (\Omega,\mathcal{F}) \to (N,\Sigma_N)$ mediante $X^{-1}(B) \in \mathcal{F}$, Lema del Generador de Schuller, criterio $\{X \le x\} \in \mathcal{F}$ y composición con funciones continuas

#### Fused Distractor Models (4)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Medibilidad con imagen directa | conceptual_swap | high | $X(A) \in \Sigma_N$ para todo $A \in \mathcal{F}$ | Note que la imagen directa no conmuta con intersecciones ni complementos para funciones no inyectivas, por lo que solo la preimagen transporta la estructura. |
| `D-C03-02` | Dependencia de la medida P | conceptual_swap | high | Medibilidad depende de $\mathbb{P}$ | Separe la estructura de información del cálculo probabilístico: la medibilidad solo involucra las sigma-álgebras de partida y de llegada. |
| `D-C03-03` | Exige verificar todo boreliano | conceptual_swap | high | Comprobar $X^{-1}(B) \in \mathcal{F}$ en todo $B$ | Aplique el Lema del Generador mediante el principio de conjuntos buenos para reducir la verificación únicamente a los rayos cerrados generadores. |
| `D-C03-04` | Falla en composición continua | conceptual_swap | high | $g(X)$ requiere recalcular preimágenes | Use que toda función continua es Borel-medible y que la composición de mapas medibles preserva automáticamente la medibilidad respecto a la misma información. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | La colección generadora $\mathcal{E} \subseteq \mathcal{P}(N)$ satisface $\Sigma_N = \sigma(\mathcal{E})$ | Si $\mathcal{E}$ no genera toda la sigma-álgebra de llegada, verificar preimágenes en $\mathcal{E}$ no garantiza medibilidad global. | - |
| `A-C03-02` | - | En el criterio de composición, la función $g : \mathbb{R} \to \mathbb{R}$ es continua | Una función $g$ discontinua arbitraria podría no ser Borel-medible y romper la medibilidad de $g \circ X$. | - |

---

### [Hab-02] Verificación de Medibilidad sobre Átomos (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Verificación de Medibilidad sobre Átomos
- **Prerequisites:** Hab-01, C-03
- **Recommended Modalities:** open_symbolic, adversarial_break, unstructured_model
- **Evidence Citations:** `01_measure_theory_bridge.pdf` (page 5)

#### Description & Cognitive Model
Evaluación operativa de $\mathcal{F}$-medibilidad de una función $X : \Omega \to \mathbb{R}$ mediante el criterio de constancia sobre cada átomo $A_j$ y determinación de $\sigma(X)$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Confunde inyectividad con medibilidad | skipped_step | high | $X$ medible $\Rightarrow X$ distinta en cada $\omega$ | Recuerde que la medibilidad sobre una sigma-álgebra finita exige exactamente constancia dentro de cada átomo, nunca valores distintos en escenarios indistinguibles. |
| `D-Hab02-02` | Evalúa un solo átomo | skipped_step | high | Constante en $A_1 \Rightarrow \mathcal{F}$-medible | Inspeccione todos y cada uno de los átomos de la partición, pues basta que la función varíe dentro de un solo átomo para perder la medibilidad. |
| `D-Hab02-03` | Exige misma constante global | conceptual_swap | high | $X$ constante en todo $\Omega$ | Distinga constancia intra-átomo de constancia global: la función puede tomar valores distintos en átomos separados y seguir siendo medible. |
| `D-Hab02-04` | Ignora dependencia de F | conceptual_swap | high | Medibilidad es propiedad intrínseca de $X$ | Especifique siempre la sigma-álgebra de partida, ya que una misma función puede ser medible respecto a una partición fina y no medible respecto a una gruesa. |
| `D-Hab02-05` | Preimagen parcial de átomo | conceptual_swap | high | $X^{-1}(\{c\}) \subsetneq A_j$ es medible | Verifique que toda preimagen de un punto o boreliano debe expresarse como unión exacta de átomos completos y nunca partir un átomo. |
| `D-Hab02-06` | Confunde sigma(X) con P(Omega) | conceptual_swap | high | $\sigma(X) = \mathcal{P}(\Omega)$ siempre | Construya $\sigma(X)$ a partir de las preimágenes de los valores distintos que toma la variable, las cuales coinciden con uniones de átomos cuando $X$ es medible. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | La sigma-álgebra $\mathcal{F} = \sigma(\{A_1,\dots,A_k\})$ proviene de una partición finita de $\Omega$ | En espacios infinitos sin estructura atómica finita, el criterio discreto de constancia sobre átomos no basta por sí solo. | - |

---

### [C-04] Filtraciones y Procesos Adaptados (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 6: Filtraciones y Procesos Adaptados
- **Prerequisites:** C-03, Hab-02
- **Recommended Modalities:** unstructured_model, adversarial_break, multiple_select
- **Evidence Citations:** `01_measure_theory_bridge.pdf` (page 6)

#### Description & Cognitive Model
Estructura de filtración $\{\mathcal{F}_t\}_{t \in T}$ como familia creciente $\mathcal{F}_s \subseteq \mathcal{F}_t$, condición de proceso adaptado $\sigma(X_t) \subseteq \mathcal{F}_t$, filtración natural $\mathcal{F}_t^X$ y refinamiento de átomos

#### Fused Distractor Models (4)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Inclusión decreciente de información | conceptual_swap | high | $\mathcal{F}_t \subseteq \mathcal{F}_s$ para $s \le t$ | Asegure que la familia de sigma-álgebras sea creciente en el tiempo, reflejando que la información histórica acumulada nunca se olvida. |
| `D-C04-02` | Anticipación futura en t | conceptual_swap | high | $X_{t+1}$ es $\mathcal{F}_t$-medible | Verifique si la variable futura distingue escenarios que permanecen agrupados dentro de un mismo átomo de la información actual; si es así, no es adaptada en ese instante. |
| `D-C04-03` | Constancia temporal de átomos | conceptual_swap | high | Átomos de $\mathcal{F}_t$ no se refinan | Observe que revelar nueva información en cada periodo parte los átomos vigentes en sub-átomos más finos, incrementando los eventos decidibles. |
| `D-C04-04` | Exige adaptabilidad solo al final | conceptual_swap | high | $X_t$ medible solo en $\mathcal{F}_T$ | Compruebe la condición de adaptabilidad en cada instante de tiempo de manera individual, exigiendo que el valor en ese instante dependa solo de la historia hasta ese momento. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | El conjunto de tiempos $T$ está totalmente ordenado, como $\{0,1,2,\dots\}$ o $[0,\infty)$ | Sin un orden temporal definido no tiene sentido la condición de monotonicidad $\mathcal{F}_s \subseteq \mathcal{F}_t$ para $s \le t$. | - |
| `A-C04-02` | - | Cada $\mathcal{F}_t$ es una sub-sigma-álgebra de $\mathcal{F}$ | Si $\mathcal{F}_t$ no está contenida en $\mathcal{F}$, las probabilidades del espacio base no estarían definidas sobre los eventos observados en $t$. | - |

---

### [C-05] Esperanza Condicional como Variable Aleatoria (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 2: Esperanza Condicional como Variable Aleatoria
- **Prerequisites:** C-03
- **Recommended Modalities:** multiple_select, adversarial_break, concept_matching
- **Evidence Citations:** `02_stat110_lec27_conditional_expectation.pdf` (page 2)

#### Description & Cognitive Model
Definición de $\mathbb{E}[Y\mid X]:=g(X)$ con $g(x)=\mathbb{E}[Y\mid X=x]$ como variable aleatoria $\sigma(X)$-medible, propiedades algebraicas y distinción frente a $\mathbb{E}[Y\mid A]$ constante

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Confundir con constante | conceptual_swap | high | $\mathbb{E}[Y\mid X]\in\mathbb{R}$ constante | Distinga entre condicionar en un evento $A$, que produce un número real, y condicionar en una variable aleatoria $X$, que genera una función $\sigma(X)$-medible. |
| `D-C05-02` | Recíproco de independencia | conceptual_swap | high | $\mathbb{E}[Y\mid X]=\mathbb{E}[Y]\Rightarrow X\perp Y$ | Recuerde que la igualdad de medias condicionales no garantiza independencia estadística; la dependencia puede manifestarse en la varianza o en el soporte condicional. |
| `D-C05-03` | Sacar variable no medible | conceptual_swap | high | $\mathbb{E}[h(Y)X\mid X]=h(Y)\mathbb{E}[X\mid X]$ | Solo las funciones medibles del elemento condicionante $h(X)$ salen de la esperanza condicional; cualquier función de $Y$ permanece dentro del operador. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Integrabilidad absoluta de la variable objetivo $\mathbb{E}[|Y|]<\infty$ ($Y\in L^1$) | Sin integrabilidad $L^1$, la esperanza condicional $\mathbb{E}[Y\mid X]$ puede no existir. | - |
| `A-C05-02` | - | Integrabilidad del producto $\mathbb{E}[|h(X)Y|]<\infty$ al aplicar sacar lo conocido | Si el producto no es integrable, la factorización $h(X)\mathbb{E}[Y\mid X]$ pierde validez. | - |

---

### [C-06] Ley de Adam y Estrategia de Iteración (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Ley de Adam y Estrategia de Iteración
- **Prerequisites:** C-05
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `02_stat110_lec27_conditional_expectation.pdf` (page 3)

#### Description & Cognitive Model
Ley de esperanzas iteradas $\mathbb{E}[\mathbb{E}[Y\mid X]]=\mathbb{E}[Y]$ para $Y\in L^1$, justificada por LOTUS y Fubini, para descomponer $\mathbb{E}[Y]$ condicionando en una variable auxiliar $X$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Omitir esperanza exterior | conceptual_swap | high | $\mathbb{E}[Y\mid X]=\mathbb{E}[Y]$ | Aplique la esperanza incondicional exterior sobre la variable aleatoria $\mathbb{E}[Y\mid X]$ para promediar sobre la incertidumbre de $X$ y recuperar $\mathbb{E}[Y]$. |
| `D-C06-02` | Invertir orden de variables | conceptual_swap | high | $\mathbb{E}[\mathbb{E}[X\mid Y]]=\mathbb{E}[Y]$ | Identifique cuál variable está siendo promediada en el nivel interno: $\mathbb{E}[\mathbb{E}[Y\mid X]]$ recupera la media de $Y$, nunca la de la variable condicionante. |
| `D-C06-03` | Ignorar integrabilidad L1 | conceptual_swap | high | $\mathbb{E}[\mathbb{E}[Y\mid X]]=\mathbb{E}[Y]$ siempre sin supuestos | Verifique que $Y\in L^1$ antes de intercambiar sumas o integrales mediante Fubini; en distribuciones de cola pesada sin media finita la identidad falla. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Existencia de primer momento absoluto $\mathbb{E}[|Y|]<\infty$ ($Y\in L^1$) | Sin convergencia absoluta no es legítimo intercambiar sumatorias o integrales por Fubini. | - |

---

### [C-07] Proyección Ortogonal en L2 y Optimalidad MSE (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Proyección Ortogonal en L2 y Optimalidad MSE
- **Prerequisites:** C-05, C-06
- **Recommended Modalities:** proof_dag, adversarial_break, unstructured_model
- **Evidence Citations:** `02_stat110_lec27_conditional_expectation.pdf` (page 4)

#### Description & Cognitive Model
Propiedad de ortogonalidad del residuo $\mathbb{E}[(Y-\mathbb{E}[Y\mid X])h(X)]=0$ y optimalidad de $\mathbb{E}[Y\mid X]$ como único predictor que minimiza el error cuadrático medio $\mathbb{E}[(Y-h(X))^2]$ en $L^2$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Restringir a predictores lineales | conceptual_swap | high | $\mathbb{E}[Y\mid X]$ solo minimiza MSE entre funciones lineales $aX+b$ | Reconozca que $\mathbb{E}[Y\mid X]$ minimiza el error cuadrático medio sobre todo el subespacio de funciones medibles $h(X)\in L^2$, no únicamente sobre las lineales. |
| `D-C07-02` | Olvidar supuesto L2 | conceptual_swap | high | La proyección MSE aplica a toda variable en $L^1\setminus L^2$ | Exija segundo momento finito $Y,h(X)\in L^2$ para definir el producto interno $\langle U,V\rangle=\mathbb{E}[UV]$ y garantizar la descomposición pitagórica del error. |
| `D-C07-03` | Signo del residuo en Pitágoras | conceptual_swap | high | $\mathbb{E}[(Y-h(X))^2]=\mathbb{E}[(Y-\hat{Y})^2]-\mathbb{E}[(\hat{Y}-h(X))^2]$ | Aplique el teorema de Pitágoras con el término cruzado nulo por ortogonalidad: ambos cuadrados se suman, demostrando que $\hat{Y}=\mathbb{E}[Y\mid X]$ logra el mínimo. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Segundo momento finito $\mathbb{E}[Y^2]<\infty$ y $\mathbb{E}[h(X)^2]<\infty$ ($Y,h(X)\in L^2$) | Si $\mathbb{E}[Y^2]=\infty$, el producto interno $L^2$ diverge y falla la proyección MSE. | - |

---

### [C-08] Varianza Condicional y Ley de Eve (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Varianza Condicional y Ley de Eve
- **Prerequisites:** C-06
- **Recommended Modalities:** adversarial_break, multiple_select, proof_dag
- **Evidence Citations:** `02_stat110_lec27_conditional_expectation.pdf` (page 4)

#### Description & Cognitive Model
Definición de la varianza condicional $\operatorname{Var}(Y\mid X)=\mathbb{E}[Y^2\mid X]-(\mathbb{E}[Y\mid X])^2$ como variable aleatoria y descomposición de la varianza total $\operatorname{Var}(Y)=\mathbb{E}[\operatorname{Var}(Y\mid X)]+\operatorname{Var}(\mathbb{E}[Y\mid X])$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Omitir barra exterior | conceptual_swap | high | $\operatorname{Var}(Y\mid X)=\mathbb{E}[(Y-\mathbb{E}[Y\mid X])^2]$ | Mantenga la barra condicionante exterior $\mid X$ en la definición de varianza condicional; omitirla evalúa su esperanza $\mathbb{E}[\operatorname{Var}(Y\mid X)]$, que es una constante. |
| `D-C08-02` | Invertir operadores EVVE | conceptual_swap | high | $\operatorname{Var}(Y)=\operatorname{Var}(\operatorname{Var}(Y\mid X))+\mathbb{E}[\mathbb{E}[Y\mid X]]$ | Recuerde la estructura EVVE: sume la esperanza de la varianza condicional (variabilidad intra-grupo) más la varianza de la esperanza condicional (entre-grupos). |
| `D-C08-03` | Omitir variabilidad entre grupos | conceptual_swap | high | $\operatorname{Var}(Y)=\mathbb{E}[\operatorname{Var}(Y\mid X)]$ | Incluya la fluctuación de la media condicional $\operatorname{Var}(\mathbb{E}[Y\mid X])$ al calcular la varianza total, salvo en el caso degenerado donde $\mathbb{E}[Y\mid X]$ sea constante. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C08-01` | - | Segundo momento finito $\mathbb{E}[Y^2]<\infty$ ($Y\in L^2$) | Sin segundo momento finito no existen $\operatorname{Var}(Y)$ ni $\operatorname{Var}(Y\mid X)$ y falla EVVE. | - |

---

### [Hab-03] Cálculo Jerárquico con Adam y Eve (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Cálculo Jerárquico con Adam y Eve
- **Prerequisites:** C-06, C-08
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `02_stat110_lec27_conditional_expectation.pdf` (page 5)

#### Description & Cognitive Model
Cálculo analítico de $\mathbb{E}[X]$ y $\operatorname{Var}(X)$ en modelos jerárquicos compuestos (Beta-Binomial y adelgazamiento Poisson-Binomial) aplicando Ley de Adam, Ley de Eve y momentos condicionales

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Olvidar factor cuadrado | skipped_step | high | $\operatorname{Var}(nQ)=n\operatorname{Var}(Q)$ | Extraiga las constantes multiplicativas elevadas al cuadrado al calcular la varianza de la media condicional: $\operatorname{Var}(nQ)=n^2\operatorname{Var}(Q)$. |
| `D-Hab03-02` | Tratar parámetro como fijo | skipped_step | high | $\operatorname{Var}(X)=np(1-p)$ con $Q$ aleatorio | Aplique la Ley de Eve completa para combinar el promedio de la varianza condicional con la varianza de la media condicional inducida por el parámetro aleatorio. |
| `D-Hab03-03` | Confundir E[Q(1-Q)] | conceptual_swap | high | $\mathbb{E}[Q(1-Q)]=\mathbb{E}[Q](1-\mathbb{E}[Q])$ | Evalúe $\mathbb{E}[Q(1-Q)]=\mathbb{E}[Q]-\mathbb{E}[Q^2]$ usando $\mathbb{E}[Q^2]=\operatorname{Var}(Q)+(\mathbb{E}[Q])^2$ o la función Beta; la esperanza del cuadrado no es el cuadrado de la media. |
| `D-Hab03-04` | Omitir varianza de N | conceptual_swap | high | $\operatorname{Var}(Np)=p^2\mathbb{E}[N]$ si $N$ no es Poisson | Use la igualdad $\operatorname{Var}(N)=\mathbb{E}[N]$ únicamente cuando la variable de conteo $N$ siga una distribución de Poisson; en otro caso calcule $\operatorname{Var}(N)$ explícitamente. |
| `D-Hab03-05` | Perder término intra-grupo | conceptual_swap | high | $\operatorname{Var}(X)=\operatorname{Var}(\mathbb{E}[X\mid N])$ | Incluya la varianza condicional promedio $\mathbb{E}[Np(1-p)]$ antes de simplificar con $p^2\operatorname{Var}(N)$ para obtener la varianza total del proceso adelgazado. |
| `D-Hab03-06` | Invertir Beta en Gamma | conceptual_swap | high | $\int_0^1 q^a(1-q)^b dq=\frac{\Gamma(a)\Gamma(b)}{\Gamma(a+b)}$ | Identifique la constante normalizadora de $\operatorname{Beta}(a+1,b+1)$ usando $\Gamma(a+1)\Gamma(b+1)/\Gamma(a+b+2)$ y luego reduzca con la identidad $\Gamma(z+1)=z\Gamma(z)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | Parámetros positivos en la previa Beta ($a,b>0$) e independencia condicional de ensayos | Sin $a,b>0$ la densidad previa no integra a uno y los momentos condicionales dejan de ser válidos. | - |

---

### [Hab-04] Esperanza Condicional en Sigma-Álgebras y Propiedad Torre (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 6: Esperanza Condicional en Sigma-Álgebras y Propiedad Torre
- **Prerequisites:** C-06, C-04
- **Recommended Modalities:** open_symbolic, proof_dag, unstructured_model
- **Evidence Citations:** `02_stat110_lec27_conditional_expectation.pdf` (page 6)

#### Description & Cognitive Model
Cálculo de $\mathbb{E}[Y\mid\mathcal{F}]$ como promedio ponderado constante por átomo en particiones finitas, aplicación de la propiedad torre $\mathbb{E}[\mathbb{E}[Y\mid\mathcal{F}_t]\mid\mathcal{F}_s]=\mathbb{E}[Y\mid\mathcal{F}_s]$ y esperanza constante en martingalas

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Domina sigma-álgebra mayor | skipped_step | high | $\mathbb{E}[\mathbb{E}[Y\mid\mathcal{F}_t]\mid\mathcal{F}_s]=\mathbb{E}[Y\mid\mathcal{F}_t]$ con $\mathcal{F}_s\subseteq\mathcal{F}_t$ | Aplique la regla de que la $\sigma$-álgebra más pequeña domina en la propiedad torre: al promediar sobre un refinamiento $\mathcal{F}_t$ desde $\mathcal{F}_s\subseteq\mathcal{F}_t$, sobrevive $\mathcal{F}_s$. |
| `D-Hab04-02` | Promedio aritmético sin pesos | skipped_step | high | $\mathbb{E}[Y\mid A_j]=\frac{1}{|A_j|}\sum_{\omega\in A_j}Y(\omega)$ | Pondere cada realización dentro del átomo $A_j$ por su probabilidad condicional $\mathbb{P}(\{\omega\})/\mathbb{P}(A_j)$ para respetar la medida de probabilidad del espacio. |
| `D-Hab04-03` | Variable no constante en átomo | conceptual_swap | high | $\mathbb{E}[Y\mid\mathcal{F}](\omega)=Y(\omega)$ dentro de $A_j$ | Garantice que $\mathbb{E}[Y\mid\mathcal{F}]$ sea $\mathcal{F}$-medible manteniendo un valor único constante para todo $\omega$ perteneciente al mismo átomo $A_j$. |
| `D-Hab04-04` | Invertir inclusión de filtración | conceptual_swap | high | $\mathcal{F}_t\subseteq\mathcal{F}_s$ implica $\mathbb{E}[\mathbb{E}[Y\mid\mathcal{F}_t]\mid\mathcal{F}_s]=\mathbb{E}[Y\mid\mathcal{F}_s]$ | Verifique la dirección de la inclusión $\mathcal{F}_s\subseteq\mathcal{F}_t$ antes de simplificar: si la filtración externa es más fina, $\mathbb{E}[Y\mid\mathcal{F}_t]$ ya es $\mathcal{F}_s$-medible y queda igual. |
| `D-Hab04-05` | Omitir condición de martingala | conceptual_swap | high | $\mathbb{E}[X_{n+k}\mid\mathcal{F}_n]=X_n$ sin adaptabilidad ni $L^1$ | Confirme las tres condiciones de martingala (proceso adaptado, integrabilidad $L^1$ y $\mathbb{E}[X_{n+1}\mid\mathcal{F}_n]=X_n$) antes de extender por inducción vía propiedad torre. |
| `D-Hab04-06` | Confundir átomo con evento nulo | conceptual_swap | high | Calcular $\mathbb{E}[Y\mid A_j]$ cuando $\mathbb{P}(A_j)=0$ | Restrinja la fórmula explícita de promedio por átomos a particiones finitas con probabilidad estrictamente positiva $\mathbb{P}(A_j)>0$ para evitar divisiones indefinidas. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Partición finita con átomos de probabilidad positiva $\mathbb{P}(A_j)>0$ y filtración anidada $\mathcal{F}_s\subseteq\mathcal{F}_t$ | Si $\mathbb{P}(A_j)=0$ o no hay inclusión $\mathcal{F}_s\subseteq\mathcal{F}_t$, la fórmula por átomos o la propiedad torre fallan. | - |

---

### [H-01] Definición de Proceso Estocástico (Fact)

- **Bloom Level:** Understand
- **Session:** Unidad 1: Definición de Proceso Estocástico
- **Prerequisites:** C-03
- **Recommended Modalities:** fill_in_the_blank, multiple_select, concept_matching
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 1)

#### Description & Cognitive Model
Colección de variables aleatorias $\{X_t : t \in T\}$ parametrizada por $T$ con valores en el espacio de estados $S$ y trayectorias $t \mapsto X_t(\omega)$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Confunde trayectoria y variable | conceptual_swap | high | $X_t(\omega)$ fijo en $\omega$ es variable aleatoria | Distinga que fijando $t$ se obtiene una variable aleatoria $\omega \mapsto X_t(\omega)$, mientras que fijando $\omega$ se obtiene una trayectoria temporal. |
| `D-H01-02` | Confunde espacio T y S | conceptual_swap | high | $T$ es el conjunto de valores de $X_t$ | Recuerde que el espacio parametral $T$ indexa los tiempos de observación, mientras que el espacio de estados $S$ contiene los valores posibles de $X_t$. |
| `D-H01-03` | Exige independencia mutua | conceptual_swap | high | $X_t$ son siempre independientes entre sí | Tenga presente que en general las variables $X_t$ de un proceso estocástico presentan relaciones de dependencia temporal que caracterizan cada modelo. |

---

### [C-09] Propiedad de Markov (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Propiedad de Markov
- **Prerequisites:** H-01
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 4)

#### Description & Cognitive Model
Condición de independencia condicional donde el estado futuro $X_{n+1}$ depende únicamente del estado presente $X_n$ y no de la historia previa $X_0,\dots,X_{n-1}$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Confunde con independencia total | conceptual_swap | high | $P(X_{n+1}=x_{n+1} \mid X_n=x_n)=P(X_{n+1}=x_{n+1})$ | No confunda la propiedad de Markov con independencia total: el futuro sí depende del presente $X_n$, lo irrelevante es la historia anterior $X_0,\dots,X_{n-1}$. |
| `D-C09-02` | Conserva el estado inicial | conceptual_swap | high | $P(X_{n+1}=x_{n+1} \mid X_0=x_0, X_n=x_n)$ | Verifique que conocido el estado presente $X_n=x_n$, el estado inicial $X_0=x_0$ y todo el pasado dejan de aportar información para predecir $X_{n+1}$. |
| `D-C09-03` | Invierte dirección temporal | conceptual_swap | high | $P(X_{n-1}=x_{n-1} \mid X_n=x_n, X_{n+1}=x_{n+1})$ | Aplique la propiedad de Markov hacia adelante en el tiempo: la distribución condicional de $X_{n+1}$ dada toda la historia se reduce a condicionar solo en $X_n$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | Eventos condicionantes con probabilidad positiva $P(X_0=x_0,\dots,X_n=x_n)>0$ | Si el evento pasado tiene probabilidad cero, la probabilidad condicional elemental queda indefinida. | - |

---

### [C-10] Incrementos Independientes y Estacionarios (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Incrementos Independientes y Estacionarios
- **Prerequisites:** H-01
- **Recommended Modalities:** multiple_select, adversarial_break, concept_matching
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 5)

#### Description & Cognitive Model
Caracterización de procesos a tiempo continuo mediante independencia de desplazamientos en intervalos disjuntos y distribución invariante bajo traslaciones temporales $h>0$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C10-01` | Confunde variables con incrementos | conceptual_swap | high | $X_{t_1}, X_{t_2}, \dots, X_{t_n}$ son independientes | Distinga entre independencia de los estados $X_t$ e independencia de los incrementos $X_{t_k}-X_{t_{k-1}}$ sobre intervalos temporales disjuntos. |
| `D-C10-02` | Confunde estacionario con incremento | conceptual_swap | high | $X_t$ tiene la misma distribución que $X_{t+h}-X_s$ | Separe estacionariedad estricta, que exige invariancia de las distribuciones finito-dimensionales de $X_t$, de incrementos estacionarios que solo depende de $t-s$. |
| `D-C10-03` | Intervalos traslapados | conceptual_swap | high | $X_{t_3}-X_{t_1}$ y $X_{t_2}-X_{t_1}$ independientes | Verifique que la independencia de incrementos requiere tiempos ordenados $0 \le t_1 < t_2 < \dots < t_n$ para garantizar intervalos de tiempo disjuntos. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C10-01` | - | Orden estricto de los tiempos $0 \le t_1 < t_2 < \dots < t_n$ en $T=[0,\infty)$ | Sin intervalos disjuntos los incrementos se solapan y pierden independencia. | - |

---

### [C-11] Condición de Martingala Discreta (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Condición de Martingala Discreta
- **Prerequisites:** H-01, C-05
- **Recommended Modalities:** adversarial_break, unstructured_model, multiple_select
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 5)

#### Description & Cognitive Model
Proceso a tiempo discreto que modela juegos justos satisfaciendo $E(X_{n+1} \mid X_0=x_0,\dots,X_n=x_n)=x_n$ donde el valor esperado futuro coincide con el último observado

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C11-01` | Iguala con esperanza incondicional | conceptual_swap | high | $E(X_{n+1})=E(X_0)$ implica martingala | Recuerde que la propiedad de martingala exige igualdad de la esperanza condicional dada toda la historia $X_0,\dots,X_n$ con el valor observado $x_n$. |
| `D-C11-02` | Confunde martingala con Markov | conceptual_swap | high | Toda cadena de Markov es martingala | Distinga la propiedad de Markov, sobre la distribución condicional completa, de la martingala, que restringe únicamente el valor esperado condicional. |
| `D-C11-03` | Agrega deriva constante | conceptual_swap | high | $E(X_{n+1} \mid X_0,\dots,X_n)=x_n + \mu$ con $\mu \neq 0$ | Verifique que en una martingala el juego es equilibrado: el cambio esperado condicional $E(X_{n+1}-X_n \mid X_0,\dots,X_n)$ debe ser exactamente cero. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C11-01` | - | Integrabilidad de las variables aleatorias $E(|X_n|) < \infty$ para todo $n \ge 0$ | Sin integrabilidad la esperanza condicional no está bien definida. | - |

---

### [C-12] Caminata Aleatoria Simple en Enteros (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 8: Caminata Aleatoria Simple en Enteros
- **Prerequisites:** H-01, C-09
- **Recommended Modalities:** unstructured_model, adversarial_break, multiple_select
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 8)

#### Description & Cognitive Model
Proceso discreto $X_n = X_0 + \sum_{i=1}^n \xi_i$ sobre $\mathbb{Z}$ con pasos $\xi_i \in \{+1,-1\}$ i.i.d., probabilidades homogéneas $p+q=1$ y propiedad de Markov

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C12-01` | Permite saltos arbitrarios | conceptual_swap | high | $P(X_{n+1}=j \mid X_n=i)>0$ para $|j-i|>1$ | Recuerde que en la caminata aleatoria simple sin permanencia el proceso solo puede avanzar a $i+1$ con probabilidad $p$ o retroceder a $i-1$ con probabilidad $q$. |
| `D-C12-02` | Probabilidades suman distinto de uno | conceptual_swap | high | $p+q < 1$ sin estado de permanencia | Verifique que si no existe probabilidad $r$ de permanecer en el mismo estado, las probabilidades de paso a derecha e izquierda deben satisfacer $p+q=1$. |
| `D-C12-03` | Pasos dependientes entre sí | conceptual_swap | high | $\xi_{n+1}$ depende del signo de $\xi_n$ | Asegure que las variables de paso $\xi_1,\xi_2,\dots$ sean independientes e idénticamente distribuidas para preservar la homogeneidad y la propiedad de Markov. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C12-01` | - | Pasos $\xi_i$ independientes e idénticamente distribuidos con $p+q=1$ | Sin independencia ni distribución idéntica se rompe la estructura homogénea de la caminata. | - |

---

### [Hab-05] Esperanza y Varianza de Caminata (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 8: Esperanza y Varianza de Caminata
- **Prerequisites:** C-12
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 8)

#### Description & Cognitive Model
Cálculo analítico de $E(X_n)=n(p-q)$ y $\mathrm{Var}(X_n)=4npq$ para $X_0=0$ mediante linealidad e independencia de $\xi_i$, identificando simetría $p=1/2$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Omite factor 4 en varianza | skipped_step | high | $\mathrm{Var}(X_n)=npq$ | Calcule $\mathrm{Var}(\xi)=E(\xi^2)-[E(\xi)]^2=1-(p-q)^2=4pq$ antes de sumar $n$ varianzas independientes; la amplitud de paso es $2$, lo que aporta el factor $4$. |
| `D-Hab05-02` | Suma probabilidades en esperanza | skipped_step | high | $E(X_n)=n(p+q)=n$ | Pondera cada paso por su signo: $E(\xi)=(+1)p+(-1)q=p-q$, de modo que la tendencia promedio tras $n$ pasos es $n(p-q)$. |
| `D-Hab05-03` | Varianza cuadrática en n | conceptual_swap | high | $\mathrm{Var}(X_n)=4n^2 pq$ | Aplique la aditividad de la varianza para variables independientes: la varianza de la suma de $n$ pasos es $n\,\mathrm{Var}(\xi)$, lineal en $n$. |
| `D-Hab05-04` | Error en varianza máxima | conceptual_swap | high | $\mathrm{Var}(X_n)$ es máxima en $p=1$ | Analice la cuadrática $4pq=4p(1-p)$ sobre $p \in (0,1)$: alcanza su máximo en la caminata simétrica $p=q=1/2$, donde $\mathrm{Var}(X_n)=n$. |
| `D-Hab05-05` | Esperanza no nula si simétrica | conceptual_swap | high | $E(X_n)=n/2$ cuando $p=q=1/2$ | Verifique que en el caso simétrico $p=q=1/2$ los desplazamientos a derecha e izquierda se compensan en promedio, resultando $E(X_n)=0$. |
| `D-Hab05-06` | Varianza sin signo en p-q | conceptual_swap | high | $\mathrm{Var}(\xi)=1-(p+q)^2$ | Recuerde que $[E(\xi)]^2=(p-q)^2$, por lo cual $1-(p-q)^2=(p+q)^2-(p-q)^2=4pq$ usando $p+q=1$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | Condición inicial fija $X_0=0$ e independencia entre $\xi_1,\dots,\xi_n$ | Si los pasos son correlacionados aparecen términos de covarianza y falla $n\,\mathrm{Var}(\xi)$. | - |

---

### [Hab-06] Distribución de Transición Binomial (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 10: Distribución de Transición Binomial
- **Prerequisites:** C-12
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, adversarial_break
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 10)

#### Description & Cognitive Model
Determinación de $P(X_n=x \mid X_0=y)=\binom{n}{\frac{1}{2}(n+x-y)}p^{\frac{1}{2}(n+x-y)}q^{\frac{1}{2}(n-x+y)}$ validando alcance $|x-y| \le n$ y misma paridad entre $n$ y $x-y$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Exponente de pasos a derecha | skipped_step | high | $R_n = x-y$ en lugar de $\frac{1}{2}(n+x-y)$ | Resuelva el sistema $R_n+L_n=n$ y $R_n-L_n=x-y$ sumando ambas ecuaciones para obtener el conteo entero de pasos a la derecha $R_n=\frac{1}{2}(n+x-y)$. |
| `D-Hab06-02` | Ignora restricción de paridad | skipped_step | high | Aplica la fórmula binomial aunque $n$ y $x-y$ tengan distinta paridad | Compruebe antes de calcular que $n$ y el desplazamiento $x-y$ sean ambos pares o ambos impares y que $|x-y|\le n$; en otro caso la probabilidad es cero. |
| `D-Hab06-03` | Invierte exponentes p y q | conceptual_swap | high | $p^{\frac{1}{2}(n-x+y)}q^{\frac{1}{2}(n+x-y)}$ | Asocie la probabilidad $p$ al número de pasos hacia la derecha $R_n=\frac{1}{2}(n+x-y)$ y la probabilidad $q$ al número de pasos hacia la izquierda $L_n=\frac{1}{2}(n-x+y)$. |
| `D-Hab06-04` | Omite desplazamiento inicial y | conceptual_swap | high | Usa $x$ en vez de $x-y$ cuando $X_0=y$ | Traslade el proceso mediante $Z_n=X_n-y$ para reducir el problema a una caminata que inicia en cero y termina en $x-y$. |
| `D-Hab06-05` | Omite coeficiente binomial | conceptual_swap | high | $p^{\frac{1}{2}(n+x-y)}q^{\frac{1}{2}(n-x+y)}$ sin $\binom{n}{R_n}$ | Multiplique por el coeficiente binomial $\binom{n}{R_n}$ para contar todas las trayectorias posibles de $n$ pasos con exactamente $R_n$ avances a la derecha. |
| `D-Hab06-06` | Error en caso simétrico | conceptual_swap | high | Usa $2^{-R_n}$ en lugar de $2^{-n}$ cuando $p=1/2$ | Recuerde que cuando $p=q=1/2$ el producto $p^{R_n}q^{L_n}$ se simplifica a $(1/2)^{R_n+L_n}=2^{-n}$ porque cada trayectoria de longitud $n$ es equiprobable. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Misma paridad entre $n$ y $x-y$ junto con $-n \le x-y \le n$ | Fuera de estas condiciones no existe ninguna trayectoria válida y la probabilidad vale cero. | - |

---

### [C-13] Recurrencia y Retorno al Origen (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 12: Recurrencia y Retorno al Origen
- **Prerequisites:** Hab-06
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 12)

#### Description & Cognitive Model
Probabilidad de eventual regreso al origen $1-|p-q|$ vía función generadora $G(t)=1-(1-4pqt^2)^{1/2}$: certeza de retorno si $p=q$ pero tiempo esperado infinito

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C13-01` | Tiempo medio finito si p=q | conceptual_swap | high | Si $p=q$, el tiempo esperado de regreso es finito | Recuerde que en la caminata simétrica $p=q=1/2$ el retorno es seguro ($\sum f_n=1$), pero el tiempo promedio $\lim_{t \nearrow 1} G'(t)=\infty$ diverge. |
| `D-C13-02` | Retorno seguro si asimétrica | conceptual_swap | high | $1-|p-q|=1$ para todo $p \in (0,1)$ | Observe que si $p \neq 1/2$ entonces $|p-q|>0$, por lo que la probabilidad de eventual regreso $1-|p-q|$ es estrictamente menor que uno. |
| `D-C13-03` | Confunde pn con fk | conceptual_swap | high | $G(t)=\sum_{n=0}^\infty p_n t^n$ da probabilidad de retorno | Distinga entre $p_n=P(X_n=0 \mid X_0=0)$ y $f_k$ (primera visita al origen en el paso $k$); el regreso eventual corresponde a $\sum_{k=0}^\infty f_k = \lim_{t \nearrow 1} G(t)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C13-01` | - | Caminata aleatoria simple irrestricta sobre todo $\mathbb{Z}$ iniciando en $X_0=0$ | En dominios finitos con barreras absorbentes el retorno al origen deja de regirse por $1-|p-q|$. | - |

---

### [Hab-07] Probabilidad de Ruina del Jugador (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 17: Probabilidad de Ruina del Jugador
- **Prerequisites:** C-09, C-12
- **Recommended Modalities:** open_symbolic, unstructured_model, adversarial_break
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 17)

#### Description & Cognitive Model
Resolución de la ecuación en diferencias homogénea $u_k=pu_{k+1}+qu_{k-1}$ con $u_0=1$ y $u_N=0$ para hallar $u_k=P(X_\tau=0 \mid X_0=k)$ en los casos $p=1/2$ y $p \neq 1/2$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Invierte condiciones de frontera | skipped_step | high | $u_0=0$ y $u_N=1$ para probabilidad de ruina | Verifique el significado de $u_k=P(X_\tau=0 \mid X_0=k)$: partiendo de $0$ la ruina ya ocurrió ($u_0=1$), mientras que en $N$ el jugador ganó todo ($u_N=0$). |
| `D-Hab07-02` | Usa razón p/q en lugar de q/p | skipped_step | high | $u_k=\frac{(p/q)^k-(p/q)^N}{1-(p/q)^N}$ | Agrupe $(p+q)u_k=pu_{k+1}+qu_{k-1}$ para verificar que el factor de razón entre diferencias sucesivas es $q/p$, no $p/q$. |
| `D-Hab07-03` | Aplica fórmula asimétrica en p=1/2 | conceptual_swap | high | Evalúa $\frac{(q/p)^k-(q/p)^N}{1-(q/p)^N}$ directamente en $p=1/2$ | Separe explícitamente el caso simétrico $p=1/2$, donde $S_k=k+1$ y la probabilidad de ruina es lineal: $u_k=(N-k)/N$. |
| `D-Hab07-04` | Confunde ruina con victoria | conceptual_swap | high | $u_k=k/N$ cuando $p=1/2$ | Note que la probabilidad de ruina decrece al aumentar el capital inicial $k$; en el caso justo corresponde a $(N-k)/N$, mientras que $k/N$ es la probabilidad de triunfo. |
| `D-Hab07-05` | Omite término independiente en suma | conceptual_swap | high | $S_k=(q/p)+\dots+(q/p)^k$ sin el $1$ inicial | Incluya el término inicial $1$ en $S_k=\sum_{j=0}^k (q/p)^j$ para que la relación $u_k=1-S_{k-1}/S_{N-1}$ satisfaga $u_0=1$ y $u_N=0$. |
| `D-Hab07-06` | Usa capital de B como N | conceptual_swap | high | Reemplaza $N$ por $N-k$ en el denominador | Identifique $N$ como la suma fija de los capitales de ambos jugadores (la barrera absorbente superior), no como la fortuna inicial del jugador $B$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Estados absorbentes en $0$ y $N$, sin empates ($p+q=1$) y $0 < k < N$ | Si hay empates ($r>0$) o barreras reflejantes cambia la ecuación en diferencias y sus fronteras. | - |

---

### [Hab-08] Duración Esperada Antes de Ruina (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 20: Duración Esperada Antes de Ruina
- **Prerequisites:** Hab-07
- **Recommended Modalities:** open_symbolic, unstructured_model, fill_in_the_blank
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 20)

#### Description & Cognitive Model
Resolución de la ecuación en diferencias no homogénea $m_k=1+pm_{k+1}+qm_{k-1}$ con $m_0=m_N=0$ para hallar el número esperado de apuestas $m_k$ antes de absorción

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | Omite el +1 de la apuesta actual | skipped_step | high | $m_k=pm_{k+1}+qm_{k-1}$ | Incluya el término $+1$ en $m_k=1+pm_{k+1}+qm_{k-1}$ porque, independientemente de ganar o perder, ya se ha efectuado una apuesta al transicionar desde $k$. |
| `D-Hab08-02` | Frontera no nula en origen | skipped_step | high | $m_0=1$ y $m_N=0$ | Recuerde que tanto en $0$ como en $N$ el juego ya ha terminado, por lo que no restan apuestas por jugar y ambas fronteras valen cero: $m_0=0$ y $m_N=0$. |
| `D-Hab08-03` | Signo invertido en q-p | conceptual_swap | high | $m_k=\frac{1}{p-q}\left(k-N\frac{1-(q/p)^k}{1-(q/p)^N}\right)$ | Verifique el signo del factor global $1/(q-p)$ comprobando que $m_k > 0$ para todo $0 < k < N$ tanto cuando $p>q$ como cuando $p<q$. |
| `D-Hab08-04` | Linealiza caso simétrico | conceptual_swap | high | $m_k=N-k$ o $k/N$ cuando $p=q$ | Note que la duración esperada simétrica $m_k=k(N-k)$ es una parábola cóncava que se anula en $0$ y $N$ y alcanza su máximo $(N/2)^2$ en $k=N/2$. |
| `D-Hab08-05` | Signo erróneo en 1/p | conceptual_swap | high | $m_{k+1}-m_k=\frac{q}{p}(m_k-m_{k-1})+\frac{1}{p}$ | Despeje cuidadosamente $pm_{k+1}=m_k-1-qm_{k-1}$ usando $m_k=(p+q)m_k$ para obtener el término $-1/p$ con signo negativo. |
| `D-Hab08-06` | Fórmula asimétrica en p=q | conceptual_swap | high | Evalúa $\frac{1}{q-p}(\dots)$ cuando $p=q=1/2$ | Aplique la expresión cuadrática $m_k=k(N-k)$ específicamente en el régimen simétrico $p=q=1/2$, reservando el cociente con $q-p$ para $p \neq q$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab08-01` | - | Tiempo de absorción $\tau$ finito casi seguramente con $0 \le k \le N$ | Si el juego pudiera continuar indefinidamente sin absorción, $m_k$ podría diverger. | - |

---
