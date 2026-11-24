# Cognitive Task Analysis (CTA): Estadistica 3 Pre Cl K3

- **Course ID:** `estadistica_3_pre_cl_k3`
- **Macro-Competency:** Dominio y aplicación analítica integral de Estadistica 3 Pre Cl K3
- **Structure:** 18 total competencies (0 Facts, 10 Concepts, 8 Skills) with 78 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Sigma-Álgebra Generada e Información Observable | Concept | Evaluate | Unidad 3: Sigma-Álgebra Generada e Información Observable | - | 3 |
| `Hab-01` | Particiones Atómicas y Conteo en Espacios Finitos | Skill | Evaluate | Unidad 3: Particiones Atómicas y Conteo en Espacios Finitos | C-01 | 6 |
| `C-02` | Sigma-Álgebra de Borel y Generadores Equivalentes | Concept | Analyze | Unidad 4: Sigma-Álgebra de Borel y Generadores Equivalentes | C-01 | 3 |
| `C-03` | Mapas Medibles, Preimágenes y Lema del Generador | Concept | Evaluate | Unidad 5: Mapas Medibles, Preimágenes y Lema del Generador | C-01, C-02 | 3 |
| `Hab-02` | Criterio de Constancia sobre Átomos y Sigma(X) | Skill | Evaluate | Unidad 5: Criterio de Constancia sobre Átomos y Sigma(X) | Hab-01, C-03 | 6 |
| `Hab-03` | Filtraciones, Procesos Adaptados y Refinamiento Atómico | Skill | Analyze | Unidad 6: Filtraciones, Procesos Adaptados y Refinamiento Atómico | C-03, Hab-02 | 6 |
| `C-04` | Definición de Esperanza Condicional | Concept | Evaluate | Unidad 2: Definición de Esperanza Condicional | C-03 | 3 |
| `Hab-04` | Propiedades Algebraicas y Ley de Adam | Skill | Evaluate | Unidad 3: Propiedades Algebraicas y Ley de Adam | C-04 | 6 |
| `C-05` | Proyección Ortogonal en Espacio L2 | Concept | Evaluate | Unidad 4: Proyección Ortogonal en Espacio L2 | Hab-04 | 3 |
| `Hab-05` | Varianza Condicional y Ley de Eve | Skill | Evaluate | Unidad 5: Varianza Condicional y Ley de Eve | Hab-04 | 6 |
| `C-06` | Propiedad Torre y Martingalas por Átomos | Concept | Evaluate | Unidad 6: Propiedad Torre y Martingalas | C-04, Hab-04 | 3 |
| `C-07` | Contraejemplos y Límites de Supuestos | Concept | Evaluate | Unidad 7: Contraejemplos y Límites de Supuestos | C-05, Hab-05 | 3 |
| `C-08` | Espacio Parametral y Trayectorias | Concept | Analyze | Unidad 1: Espacio Parametral y Trayectorias | C-03 | 3 |
| `C-09` | Dependencia Markoviana y Martingalas Discretas | Concept | Evaluate | Unidad 4: Dependencia Markoviana y Martingalas | C-08, C-04 | 3 |
| `Hab-06` | Momentos y Transición de Caminata | Skill | Evaluate | Unidad 10: Momentos y Transición de Caminata | C-09 | 6 |
| `C-10` | Recurrencia y Retorno al Origen | Concept | Evaluate | Unidad 12: Recurrencia y Retorno al Origen | Hab-06 | 3 |
| `Hab-07` | Probabilidad de Ruina del Jugador | Skill | Evaluate | Unidad 18: Probabilidad de Ruina del Jugador | C-09, Hab-06 | 6 |
| `Hab-08` | Duración Esperada Antes de Ruina | Skill | Evaluate | Unidad 20: Duración Esperada Antes de Ruina | Hab-07 | 6 |

---

## Detailed Competency Specifications

### [C-01] Sigma-Álgebra Generada e Información Observable (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Sigma-Álgebra Generada e Información Observable
- **Prerequisites:** None
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `01_measure_theory_bridge.pdf` (page 3)

#### Description & Cognitive Model
Definición y minimalidad de la $\sigma$-álgebra generada $\sigma(\mathcal{C}) := \bigcap_{\Sigma \supseteq \mathcal{C}} \Sigma$ como colección cerrada bajo complementos y uniones numerables que modela eventos decidibles.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Unión de sigma-álgebras | conceptual_swap | high | $\sigma(\mathcal{C}) = \bigcup_{\Sigma \supseteq \mathcal{C}} \Sigma$ | Recuerde que la unión de $\sigma$-álgebras no es necesariamente una $\sigma$-álgebra; la intersección arbitraria sí preserva todos los axiomas y garantiza minimalidad. |
| `D-C01-02` | Confunde F con P(Omega) | conceptual_swap | high | $\mathcal{F} = \mathcal{P}(\Omega)$ | Distinga el conjunto potencia $\mathcal{P}(\Omega)$ de una sub-$\sigma$-álgebra $\mathcal{F}$: bajo información incompleta, un evento elemental puede no ser decidible. |
| `D-C01-03` | Cierre solo finito | conceptual_swap | high | $\mathcal{F}$ cierra solo bajo uniones finitas | Exija cerradura bajo uniones numerables infinitas además de complementos y pertenencia del espacio total, pues las uniones finitas solo definen un álgebra. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | $\Omega \neq \emptyset$ y $\mathcal{P}(\Omega)$ es siempre una $\sigma$-álgebra que contiene a $\mathcal{C}$ | Si la familia de $\sigma$-álgebras que contienen a $\mathcal{C}$ fuera vacía, la intersección $\sigma(\mathcal{C})$ quedaría indefinida. | - |

---

### [Hab-01] Particiones Atómicas y Conteo en Espacios Finitos (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Particiones Atómicas y Conteo en Espacios Finitos
- **Prerequisites:** C-01
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `01_measure_theory_bridge.pdf` (page 3)

#### Description & Cognitive Model
Construcción de los $k$ átomos disjuntos $\{A_1, \dots, A_k\}$ mediante intersecciones booleanas de generadores y cálculo exacto de la cardinalidad $|\sigma(\mathcal{C})| = 2^k$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Cardinalidad ingenua por generadores | skipped_step | high | $|\sigma(\mathcal{C})| = 2^{|\mathcal{C}|}$ | Verifique primero si los generadores son disjuntos y exhaustivos; cuando se solapan o no cubren $\Omega$, debe hallar los $k$ átomos reales antes de calcular $2^k$. |
| `D-Hab01-02` | Omite átomo complementario exterior | skipped_step | high | $\bigcup_{i} C_i = \Omega$ | Compruebe si la unión de los generadores cubre todo el espacio muestral $\Omega$; si falta algún elemento, la intersección de complementos forma un átomo adicional. |
| `D-Hab01-03` | Incluye intersección vacía como átomo | conceptual_swap | high | $\emptyset$ es un átomo | Excluya todo bloque vacío antes de contar átomos: por definición, un átomo es un evento observable no vacío e indivisible de la partición. |
| `D-Hab01-04` | Cardinalidad no potencia de dos | conceptual_swap | high | $|\sigma(\mathcal{C})| \in \{3, 5, 6\}$ | Recuerde que toda $\sigma$-álgebra finita está en biyección con el conjunto potencia de sus $k$ átomos, por lo que su tamaño siempre es exactamente $2^k$. |
| `D-Hab01-05` | Subdivide un átomo en F | conceptual_swap | high | $E \subsetneq A_j$ con $E \in \sigma(\mathcal{C})$ | Aplique la indivisibilidad de los átomos: ningún subconjunto propio no vacío de un átomo $A_j$ puede pertenecer a la $\sigma$-álgebra que este genera. |
| `D-Hab01-06` | Usa uniones en vez de intersecciones | conceptual_swap | high | Átomos dados por $C_1 \cup C_2$ | Construya los átomos intersectando cada generador o su complemento, pues solo las intersecciones completas refinan los bloques hasta hacerlos disjuntos. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Los átomos $\{A_1, \dots, A_k\}$ son no vacíos, disjuntos dos a dos y su unión es $\Omega$ | Si dos bloques se solapan o queda uno vacío, la correspondencia con $\mathcal{P}(\{1, \dots, k\})$ deja de ser biyectiva. | - |

---

### [C-02] Sigma-Álgebra de Borel y Generadores Equivalentes (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 4: Sigma-Álgebra de Borel y Generadores Equivalentes
- **Prerequisites:** C-01
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `01_measure_theory_bridge.pdf` (page 4)

#### Description & Cognitive Model
Estructura de $\mathcal{B}(\mathbb{R}) := \sigma(\mathcal{O}_{\mathbb{R}})$ y equivalencia entre sus colecciones generadoras: abiertos, intervalos $(a,b)$, rayos cerrados $(-\infty,x]$ y rayos abiertos $(-\infty,x)$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Topología abierta como sigma-álgebra | conceptual_swap | high | $\mathcal{O}_{\mathbb{R}}$ es una $\sigma$-álgebra | Observe que el complemento de un abierto es cerrado y una intersección numerable de abiertos puede producir un punto cerrado, violando dos axiomas. |
| `D-C02-02` | Confunde B(R) con P(R) | conceptual_swap | high | $\mathcal{B}(\mathbb{R}) = \mathcal{P}(\mathbb{R})$ | Recuerde que una $\sigma$-álgebra solo cierra bajo uniones numerables; una unión no numerable de puntos individuales puede generar conjuntos no borelianos. |
| `D-C02-03` | Rayos cerrados insuficientes | conceptual_swap | high | $\sigma(\{(-\infty, x]\}) \subsetneq \mathcal{B}(\mathbb{R})$ | Exprese cada intervalo abierto $(a, b)$ como unión numerable de intervalos semiabiertos obtenidos por diferencia de rayos cerrados para probar la igualdad. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | $\mathbb{R}$ está dotado de la topología estándar $\mathcal{O}_{\mathbb{R}}$ y $\mathbb{Q}$ es denso y numerable | Sin una base numerable de intervalos racionales, los abiertos arbitrarios no podrían expresarse como uniones numerables de intervalos básicos. | - |

---

### [C-03] Mapas Medibles, Preimágenes y Lema del Generador (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Mapas Medibles, Preimágenes y Lema del Generador
- **Prerequisites:** C-01, C-02
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `01_measure_theory_bridge.pdf` (page 5)

#### Description & Cognitive Model
Caracterización de mapas $(\mathcal{F}\text{--}\Sigma_N)$-medibles mediante $X^{-1}(B) \in \mathcal{F}$, reducción a generadores $\mathcal{E}$ (Lema de Schuller), criterio operativo $\{X \le x\} \in \mathcal{F}$ y composición con funciones continuas.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Medibilidad con imagen directa | conceptual_swap | high | $\forall A \in \mathcal{F},\, X(A) \in \Sigma_N$ | Use siempre preimágenes $X^{-1}(\cdot)$ y nunca imágenes directas, pues la imagen directa no preserva intersecciones ni complementos cuando $X$ no es inyectiva. |
| `D-C03-02` | Dependencia de la medida P | conceptual_swap | high | La medibilidad requiere definir $\mathbb{P}$ | Separe la estructura medible de la medida: la medibilidad depende exclusivamente de las $\sigma$-álgebras de partida y llegada, sin intervención de $\mathbb{P}$. |
| `D-C03-03` | Verificación parcial de borelianos | conceptual_swap | high | Basta comprobar $X^{-1}(B) \in \mathcal{F}$ para un $B$ | Aplique el Lema del Generador sobre toda una clase generadora $\mathcal{E}$ de $\Sigma_N$, como los rayos $(-\infty, x]$ para todo $x \in \mathbb{R}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | $X^{-1}(\cdot)$ conmuta exactamente con complementos, uniones e intersecciones para toda función $X$ | Si una operación conjuntista no conmutara con $X^{-1}$, la colección de conjuntos buenos no formaría una $\sigma$-álgebra en el codominio. | - |

---

### [Hab-02] Criterio de Constancia sobre Átomos y Sigma(X) (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Criterio de Constancia sobre Átomos y Sigma(X)
- **Prerequisites:** Hab-01, C-03
- **Recommended Modalities:** open_symbolic, adversarial_break, unstructured_model
- **Evidence Citations:** `01_measure_theory_bridge.pdf` (page 5)

#### Description & Cognitive Model
Evaluación de la $\mathcal{F}$-medibilidad de una función $X: \Omega \to \mathbb{R}$ en espacios finitos comprobando si $X(\omega_1) = X(\omega_2)$ dentro de cada átomo $A_j$ y determinando $\sigma(X) := \{X^{-1}(B) : B \in \mathcal{B}(\mathbb{R})\}$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Constancia parcial en átomos | skipped_step | high | Basta que $X$ sea constante en un átomo | Evalúe $X$ sobre absolutamente todos los átomos $A_j$ de la partición: basta un único átomo donde $X$ tome dos valores distintos para romper la medibilidad. |
| `D-Hab02-02` | Ignora cambio de sigma-álgebra F | skipped_step | high | La medibilidad solo depende de la fórmula de $X$ | Recuerde que la medibilidad depende del par $(X, \mathcal{F})$: una misma función puede ser medible bajo $\mathcal{P}(\Omega)$ y no serlo bajo una $\sigma$-álgebra más gruesa. |
| `D-Hab02-03` | Verifica en generadores no disjuntos | conceptual_swap | high | Constancia en $C_i$ equivale a medibilidad | Refine primero los generadores hasta obtener los átomos de $\mathcal{F}$; una función puede variar dentro de un generador si es constante en cada sub-átomo. |
| `D-Hab02-04` | Exige valores distintos entre átomos | conceptual_swap | high | $X$ debe distinguir átomos distintos | Permita que $X$ repita valores entre átomos distintos: la condición de medibilidad exige constancia dentro de cada átomo, nunca inyectividad entre átomos. |
| `D-Hab02-05` | Usa imagen directa de átomos | conceptual_swap | high | Calcula $X(A_j)$ en lugar de $X^{-1}(\{c\})$ | Calcule la preimagen $X^{-1}(\{c\})$ de cada valor tomado por $X$ y compruebe que resulta una unión exacta de átomos perteneciente a $\mathcal{F}$. |
| `D-Hab02-06` | Duda de singletons en B(R) | conceptual_swap | high | $\{c\} \notin \mathcal{B}(\mathbb{R})$ | Recuerde que todo conjunto unitario $\{c\}$ es cerrado en $\mathbb{R}$ y por tanto pertenece a $\mathcal{B}(\mathbb{R})$, lo que valida analizar $X^{-1}(\{c\})$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | $\mathcal{F} = \sigma(\{A_1, \dots, A_k\})$ está generada por una partición finita en átomos no vacíos | En espacios infinitos continuos sin partición atómica discreta, la medibilidad debe verificarse mediante $\{X \le x\} \in \mathcal{F}$. | - |

---

### [Hab-03] Filtraciones, Procesos Adaptados y Refinamiento Atómico (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 6: Filtraciones, Procesos Adaptados y Refinamiento Atómico
- **Prerequisites:** C-03, Hab-02
- **Recommended Modalities:** fill_in_the_blank, open_symbolic, unstructured_model
- **Evidence Citations:** `01_measure_theory_bridge.pdf` (page 6)

#### Description & Cognitive Model
Análisis de filtraciones crecientes $\mathcal{F}_0 \subseteq \mathcal{F}_1 \subseteq \dots \subseteq \mathcal{F}_t$, verificación de adaptación $\sigma(X_t) \subseteq \mathcal{F}_t$ y refinamiento de átomos en la filtración natural $\mathcal{F}_t^X := \sigma(X_s : s \le t)$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Anticipación del futuro | skipped_step | high | $X_t$ es $\mathcal{F}_{t-1}$-medible | Compruebe la adaptación en el instante correspondiente $t$: un proceso adaptado exige $\sigma(X_t) \subseteq \mathcal{F}_t$, sin requerir conocerse antes en $t-1$. |
| `D-Hab03-02` | Invierte inclusión de filtración | skipped_step | high | $\mathcal{F}_t \subseteq \mathcal{F}_s$ para $s \le t$ | Mantenga el sentido creciente $\mathcal{F}_s \subseteq \mathcal{F}_t$ para $s \le t$, pues la información acumulada aumenta y nunca se olvida. |
| `D-Hab03-03` | Confunde $F_t$ con F global | conceptual_swap | high | Basta $\sigma(X_t) \subseteq \mathcal{F}$ | Exija medibilidad respecto a la sub-$\sigma$-álgebra $\mathcal{F}_t$ del instante $t$, ya que ser medible respecto a $\mathcal{F}$ global no impide usar información futura. |
| `D-Hab03-04` | No duplica átomos al refinar | conceptual_swap | high | Los átomos no se parten de $\mathcal{F}_n$ a $\mathcal{F}_{n+1}$ | Parta cada átomo de $\mathcal{F}_n$ según los nuevos resultados observables en el paso siguiente para obtener el refinamiento exacto de $\mathcal{F}_{n+1}$. |
| `D-Hab03-05` | Variable no constante en $F_0$ | conceptual_swap | high | $X$ no constante es $\mathcal{F}_0$-medible | Aplique el criterio de constancia sobre átomos al único átomo $\Omega$ de $\mathcal{F}_0$: toda variable $\mathcal{F}_0$-medible es necesariamente constante determinista. |
| `D-Hab03-06` | Confunde sigma($X_t$) con filtración natural | conceptual_swap | high | $\mathcal{F}_t^X = \sigma(X_t)$ siempre | Incluya toda la trayectoria pasada $\sigma(X_s : s \le t)$ en la filtración natural $\mathcal{F}_t^X$, salvo que $X_t$ ya codifique por sí mismo la historia previa. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | $T$ es un conjunto ordenado de tiempos y $\mathcal{F}_t \subseteq \mathcal{F}$ para todo $t \in T$ | Sin un orden temporal definido en $T$, no existe noción coherente de información pasada frente a información futura. | - |

---

### [C-04] Definición de Esperanza Condicional (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 2: Definición de Esperanza Condicional
- **Prerequisites:** C-03
- **Recommended Modalities:** multiple_select, adversarial_break, concept_matching
- **Evidence Citations:** `02_stat110_lec27_conditional_expectation.pdf` (page 2)

#### Description & Cognitive Model
Definición de la esperanza condicional $\mathbb{E}[Y\mid X]=g(X)$ como variable aleatoria $\sigma(X)$-medible bajo $Y\in L^1$, frente al escalar $\mathbb{E}[Y\mid A]$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Confundir con constante | conceptual_swap | high | $\mathbb{E}[Y\mid X]\in\mathbb{R}$ es un número fijo | Distinga el promedio dado un evento fijo del objeto aleatorio $\mathbb{E}[Y\mid X]$ que varía según el valor observado de la variable condicionante. |
| `D-C04-02` | Invertir variable condicionante | conceptual_swap | high | $\mathbb{E}[Y\mid X]=\mathbb{E}[X\mid Y]$ | Recuerde que condicionar $Y$ en $X$ proyecta sobre la información de $X$, lo cual produce una función de $X$ y no es simétrico respecto a $Y$. |
| `D-C04-03` | Omitir integrabilidad L1 | conceptual_swap | high | $\mathbb{E}[Y\mid X]$ existe siempre sin restricciones | Verifique siempre la integrabilidad absoluta $\mathbb{E}[|Y|]<\infty$ antes de definir la esperanza condicional y aplicar sus propiedades. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | Integrabilidad absoluta de la variable objetivo: $\mathbb{E}[|Y|]<\infty$ ($Y\in L^1$) | Si $Y\notin L^1$, la esperanza condicional $\mathbb{E}[Y\mid X]$ puede no existir. | - |

---

### [Hab-04] Propiedades Algebraicas y Ley de Adam (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 3: Propiedades Algebraicas y Ley de Adam
- **Prerequisites:** C-04
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `02_stat110_lec27_conditional_expectation.pdf` (page 3)

#### Description & Cognitive Model
Cálculo de esperanzas mediante linealidad, extracción de factores medibles $\mathbb{E}[h(X)Y\mid X]=h(X)\mathbb{E}[Y\mid X]$ y Ley de Adam $\mathbb{E}[\mathbb{E}[Y\mid X]]=\mathbb{E}[Y]$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Extraer variable no conocida | skipped_step | high | $\mathbb{E}[h(Y)X\mid X]=h(Y)\mathbb{E}[X\mid X]$ | Extraiga únicamente funciones de la variable condicionante $X$, ya que las funciones de $Y$ siguen siendo aleatorias al fijar la información de $X$. |
| `D-Hab04-02` | Confundir independencia con linealidad | skipped_step | high | $\mathbb{E}[Y\mid X]=Y$ | Aplique la identidad $\mathbb{E}[h(X)\mid X]=h(X)$ solo a funciones medibles de $X$; cuando $Y$ es independiente de $X$, se reduce a la media $\mathbb{E}[Y]$. |
| `D-Hab04-03` | Omitir esperanza exterior | conceptual_swap | high | $\mathbb{E}[Y\mid X]=\mathbb{E}[Y]$ siempre | Aplique el operador de esperanza exterior sobre $\mathbb{E}[Y\mid X]$ para obtener $\mathbb{E}[Y]$, pues sin iterar queda una variable aleatoria dependiente de $X$. |
| `D-Hab04-04` | Separar producto arbitrario | conceptual_swap | high | $\mathbb{E}[YZ\mid X]=\mathbb{E}[Y\mid X]\mathbb{E}[Z\mid X]$ | Use la linealidad para sumas y combinaciones lineales; la factorización de productos condicionales solo es válida bajo independencia condicional. |
| `D-Hab04-05` | Sacar factor sin integrabilidad | conceptual_swap | high | $\mathbb{E}[h(X)Y\mid X]=h(X)\mathbb{E}[Y\mid X]$ sin $L^1$ | Compruebe que el producto $h(X)Y$ sea integrable en $L^1$ antes de extraer o reintroducir el factor conocido $h(X)$ en la esperanza condicional. |
| `D-Hab04-06` | Aplicar Adam en orden inverso | conceptual_swap | high | $\mathbb{E}[Y\mid\mathbb{E}[Y\mid X]]=\mathbb{E}[Y]$ | Promedie la variable aleatoria $\mathbb{E}[Y\mid X]$ con la esperanza incondicional exterior para recuperar $\mathbb{E}[Y]$ por la Ley de Adam. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Integrabilidad de $Y$ y del producto $h(X)Y$: $Y, h(X)Y\in L^1$ | Sin integrabilidad del producto no es válido extraer ni reintroducir $h(X)$. | - |

---

### [C-05] Proyección Ortogonal en Espacio L2 (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Proyección Ortogonal en Espacio L2
- **Prerequisites:** Hab-04
- **Recommended Modalities:** proof_dag, adversarial_break, multiple_select
- **Evidence Citations:** `02_stat110_lec27_conditional_expectation.pdf` (page 4)

#### Description & Cognitive Model
Interpretación geométrica de $\mathbb{E}[Y\mid X]$ en $L^2$ como proyección ortogonal que minimiza el error cuadrático medio $\mathbb{E}[(Y-h(X))^2]$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Restringir a predictores lineales | conceptual_swap | high | Solo MCO minimiza el ECM entre funciones de $X$ | Recuerde que $\mathbb{E}[Y\mid X]$ minimiza el error cuadrático medio sobre todo el subespacio de funciones medibles $h(X)\in L^2$, no solo las lineales. |
| `D-C05-02` | Atribuir ortogonalidad a Y | conceptual_swap | high | $\mathbb{E}[Yh(X)]=0$ para toda $h(X)$ | Aplique la ortogonalidad al residuo de predicción $Y-\mathbb{E}[Y\mid X]$ y no al vector original $Y$, pues la proyección deja perpendicular el error. |
| `D-C05-03` | Invertir desigualdad pitagórica | conceptual_swap | high | $\mathbb{E}[(Y-h(X))^2]\le \mathbb{E}[(Y-\mathbb{E}[Y\mid X])^2]$ | Use la descomposición pitagórica en $L^2$ para ver que agregar $\mathbb{E}[(\mathbb{E}[Y\mid X]-h(X))^2]\ge 0$ siempre incrementa el error cuadrático. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Segundo momento finito para $Y$ y para el predictor: $Y, h(X)\in L^2$ | Si $\mathbb{E}[Y^2]=\infty$, falla el producto interno en $L^2$ y la optimalidad MSE. | - |

---

### [Hab-05] Varianza Condicional y Ley de Eve (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 5: Varianza Condicional y Ley de Eve
- **Prerequisites:** Hab-04
- **Recommended Modalities:** open_symbolic, unstructured_model, fill_in_the_blank
- **Evidence Citations:** `02_stat110_lec27_conditional_expectation.pdf` (page 5)

#### Description & Cognitive Model
Descomposición de varianza total $\operatorname{Var}(Y)=\mathbb{E}[\operatorname{Var}(Y\mid X)]+\operatorname{Var}(\mathbb{E}[Y\mid X])$ en modelos jerárquicos con $Y\in L^2$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Omitir varianza entre grupos | skipped_step | high | $\operatorname{Var}(Y)=\mathbb{E}[\operatorname{Var}(Y\mid X)]$ | Sume siempre el segundo término $\operatorname{Var}(\mathbb{E}[Y\mid X])$, que captura cuánto fluctúa la media condicional entre distintos valores de $X$. |
| `D-Hab05-02` | Invertir operadores en EVVE | skipped_step | high | $\operatorname{Var}(Y)=\operatorname{Var}(\operatorname{Var}(Y\mid X))+\mathbb{E}[\mathbb{E}[Y\mid X]]$ | Siga la mnemotecnia EVVE: tome la esperanza de la varianza condicional y la varianza de la esperanza condicional sin invertir los operadores. |
| `D-Hab05-03` | Confundir esperanza de cuadrado | conceptual_swap | high | $\operatorname{Var}(Y\mid X)=\mathbb{E}[Y^2\mid X]-\mathbb{E}[Y\mid X]$ | Eleve al cuadrado la esperanza condicional al usar la fórmula abreviada $\mathbb{E}[Y^2\mid X]-(\mathbb{E}[Y\mid X])^2$ para la varianza condicional. |
| `D-Hab05-04` | Sacar constante sin cuadrado | conceptual_swap | high | $\operatorname{Var}(nQ)=n\operatorname{Var}(Q)$ | Eleve al cuadrado cualquier constante multiplicativa al extraerla del operador varianza, tanto en $\operatorname{Var}(cU)=c^2\operatorname{Var}(U)$ como en modelos jerárquicos. |
| `D-Hab05-05` | Sumar covarianza cruzada inexistente | conceptual_swap | high | $\operatorname{Var}(Y)=\mathbb{E}[\operatorname{Var}(Y\mid X)]+\operatorname{Var}(\mathbb{E}[Y\mid X])+2\operatorname{Cov}$ | Elimine términos cruzados porque la ortogonalidad del residuo garantiza que la variabilidad intra-grupo y entre-grupos se suman directamente. |
| `D-Hab05-06` | Tratar varianza condicional como constante | conceptual_swap | high | $\operatorname{Var}(Y\mid X)\in\mathbb{R}$ fijo | Trate $\operatorname{Var}(Y\mid X)$ como una variable aleatoria función de $X$ antes de promediarla mediante la esperanza exterior en la Ley de Eve. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | Existencia del segundo momento finito: $\mathbb{E}[Y^2]<\infty$ ($Y\in L^2$) | Si $Y\in L^1\setminus L^2$, la Ley de Adam vale pero la Ley de Eve y $\operatorname{Var}(Y)$ divergen. | - |

---

### [C-06] Propiedad Torre y Martingalas por Átomos (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 6: Propiedad Torre y Martingalas
- **Prerequisites:** C-04, Hab-04
- **Recommended Modalities:** proof_dag, multiple_select, adversarial_break
- **Evidence Citations:** `02_stat110_lec27_conditional_expectation.pdf` (page 6)

#### Description & Cognitive Model
Esperanza condicional dada $\sigma$-álgebra finita como promedio por átomo, Propiedad Torre $\mathbb{E}[\mathbb{E}[Y\mid\mathcal{F}_t]\mid\mathcal{F}_s]=\mathbb{E}[Y\mid\mathcal{F}_s]$ y martingalas

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Dominio de sigma-álgebra mayor | conceptual_swap | high | $\mathbb{E}[\mathbb{E}[Y\mid\mathcal{F}_t]\mid\mathcal{F}_s]=\mathbb{E}[Y\mid\mathcal{F}_t]$ con $\mathcal{F}_s\subseteq\mathcal{F}_t$ | Aplique la regla de que la $\sigma$-álgebra más pequeña domina en la Propiedad Torre, ya que promediar sobre átomos más gruesos borra el detalle fino. |
| `D-C06-02` | Promediar sin ponderar por átomo | conceptual_swap | high | $\mathbb{E}[Y\mid\mathcal{F}](\omega)=\sum_{\omega'\in A_j}Y(\omega')\mathbb{P}(\{\omega'\})$ | Divida la suma ponderada sobre el átomo $A_j$ entre la probabilidad total del átomo $\mathbb{P}(A_j)$ para obtener una verdadera probabilidad condicional. |
| `D-C06-03` | Variar dentro del mismo átomo | conceptual_swap | high | $\mathbb{E}[Y\mid\mathcal{F}]$ toma valores distintos en $A_j$ | Garantice que $\mathbb{E}[Y\mid\mathcal{F}]$ sea constante sobre cada átomo $A_j$ de la partición para asegurar su medibilidad respecto a $\mathcal{F}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Anidamiento de filtración $\mathcal{F}_s\subseteq\mathcal{F}_t$ para $s\le t$ e integrabilidad $Y\in L^1$ | Sin anidamiento de información no domina la $\sigma$-álgebra menor en la torre. | - |

---

### [C-07] Contraejemplos y Límites de Supuestos (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 7: Contraejemplos y Límites de Supuestos
- **Prerequisites:** C-05, Hab-05
- **Recommended Modalities:** adversarial_break, multiple_select, invariant_canvas
- **Evidence Citations:** `02_stat110_lec27_conditional_expectation.pdf` (page 7)

#### Description & Cognitive Model
Diagnóstico de falacias: $\mathbb{E}[Y\mid X]=\mathbb{E}[Y]$ no implica independencia, omisión de barra condicional en varianza y ruptura de $L^2$

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Asumir recíproco de independencia | conceptual_swap | high | $\mathbb{E}[Y\mid X]=\mathbb{E}[Y]\Rightarrow X\perp Y$ | Verifique si existe dependencia no lineal en momentos superiores o en el soporte condicional, pues la media condicional constante no garantiza independencia. |
| `D-C07-02` | Omitir barra en varianza condicional | conceptual_swap | high | $\operatorname{Var}(Y\mid X)=\mathbb{E}[(Y-\mathbb{E}[Y\mid X])^2]$ | Incluya siempre el condicionamiento exterior $|X$ dentro de la definición de $\operatorname{Var}(Y\mid X)$; sin la barra se obtiene el escalar $\mathbb{E}[\operatorname{Var}(Y\mid X)]$. |
| `D-C07-03` | Aplicar Eve con segundo momento infinito | conceptual_swap | high | Si $Y\in L^1\setminus L^2$, vale la Ley de Eve | Exija $\mathbb{E}[Y^2]<\infty$ antes de usar varianza condicional, proyección óptima o Ley de Eve; con solo $Y\in L^1$ únicamente sobrevive la Ley de Adam. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Verificación explícita de momentos finitos ($L^1$ o $L^2$) y dependencia funcional no lineal | Asumir independencia o varianza finita sin verificar supuestos produce inferencias falsas. | - |

---

### [C-08] Espacio Parametral y Trayectorias (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 1: Espacio Parametral y Trayectorias
- **Prerequisites:** C-03
- **Recommended Modalities:** concept_matching, multiple_select, adversarial_break
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 1)

#### Description & Cognitive Model
Definición de proceso estocástico $\{X_t:t\in T\}$ sobre $(\Omega,\mathscr{F},P)$ con espacio de estados $S$, distinción entre tiempo discreto y continuo, y dualidad entre variable aleatoria $\omega\mapsto X_t(\omega)$ y trayectoria $t\mapsto X_t(\omega)$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Confunde trayectoria y variable | conceptual_swap | high | $t\mapsto X_t(\omega)$ es una variable aleatoria | Fije primero $\omega\in\Omega$ para obtener una función determinista del tiempo llamada trayectoria, y fije $t\in T$ para obtener una variable aleatoria sobre $\Omega$. |
| `D-C08-02` | Invierte espacio parametral y estados | conceptual_swap | high | $T$ es el conjunto de valores que toma $X_t$ | Distinga el conjunto de índices temporales $T$ (espacio parametral) del conjunto $S$ donde toma valores cada variable $X_t$ (espacio de estados). |
| `D-C08-03` | Variables independientes obligatorias | conceptual_swap | high | $X_{t_1},\dots,X_{t_k}$ son siempre independientes | Recuerde que en un proceso estocástico general las variables $X_t$ suelen guardar dependencia temporal; la independencia es solo un caso particular. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C08-01` | - | Espacio de probabilidad $(\Omega,\mathscr{F},P)$ y $\sigma$-álgebra asociada a $S$ | Sin estructura medible en $\Omega$ y $S$, $X_t$ no constituye una variable aleatoria bien definida. | - |

---

### [C-09] Dependencia Markoviana y Martingalas Discretas (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Dependencia Markoviana y Martingalas
- **Prerequisites:** C-08, C-04
- **Recommended Modalities:** multiple_select, adversarial_break, proof_dag
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 4)

#### Description & Cognitive Model
Caracterización de la propiedad de Markov $P(X_{n+1}=x_{n+1}\mid X_0=x_0,\dots,X_n=x_n)=P(X_{n+1}=x_{n+1}\mid X_n=x_n)$, incrementos independientes o estacionarios, estacionariedad estricta y condición de martingala $E(X_{n+1}\mid X_0=x_0,\dots,X_n=x_n)=x_n$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Confunde Markov con independencia | conceptual_swap | high | $P(X_{n+1}=x_{n+1}\mid X_n=x_n)=P(X_{n+1}=x_{n+1})$ | Conserve el estado presente $X_n=x_n$ en el condicionamiento: la propiedad de Markov descarta el pasado estricto $X_0,\dots,X_{n-1}$, no el presente. |
| `D-C09-02` | Confunde estacionariedad e incrementos | conceptual_swap | high | $X_{t+h}$ tiene la misma ley que $X_t$ si tiene incrementos estacionarios | Separe la invariancia temporal de los desplazamientos $X_t-X_s$ (incrementos estacionarios) de la invariancia distribucional de los niveles $(X_{t_1},\dots,X_{t_n})$. |
| `D-C09-03` | Confunde martingala con constancia | conceptual_swap | high | $X_{n+1}=X_n$ casi seguramente | Aplique la esperanza condicional en la definición de martingala: el juego es justo en promedio $E(X_{n+1}\mid X_0,\dots,X_n)=X_n$, aunque $X_{n+1}$ sea aleatorio. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | Existencia de esperanzas finitas $E(|X_n|)<\infty$ para definir martingalas | Si la esperanza no es finita, la esperanza condicional $E(X_{n+1}\mid X_0,\dots,X_n)$ queda indeterminada. | - |

---

### [Hab-06] Momentos y Transición de Caminata (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 10: Momentos y Transición de Caminata
- **Prerequisites:** C-09
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 10)

#### Description & Cognitive Model
Cálculo de esperanza $E(X_n)=n(p-q)$, varianza $\mathrm{Var}(X_n)=4npq$ y probabilidades de transición en $n$ pasos $P(X_n=x\mid X_0=y)=\binom{n}{\frac{1}{2}(n+x-y)}p^{\frac{1}{2}(n+x-y)}q^{\frac{1}{2}(n-x+y)}$ en una caminata aleatoria simple sobre $\mathbb{Z}$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Varianza sin factor cuatro | skipped_step | high | $\mathrm{Var}(X_n)=npq$ | Considere que cada paso $\xi_i\in\{-1,+1\}$ tiene amplitud $2$, por lo que $\mathrm{Var}(\xi_i)=1-(p-q)^2=4pq$ y al sumar $n$ pasos resulta $4npq$. |
| `D-Hab06-02` | Omite restricción de paridad | skipped_step | high | $P(X_n=x\mid X_0=y)>0$ para todo $x$ en $[-n+y,n+y]$ | Verifique primero que $n$ y $x-y$ sean ambos pares o ambos impares y que $|x-y|\le n$; de otro modo $\frac{1}{2}(n+x-y)$ no es entero y la probabilidad es cero. |
| `D-Hab06-03` | Usa x en lugar de desplazamiento | conceptual_swap | high | $\binom{n}{\frac{1}{2}(n+x)}p^{\frac{1}{2}(n+x)}q^{\frac{1}{2}(n-x)}$ con $X_0=y$ | Desplace la coordenada final restando el estado inicial $y$, es decir, use $x-y$ en lugar de $x$ para reducir el problema a una caminata iniciada en cero. |
| `D-Hab06-04` | Intercambia exponentes p y q | conceptual_swap | high | $p^{\frac{1}{2}(n-x+y)}q^{\frac{1}{2}(n+x-y)}$ | Recuerde que el número de pasos a la derecha es $R_n=\frac{1}{2}(n+x-y)$, por lo cual ese exponente corresponde a la probabilidad $p$ de avanzar a la derecha. |
| `D-Hab06-05` | Esperanza con suma p más q | conceptual_swap | high | $E(X_n)=n(p+q)=n$ | Calcule $E(\xi)=(+1)p+(-1)q=p-q$ atendiendo al signo negativo del paso hacia la izquierda antes de multiplicar por el número de pasos $n$. |
| `D-Hab06-06` | Factor binomial en lugar de potencia | conceptual_swap | high | $\mathrm{Var}(X_n)=4pq$ | Sume las varianzas de los $n$ incrementos independientes e idénticamente distribuidos $\xi_1,\dots,\xi_n$ para obtener $\mathrm{Var}(X_n)=n\mathrm{Var}(\xi)=4npq$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Incrementos $\xi_i\in\{-1,+1\}$ independientes con $p+q=1$ y $p,q\in(0,1)$ | Si los pasos no son independientes o permiten permanencia, la distribución de $R_n$ deja de ser $\mathrm{Bin}(n,p)$. | - |

---

### [C-10] Recurrencia y Retorno al Origen (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 12: Recurrencia y Retorno al Origen
- **Prerequisites:** Hab-06
- **Recommended Modalities:** proof_dag, adversarial_break, invariant_canvas
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 12)

#### Description & Cognitive Model
Probabilidad de eventual regreso al origen en una caminata aleatoria simple sobre $\mathbb{Z}$ dada por $1-|p-q|$ mediante funciones generadoras $G(t)=1-(1-4pqt^2)^{1/2}$: retorno seguro solo si $p=q=1/2$ con tiempo promedio infinito, y retorno menor que $1$ si $p\neq q$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C10-01` | Tiempo medio finito si p igual q | conceptual_swap | high | $\sum_{n=0}^\infty n f_n<\infty$ cuando $p=q=1/2$ | Distinga certeza de retorno ($\lim_{t\nearrow 1}G(t)=1$) de finitud de la esperanza: al derivar $G(t)=1-(1-t^2)^{1/2}$ resulta $\lim_{t\nearrow 1}G'(t)=\infty$. |
| `D-C10-02` | Retorno seguro en caso asimétrico | conceptual_swap | high | $P(\text{regreso})=1$ para todo $p\in(0,1)$ | Evalúe $1-|p-q|=1-(1-4pq)^{1/2}$: cuando $p\neq q$ se tiene $|p-q|>0$, de modo que la probabilidad de regreso eventual es estrictamente menor que $1$. |
| `D-C10-03` | Confunde $p_n$ con $f_n$ | conceptual_swap | high | $p_n=f_n$ para todo $n\ge 1$ | Diferencie $p_n=P(X_n=0\mid X_0=0)$ (visita en $n$, no necesariamente primera) de $f_n$ (primera visita en $n$), ligadas por la convolución $p_n=\sum_{k=0}^n f_k p_{n-k}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C10-01` | - | Caminata homogénea irreducible en $\mathbb{Z}$ con $p+q=1$ sin estados absorbentes | En presencia de barreras absorbentes o pasos nulos, la función generadora $G(t)$ cambia. | - |

---

### [Hab-07] Probabilidad de Ruina del Jugador (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 18: Probabilidad de Ruina del Jugador
- **Prerequisites:** C-09, Hab-06
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 18)

#### Description & Cognitive Model
Planteamiento y resolución de la ecuación en diferencias homogénea $u_k=pu_{k+1}+qu_{k-1}$ con condiciones de frontera $u_0=1$ y $u_N=0$ para la probabilidad de ruina $u_k=P(X_\tau=0\mid X_0=k)$ en los casos $p=1/2$ y $p\neq 1/2$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Invierte condiciones de frontera | skipped_step | high | $u_0=0$ y $u_N=1$ | Verifique el significado del estado absorbente: si el jugador inicia en $0$ ya está arruinado ($u_0=1$), y si inicia en $N$ ya ganó todo el capital ($u_N=0$). |
| `D-Hab07-02` | Aplica fórmula simétrica cuando p distinto q | skipped_step | high | $u_k=\frac{N-k}{N}$ para todo $p\in(0,1)$ | Compruebe si $p=1/2$ antes de elegir la rama de la solución: cuando $p\neq 1/2$ la suma $S_k=\sum_{i=0}^k (q/p)^i$ es geométrica y produce cocientes de potencias de $q/p$. |
| `D-Hab07-03` | Usa razón p entre q | conceptual_swap | high | $u_k=\frac{(p/q)^k-(p/q)^N}{1-(p/q)^N}$ | Reescriba $u_k=(p+q)u_k=pu_{k+1}+qu_{k-1}$ para obtener $u_{k+1}-u_k=(q/p)(u_k-u_{k-1})$, de donde la razón geométrica correcta de la ruina es $q/p$. |
| `D-Hab07-04` | Calcula probabilidad de victoria | conceptual_swap | high | $u_k=\frac{k}{N}$ para $p=1/2$ | Recuerde que $u_k$ mide la ruina (absorción en $0$), la cual decrece al aumentar el capital inicial $k$; $k/N$ corresponde a la absorción en $N$ cuando $p=1/2$. |
| `D-Hab07-05` | Omite restar término en N | conceptual_swap | high | $u_k=\frac{(q/p)^k}{1-(q/p)^N}$ | Asegúrese de que la fórmula satisfaga la frontera $u_N=0$: restar $(q/p)^N$ en el numerador anula $u_k$ exactamente cuando $k=N$. |
| `D-Hab07-06` | Índice de suma $S_k$ erróneo | conceptual_swap | high | $u_k=1-\frac{S_k}{S_N}$ | Cuente los términos al sumar desde $u_2-u_1$ hasta $u_k-u_{k-1}$: son $k-1$ ecuaciones cuya suma involucra $S_{k-1}$ y al imponer $u_N=0$ aparece $S_{N-1}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Estados absorbentes $0$ y $N$, sin empates ($p+q=1$) y tiempo finito $\tau<\infty$ c.s. | Si hay empates ($r>0$) o barreras reflejantes, la ecuación en diferencias cambia sus coeficientes o fronteras. | - |

---

### [Hab-08] Duración Esperada Antes de Ruina (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 20: Duración Esperada Antes de Ruina
- **Prerequisites:** Hab-07
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, adversarial_break
- **Evidence Citations:** `03_rincon_cl_caps1_2.pdf` (page 20)

#### Description & Cognitive Model
Planteamiento y resolución de la ecuación en diferencias no homogénea $m_k=1+pm_{k+1}+qm_{k-1}$ con fronteras $m_0=0$ y $m_N=0$ para el número esperado de apuestas $m_k$ antes de la ruina, obteniendo $m_k=k(N-k)$ si $p=q$ y su expresión explícita si $p\neq q$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | Omite término independiente uno | skipped_step | high | $m_k=pm_{k+1}+qm_{k-1}$ | Incluya el $+1$ correspondiente a la primera apuesta realizada desde el estado $k$ antes de transicionar a $k+1$ o $k-1$ por probabilidad total. |
| `D-Hab08-02` | Frontera $m_0$ igual uno | skipped_step | high | $m_0=1$ y $m_N=0$ | Distinga el tiempo esperado de absorción de la probabilidad de ruina: si el proceso inicia en cualquiera de los estados absorbentes $0$ o $N$, el juego termina de inmediato y $m_0=m_N=0$. |
| `D-Hab08-03` | Signo invertido en q menos p | conceptual_swap | high | $m_k=\frac{1}{p-q}\left(k-N\frac{1-(q/p)^k}{1-(q/p)^N}\right)$ | Verifique el signo del factor $1/(q-p)$ exigiendo que $m_k>0$ para $0<k<N$: cuando $p>q$, $q-p<0$ y el paréntesis también es negativo, manteniendo positiva la duración esperada. |
| `D-Hab08-04` | Usa fórmula simétrica siempre | conceptual_swap | high | $m_k=k(N-k)$ para todo $p\in(0,1)$ | Compruebe la simetría $p=q=1/2$ antes de usar $k(N-k)$; en juegos asimétricos ($p\neq q$) la deriva acelera la absorción y reduce el número esperado de apuestas. |
| `D-Hab08-05` | Máximo en frontera | conceptual_swap | high | $m_k$ alcanza su máximo cuando $k=1$ o $k=N-1$ | Observe que cuando $p=1/2$, la parábola $m_k=k(N-k)$ se anula en $0$ y $N$ y alcanza su máximo $(N/2)^2$ en el punto medio $k=N/2$. |
| `D-Hab08-06` | Signo positivo en término 1/p | conceptual_swap | high | $m_{k+1}-m_k=\frac{q}{p}(m_k-m_{k-1})+\frac{1}{p}$ | Despeje con cuidado desde $pm_{k+1}-pm_k=qm_k-qm_{k-1}-1$: al dividir entre $p$, el término independiente pasa con signo negativo $-1/p$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab08-01` | - | Fronteras absorbentes $m_0=m_N=0$ y duración finita casi seguramente ($p,q>0$) | Si $p=0$ o $q=0$, el denominador o la razón $q/p$ se indetermina y el juego es determinista. | - |

---
