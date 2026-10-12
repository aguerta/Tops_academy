# Cognitive Task Analysis (CTA): El Modelo de Crecimiento de Solow (1956)

**Curso:** El Modelo de Crecimiento Económico de Solow (1956) (`solow_growth_model`)
**Macro-competencia:** Comprender, formular y resolver dinámicamente el modelo neoclásico de crecimiento económico de Solow (1956), analizando sus propiedades de estabilidad, implicaciones de precios factoriales, dinámicas de transición y extensiones analíticas.

## Resumen del Currículo Cognitivo y Triada de Conocimiento

- **Total de Competencias:** 25
  - Hechos [H] (`fact`): 5
  - Conceptos [C] (`concept`): 12
  - Habilidades [Hab] (`skill`): 8
- **Total de Distractores Fused:** 99

---

## Sesión 1: Fundamentos y Ecuación Diferencial Fundamental de Solow

### `H-01`: Definición e Identidad del Ratio Capital-Trabajo Intensivo $k \equiv K/L$ y Homogeneidad de Grado Uno
- **Tipo:** `fact` | **Nivel Bloom:** `Remember` | **Unidad:** `1`
- **Descripción:** Identificar la definición matemática del ratio capital-trabajo $k \equiv \frac{K}{L}$ y la propiedad de homogeneidad lineal de la función de producción neoclásica $Q = f(K, L) = L f\left(\frac{K}{L}, 1\right) = L\phi(k)$, donde $\phi(k)$ representa el producto medio del trabajo $\text{APP}_L$.
- **Prerrequisitos:** Ninguno (nodo raíz)
- **Evidencia:** [05_15_07_El_modelo_de_crecimiento_de_Solow.pdf, pág. 2]
- **Distractores (3):**
  - `D-H01-01` (conceptual_swap, severidad `high`): **Confusión entre ratio capital-trabajo y ratio capital-producto**
    - *Creencia errónea:* El estudiante asume que $k$ representa la relación capital-producto $K/Q$ en lugar de capital-trabajo $K/L$.
    - *Manifestación:* $k = K/Q$ lo que distorsiona la forma intensiva en $\phi(k) = 1/k$.
    - *Remediación:* Recuerde que en el modelo de Solow la variable intensiva clave es $k \equiv K/L$, el capital por trabajador, mientras que el ratio capital-producto es $K/Q = k/\phi(k)$.
  - `D-H01-02` (overgeneralization, severidad `medium`): **Violación de la homogeneidad lineal al dividir por $L$**
    - *Creencia errónea:* Creer que cualquier función de producción puede expresarse como $Q = L\phi(K/L)$ sin requerir rendimientos constantes a escala.
    - *Manifestación:* Escribir $Q = L\phi(k)$ para una función con rendimientos a escala de grado $\gamma \ne 1$ sin el factor $L^\gamma$.
    - *Remediación:* La reducción de $Q = f(K, L)$ a $Q = L\phi(k)$ sólo es válida si $f$ es homogénea de grado 1. Si los rendimientos a escala fueran distintos, $L$ aparecería elevado a una potencia distinta de la unidad.
  - `D-H01-03` (conceptual_swap, severidad `medium`): **Interpretación errónea de $\phi(k)$ como producto marginal en vez de medio**
    - *Creencia errónea:* Interpretar $\phi(k)$ como el producto marginal del trabajo en lugar del producto por trabajador (producto medio).
    - *Manifestación:* Asignar $\text{MPP}_L = \phi(k)$ ignorando que $\text{MPP}_L = \phi(k) - k\phi'(k)$.
    - *Remediación:* Por definición, $\phi(k) \equiv Q/L$ mide el producto medio de la mano de obra. El producto marginal de $K$ es $\phi'(k)$ y el del trabajo es $\phi(k) - k\phi'(k)$.

### `C-01`: Propiedades de Concavidad y Derivadas de la Función de Producción Intensiva $\phi(k)$
- **Tipo:** `concept` | **Nivel Bloom:** `Understand` | **Unidad:** `2`
- **Descripción:** Comprender la relación analítica entre las productividades marginales en niveles ($f_K > 0, f_{KK} < 0$) y las derivadas de la forma intensiva: $\phi'(k) = f_K > 0$ y $\phi''(k) = L f_{KK} < 0$, garantizando rendimientos decrecientes del capital por trabajador.
- **Prerrequisitos:** `H-01`
- **Evidencia:** [05_15_07_El_modelo_de_crecimiento_de_Solow.pdf, pág. 2]
- **Distractores (3):**
  - `D-C01-01` (procedural_slip, severidad `medium`): **Confusión de la regla de la cadena al derivar $\phi'(k)$ respecto a $K$**
    - *Creencia errónea:* El estudiante olvida que $\partial k/\partial K = 1/L$, concluyendo incorrectamente que $f_{KK} = \phi''(k)$ sin normalizar por $L$.
    - *Manifestación:* $f_{KK} = \phi''(k)$, omitiendo el factor escalar $1/L$.
    - *Remediación:* Al derivar $\phi'(k)$ respecto a $K$, aplique la regla de la cadena: $\frac{\partial \phi'(k)}{\partial K} = \phi''(k) \frac{\partial k}{\partial K} = \phi''(k)\frac{1}{L}$.
  - `D-C01-02` (conceptual_swap, severidad `high`): **Creencia errónea de que $\phi'(k)$ representa el producto marginal del trabajo**
    - *Creencia errónea:* Suponer que derivar $\phi(k)$ con respecto a $k$ entrega el producto marginal del trabajo $\text{MPP}_L$.
    - *Manifestación:* Escribir $\text{MPP}_L = \phi'(k)$ en vez de $\text{MPP}_K = \phi'(k)$.
    - *Remediación:* Derivar $Q = L\phi(k)$ respecto a $K$ da $\frac{\partial Q}{\partial K} = L \phi'(k) \frac{1}{L} = \phi'(k)$. Por ende, $\phi'(k)$ es el producto marginal del capital.
  - `D-C01-03` (overgeneralization, severidad `medium`): **Suposición de convexidad de $\phi(k)$ por retornos constantes a escala**
    - *Creencia errónea:* Creer que como la función global $f(K,L)$ tiene rendimientos constantes a escala, $\phi''(k)$ debe ser nula o positiva.
    - *Manifestación:* Graficar $\phi(k)$ como una recta lineal o curva convexa hacia arriba.
    - *Remediación:* Los rendimientos constantes a escala operan al variar ambos insumos simultáneamente. Al variar únicamente el capital por trabajador $k$, rige la ley de rendimientos decrecientes: $\phi''(k) < 0$.

### `Hab-01`: Deducción Algebraica de la Ecuación Fundamental $\dot{k} = s\phi(k) - \lambda k$
- **Tipo:** `skill` | **Nivel Bloom:** `Apply` | **Unidad:** `3`
- **Descripción:** Deducir algebraicamente la ecuación diferencial de primer orden $\dot{k} = s\phi(k) - \lambda k$ a partir de la regla del producto aplicada a la identidad $K = kL$, la condición de inversión $\dot{K} = sQ = sL\phi(k)$ y la tasa de crecimiento poblacional $\dot{L}/L = \lambda$.
- **Prerrequisitos:** `H-01`, `C-01`
- **Evidencia:** [05_15_07_El_modelo_de_crecimiento_de_Solow.pdf, pág. 2], [05_15_07_El_modelo_de_crecimiento_de_Solow.pdf, pág. 3]
- **Distractores (6):**
  - `D-Hab01-01` (sign_error, severidad `high`): **Error de signo en el término de dilución poblacional**
    - *Creencia errónea:* Sumar en lugar de restar el término $\lambda k$ al despejar $\dot{k}$.
    - *Manifestación:* $\dot{k} = s\phi(k) + \lambda k$.
    - *Remediación:* Al despejar $\dot{k}$ de $L\dot{k} + \lambda k L = sL\phi(k)$, el término $\lambda k L$ pasa restando al miembro derecho, resultando en $\dot{k} = s\phi(k) - \lambda k$.
  - `D-Hab01-02` (skipped_step, severidad `high`): **Omisión de la diferenciación del factor trabajo en la regla del producto** *(Paso omitido: Aplicar la derivada temporal al factor $L(t)$ dentro de la identidad $K = kL$ mediante la regla del producto.)*
    - *Manifestación:* Escribir $\dot{K} = L\dot{k}$ y obtener erróneamente $\dot{k} = s\phi(k)$ sin el término $-\lambda k$.
    - *Remediación:* Recuerde que $L$ varía en el tiempo según $\dot{L} = \lambda L$. Por la regla del producto, $\frac{d}{dt}(kL) = L\dot{k} + k\dot{L}$.
  - `D-Hab01-03` (skipped_step, severidad `medium`): **Olvidar simplificar el factor común de escala $L$** *(Paso omitido: Dividir la ecuación agregada de acumulación por el tamaño de la fuerza laboral $L$.)*
    - *Manifestación:* $\dot{k} = s\phi(k) - \lambda k L$ o mantener dependencias de escala en la ecuación intensiva.
    - *Remediación:* Una vez igualados los dos términos de $\dot{K}$, factorice y cancele $L$ en todos los sumandos para obtener una ecuación diferencial autónoma pura en $k$.
  - `D-Hab01-04` (procedural_slip, severidad `high`): **Sustitución incorrecta de la tasa de crecimiento de la población**
    - *Creencia errónea:* Reemplazar $\dot{L}$ directamente por $\lambda$ en lugar de $\lambda L$.
    - *Manifestación:* $k\dot{L} = k\lambda$, conduciendo a $\dot{k} = s\phi(k) - \frac{\lambda k}{L}$.
    - *Remediación:* La tasa $\lambda$ es relativa ($\dot{L}/L = \lambda$). Por tanto, la derivada absoluta es $\dot{L} = \lambda L$. Al sustituir en $k\dot{L}$, queda $\lambda k L$.
  - `D-Hab01-05` (unit_or_scale, severidad `medium`): **Confusión entre propensión al ahorro $s$ y nivel de ahorro $S$**
    - *Creencia errónea:* Interpretar el parámetro $s$ como el ahorro total $S$ en unidades monetarias en vez de una fracción constante de $Q$.
    - *Manifestación:* Escribir $\dot{K} = s$ o dividir $s$ por $Q$.
    - *Remediación:* Recuerde que $s$ es un coeficiente adimensional entre 0 y 1. La inversión total es $sQ = sL\phi(k)$.
  - `D-Hab01-06` (conceptual_swap, severidad `high`): **Inversión de los roles de $k$ y $\phi(k)$ en los términos de la ecuación**
    - *Creencia errónea:* Asignar la tasa demográfica a la función de producción y el ahorro al término lineal.
    - *Manifestación:* $\dot{k} = \lambda \phi(k) - s k$.
    - *Remediación:* El término positivo que acumula capital proviene del ahorro ($s\phi(k)$) y el término negativo que diluye la dotación per cápita proviene del incremento demográfico ($-\lambda k$).

### `C-02`: Análisis Cualitativo del Diagrama de Fase y Estabilidad Asintótica del Equilibrio $\bar{k}$
- **Tipo:** `concept` | **Nivel Bloom:** `Analyze` | **Unidad:** `4`
- **Descripción:** Interpretar la línea de fase en los paneles (a) y (b) de la Figura 15.5 de Chiang, determinando que en el punto de intersección $s\phi(\bar{k}) = \lambda \bar{k}$, la pendiente de la línea de fase es estrictamente negativa $\left.\frac{d\dot{k}}{dk}\right|_{k=\bar{k}} < 0$, garantizando estabilidad dinámica asintótica global.
- **Prerrequisitos:** `Hab-01`
- **Evidencia:** [05_15_07_El_modelo_de_crecimiento_de_Solow.pdf, pág. 3]
- **Distractores (3):**
  - `D-C02-01` (conceptual_swap, severidad `high`): **Criterio de estabilidad invertido para ecuaciones diferenciales continuas**
    - *Creencia errónea:* Creer que la estabilidad dinámica exige pendiente positiva de la línea de fase, confundiendo el criterio continuo con el de ecuaciones en diferencias.
    - *Manifestación:* Declarar inestable un equilibrio con pendiente negativa $\frac{d\dot{k}}{dk} < 0$.
    - *Remediación:* En tiempo continuo, si $k < \bar{k}$ se necesita $\dot{k} > 0$ (flecha hacia la derecha) y si $k > \bar{k}$ se necesita $\dot{k} < 0$ (flecha hacia la izquierda), lo cual exige que la curva cruce el eje horizontal con pendiente estrictamente negativa.
  - `D-C02-02` (boundary_case, severidad `medium`): **Identificar el origen $k = 0$ como equilibrio económico estable**
    - *Creencia errónea:* Asumir que como $\dot{k} = 0$ en $k = 0$, el origen es un equilibrio operativo de la economía.
    - *Manifestación:* Clasificar el punto $k = 0$ como equilibrio asintóticamente estable.
    - *Remediación:* Para $0 < k < \bar{k}$, $s\phi(k) > \lambda k \implies \dot{k} > 0$, lo que impulsa al sistema alejándolo del origen hacia $\bar{k}$.
  - `D-C02-03` (conceptual_swap, severidad `medium`): **Interpretación errónea de la distancia vertical en el Panel (a)**
    - *Creencia errónea:* Pensar que la distancia vertical entre $s\phi(k)$ y $\lambda k$ mide el producto per cápita en vez de la velocidad neta de acumulación $\dot{k}$.
    - *Manifestación:* Asignar la brecha $s\phi(k) - \lambda k$ al consumo o a la inversión bruta total.
    - *Remediación:* Por la ecuación fundamental $\dot{k} = s\phi(k) - \lambda k$, la separación vertical entre ambas curvas en el panel (a) proyecta directamente el valor de la ordenada $\dot{k}$ en el panel (b).

## Sesión 2: Dinámica de Transición, Solución Cerrada y Crecimiento Equilibrado

### `H-02`: Caracterización del Estado Uniforme ('Steady State') vs. Estado Estacionario
- **Tipo:** `fact` | **Nivel Bloom:** `Understand` | **Unidad:** `5`
- **Descripción:** Diferenciar conceptualmente el estado uniforme ('steady state'), en el cual las variables agregadas $K, L, Q$ crecen a la tasa constante idéntica $\lambda$ manteniendo constantes los ratios intensivos ($k = \bar{k}, q = \phi(\bar{k})$), del estado estacionario ('stationary state') donde todas las tasas de crecimiento son cero.
- **Prerrequisitos:** `C-02`
- **Evidencia:** [05_15_07_El_modelo_de_crecimiento_de_Solow.pdf, pág. 4]
- **Distractores (3):**
  - `D-H02-01` (conceptual_swap, severidad `high`): **Confundir crecimiento cero en variables per cápita con crecimiento cero en variables agregadas**
    - *Creencia errónea:* Creer que en el estado uniforme de Solow la inversión neta y el producto agregado dejan de crecer.
    - *Manifestación:* Afirmar que $\dot{K} = 0$ y $\dot{Q} = 0$ en estado uniforme.
    - *Remediación:* En el estado uniforme las variables intensivas no cambian ($k = \text{cte}$), pero como $L$ crece a tasa $\lambda$, $K = kL$ y $Q = L\phi(k)$ crecen también exactamente a la tasa $\lambda$.
  - `D-H02-02` (notation, severidad `medium`): **Equiparar erróneamente estado uniforme y estado estacionario clásico**
    - *Creencia errónea:* Considerar que estado uniforme y estado estacionario son sinónimos idénticos en economía matemática.
    - *Manifestación:* Definir estado uniforme como una situación donde la economía deja de expandirse.
    - *Remediación:* Chiang precisa que el estado uniforme es una generalización del estado estacionario: en el estado estacionario las variables crecen a tasa cero, mientras que en el estado uniforme crecen a la tasa común $\lambda$.
  - `D-H02-03` (overgeneralization, severidad `medium`): **Asumir que la inversión neta permanece constante en lugar de crecer al ritmo $\lambda$**
    - *Creencia errónea:* Asumir que en el estado uniforme la inversión neta $\dot{K}$ es constante en el tiempo en lugar de crecer exponencialmente.
    - *Manifestación:* Escribir $\frac{d}{dt}(\dot{K}) = 0$ en lugar de $\frac{d\dot{K}/dt}{\dot{K}} = \lambda$.
    - *Remediación:* Dado que $K$ crece a tasa $\lambda$, su derivada temporal $\dot{K} = \lambda K$ también crece a la misma tasa constante $\lambda$.

### `Hab-02`: Resolución de la Ecuación de Bernoulli del Modelo de Solow con Tecnología Cobb-Douglas
- **Tipo:** `skill` | **Nivel Bloom:** `Apply` | **Unidad:** `6`
- **Descripción:** Resolver cuantitativamente la ecuación diferencial no lineal $\dot{k} + \lambda k = s k^\alpha$ mediante la sustitución de Bernoulli $z = k^{1-\alpha}$, obteniendo la ecuación linealizada $\frac{dz}{dt} + (1-\alpha)\lambda z = (1-\alpha)s$ y su trayectoria temporal exacta $k(t)^{1-\alpha} = \left[k(0)^{1-\alpha} - \frac{s}{\lambda}\right]e^{-(1-\alpha)\lambda t} + \frac{s}{\lambda}$.
- **Prerrequisitos:** `Hab-01`, `H-02`
- **Evidencia:** [05_15_07_El_modelo_de_crecimiento_de_Solow.pdf, pág. 4], [05_15_07_El_modelo_de_crecimiento_de_Solow.pdf, pág. 5]
- **Distractores (6):**
  - `D-Hab02-01` (sign_error, severidad `high`): **Error de signo en la potencia de la transformación de Bernoulli**
    - *Creencia errónea:* Definir el cambio de variable como $z = k^{\alpha - 1}$ en lugar de $z = k^{1 - \alpha}$.
    - *Manifestación:* $z = k^{\alpha - 1}$ produciendo exponentes invertidos en toda la integración.
    - *Remediación:* La fórmula general de Bernoulli para transformar una ecuación no lineal en lineal utiliza $z = y^{1-m}$, donde $m$ es el exponente no lineal. Aquí $m = \alpha$, por tanto $z = k^{1-\alpha}$.
  - `D-Hab02-02` (skipped_step, severidad `high`): **Omisión del factor $(1-\alpha)$ al transformar la derivada temporal $dz/dt$** *(Paso omitido: Multiplicar toda la ecuación diferencial por $(1-\alpha)k^{-\alpha}$ antes de introducir la variable $z$.)*
    - *Manifestación:* Escribir $\dot{z} + \lambda z = s$ omitiendo el término $(1-\alpha)$ en los coeficientes.
    - *Remediación:* Al derivar $z = k^{1-\alpha}$, aplique la regla de la cadena: $\dot{z} = (1-\alpha)k^{-\alpha}\dot{k}$. Multiplique la ecuación original por $(1-\alpha)k^{-\alpha}$ para obtener $\dot{z} + (1-\alpha)\lambda z = (1-\alpha)s$.
  - `D-Hab02-03` (skipped_step, severidad `medium`): **Olvidar invertir la potencia al despejar $k(t)$ a partir de $z(t)$** *(Paso omitido: Aplicar la raíz de orden $(1-\alpha)$ al miembro derecho para recuperar la variable primitiva $k(t) = [z(t)]^{1/(1-\alpha)}$.)*
    - *Manifestación:* Declarar $k(t) = [k(0)^{1-\alpha} - s/\lambda]e^{-(1-\alpha)\lambda t} + s/\lambda$.
    - *Remediación:* Recuerde deshacer el cambio de variable: como $z(t) = k(t)^{1-\alpha}$, la trayectoria de $k(t)$ requiere aplicar la potencia inversa: $k(t) = [z(t)]^{\frac{1}{1-\alpha}}$.
  - `D-Hab02-04` (procedural_slip, severidad `medium`): **Confusión en el exponente de convergencia temporal**
    - *Creencia errónea:* Creer que la tasa exponencial de convergencia es simplemente $-\lambda t$ ignorando el coeficiente de escala $(1-\alpha)$.
    - *Manifestación:* Escribir $e^{-\lambda t}$ en la solución general de $z(t)$.
    - *Remediación:* El coeficiente lineal de la ecuación en $z$ es $a = (1-\alpha)\lambda$. Por ende, la solución exponencial es $e^{-a t} = e^{-(1-\alpha)\lambda t}$.
  - `D-Hab02-05` (procedural_slip, severidad `low`): **Error algebraico en el cálculo de la solución particular constante $b/a$**
    - *Creencia errónea:* Dividir erróneamente $b/a = \frac{(1-\alpha)s}{(1-\alpha)\lambda}$ como $\lambda/s$ en vez de $s/\lambda$.
    - *Manifestación:* Obtener $z^* = \lambda/s$ en lugar de $s/\lambda$.
    - *Remediación:* La integral particular constante es $\bar{z} = b/a = \frac{(1-\alpha)s}{(1-\alpha)\lambda} = \frac{s}{\lambda}$.
  - `D-Hab02-06` (overgeneralization, severidad `high`): **Aplicar linealización estática en vez de integración diferencial exacta**
    - *Creencia errónea:* Aproximar la solución simplemente igualando $sk^\alpha = \lambda k$ para todo tiempo $t$, omitiendo el transitorio dinámico.
    - *Manifestación:* Declarar que $k(t)$ es inmediatamente constante e igual a $(s/\lambda)^{1/(1-\alpha)}$ para todo $t$.
    - *Remediación:* A menos que la economía comience exactamente en $k(0) = \bar{k}$, existirá un período de transición dinámica gobernado por la función exponencial temporal.

### `C-03`: Estática Comparativa del Capital de Estado Uniforme frente a $s$ y $\lambda$
- **Tipo:** `concept` | **Nivel Bloom:** `Analyze` | **Unidad:** `7`
- **Descripción:** Analizar analítica y gráficamente la respuesta del capital de estado uniforme $\bar{k} = (s/\lambda)^{1/(1-\alpha)}$ ante variaciones en la propensión al ahorro $(\partial \bar{k}/\partial s > 0)$ y en la tasa de crecimiento demográfico $(\partial \bar{k}/\partial \lambda < 0)$.
- **Prerrequisitos:** `Hab-02`
- **Evidencia:** [05_15_07_El_modelo_de_crecimiento_de_Solow.pdf, pág. 5]
- **Distractores (3):**
  - `D-C03-01` (conceptual_swap, severidad `high`): **Creer que una mayor tasa de ahorro aumenta permanentemente la tasa de crecimiento de largo plazo de $k$**
    - *Creencia errónea:* Suponer que aumentar $s$ genera una tasa de crecimiento de $k$ permanentemente más alta en estado uniforme.
    - *Manifestación:* Afirmar que un país con mayor tasa de ahorro crece permanentemente a una tasa más veloz en estado uniforme.
    - *Remediación:* En el modelo neoclásico, la tasa de ahorro tiene efectos nivel (eleva $\bar{k}$ y el producto per cápita), pero no efecto crecimiento en el largo plazo (la tasa de crecimiento de estado uniforme sigue siendo $\lambda$).
  - `D-C03-02` (sign_error, severidad `medium`): **Inversión del efecto del crecimiento demográfico sobre el capital por trabajador**
    - *Creencia errónea:* Afirmar que un mayor crecimiento poblacional $\lambda$ estimula la acumulación de capital por trabajador $\bar{k}$.
    - *Manifestación:* Predecir $\frac{\partial \bar{k}}{\partial \lambda} > 0$.
    - *Remediación:* Dado que $\lambda$ está en el denominador de $(s/\lambda)^{1/(1-\alpha)}$, un incremento en la tasa de crecimiento demográfico reduce el capital de estado uniforme: $\frac{\partial \bar{k}}{\partial \lambda} < 0$.
  - `D-C03-03` (overgeneralization, severidad `high`): **Asumir sensibilidad infinita de $\bar{k}$ ante variaciones infinitesimales de parámetros (falacia del filo de la navaja)**
    - *Creencia errónea:* Predecir que cualquier cambio en $s$ o $\lambda$ destruye el equilibrio causando desempleo permanente como en Harrod-Domar.
    - *Manifestación:* Afirmar que la economía colapsa si $s$ no se ajusta exactamente al valor de $\lambda$.
    - *Remediación:* A diferencia del delicado balance de Harrod-Domar, la sustituibilidad factorial permite que el sistema converja suavemente a un nuevo $\bar{k}$ para cualquier par de valores positivos de $s$ y $\lambda$.

## Sesión 3: El Dilema Harrod-Domar y el Modelo Neoclásico de Solow

### `H-03`: Comparación Estructural: Proporciones Fijas de Harrod-Domar vs. Sustituibilidad Neoclásica
- **Tipo:** `fact` | **Nivel Bloom:** `Remember` | **Unidad:** `8`
- **Descripción:** Identificar la distinción formal planteada por Solow (1956) entre el modelo de Harrod-Domar —donde la tecnología de coeficientes fijos impone una tasa garantizada $s/v$ rígidamente contrapuesta a la tasa natural $n$— y el modelo neoclásico con sustituibilidad suave entre capital y trabajo.
- **Prerrequisitos:** `H-01`, `C-02`
- **Evidencia:** [solow1956.pdf, pág. 2], [solow1956.pdf, pág. 3]
- **Distractores (3):**
  - `D-H03-01` (conceptual_swap, severidad `high`): **Atribuir la inestabilidad de Harrod-Domar a la falta de ahorro en vez de a la rigidez de proporciones**
    - *Creencia errónea:* Pensar que el problema del filo de la navaja surge por insuficiencia de ahorro agregado.
    - *Manifestación:* Afirmar que el modelo de Harrod falla por fluctuaciones de la propensión marginal al ahorro.
    - *Remediación:* Solow explica explícitamente en la introducción que la oposición rígida entre tasa natural y garantizada se debe al supuesto de proporciones fijas y ausencia de sustitución factorial.
  - `D-H03-02` (conceptual_swap, severidad `medium`): **Confundir la tasa natural de Harrod con la tasa de interés de mercado**
    - *Creencia errónea:* Interpretar la tasa natural de crecimiento como una tasa de rendimiento financiero.
    - *Manifestación:* Reemplazar la tasa demográfica $n$ por la tasa de interés real $r$.
    - *Remediación:* La tasa natural en Harrod-Domar es la tasa biológica/demográfica de expansión de la población activa $n$, no una variable monetaria ni una tasa de interés.
  - `D-H03-03` (overgeneralization, severidad `medium`): **Suponer que Solow rechaza todos los supuestos de Harrod-Domar**
    - *Creencia errónea:* Creer que Solow abandona el ahorro constante o el horizonte temporal de largo plazo de Harrod-Domar.
    - *Manifestación:* Afirmar que Solow introdujo ahorro endógeno intertemporal en su modelo base.
    - *Remediación:* Solow señala en la sección I que acepta todos los supuestos de Harrod-Domar excepto el de proporciones fijas, manteniendo la propensión constante al ahorro $s$.

### `C-04`: Hipótesis de Pleno Empleo Continuo y Flexibilidad de Precios Factoriales en Tiempo Continuo
- **Tipo:** `concept` | **Nivel Bloom:** `Understand` | **Unidad:** `9`
- **Descripción:** Comprender la articulación del cierre del modelo neoclásico en Solow (1956): oferta inelástica de factores $L(t) = L_0 e^{nt}$ y $K(t)$, y ajuste instantáneo de los precios reales de los factores ($w/p = \partial F/\partial L$, $q/p = \partial F/\partial K$) que garantiza equilibrio continuo de pleno empleo.
- **Prerrequisitos:** `H-03`
- **Evidencia:** [solow1956.pdf, pág. 4], [solow1956.pdf, pág. 5]
- **Distractores (3):**
  - `D-C04-01` (overgeneralization, severidad `high`): **Suponer que el pleno empleo es una conclusión demostrada en lugar de un supuesto axiomático del modelo**
    - *Creencia errónea:* Creer que el modelo de Solow demuestra empíricamente que nunca puede existir desempleo involuntario en el corto plazo.
    - *Manifestación:* Tratar la igualdad entre empleo y fuerza laboral como un teorema dinámico en lugar de un supuesto de cierre.
    - *Remediación:* Solow aclara en la página 67 que al identificar empleo con oferta laboral $L_0 e^{nt}$, se asume por hipótesis que el pleno empleo se mantiene perpetuamente mediante precios flexibles.
  - `D-C04-02` (conceptual_swap, severidad `medium`): **Confusión sobre la determinación del salario real en el cierre del sistema**
    - *Creencia errónea:* Creer que el salario real está fijado exógenamente por un nivel institucional de subsistencia en el modelo base.
    - *Manifestación:* Modelar $w/p = \bar{w}$ exógeno en el modelo neoclásico sin fricciones.
    - *Remediación:* En el modelo de Solow, el salario real no es rígido sino perfectamente elástico: se ajusta continuamente para que $w/p = \partial F/\partial L$ a pleno empleo.
  - `D-C04-03` (boundary_case, severidad `medium`): **Olvidar que el capital instalado se oferta de manera perfectamente inelástica en cada instante**
    - *Creencia errónea:* Considerar que los dueños de capital retiran capacidad instalada cuando la tasa de ganancia $q/p$ cae.
    - *Manifestación:* Introducir una función de oferta de capital dependiente de la tasa de interés dentro de la estática de mercado a corto plazo.
    - *Remediación:* Al igual que el trabajo, en cada punto del tiempo el stock preexistente de capital es una cantidad fija ofrecida inelásticamente, cuyo canon de alquiler $q/p$ se ajusta por productividad marginal.

### `Hab-03`: Formulación y Deducción de la Ecuación Fundamental $\dot{r} = sF(r, 1) - nr$ a partir de Tasas Relativas
- **Tipo:** `skill` | **Nivel Bloom:** `Apply` | **Unidad:** `10`
- **Descripción:** Deducir la ecuación fundamental de acumulación $\dot{r} = sF(r, 1) - nr$ para la relación capital-trabajo $r = K/L$ aplicando la descomposición de tasas de crecimiento relativas $\frac{\dot{r}}{r} = \frac{\dot{K}}{K} - \frac{\dot{L}}{L}$ y sustituyendo $\frac{\dot{K}}{K} = \frac{sF(K,L)}{K} = \frac{sF(r,1)}{r}$.
- **Prerrequisitos:** `Hab-01`, `C-04`
- **Evidencia:** [solow1956.pdf, pág. 5], [solow1956.pdf, pág. 6]
- **Distractores (6):**
  - `D-Hab03-01` (sign_error, severidad `high`): **Error de signos en la diferencia de tasas relativas logarítmicas**
    - *Creencia errónea:* Escribir $\dot{r}/r = \dot{L}/L - \dot{K}/K$ al derivar el cociente $K/L$.
    - *Manifestación:* $\dot{r}/r = n - \dot{K}/K$, invirtiendo los signos de la ecuación dinámica.
    - *Remediación:* La tasa relativa de un cociente $r = K/L$ es la tasa del numerador menos la del denominador: $\dot{r}/r = \dot{K}/K - \dot{L}/L$.
  - `D-Hab03-02` (skipped_step, severidad `medium`): **Omisión de la multiplicación por $r$ al recuperar $\dot{r}$ a partir de $\dot{r}/r$** *(Paso omitido: Multiplicar ambos lados de la ecuación de tasas de crecimiento $\frac{\dot{r}}{r} = \frac{sF(r,1)}{r} - n$ por la variable de nivel $r$.)*
    - *Manifestación:* Escribir $\dot{r} = \frac{sF(r,1)}{r} - n$ olvidando multiplicar por $r$.
    - *Remediación:* Recuerde multiplicar toda la expresión por $r$ para despejar $\dot{r}$: $r \left[ \frac{sF(r,1)}{r} - n \right] = sF(r,1) - nr$.
  - `D-Hab03-03` (skipped_step, severidad `high`): **Omisión de la homogeneidad de grado 1 al transformar el cociente $F(K, L)/K$** *(Paso omitido: Factorizar $L$ de $F(K, L)$ como $L F(r, 1)$ y observar que $L/K = 1/r$.)*
    - *Manifestación:* Mantener términos mixtos $F(K, L)/K$ sin reducir a la función intensiva univariada $F(r, 1)/r$.
    - *Remediación:* Divida tanto el numerador como el argumento de $F$ entre $L$: $F(K,L) = L F(K/L, 1) = L F(r,1)$. Al dividir entre $K$, observe que $L/K = 1/r$, por lo que $F(K,L)/K = F(r,1)/r$.
  - `D-Hab03-04` (notation, severidad `medium`): **Confundir la notación $r$ de Solow (1956) con una tasa de interés**
    - *Creencia errónea:* Interpretar el símbolo $r$ en el artículo original de Solow como la tasa de interés real en vez del ratio capital-trabajo $K/L$.
    - *Manifestación:* Tratar a $\dot{r}$ como la dinámica de la tasa de interés bancaria.
    - *Remediación:* En el artículo de 1956, Solow emplea la letra $r$ para la relación capital-trabajo $K/L$ (mientras que la tasa de interés se denota $i$ y la renta del capital $q$).
  - `D-Hab03-05` (overgeneralization, severidad `medium`): **Tratar a $F(r, 1)$ como una constante en lugar de una función no lineal de $r$**
    - *Creencia errónea:* Suponer que $F(r, 1)$ no cambia con $r$ al integrar o graficar la ecuación fundamental.
    - *Manifestación:* Integrar $\dot{r} = sF(r,1) - nr$ considerando a $F(r,1)$ como una constante independiente de $r$.
    - *Remediación:* La función $F(r, 1)$ representa la productividad media del trabajo en función del capital por trabajador; no es una constante sino una función estrictamente cóncava de $r$.
  - `D-Hab03-06` (conceptual_swap, severidad `high`): **Olvidar restar la tasa poblacional $n$ de la tasa de acumulación del capital**
    - *Creencia errónea:* Considerar que la dinámica de $r$ depende únicamente de la inversión $sF(r,1)$, sin dilución poblacional.
    - *Manifestación:* $\dot{r} = sF(r, 1)$, ignorando el término de mantenimiento demográfico $-nr$.
    - *Remediación:* El aumento en el número de trabajadores requiere asignar capital simplemente para mantener constante la dotación de los nuevos entrantes; este efecto de dilución requiere restar el término $nr$.

### `C-05`: Convergencia Global y Dinámica de Inversión Efectiva vs. Dilución de Capital (Figura I)
- **Tipo:** `concept` | **Nivel Bloom:** `Analyze` | **Unidad:** `11`
- **Descripción:** Interpretar el diagrama canónico de Solow (1956, Figura I): interacción entre la curva cóncava de inversión $sF(r, 1)$ y el rayo de dilución $nr$, demostrando que para todo $r(0) > 0$ el sistema converge asintóticamente a un único estado de crecimiento equilibrado $r^*$ con $sF(r^*, 1) = nr^*$.
- **Prerrequisitos:** `Hab-03`
- **Evidencia:** [solow1956.pdf, pág. 6], [solow1956.pdf, pág. 7]
- **Distractores (3):**
  - `D-C05-01` (sign_error, severidad `medium`): **Creer que si $r(0) < r^*$, el producto agregado crece más lento que la población**
    - *Creencia errónea:* Afirmar que cuando una economía parte de escasez de capital ($r < r^*$), su producto crece a una tasa menor que $n$.
    - *Manifestación:* Afirmar que $\dot{Y}/Y < n$ cuando $r < r^*$.
    - *Remediación:* Si $r < r^*$, la inversión excede la dilución ($sF(r,1) > nr$), por lo que el capital y el producto crecen a tasas estrictamente mayores que $n$, permitiendo la convergencia hacia $r^*$.
  - `D-C05-02` (conceptual_swap, severidad `low`): **Confundir la pendiente del rayo $nr$ con la tasa de depreciación en ausencia de desgaste físico**
    - *Creencia errónea:* Asumir que la recta $nr$ en el modelo de Solow (1956) incluye depreciación física del capital.
    - *Manifestación:* Escribir $(n + \delta)r$ atribuyéndolo al texto original de 1956.
    - *Remediación:* Solow define explícitamente $Y$ en la página 66 como producto neto tras reponer la depreciación del capital; por tanto, la pendiente del rayo es exactamente $n$.
  - `D-C05-03` (overgeneralization, severidad `high`): **Asumir que el estado estacionario $r^*$ es dependiente de las condiciones iniciales $r(0)$**
    - *Creencia errónea:* Creer que diferentes niveles iniciales de capital per cápita conducen a diferentes estados estacionarios en la Figura I.
    - *Manifestación:* Afirmar histéresis o dependencia de trayectoria para el estado estacionario de la Figura I.
    - *Remediación:* En la configuración canónica de la Figura I con rendimientos estrictamente decrecientes y condiciones de Inada implícitas, existe una única intersección $r^*$, la cual es globalmente atractora.

## Sesión 4: Topologías No Estándar, Equilibrios Múltiples y el Caso Harrod-Domar

### `C-06`: Equilibrios Múltiples, Umbral de Despegue Inestable y Trampas de Pobreza (Figura II)
- **Tipo:** `concept` | **Nivel Bloom:** `Analyze` | **Unidad:** `12`
- **Descripción:** Analizar configuraciones con funciones de producción no monótonamente cóncavas o con intercepto positivo (Figura II de Solow 1956), identificando la existencia de tres equilibrios ($r_1, r_2, r_3$) donde $r_1$ y $r_3$ son localmente estables y $r_2$ actúa como un umbral inestable de despegue ('tipping point').
- **Prerrequisitos:** `C-05`
- **Evidencia:** [solow1956.pdf, pág. 8]
- **Distractores (3):**
  - `D-C06-01` (conceptual_swap, severidad `high`): **Clasificar el punto de corte intermedio $r_2$ como un equilibrio dinámicamente estable**
    - *Creencia errónea:* Creer que todos los puntos donde $sF(r, 1) = nr$ son atractores estables del sistema.
    - *Manifestación:* Afirmar que si la economía perturba $r_2$ regresará automáticamente a $r_2$.
    - *Remediación:* En $r_2$, si $r > r_2$ entonces $\dot{r} > 0$ (el capital crece alejándose hacia $r_3$), y si $r < r_2$ entonces $\dot{r} < 0$ (el capital cae alejándose hacia $r_1$). Por tanto, $r_2$ es inestable.
  - `D-C06-02` (boundary_case, severidad `high`): **Ignorar el papel de las condiciones iniciales en presencia de equilibrios múltiples**
    - *Creencia errónea:* Asumir que la economía siempre alcanzará el nivel de alto desarrollo $r_3$ independientemente de su dotación inicial.
    - *Manifestación:* Predecir convergencia a $r_3$ para cualquier $r(0) > 0$.
    - *Remediación:* El valor $r_2$ divide el espacio de estados: la cuenca de atracción $[0, r_2)$ converge a la trampa de bajo ingreso $r_1$, mientras que $(r_2, \infty)$ converge a $r_3$.
  - `D-C06-03` (overgeneralization, severidad `medium`): **Atribuir equilibrios múltiples a la existencia de monopolios o externalidades en lugar de a la geometría de $F(r, 1)$**
    - *Creencia errónea:* Pensar que Solow introdujo imperfecciones de mercado para obtener la Figura II.
    - *Manifestación:* Explicar la Figura II invocando poder de monopolio o fallas de mercado.
    - *Remediación:* La presencia de múltiples equilibrios en la Figura II proviene únicamente de la no convexidad local de la función de producción $F(r,1)$ en un entorno puramente competitivo.

### `C-07`: Casos Límite sin Estado Estacionario: Expansión Perpetua vs. Colapso hacia Cero (Figura III)
- **Tipo:** `concept` | **Nivel Bloom:** `Analyze` | **Unidad:** `13`
- **Descripción:** Evaluar escenarios analíticos donde no existe intersección entre $sF(r, 1)$ y $nr$ (Figura III de Solow 1956): el caso hiperproductivo ($s_1 F^1(r, 1) > nr$ para todo $r$), que genera acumulación indefinida de capital per cápita, y el caso hipoproductivo ($s_2 F^2(r, 1) < nr$), que conduce a una caída asintótica de $r$ hacia cero.
- **Prerrequisitos:** `C-05`
- **Evidencia:** [solow1956.pdf, pág. 9], [solow1956.pdf, pág. 10]
- **Distractores (3):**
  - `D-C07-01` (overgeneralization, severidad `medium`): **Creer que la ausencia de intersección implica violación matemática de los rendimientos a escala**
    - *Creencia errónea:* Suponer que funciones donde $sF(r, 1)$ no corta a $nr$ violan el supuesto de rendimientos constantes a escala.
    - *Manifestación:* Afirmar que la Figura III contradice el teorema de Euler o la homogeneidad lineal.
    - *Remediación:* Solow aclara en la nota al pie 5 que cualquier función $F(r,1)$ no decreciente da lugar a una función de producción legítima con rendimientos constantes al escalarse por $L$.
  - `D-C07-02` (conceptual_swap, severidad `high`): **Confundir la contracción de $r \to 0$ con una contracción del producto agregado absoluto**
    - *Creencia errónea:* Afirmar que cuando $r \to 0$ el producto total agregado $Y(t)$ necesariamente decrece.
    - *Manifestación:* Afirmar que $\dot{Y} < 0$ para todo $t$ en el sistema hipoproductivo.
    - *Remediación:* Solow subraya que como la inversión neta es siempre positiva y la población crece, el ingreso agregado $Y(t)$ sólo puede crecer; lo que colapsa es el ingreso por habitante.
  - `D-C07-03` (boundary_case, severidad `medium`): **Asumir que el crecimiento perpetuo de $r$ viola la ley de rendimientos decrecientes del capital**
    - *Creencia errónea:* Creer que para que $sF(r, 1) > nr$ en todo $r$ se requiere que la productividad marginal del capital sea creciente.
    - *Manifestación:* Afirmar que la curva superior exige $\phi''(r) > 0$.
    - *Remediación:* La función $s_1 F^1(r, 1) = nr + \sqrt{r}$ posee $\frac{d^2}{dr^2}(nr + \sqrt{r}) = -\frac{1}{4}r^{-3/2} < 0$, confirmando rendimientos estrictamente decrecientes a pesar del crecimiento ilimitado.

### `Hab-04`: Análisis por Regímenes de la Tecnología de Proporciones Fijas de Leontief / Harrod-Domar (Figura IV)
- **Tipo:** `skill` | **Nivel Bloom:** `Apply` | **Unidad:** `14`
- **Descripción:** Resolver la dinámica por tramos de la ecuación diferencial $\dot{r} = s \min\left(\frac{r}{a}, \frac{1}{b}\right) - nr$ correspondiente a la tecnología de Leontief (Figura IV de Solow 1956), clasificando los tres regímenes según la relación entre la tasa natural $n$ y la tasa garantizada $s/a$.
- **Prerrequisitos:** `H-03`, `Hab-03`
- **Evidencia:** [solow1956.pdf, pág. 10], [solow1956.pdf, pág. 11], [solow1956.pdf, pág. 12]
- **Distractores (6):**
  - `D-Hab04-01` (conceptual_swap, severidad `high`): **Identificar incorrectamente el factor cuello de botella según el nivel de $r$**
    - *Creencia errónea:* Creer que cuando $r > a/b$ el capital es el factor escaso que limita la producción.
    - *Manifestación:* Plantear que el producto es $r/a$ cuando $r > a/b$.
    - *Remediación:* Si $r > a/b$, entonces $r/a > 1/b$; por la función Leontief, el producto por trabajador es el menor de los dos, a saber $1/b$, lo que significa que el trabajo es el factor limitante.
  - `D-Hab04-02` (skipped_step, severidad `high`): **Omisión del cálculo del tiempo crítico de cruce entre regímenes** *(Paso omitido: Determinar el instante $t_1$ en que la trayectoria $r(t)$ alcanza la discontinuidad técnica $a/b$ para conmutar a la solución del segundo régimen.)*
    - *Manifestación:* Aplicar la solución asintótica del primer tramo para todo $t > 0$ sin cambiar de ecuación al cruzar $a/b$.
    - *Remediación:* La función $\min$ cambia de expresión analítica en $r = a/b$. Al resolver la trayectoria temporal, se debe hallar el tiempo $t_1$ de contacto y cambiar la ley diferencial para $t > t_1$.
  - `D-Hab04-03` (skipped_step, severidad `medium`): **Omisión de la condición de redundancia de capital en el régimen $n_3 < s/a$** *(Paso omitido: Verificar si la productividad marginal del capital es nula evaluando la derivada en el tramo horizontal de la función $\min$.)*
    - *Manifestación:* Declarar pleno empleo de capital en $r^* = s/(n_3 b)$ sin reconocer el desempleo de máquinas.
    - *Remediación:* En $r^* = s/(n_3 b) > a/b$, la producción está en el tramo horizontal donde el capital adicional no aporta producto: la fracción empleada de capital es $a n_3 / s < 1$, habiendo exceso de capacidad permanente.
  - `D-Hab04-04` (conceptual_swap, severidad `high`): **Confusión entre desempleo de mano de obra y capacidad ociosa de capital**
    - *Creencia errónea:* Predecir desempleo de trabajadores cuando la tasa garantizada supera a la natural ($s/a > n$).
    - *Manifestación:* Asignar desempleo laboral al régimen $s/a > n$.
    - *Remediación:* Si $s/a > n$, el capital se expande más rápido que la mano de obra disponible; por lo tanto, el factor excedente es el capital (exceso de capacidad), mientras que el trabajo está plenamente ocupado.
  - `D-Hab04-05` (procedural_slip, severidad `medium`): **Error algebraico en la solución del tramo lineal para $r < a/b$**
    - *Creencia errónea:* Resolver la ecuación lineal $\dot{r} = (s/a - n)r$ como si fuera una constante en vez de un crecimiento/decrecimiento exponencial.
    - *Manifestación:* Escribir $r(t) = r_0 + (s/a - n)t$.
    - *Remediación:* La ecuación $\frac{\dot{r}}{r} = \frac{s}{a} - n$ es de variables separables con solución exponencial directa: $r(t) = r(t_1) e^{(s/a - n)(t - t_1)}$.
  - `D-Hab04-06` (boundary_case, severidad `medium`): **Asumir que el caso (b) con $n = s/a$ es un atractor asintótico estable**
    - *Creencia errónea:* Creer que cuando $n = s/a$ el sistema se ajusta dinámicamente hacia una relación única $a/b$.
    - *Manifestación:* Afirmar que todo $r(0)$ converge a $a/b$ cuando $n_2 = s/a$.
    - *Remediación:* Si $n = s/a$, en el tramo inclinado $\dot{r} = (s/a - n)r = 0$, lo que significa que el ratio de capital no cambia: cualquier desempleo o redundancia inicial se perpetúa congelada.

## Sesión 5: Soluciones Explícitas: Cobb-Douglas y Familias de Sustituibilidad Variable

### `Hab-05`: Trayectoria Temporal y Equilibrio del Coeficiente de Capital en Tecnología Cobb-Douglas
- **Tipo:** `skill` | **Nivel Bloom:** `Apply` | **Unidad:** `15`
- **Descripción:** Calcular la trayectoria del stock de capital $K(t) = \left[K_0^b - \frac{s}{n}L_0^b + \frac{s}{n}L_0^b e^{nbt}\right]^{1/b}$ (con $b = 1-a$) y deducir que el coeficiente de capital de equilibrio de Harrod $C^* = K/Y$ converge endógenamente a $s/n$, igualando la tasa natural con la garantizada.
- **Prerrequisitos:** `Hab-02`, `Hab-03`
- **Evidencia:** [solow1956.pdf, pág. 13], [solow1956.pdf, pág. 14]
- **Distractores (6):**
  - `D-Hab05-01` (procedural_slip, severidad `high`): **Inversión del ratio capital-producto de equilibrio $C^*$**
    - *Creencia errónea:* Calcular el coeficiente de capital como $C^* = n/s$ en lugar de $s/n$.
    - *Manifestación:* $C^* = n/s$, invirtiendo los roles de ahorro y crecimiento poblacional.
    - *Remediación:* En estado uniforme, $\dot{K}/K = s/(K/Y) = n$; despejando el ratio capital-producto $C = K/Y$, se obtiene $C = s/n$.
  - `D-Hab05-02` (skipped_step, severidad `medium`): **Omisión de la sustitución del producto intensivo $y = r^a$ para hallar $K/Y$** *(Paso omitido: Dividir el ratio capital-trabajo $r^*$ entre el producto per cápita $r^{*a}$ para obtener la relación capital-producto $C^*$.)*
    - *Manifestación:* Afirmar que $C^*$ depende de la escala de la fuerza laboral o de $L_0$.
    - *Remediación:* Divida $r^*$ entre $y^*$: $\frac{r^*}{(r^*)^a} = (r^*)^{1-a}$. Como $r^* = (s/n)^{1/(1-a)}$, al elevar a $(1-a)$ queda directamente $C^* = s/n$.
  - `D-Hab05-03` (skipped_step, severidad `medium`): **Omisión de la condición asintótica $t \to \infty$ al evaluar la tasa de crecimiento de $K(t)$** *(Paso omitido: Factorizar el término dominante $e^{nbt}$ dentro del paréntesis antes de aplicar la potencia $1/b$ en el límite temporal.)*
    - *Manifestación:* Declarar que la tasa de crecimiento de $K(t)$ es $nb$ en lugar de $n$.
    - *Remediación:* Al tomar el límite cuando $t$ es grande, el término dentro del corchete es dominado por $\frac{s}{n}L_0^b e^{nbt}$; al elevar a $1/b$, la potencia de $e$ pasa a ser $\frac{nbt}{b} = nt$, creciendo a la tasa $n$.
  - `D-Hab05-04` (conceptual_swap, severidad `high`): **Creer que la igualdad $n = s/C^*$ es una coincidencia accidental**
    - *Creencia errónea:* Interpretar la igualdad $n = s/C^*$ como una casualidad exógena idéntica a la navaja de Harrod.
    - *Manifestación:* Afirmar que el modelo neoclásico requiere una política de sintonía fina para que $n = s/C^*$.
    - *Remediación:* Solow resalta que $n = s/C$ no es una casualidad afortunada, sino una consecuencia necesaria del ajuste endógeno de los precios y de la técnica elegida.
  - `D-Hab05-05` (procedural_slip, severidad `medium`): **Error en el exponente del producto per cápita de equilibrio**
    - *Creencia errónea:* Calcular el ingreso por habitante de estado estacionario como $(s/n)^a$ en lugar de $(s/n)^{a/(1-a)}$.
    - *Manifestación:* $y^* = (s/n)^a$, omitiendo la división por $1-a$ en el exponente.
    - *Remediación:* Como $r^* = (s/n)^{1/(1-a)}$, al sustituir en $y^* = (r^*)^a$ se obtiene $(s/n)^{a/(1-a)}$.
  - `D-Hab05-06` (notation, severidad `low`): **Confundir la participación del capital $a$ con el exponente de la mano de obra**
    - *Creencia errónea:* Intercambiar los exponentes $a$ y $1-a$ en la derivación de la ecuación de acumulación.
    - *Manifestación:* $b = a$ en lugar de $b = 1 - a$.
    - *Remediación:* En la notación de Solow (1956), $a$ acompaña a $K$ y el parámetro auxiliar se define como $b \equiv 1 - a$.

### `Hab-06`: Determinación del Umbral Crítico y Dinámica de la Familia de Producción CES con $p = 1/2$ (Figura V)
- **Tipo:** `skill` | **Nivel Bloom:** `Apply` | **Unidad:** `16`
- **Descripción:** Resolver la dinámica de la función $Y = (a\sqrt{K} + \sqrt{L})^2$ (Ejemplo 3 de Solow 1956), identificando el umbral paramétrico $s a^2 < n$ para la existencia de un estado estacionario estable $r^* = \left(\frac{1}{\sqrt{n/s} - a}\right)^2$ y la condición $s a^2 > n$ para crecimiento ilimitado.
- **Prerrequisitos:** `Hab-03`, `C-05`
- **Evidencia:** [solow1956.pdf, pág. 14], [solow1956.pdf, pág. 15]
- **Distractores (6):**
  - `D-Hab06-01` (sign_error, severidad `high`): **Inversión de la desigualdad de viabilidad del estado estacionario**
    - *Creencia errónea:* Afirmar que existe un estado estacionario estable cuando $s a^2 > n$.
    - *Manifestación:* Declarar que $s a^2 > n$ garantiza convergencia a un ratio $r^*$ finito.
    - *Remediación:* Para que la curva de inversión corte al rayo $nr$ desde arriba, su pendiente asintótica $s a^2$ debe ser estrictamente menor que la pendiente del rayo $n$, es decir $s a^2 < n$.
  - `D-Hab06-02` (skipped_step, severidad `high`): **Omisión de la factorización de raíces en la ecuación diferencial de $\dot{r}$** *(Paso omitido: Factorizar el polinomio cuadrático en $\sqrt{r}$ como $s(A\sqrt{r} + 1)(B\sqrt{r} + 1)$ con $A = a - \sqrt{n/s}$ y $B = a + \sqrt{n/s}$.)*
    - *Manifestación:* Tratar la ecuación no lineal como separable directa sin descomponer en factores lineales en $\sqrt{r}$.
    - *Remediación:* La expresión entre corchetes es un trinomio en $\sqrt{r}$: $(a^2 - n/s)r + 2a\sqrt{r} + 1 = (A\sqrt{r} + 1)(B\sqrt{r} + 1)$. Factorizarla es esencial para integrar mediante fracciones simples.
  - `D-Hab06-03` (skipped_step, severidad `medium`): **Omisión de la condición de no negatividad de $(\sqrt{n/s} - a)$** *(Paso omitido: Verificar que $\sqrt{n/s} > a$ para asegurar que el denominador de $r^*$ sea un número real estrictamente positivo.)*
    - *Manifestación:* Aceptar valores de $r^*$ con denominadores negativos asumiendo que el cuadrado elimina la inconsistencia.
    - *Remediación:* Al resolver $\sqrt{r^*} = \frac{1}{\sqrt{n/s} - a}$, se requiere que $\sqrt{n/s} > a$ para que $\sqrt{r^*}$ sea positivo; de lo contrario no hay intersección para $r > 0$.
  - `D-Hab06-04` (procedural_slip, severidad `medium`): **Error en el cálculo del producto por trabajador de estado estacionario**
    - *Creencia errónea:* Calcular el ingreso per cápita límite como $1/(1 - a\sqrt{s/n})$ omitiendo el cuadrado de la función de producción.
    - *Manifestación:* Omitir el cuadrado exterior obteniendo un producto per cápita lineal en los parámetros.
    - *Remediación:* Recuerde que la función intensiva es $F(r, 1) = (a\sqrt{r} + 1)^2$. Al sustituir $\sqrt{r^*} = \frac{1}{\sqrt{n/s} - a}$, se debe elevar toda la suma al cuadrado.
  - `D-Hab06-05` (boundary_case, severidad `medium`): **Asumir que la producción requiere indispensablemente ambos factores**
    - *Creencia errónea:* Creer que si $K = 0$, la producción $Y$ en este ejemplo CES debe ser cero como en Cobb-Douglas.
    - *Manifestación:* Hacer que la curva $sF(r, 1)$ parta del origen $(0,0)$ en vez de tener intercepto positivo $s$.
    - *Remediación:* A diferencia de Cobb-Douglas, esta función permite producir sólo con trabajo: para $r = 0$, $F(0, 1) = (a\cdot 0 + 1)^2 = 1$, por lo que la curva de inversión parte a una altura $s$ en el eje vertical.
  - `D-Hab06-06` (conceptual_swap, severidad `medium`): **Confundir el parámetro de elasticidad $p$ con la participación de factores**
    - *Creencia errónea:* Tratar al parámetro $p = 1/2$ como la participación del capital en el ingreso.
    - *Manifestación:* Afirmar que el capital recibe el 50% del producto nacional.
    - *Remediación:* En la función CES general, $p$ define la curvatura de las isocuantas ($\\sigma = 1/(1-p)$); no representa las participaciones de los factores en el ingreso.

## Sesión 6: Dinámica y Comportamiento de los Precios Factoriales y la Tasa de Interés

### `H-04`: Condiciones de Arbitraje entre la Tasa de Interés y el Rendimiento del Capital Propio
- **Tipo:** `fact` | **Nivel Bloom:** `Remember` | **Unidad:** `17`
- **Descripción:** Identificar la ecuación canónica de arbitraje entre la tasa monetaria de interés $i(t)$, la renta real del capital $q(t)/p(t)$ y la inflación de bienes de capital: $i(t) = \frac{q(t)}{p(t)} + \frac{\dot{p}(t)}{p(t)}$ (Solow 1956, ec. 12).
- **Prerrequisitos:** `C-04`
- **Evidencia:** [solow1956.pdf, pág. 16], [solow1956.pdf, pág. 17]
- **Distractores (3):**
  - `D-H04-01` (sign_error, severidad `high`): **Error de signo en la ganancia de capital del precio del producto**
    - *Creencia errónea:* Restar la tasa de inflación $\dot{p}/p$ al rendimiento propio del capital para igualarlo con la tasa de interés nominal.
    - *Manifestación:* $i(t) = q(t)/p(t) - \dot{p}(t)/p(t)$.
    - *Remediación:* Tener una unidad de capital rinde un alquiler monetario $q$ más la apreciación del precio del activo $\dot{p}$. Por ende, el rendimiento total es $q/p + \dot{p}/p = i$.
  - `D-H04-02` (conceptual_swap, severidad `medium`): **Confundir el precio del alquiler del capital $q$ con la tasa de interés $i$**
    - *Creencia errónea:* Suponer que el canon de arrendamiento del capital $q$ y la tasa de interés $i$ son exactamente la misma variable dimensional.
    - *Manifestación:* Reemplazar indistintamente $q/p$ por $i$ sin considerar la variación del precio del capital.
    - *Remediación:* Solow distingue explícitamente cuatro precios: $p$ (precio del producto), $w$ (salario), $q$ (alquiler del capital) e $i$ (tasa de interés monetaria).
  - `D-H04-03` (boundary_case, severidad `low`): **Olvidar que con nivel de precios constante el rendimiento propio coincide con la tasa de interés**
    - *Creencia errónea:* Creer que aún cuando $\dot{p} = 0$, debe existir una prima de riesgo estructural en el modelo neoclásico base.
    - *Manifestación:* Introducir discrepancias arbitrarias entre $i$ y $q/p$ sin inflación ni incertidumbre.
    - *Remediación:* Si $p$ es constante, $\dot{p} = 0$, por lo que la ecuación (12) se reduce a $i(t) = q(t)/p(t) = \partial F/\partial K$.

### `C-08`: Relación Monótona entre el Ratio Capital-Trabajo $r$ y el Ratio Salario-Renta $w/q$ (Figuras VI y VII)
- **Tipo:** `concept` | **Nivel Bloom:** `Analyze` | **Unidad:** `18`
- **Descripción:** Interpretar el comportamiento de los precios factoriales a lo largo de las trayectorias de ajuste en el mapa de isocuantas (Figuras VI y VII de Solow 1956): a medida que $r$ aumenta hacia $r^*$, el ratio salario-renta $w/q$ se incrementa de forma monótona y continua debido a rendimientos decrecientes.
- **Prerrequisitos:** `H-04`, `C-05`
- **Evidencia:** [solow1956.pdf, pág. 18], [solow1956.pdf, pág. 19], [solow1956.pdf, pág. 20]
- **Distractores (3):**
  - `D-C08-01` (conceptual_swap, severidad `high`): **Invertir la dirección del cambio en la relación de precios factoriales ante la acumulación de capital**
    - *Creencia errónea:* Afirmar que a medida que el capital se vuelve más abundante respecto al trabajo, el salario real cae y la tasa de ganancia aumenta.
    - *Manifestación:* Predecir que $\frac{d(w/q)}{dr} < 0$.
    - *Remediación:* Al aumentar el capital por trabajador, el capital se vuelve relativamente abundante y el trabajo escaso; por ende, el salario real sube y la renta del capital baja, elevando $w/q$.
  - `D-C08-02` (overgeneralization, severidad `medium`): **Predecir saltos catastróficos discontinuos en los precios de factores neoclásicos**
    - *Creencia errónea:* Esperar que los salarios o alquileres se desplomen a cero de forma brusca ante pequeñas desviaciones del equilibrio.
    - *Manifestación:* Afirmar que si $r \ne r^*$, uno de los precios factoriales se hace cero de inmediato.
    - *Remediación:* Solow resalta que en el mundo neoclásico las variaciones en las tasas salariales y de beneficio son suaves y no catastróficas, a diferencia del colapso de precios en Harrod-Domar.
  - `D-C08-03` (boundary_case, severidad `medium`): **Asumir que a lo largo de un rayo desde el origen la pendiente de las isocuantas varía**
    - *Creencia errónea:* Creer que la tasa marginal de sustitución técnica cambia a lo largo de un rayo con $r$ constante.
    - *Manifestación:* Asignar diferentes ratios $w/q$ a puntos situados sobre el mismo rayo $K = r^* L$.
    - *Remediación:* En funciones homogéneas de grado 1, las productividades marginales dependen únicamente del ratio $K/L = r$; por lo tanto, a lo largo de un rayo constante la pendiente de las isocuantas no varía.

### `Hab-07`: Cálculo de la Distribución del Ingreso y Participación del Trabajo según Formas Funcionales
- **Tipo:** `skill` | **Nivel Bloom:** `Apply` | **Unidad:** `19`
- **Descripción:** Calcular la participación factorial del trabajo en el ingreso nacional $\frac{w L}{p Y}$ bajo tecnologías Cobb-Douglas (constante e igual a $1-a$) y bajo la tecnología CES $p = 1/2$ de Solow (1956), donde la participación del trabajo en equilibrio es dependiente de los parámetros: $1 - a\sqrt{s/n}$.
- **Prerrequisitos:** `C-08`, `Hab-05`
- **Evidencia:** [solow1956.pdf, pág. 20], [solow1956.pdf, pág. 21]
- **Distractores (6):**
  - `D-Hab07-01` (overgeneralization, severidad `high`): **Generalizar erróneamente la constancia de las participaciones factoriales de Cobb-Douglas a cualquier tecnología**
    - *Creencia errónea:* Creer que la participación del trabajo en el producto es siempre independiente de la tasa de ahorro y de la población en todos los modelos neoclásicos.
    - *Manifestación:* Declarar que la participación del trabajo en el Ejemplo 3 es constante e independiente de $s$ y $n$.
    - *Remediación:* Solow contrasta explícitamente el caso Cobb-Douglas con el Ejemplo 3: en el Ejemplo 3, la cuota laboral en equilibrio es $1 - a\sqrt{s/n}$, la cual depende directamente de $s$ y $n$.
  - `D-Hab07-02` (skipped_step, severidad `medium`): **Omisión de la multiplicación por la inversa del producto medio $L/Y$ al calcular la participación** *(Paso omitido: Multiplicar el salario real $w/p$ por la relación trabajo-producto $L/Y = 1/y^*$ para obtener la participación porcentual del trabajo.)*
    - *Manifestación:* Confundir la evolución del nivel salarial real $w/p$ con la cuota distributiva del trabajo.
    - *Remediación:* Para obtener la cuota relativa del factor trabajo en el ingreso, se debe normalizar el salario real por el producto por trabajador: $\text{Share}_L = \frac{w/p}{Y/L}$.
  - `D-Hab07-03` (skipped_step, severidad `medium`): **Omisión de la sustitución del ratio de equilibrio $r^*$ en la derivada marginal del trabajo** *(Paso omitido: Evaluar la derivada $\partial Y/\partial L = a\sqrt{r} + 1$ en el valor concreto de equilibrio de largo plazo $r^*$.)*
    - *Manifestación:* Dejar la participación como una función implícita no resuelta de $r$ en lugar de sustituir $r^* = \left(\frac{1}{\sqrt{n/s}-a}\right)^2$.
    - *Remediación:* Evalúe $\partial Y/\partial L = a\sqrt{r^*} + 1$ sustituyendo $\sqrt{r^*} = \frac{1}{\sqrt{n/s} - a}$ y simplifique con $y^*$ para llegar a la expresión limpia $1 - a\sqrt{s/n}$.
  - `D-Hab07-04` (sign_error, severidad `high`): **Error en la dirección del impacto de la tasa de ahorro sobre la participación laboral en el caso CES**
    - *Creencia errónea:* Afirmar que un aumento en la tasa de ahorro $s$ eleva la participación del trabajo en la tecnología CES con $p = 1/2$.
    - *Manifestación:* Predecir $\frac{\partial \text{Share}_L}{\partial s} > 0$ en el Ejemplo 3.
    - *Remediación:* En la fórmula $1 - a\sqrt{s/n}$, $s$ entra con signo negativo precedido por $a$; por lo tanto, mayor ahorro reduce la participación laboral relativa.
  - `D-Hab07-05` (conceptual_swap, severidad `medium`): **Confundir la participación del trabajo con la participación del capital**
    - *Creencia errónea:* Calcular $a\sqrt{s/n}$ como la participación de la mano de obra en vez de la del capital.
    - *Manifestación:* Asignar $a\sqrt{s/n}$ a los trabajadores.
    - *Remediación:* La participación del capital es $qK/pY = a\sqrt{s/n}$, mientras que la del trabajo es el remanente $1 - a\sqrt{s/n}$.
  - `D-Hab07-06` (boundary_case, severidad `low`): **Asumir indeterminación en las cuotas factoriales bajo rendimientos constantes**
    - *Creencia errónea:* Creer que la retribución según producto marginal no agota el producto total en competencia perfecta.
    - *Manifestación:* Plantear que queda un beneficio extraordinario puro no distribuido entre $K$ y $L$.
    - *Remediación:* Bajo competencia perfecta y rendimientos constantes a escala, el teorema de Euler establece que $L \frac{\partial F}{\partial L} + K \frac{\partial F}{\partial K} = F(K, L)$, agotando exactamente el producto total.

## Sesión 7: Extensiones Analíticas: Progreso Técnico, Oferta de Trabajo y Tasa de Ahorro Variable

### `Hab-08`: Incorporación de Progreso Tecnológico Neutral y Dinámica Asintótica del Capital
- **Tipo:** `skill` | **Nivel Bloom:** `Apply` | **Unidad:** `20`
- **Descripción:** Resolver la dinámica de acumulación con progreso técnico neutral exponencial $Y = e^{gt} K^a L^{1-a}$, deduciendo que el capital crece a la tasa $n + g/(1-a)$, el producto a la tasa $n + ag/(1-a)$, y la relación capital-trabajo crece perpetuamente a la tasa $g/(1-a)$.
- **Prerrequisitos:** `Hab-05`
- **Evidencia:** [solow1956.pdf, pág. 22], [solow1956.pdf, pág. 23]
- **Distractores (6):**
  - `D-Hab08-01` (conceptual_swap, severidad `high`): **Asumir que el ratio capital-trabajo alcanza un estado estacionario finito y constante**
    - *Creencia errónea:* Creer que $k$ se estabiliza en una constante cuando hay progreso técnico neutral que multiplica a la función de producción.
    - *Manifestación:* Afirmar que $\dot{r} \to 0$ con $A(t) = e^{gt}$.
    - *Remediación:* Solow señala en la página 85 que con cambio técnico el capital por trabajador nunca alcanza un valor constante sino que crece indefinidamente a la tasa $g/b = g/(1-a)$.
  - `D-Hab08-02` (skipped_step, severidad `high`): **Omisión de la renormalización temporal del exponente $(n(1-a) + g)$ al integrar la ecuación diferencial** *(Paso omitido: Agrupar los exponentes de la fuerza laboral y del progreso técnico como $e^{[n(1-a) + g]t}$ antes de integrar la ecuación de Bernoulli.)*
    - *Manifestación:* Integrar separadamente $e^{gt}$ y $e^{nt(1-a)}$ generando productos cruzados erróneos.
    - *Remediación:* Multiplique los términos exponenciales: $e^{gt} \cdot [e^{nt}]^{1-a} = e^{[n(1-a) + g]t} = e^{(nb + g)t}$. Este exponente combinado es el que entra en la solución de Bernoulli.
  - `D-Hab08-03` (skipped_step, severidad `medium`): **Omisión de la tasa de crecimiento del coeficiente de capital $K/Y$** *(Paso omitido: Restar la tasa de crecimiento del producto a la tasa de crecimiento del capital para obtener la dinámica temporal de la relación capital-producto.)*
    - *Manifestación:* Declarar que $K/Y$ permanece constante en el modelo de Solow con progreso técnico Hicks-neutral.
    - *Remediación:* La tasa de crecimiento de $K/Y$ es la tasa de $K$ menos la de $Y$: $(n + g/b) - (n + ag/b) = (1-a)g/b = g$.
  - `D-Hab08-04` (procedural_slip, severidad `medium`): **Error en la tasa asintótica de crecimiento del producto agregado**
    - *Creencia errónea:* Calcular que el producto crece a la tasa simple $n + g$ sin considerar el efecto multiplicador de la acumulación inducida de capital.
    - *Manifestación:* Escribir $\dot{Y}/Y = n + g$.
    - *Remediación:* El progreso técnico induce acumulación adicional de capital; la tasa final de crecimiento de $Y$ es $n + \frac{ag}{1-a}$, la cual supera a $n+g$ si $a > 1/2$.
  - `D-Hab08-05` (notation, severidad `medium`): **Confundir progreso técnico Hicks-neutral con progreso aumentador de mano de obra (Harrod-neutral)**
    - *Creencia errónea:* Asumir que la formulación $A(t)F(K, L)$ equivale a multiplicar únicamente a la variable trabajo $F(K, A(t)L)$.
    - *Manifestación:* Modelar $Y = F(K, A(t)L)$ en lugar de $Y = A(t)F(K, L)$.
    - *Remediación:* Solow adopta explícitamente en la ecuación (13) progreso Hicks-neutral, multiplicando la función de producción global por una escala temporal $A(t)$.
  - `D-Hab08-06` (conceptual_swap, severidad `low`): **Afirmar que los salarios reales se estancan a pesar del progreso técnico**
    - *Creencia errónea:* Suponer que el crecimiento de la fuerza laboral a tasa $n$ mantiene los salarios reales deprimidos en el tiempo.
    - *Manifestación:* Declarar salario real constante cuando la economía tiene progreso tecnológico exógeno.
    - *Remediación:* A medida que $K/L$ crece indefinidamente, cada trabajador cuenta con más capital y mejor tecnología, provocando que el salario real aumente sin límite.

### `C-09`: Oferta de Trabajo con Elasticidad Salarial Positiva y Preservación del Estado Estacionario
- **Tipo:** `concept` | **Nivel Bloom:** `Understand` | **Unidad:** `21`
- **Descripción:** Comprender la generalización de Solow (1956) para una curva de oferta de mano de obra con elasticidad constante respecto al salario real $L = L_0 e^{nt} (w/p)^h$, analizando la ecuación modificada $\dot{r} = (sF(r, 1) - nr)(1 + ah)^{-1}$ y demostrando que el ratio capital-trabajo de estado estacionario permanece idéntico.
- **Prerrequisitos:** `Hab-03`, `C-08`
- **Evidencia:** [solow1956.pdf, pág. 23], [solow1956.pdf, pág. 24]
- **Distractores (3):**
  - `D-C09-01` (conceptual_swap, severidad `high`): **Creer que la elasticidad de oferta laboral altera el valor de equilibrio $r^*$ en la función Cobb-Douglas**
    - *Creencia errónea:* Afirmar que un cambio en la elasticidad salarial $h$ desplaza el capital por trabajador de estado estacionario.
    - *Manifestación:* Calcular un $r^*$ dependiente de $h$.
    - *Remediación:* La ecuación $\dot{r} = (sF(r,1) - nr)(1 + ah)^{-1}$ se anula exactamente cuando $sF(r,1) = nr$; por tanto, el ratio de capital de equilibrio no se ve afectado por la elasticidad de la oferta de trabajo $h$.
  - `D-C09-02` (procedural_slip, severidad `medium`): **Confundir la velocidad de ajuste dinámico con la posición final de equilibrio**
    - *Creencia errónea:* Suponer que el factor $(1 + ah)^{-1}$ acelera la velocidad de transición hacia el equilibrio.
    - *Manifestación:* Afirmar que mayor elasticidad salarial hace que la economía converja más rápidamente.
    - *Remediación:* Dado que $h > 0$ y $a > 0$, el denominador es mayor que 1, lo que reduce la magnitud de $\dot{r}$ en cada punto, ralentizando la velocidad de ajuste transitorio.
  - `D-C09-03` (overgeneralization, severidad `medium`): **Generalizar la invariancia de $r^*$ a funciones generales de oferta de trabajo $G(t, w/p)$**
    - *Creencia errónea:* Creer que cualquier función arbitraria de oferta de trabajo preservará intacto el valor $r^*$ del modelo base.
    - *Manifestación:* Afirmar que ninguna especificación de oferta laboral puede cambiar el valor de $r^*$.
    - *Remediación:* Solow aclara que la invariancia de $r^*$ es una consecuencia particular de la función multiplicativa con elasticidad constante (14), pero con una función general $G$ el estado estacionario sí se verá alterado.

### `C-10`: Tasa de Ahorro Endógena Dependiente del Rendimiento del Capital y Garantía de Estabilidad (Figura VIII)
- **Tipo:** `concept` | **Nivel Bloom:** `Analyze` | **Unidad:** `22`
- **Descripción:** Analizar el comportamiento del modelo cuando la propensión al ahorro depende positivamente del rendimiento del capital y negativamente del ratio capital-trabajo $s = s(r)$ (Figura VIII de Solow 1956), eliminando trayectorias explosivas y reforzando la estabilidad asintótica.
- **Prerrequisitos:** `C-05`, `C-08`
- **Evidencia:** [solow1956.pdf, pág. 24], [solow1956.pdf, pág. 25], [solow1956.pdf, pág. 26]
- **Distractores (3):**
  - `D-C10-01` (conceptual_swap, severidad `high`): **Creer que permitir ahorro variable hace posible un estado estacionario ricardiano con población creciente**
    - *Creencia errónea:* Suponer que si el ahorro cae a cero cuando el rendimiento es muy bajo, la economía alcanza un estado totalmente estacionario.
    - *Manifestación:* Afirmar que el capital se estaciona indefinidamente a pesar del crecimiento de la fuerza de trabajo.
    - *Remediación:* Solow recalca que mientras la fuerza laboral siga creciendo a tasa $n > 0$, la dilución del capital impedirá cualquier estado estacionario absoluto: si el ahorro cesa, $r$ cae hasta que la rentabilidad estimula de nuevo el ahorro.
  - `D-C10-02` (sign_error, severidad `medium`): **Invertir la dirección de la respuesta estabilizadora del ahorro variable**
    - *Creencia errónea:* Afirmar que un ahorro decreciente en $r$ desestabiliza el sistema económico aumentando la dispersión.
    - *Manifestación:* Concluir que $s'(r) < 0$ genera bifurcaciones caóticas o inestabilidad.
    - *Remediación:* Cuando el capital es escaso (bajo $r$), el rendimiento es alto y se ahorra más; cuando es abundante (alto $r$), se ahorra menos. Esta respuesta amortigua las desviaciones y refuerza la estabilidad.
  - `D-C10-03` (boundary_case, severidad `low`): **Suponer que la curva $s(r)F(r, 1)$ siempre debe situarse por debajo de la curva con ahorro constante**
    - *Creencia errónea:* Creer que la función de ahorro variable nunca puede superar a la función de ahorro fija.
    - *Manifestación:* Dibujar $s(r)F(r,1)$ estrictamente por debajo de $sF(r,1)$ para todo $r$.
    - *Remediación:* Para niveles bajos de $r$, la mayor rentabilidad del capital hace que $s(r) > s_{fijo}$, situando la curva por encima del modelo de referencia a la izquierda del punto de cruce.

## Sesión 8: Política Fiscal, Crecimiento Demográfico Endógeno y Rigideces Keynesianas

### `H-05`: Incidencia de la Tributación Proporcional sobre la Tasa Efectiva de Acumulación de Capital
- **Tipo:** `fact` | **Nivel Bloom:** `Remember` | **Unidad:** `23`
- **Descripción:** Identificar las fórmulas de la propensión efectiva al ahorro bajo un impuesto sobre la renta a tasa $t$: $s_{eff} = s + t(1-s)$ si la recaudación se invierte íntegramente, $s_{eff} = s(1-t)$ si se consume, y $s_{eff} = s + (v-s)t$ si el sector público invierte una fracción $v$ de sus ingresos.
- **Prerrequisitos:** `Hab-03`
- **Evidencia:** [solow1956.pdf, pág. 26], [solow1956.pdf, pág. 27]
- **Distractores (3):**
  - `D-H05-01` (conceptual_swap, severidad `high`): **Creer que cualquier impuesto sobre la renta necesariamente reduce la acumulación de capital**
    - *Creencia errónea:* Asumir que gravar la renta siempre deprime la tasa efectiva de ahorro de la economía.
    - *Manifestación:* Afirmar que un impuesto proporcional $t$ siempre reduce el capital de estado estacionario.
    - *Remediación:* Solow muestra que la tasa efectiva de ahorro pasa a ser $s + (v-s)t$. Si el Estado invierte una proporción mayor que el sector privado ($v > s$), el efecto neto del impuesto es elevar la acumulación de capital.
  - `D-H05-02` (procedural_slip, severidad `medium`): **Error de ponderación en la fórmula cuando el impuesto se invierte en su totalidad**
    - *Creencia errónea:* Calcular la nueva tasa de ahorro simplemente como $s + t$ sin ajustar la base de ingreso disponible privado.
    - *Manifestación:* Escribir $s_{eff} = s + t$.
    - *Remediación:* El ahorro privado es $s(1-t)Y$ y la inversión pública es $tY$. Al sumar ambos términos, se obtiene $[s(1-t) + t]Y = [s + t(1-s)]Y$.
  - `D-H05-03` (overgeneralization, severidad `low`): **Suponer que los impuestos distorsionan la estabilidad asintótica de la Figura I**
    - *Creencia errónea:* Afirmar que un impuesto proporcional altera la concavidad de la función de ahorro eliminando la estabilidad.
    - *Manifestación:* Predecir inestabilidad dinámica inducida por impuestos proporcionales.
    - *Remediación:* La introducción de un impuesto proporcional a tasa constante modifica la escala vertical de la curva $s_{eff}F(r,1)$, desplazando el valor de $r^*$, pero preservando intacta la estabilidad asintótica.

### `C-11`: Crecimiento Poblacional Endógeno $n(r)$, Trampa Malthusiana y Umbrales Críticos de Inversión (Figura IX)
- **Tipo:** `concept` | **Nivel Bloom:** `Analyze` | **Unidad:** `24`
- **Descripción:** Interpretar el diagrama de crecimiento poblacional endógeno dependiente del ingreso per cápita $\dot{r} = sF(r, 1) - n(r)r$ (Figura IX de Solow 1956): existencia de una trampa de estancamiento de bajo ingreso en $r_1$, un umbral crítico inestable en $r_2$, y la necesidad de un gran impulso de inversión ('big push') para alcanzar crecimiento auto-sostenido.
- **Prerrequisitos:** `C-05`, `C-06`
- **Evidencia:** [solow1956.pdf, pág. 27], [solow1956.pdf, pág. 28]
- **Distractores (3):**
  - `D-C11-01` (boundary_case, severidad `high`): **Creer que pequeñas acumulaciones graduales de capital pueden rescatar a una economía de la trampa malthusiana en $r_1$**
    - *Creencia errónea:* Suponer que pequeñas inyecciones marginales de capital permitirán escapar del equilibrio de bajo ingreso $r_1$.
    - *Manifestación:* Predecir convergencia a crecimiento autosostenido mediante pequeñas inversiones graduales inferiores a $r_2$.
    - *Remediación:* Solow demuestra que para cualquier $r < r_2$, la economía es atraída de regreso a $r_1$. Se requiere un impulso masivo ('big push') que eleve el capital inmediatamente por encima de $r_2$ para generar expansión autosostenida.
  - `D-C11-02` (conceptual_swap, severidad `high`): **Atribuir la necesidad de un 'Big Push' a indivisibilidades tecnológicas o rendimientos crecientes**
    - *Creencia errónea:* Afirmar que el fenómeno de umbral de despegue en la Figura IX requiere rendimientos crecientes a escala.
    - *Manifestación:* Explicar la trampa de desarrollo asumiendo curvas de costos con forma de U o rendimientos crecientes.
    - *Remediación:* Solow subraya que este resultado se obtiene en ausencia total de indivisibilidades o de rendimientos crecientes, emergiendo exclusivamente de la respuesta endógena de la fertilidad y mortalidad frente al ingreso per cápita.
  - `D-C11-03` (overgeneralization, severidad `medium`): **Asumir que la tasa de crecimiento demográfico $n(r)$ es monótonamente creciente en todo el dominio**
    - *Creencia errónea:* Creer que $n(r)$ crece indefinidamente con el ingreso per cápita.
    - *Manifestación:* Modelar $n(r)$ como una función lineal creciente sin saturación.
    - *Remediación:* La curva de población en la Figura IX refleja la transición demográfica: crece inicialmente con el ingreso pero luego se aplana y disminuye, permitiendo que la inversión supere a la dilución a altos niveles de capital.

### `C-12`: Salarios Reales Rígidos, Brecha de Empleo y Límites de la Ajustabilidad Neoclásica
- **Tipo:** `concept` | **Nivel Bloom:** `Understand` | **Unidad:** `25`
- **Descripción:** Comprender la sección final de Solow (1956): fijar un salario real rígido $\bar{w}/p$ fija la relación técnica en $\bar{r}$, determinando un crecimiento del empleo $\dot{L}/L = (s/\bar{r})F(\bar{r}, 1)$; si esta tasa es menor que el crecimiento demográfico $n$, surge desempleo involuntario permanente y creciente.
- **Prerrequisitos:** `C-04`, `C-08`
- **Evidencia:** [solow1956.pdf, pág. 28], [solow1956.pdf, pág. 29], [solow1956.pdf, pág. 30]
- **Distractores (3):**
  - `D-C12-01` (conceptual_swap, severidad `high`): **Creer que con salarios reales rígidos el ratio capital-trabajo continúa ajustándose dinámicamente**
    - *Creencia errónea:* Asumir que la variable $r$ puede continuar variando en el tiempo aun cuando el salario real permanezca inamovible.
    - *Manifestación:* Permitir que $\dot{r} \ne 0$ mientras $\bar{w}/p$ está congelado.
    - *Remediación:* Como $w/p = \partial F/\partial L$ depende exclusivamente de $r$, fijar el salario real fija directamente $r$ en $\bar{r}$; por ende, la variable de ajuste ya no es el ratio de capital sino el nivel de empleo.
  - `D-C12-02` (overgeneralization, severidad `high`): **Confundir la pendiente del rayo con la tasa de crecimiento del empleo**
    - *Creencia errónea:* Suponer que el empleo crece a la tasa demográfica $n$ independientemente del nivel del salario rígido.
    - *Manifestación:* Escribir $\dot{L}/L = n$ aun bajo salario real superior al de equilibrio.
    - *Remediación:* El empleo efectivo crece a la tasa $\frac{\dot{L}}{L} = \frac{s}{\bar{r}}F(\bar{r}, 1)$, que es la pendiente del rayo desde el origen a la curva de inversión en $\bar{r}$. Si esta pendiente es menor que $n$, el desempleo se magnifica continuamente.
  - `D-C12-03` (conceptual_swap, severidad `medium`): **Atribuir el desempleo a insuficiencia técnica de factores en vez de a la rigidez de precios**
    - *Creencia errónea:* Pensar que la falta de empleo se debe a proporciones fijas en la tecnología como en Harrod-Domar.
    - *Manifestación:* Afirmar que los coeficientes de producción se volvieron rígidos por razones de ingeniería.
    - *Remediación:* En la sección VII, la función de producción sigue siendo neoclásica con infinitas posibilidades de sustitución; el desempleo no surge de la tecnología, sino de la rigidez institucional del salario real.

