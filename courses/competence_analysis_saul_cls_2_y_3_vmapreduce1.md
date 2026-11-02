# Cognitive Task Analysis (CTA): Saul Cls 2 Y 3 Vmapreduce1

- **Course ID:** `saul_cls_2_y_3_vmapreduce1`
- **Macro-Competency:** Dominio y aplicación analítica integral de Saul Cls 2 Y 3 Vmapreduce1
- **Structure:** 15 total competencies (3 Facts, 7 Concepts, 5 Skills) with 90 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Distinción Económica entre Flujo y Stock de Contaminación | Concept | Understand | Unidad 2: Distinción Económica entre Flujo y Stock de Contaminación | - | 6 |
| `H-01` | Estructura del Funcional de Bienestar Social y Regularidad | Fact | Remember | Unidad 3: Estructura del Funcional de Bienestar Social y Regularidad | C-01 | 6 |
| `C-02` | Estructura Tecnológica y Dinámica del Modelo I | Concept | Understand | Unidad 5: Estructura Tecnológica y Dinámica del Modelo I | C-01 | 6 |
| `Hab-01` | Derivación de Condiciones de Primer Orden y Co-Estados en Modelo I | Skill | Apply | Unidad 5: Derivación de Condiciones de Primer Orden y Co-Estados en Modelo I | C-02, H-01 | 6 |
| `C-03` | Equilibrios de Estado Estacionario: Murky Age vs Golden Age | Concept | Analyze | Unidad 6: Equilibrios de Estado Estacionario: Murky Age vs Golden Age | C-02 | 6 |
| `H-02` | Regla de Acumulación Modificada de Capital en la Golden Age | Fact | Remember | Unidad 6: Regla de Acumulación Modificada de Capital en la Golden Age | C-03 | 6 |
| `Hab-02` | Determinación del Umbral Crítico y Política de Cierre en Modelo II | Skill | Analyze | Unidad 10: Determinación del Umbral Crítico y Política de Cierre en Modelo II | C-01, H-01 | 6 |
| `Hab-03` | Análisis de Estática Comparativa Dinámica ante Variaciones en la Tasa de Decaimiento | Skill | Evaluate | Unidad 11: Análisis de Estática Comparativa Dinámica ante Variaciones en la Tasa de Decaimiento | Hab-01, Hab-02 | 6 |
| `C-04` | Principio de Optimalidad de Bellman | Concept | Understand | Unidad 12: Principio de Optimalidad de Bellman | Hab-03 | 6 |
| `H-03` | Ecuación Recurrente de Asignación Óptima de Bellman | Fact | Remember | Unidad 4: Ecuación Recurrente de Asignación Óptima de Bellman | C-04 | 6 |
| `C-05` | Reducción de Dimensionalidad y Dualidad Valor-Política | Concept | Analyze | Unidad 4: Reducción de Dimensionalidad y Dualidad Valor-Política | H-03 | 6 |
| `C-06` | Estructura de Políticas Óptimas: Convexidad versus Concavidad | Concept | Analyze | Unidad 6: Estructura de Políticas Óptimas: Convexidad versus Concavidad | C-05 | 6 |
| `Hab-04` | Cálculo de Umbrales de Decisión en Políticas de Potencias | Skill | Apply | Unidad 6: Cálculo de Umbrales de Decisión en Políticas de Potencias | C-06 | 6 |
| `C-07` | Procesos Estocásticos de Decisión y Formulación de Minería de Oro | Concept | Understand | Unidad 10: Procesos Estocásticos de Decisión y Formulación de Minería de Oro | C-04 | 6 |
| `Hab-05` | Criterio de Selección por Ratio Ganancia-Pérdida en Procesos Estocásticos | Skill | Apply | Unidad 11: Criterio de Selección por Ratio Ganancia-Pérdida en Procesos Estocásticos | C-07 | 6 |

---

## Detailed Competency Specifications

### [C-01] Distinción Económica entre Flujo y Stock de Contaminación (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 2: Distinción Económica entre Flujo y Stock de Contaminación
- **Prerequisites:** None
- **Evidence Citations:** `SEGUNDO CONTROL DE LECTURA.pdf` (page 2)

#### Description & Cognitive Model
Marco teórico que formaliza la contaminación como problema de control óptimo distinguiendo variables de control (flujos como emisiones o abatimiento) de variables de estado (stocks acumulados $P$ sujetos a decaimiento natural a tasa $b$). A diferencia del capital tradicional (que rinde servicios positivos como stock y costo de acumulación como flujo), un contaminante típico genera un flujo beneficioso o producto conjunto en la producción pero causa desutilidad o daño social marginal negativo ($u_P < 0$) como stock acumulado.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Confusión conceptual | conceptual_swap | high | Considerar la contaminación únicamente como un flujo instantáneo que desaparece sin acumulación temporal | La contaminación genera desutilidad primaria a través de su nivel de stock acumulado en el medio ambiente, no solo por el flujo instantáneo. |
| `D-C01-02` | Inversión de propiedades | conceptual_swap | high | Modelar el contaminante como idéntico al capital: producto marginal negativo como flujo y utilidad positiva como stock | A diferencia del capital que brinda servicios positivos como stock y costo como flujo de inversión, el contaminante aporta al producto como flujo pero genera daño como stock acumulado. |
| `D-C01-03` | Error de delimitación de variables | conceptual_swap | high | Tratar el stock de contaminación $P$ como una variable de control directa seleccionada instantáneamente por el planificador | En la teoría de control óptimo, el stock no puede alterarse de manera instantánea; solo los controles determinan su tasa de cambio temporal. |
| `D-C01-04` | Sobre-generalización | conceptual_swap | high | Asumir que si la tasa de decaimiento $b$ es muy elevada, el problema debe continuar modelándose estrictamente como control de stock | Cuando la disipación natural es casi instantánea (como en la contaminación acústica), el stock no se acumula apreciablemente y el problema se reduce a regular el flujo. |
| `D-C01-05` | Error de alcance | conceptual_swap | high | Definir la contaminación únicamente como sustancias tóxicas industriales ignorando el agotamiento de recursos naturales renovables | Los autores establecen una definición comprehensiva que abarca basura física, radiación, pesticidas y el agotamiento de recursos naturales a ritmos superiores a su regeneración natural. |
| `D-C01-06` | Error de asignación de bienestar | conceptual_swap | high | Tratar el stock de contaminación como un bien privado divisible y asignable individualmente en la función de utilidad | El nivel de contaminación es un mal público indivisible que afecta el bienestar agregado de la sociedad y no puede desagregarse como un bien privado transferible. |

---

### [H-01] Estructura del Funcional de Bienestar Social y Regularidad (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 3: Estructura del Funcional de Bienestar Social y Regularidad
- **Prerequisites:** C-01
- **Evidence Citations:** `SEGUNDO CONTROL DE LECTURA.pdf` (page 3)

#### Description & Cognitive Model
El bienestar social intertemporal se formula como el funcional $W = \int_0^\infty u(c, P) e^{-rt} dt$, donde $r > 0$ es la tasa subjetiva de descuento temporal, $c$ es el flujo de consumo y $P$ es el stock acumulado de contaminación. La función de utilidad instantánea satisface $u_c > 0$, $u_{cc} < 0$, $u_P < 0$, $u_{PP} < 0$, la condición de Inada $\lim_{c \to 0} u_c = \infty$, curvatura estándar de curvas de indiferencia ($u_{cc}u_{PP} - u_{cP}^2 > 0$) y supuestos de no inferioridad.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Error de signos en derivadas | conceptual_swap | high | $u_c > 0, \quad u_{cc} > 0, \quad u_P > 0, \quad u_{PP} > 0$ | El consumo presenta utilidad marginal positiva y decreciente ($u_c > 0, u_{cc} < 0$), mientras que la contaminación genera desutilidad marginal creciente en magnitud ($u_P < 0, u_{PP} < 0$). |
| `D-H01-02` | Error en condición de no inferioridad | conceptual_swap | high | $u_{cc}u_{PP} - u_{cP}^2 < 0$ | Para garantizar que las curvas de indiferencia tengan la curvatura habitual en el plano $(c, P)$, el determinante debe ser positivo: $u_{cc}u_{PP} - u_{cP}^2 > 0$. |
| `D-H01-03` | Error de tasa de descuento | conceptual_swap | high | $W = \int_0^\infty u(c, P) e^{rt} dt \quad \text{con } r > 0$ | El descuento intertemporal exige el factor de descuento $e^{-rt}$ con $r > 0$ para que la integral de bienestar converja adecuadamente. |
| `D-H01-04` | Error en condición de Inada | conceptual_swap | high | $\lim_{c \to 0} u_c(c, P) = 0$ | Se postula que para $c = 0$, $u_c = \infty$, garantizando que el consumo nunca se anule en una trayectoria óptima interior. |
| `D-H01-05` | Confusión con separabilidad aditiva estricta | conceptual_swap | high | $u_{cP} = 0$ | En el Modelo I se permite la interacción $u_{cP} \ne 0$ sujeta a no inferioridad; la separabilidad aditiva $u(c, P) = g(c) - h(P)$ se introduce recién en el Modelo II. |
| `D-H01-06` | Error de especificación de argumentos | conceptual_swap | high | La utilidad depende de las derivadas temporales $\dot{c}$ y $\dot{P}$ en lugar de los niveles instantáneos | El bienestar social instantáneo evalúa directamente el flujo de consumo disponible $c$ y el nivel acumulado del mal ambiental $P$. |

---

### [C-02] Estructura Tecnológica y Dinámica del Modelo I (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 5: Estructura Tecnológica y Dinámica del Modelo I
- **Prerequisites:** C-01
- **Evidence Citations:** `SEGUNDO CONTROL DE LECTURA.pdf` (page 5)

#### Description & Cognitive Model
En el Modelo I la producción total $y = f(K)$ (con $f' > 0, f'' < 0$) se reparte entre consumo fraccional $\alpha$, abatimiento de contaminación fraccional $\beta$ e inversión en capital $(1 - \alpha - \beta)$. La dinámica del capital es $\dot{K} = (1 - \alpha - \beta)f(K) - aK$ con depreciación $a > 0$. La contaminación es un subproducto conjunto a razón unitaria de la producción y su abatimiento tiene productividad lineal $d$, resultando en la dinámica de acumulación $\dot{P} = (1 - \beta d)f(K) - bP$ sujeta a decaimiento natural $b \ge 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Error en ecuación de acumulación de contaminación | conceptual_swap | high | $\dot{P} = (1 - \beta)f(K) - bP$ | Cada unidad de producto destinada al control de contaminación reduce el flujo de contaminante en $d$ unidades, resultando en $(1 - \beta d)f(K)$. |
| `D-C02-02` | Error en balance presupuestario del producto | conceptual_swap | high | $\alpha + \beta + I = 1 + f(K)$ | El producto total $f(K)$ se asigna exhaustivamente a consumo $\alpha f(K)$, abatimiento $\beta f(K)$ e inversión bruta $\dot{K} + aK$. |
| `D-C02-03` | Confusión sobre la relación producto-contaminante | conceptual_swap | high | El flujo bruto de contaminación generado es exógeno e independiente de la producción $f(K)$ | El Modelo I asume producción conjunta estricta: cada unidad de producto genera una unidad proporcional de contaminante antes de aplicar depolución. |
| `D-C02-04` | Inversión de signos en la depreciación natural | conceptual_swap | high | $\dot{P} = (1 - \beta d)f(K) + bP \quad \text{con } b > 0$ | La asimilación natural descompone el stock contaminante a tasa $b$, reduciendo el stock existente con término negativo $-bP$. |
| `D-C02-05` | Error en rendimientos de abatimiento | conceptual_swap | high | Rendimientos decrecientes en el abatimiento con productividad marginal $d / \beta$ | El modelo postula retornos constantes en el esfuerzo de descontaminación: una unidad de producto gastada elimina exactamente $d$ unidades de polución. |
| `D-C02-06` | Error en la naturaleza del contaminante en Modelo I | conceptual_swap | high | El contaminante actúa como un insumo intermedio indispensable en la función de producción del Modelo I | En el Modelo I el contaminante no tiene utilidad productiva; su rol como insumo intermedio corresponde exclusivamente a la formulación del Modelo II. |

---

### [Hab-01] Derivación de Condiciones de Primer Orden y Co-Estados en Modelo I (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 5: Derivación de Condiciones de Primer Orden y Co-Estados en Modelo I
- **Prerequisites:** C-02, H-01
- **Evidence Citations:** `SEGUNDO CONTROL DE LECTURA.pdf` (page 5)

#### Description & Cognitive Model
Procedimiento para aplicar el Principio del Máximo de Pontryagin al Modelo I. Se formula el Hamiltoniano $H = e^{-rt}[u(\alpha f(K), P) + \kappa((1 - \alpha - \beta)f(K) - aK) + \pi((1 - \beta d)f(K) - bP)]$, se deducen las ecuaciones de co-estado de previsión perfecta $\dot{\kappa} = -\frac{\partial H}{\partial K}e^{rt} + r\kappa$ y $\dot{\pi} = -\frac{\partial H}{\partial P}e^{rt} + r\pi = (r + b)\pi - u_P$, y se resuelven las derivadas parciales de control $H_\alpha = e^{-rt}(u_c - \kappa)f(K)$ y $H_\beta = e^{-rt}(-\kappa - d\pi)f(K)$, determinando que la depolución activa exige $\pi = -\kappa/d$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Paso omitido | skipped_step | high | $\text{dotpi = (r+b)pi quad textomitiendo el im}$ | La ecuación de co-estado para el precio sombra de la contaminación debe incorporar el costo marginal social del stock $-u_P$. |
| `D-Hab01-02` | Paso omitido | skipped_step | high | $\text{pi = -kappa quad textomitiendo la escala}$ | Al maximizar el Hamiltoniano respecto a $\beta$, la condición de primer orden exige $-\kappa - d\pi = 0$, lo que implica $\pi = -\kappa/d$. |
| `D-Hab01-03` | Error de condición de esquina en control lineal | conceptual_swap | high | Si $H_\beta < 0$, fijar $\beta = 1$ para forzar la descontaminación forzosa | Dado que el Hamiltoniano es lineal en $\beta$, si $H_\beta < 0$ el valor óptimo de abatimiento se sitúa en su cota inferior $\beta = 0$. |
| `D-Hab01-04` | Error algebraico en co-estado de capital | conceptual_swap | high | $\text{dotkappa = (r - a)kappa - f'(K) quad tex}$ | La tasa efectiva de descuento del capital físico es $r + a$, reflejando tanto la preferencia temporal como el desgaste del stock. |
| `D-Hab01-05` | Error conceptual en signo de variable co-estado | conceptual_swap | high | Exigir que el precio sombra de la contaminación sea estrictamente positivo $\pi > 0$ | Dado que $P$ es un mal con $u_P < 0$, una unidad adicional de contaminación reduce el valor presente del bienestar, por lo que $\pi \le 0$. |
| `D-Hab01-06` | Error en condición de transversalidad | conceptual_swap | high | $\lim_{t \to \infty} \kappa(t) K(t) = 1 \quad \text{como condición asintótica}$ | Las condiciones de transversalidad para horizontes infinitos requieren que el valor presente de los stocks tienda a cero a medida que $t \to \infty$. |

---

### [C-03] Equilibrios de Estado Estacionario: Murky Age vs Golden Age (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 6: Equilibrios de Estado Estacionario: Murky Age vs Golden Age
- **Prerequisites:** C-02
- **Evidence Citations:** `SEGUNDO CONTROL DE LECTURA.pdf` (page 6)

#### Description & Cognitive Model
Caracterización de los estados estacionarios en el Modelo I donde $\dot{K} = 0$ y $\dot{P} = 0$. Existen a lo sumo dos pares $(K, P)$ óptimos: la 'Murky Age' ($H_\beta < 0, \beta = 0$), donde no se efectúa gasto en descontaminación, el capital y el consumo son elevados y la polución extrema se disipa únicamente por asimilación natural $b$; y la 'Golden Age' ($H_\beta = 0, \beta > 0, \pi = -\kappa/d$), donde se invierte activamente en depolución, manteniendo niveles inferiores de capital, consumo y contaminación.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Confusión conceptual de equilibrios | conceptual_swap | high | La Murky Age se caracteriza por un menor stock de capital y mayor gasto en depolución que la Golden Age | En la Murky Age no se destina producto a limpiar ($\beta = 0$), acumulándose más capital y consumo pero a costa de un nivel de contaminación mucho más elevado que en la Golden Age. |
| `D-C03-02` | Error de multiplicidad de equilibrios | conceptual_swap | high | Existen infinitos pares de equilibrio $(K, P)$ estacionarios para cualquier conjunto de parámetros dados | Los autores demuestran analíticamente que bajo las hipótesis de regularidad y no inferioridad existen como máximo dos estados estacionarios posibles: Golden Age y Murky Age. |
| `D-C03-03` | Error de jerarquía de bienestar | conceptual_swap | high | La Golden Age proporciona siempre un bienestar $u(c, P)$ estrictamente superior al de la Murky Age bajo cualquier parámetro | Como señalan los autores (p. 26), si bien en su calibración numérica el bienestar de Golden Age (16.234) supera al de Murky Age (16.08), en otras configuraciones este orden puede revertirse. |
| `D-C03-04` | Error en mecanismo de estabilización de Murky Age | conceptual_swap | high | En la Murky Age la contaminación se estabiliza gracias a impuestos pigouvianos centralizados sobre la producción | Por definición, en la Murky Age no se ejerce intervención depuradora ($\beta = 0$), de modo que la única fuerza que frena el crecimiento del contaminante es la disipación natural $bP$. |
| `D-C03-05` | Inversión de pendientes en espacio consumo-polución | conceptual_swap | high | La curva de equilibrio entre consumo y contaminación en el espacio $(c, P)$ es vertical e independiente de la preferencia social | La condición de no inferioridad asegura que la curva que satisface $u_P = -(r+b)\frac{u_c}{d}$ tenga pendiente negativa en el plano $(c, P)$, asegurando a lo sumo una intersección. |
| `D-C03-06` | Error en condición de existencia de Golden Age | conceptual_swap | high | La Golden Age existe obligatoriamente sin importar si el consumo resultante $c$ es negativo o supera la capacidad productiva neta | El equilibrio Golden Age exige que el consumo simultáneo satisfaga $0 < c < f(K) - aK$; si no se cumple esta cota física, la Golden Age no es alcanzable. |

---

### [H-02] Regla de Acumulación Modificada de Capital en la Golden Age (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 6: Regla de Acumulación Modificada de Capital en la Golden Age
- **Prerequisites:** C-03
- **Evidence Citations:** `SEGUNDO CONTROL DE LECTURA.pdf` (page 6)

#### Description & Cognitive Model
En el equilibrio de Golden Age con abatimiento activo ($\beta > 0$), la productividad marginal del capital satisface la regla modificada $f'(K) = \frac{r + a}{1 - 1/d}$. Dado que $f'' < 0$, existe un único nivel de capital $K$ compatible con la Golden Age. Asimismo, la relación estática entre utilidades marginales en dicho estado estacionario satisface $u_P = -(r + b)\frac{u_c}{d}$, desacoplando la determinación de $K$ del nivel directo de desutilidad marginal.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H02-01` | Error en la regla de acumulación dorada modificada | conceptual_swap | high | $\text{f'(K) = r + a quad textaplicando la regl}$ | En la Golden Age, la productividad marginal del capital debe ser mayor que $r+a$ para compensar el costo de depolución del contaminante coproducido, ajustándose por el divisor $(1 - 1/d)$. |
| `D-H02-02` | Error de signos en el factor corrector | conceptual_swap | high | $f'(K) = \frac{r + a}{1 + 1/d}$ | El denominador correcto es $1 - 1/d$; un signo positivo reduciría erróneamente la tasa de retorno requerida del capital. |
| `D-H02-03` | Error de condición de viabilidad tecnológica | conceptual_swap | high | La Golden Age es tecnológicamente viable para cualquier valor positivo arbitrario de productividad $d < 1$ | Si $d \le 1$, un gasto de una unidad de producto no alcanzaría a mitigar la contaminación generada por esa misma unidad, haciendo inviable el abatimiento neto. |
| `D-H02-04` | Confusión con la regla de la Murky Age | conceptual_swap | high | $f'(K) = \frac{r + a}{1 + \frac{u_P}{u_c(r+b)}}$ | En la Murky Age rige $f'(K) = \frac{r+a}{1 + \frac{u_P}{u_c(r+b)}}$, mientras que en la Golden Age el precio sombra está anclado por $\pi = -\kappa/d$, desacoplando $f'(K)$ de $u_P$. |
| `D-H02-05` | Error en la relación marginal entre utilidades | conceptual_swap | high | $u_P = -u_c \cdot (r + b) \cdot d$ | La relación entre desutilidad marginal y utilidad del consumo en la Golden Age es $u_P = -(r+b)\frac{u_c}{d}$, reflejando que mayor $d$ reduce el daño social tolerado por unidad de consumo. |
| `D-H02-06` | Error de unicidad del capital de Golden Age | conceptual_swap | high | Debido a la no linealidad pueden existir múltiples stocks de capital $K$ que satisfagan $f'(K) = \frac{r+a}{1-1/d}$ | La monotonicidad estricta de $f'(K)$ bajo $f''(K) < 0$ garantiza que, si existe solución, existe un único valor de $K$ que satisface la condición. |

---

### [Hab-02] Determinación del Umbral Crítico y Política de Cierre en Modelo II (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 10: Determinación del Umbral Crítico y Política de Cierre en Modelo II
- **Prerequisites:** C-01, H-01
- **Evidence Citations:** `SEGUNDO CONTROL DE LECTURA.pdf` (page 10)

#### Description & Cognitive Model
Procedimiento para analizar el Modelo II donde el contaminante $j(L_1)$ es insumo intermedio productivo y la utilidad es separable $u(c, P) = g(c) - h(P)$. A partir de la condición estática $H_{L_1} = g'f' + \pi j' + s = 0$ con holgura $s L_1 = 0$, se determina la cota inferior del precio sombra $\bar{\pi} = -\frac{g'(f(0))f'(0)}{j'(0)}$. En el plano de fases $(\pi, P)$, se halla la intersección de la trayectoria óptima silla con $\pi = \bar{\pi}$ para definir el stock crítico $\bar{P}$. Si el stock inicial satisface $P_0 > \bar{P}$, la política óptima dicta suspender totalmente la emisión ($L_1 = 0$) hasta que el decaimiento natural reduzca el contaminante a $\bar{P}$, tras lo cual $L_1$ aumenta progresivamente.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Paso omitido | skipped_step | high | $\text{barpi = -fracg'(f(0))j'(0) quad textomit}$ | El valor umbral $\bar{\pi}$ se deriva de $g'(f(0))f'(0) + \bar{\pi} j'(0) = 0$; omitir $f'(0)$ distorsiona la valoración de la transferencia laboral. |
| `D-Hab02-02` | Paso omitido | skipped_step | high | Permitir producción $L_1 > 0$ aun cuando $P_0 > \bar{P}$ asumiendo que un control parcial siempre supera la prohibición | Para niveles de stock por encima del umbral crítico ($P_0 > \bar{P}$), el precio sombra cae por debajo de $\bar{\pi}$, haciendo que el multiplicador $s > 0$ fuerce $L_1 = 0$. |
| `D-Hab02-03` | Error de trayectoria de aproximación | conceptual_swap | high | Cuando $P$ alcanza $\bar{P}$, saltar instantáneamente al punto estacionario final fijando $L_1 = L_1^*$ | La trayectoria óptima es una variedad silla continua: al cruzar $\bar{P}$, $L_1$ crece de manera continua mientras el stock sigue disminuyendo hacia el punto de reposo. |
| `D-Hab02-04` | Inversión de pendiente de la isoclina de estado estacionario | conceptual_swap | high | La curva $\dot{P} = 0$ en el espacio $(\pi, P)$ tiene pendiente negativa | Un aumento en $\pi$ (menos negativo) incrementa el empleo en el contaminante $L_1$, aumentando el flujo $j(L_1)$ y por ende el stock de equilibrio $P$. |
| `D-Hab02-05` | Error en la delimitación de asignación laboral | conceptual_swap | high | Asignar mano de obra $L_1 > \bar{L}$ donde la producción de consumo decrece | Más allá del máximo técnico $\bar{L}$, aumentar $L_1$ reduce el bien de consumo e incrementa la contaminación indeseada, lo cual es estrictamente ineficiente. |
| `D-Hab02-06` | Confusión sobre la naturaleza del umbral crítico | conceptual_swap | high | El umbral $\bar{P}$ es una constante biológica fija independiente de las preferencias de la sociedad $g(c)$ y $h(P)$ | El valor de $\bar{P}$ depende conjuntamente de la tecnología productiva, las preferencias intertemporales y la dinámica del sistema. |

---

### [Hab-03] Análisis de Estática Comparativa Dinámica ante Variaciones en la Tasa de Decaimiento (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 11: Análisis de Estática Comparativa Dinámica ante Variaciones en la Tasa de Decaimiento
- **Prerequisites:** Hab-01, Hab-02
- **Evidence Citations:** `SEGUNDO CONTROL DE LECTURA.pdf` (page 11)

#### Description & Cognitive Model
Método para evaluar las consecuencias cualitativas y de política pública ante cambios en la tasa de asimilación ambiental $b$ en el diagrama de fases $(\pi, P)$ del Modelo II. La variación de $b$ induce una torsión horaria del vector de movimiento $(\dot{\pi}, \dot{P})$ dado que $\frac{d}{db}(\dot{\pi}, \dot{P}) = (\pi, -P)$, empina la isoclina $\dot{\pi} = 0$ y aplana la isoclina $\dot{P} = 0$. Esto eleva el valor sombra estacionario $\pi^*$, incrementa el nivel crítico $\bar{P}$ y demuestra formalmente que a mayor capacidad de autoreparación natural, menor es la justificación económica para prohibir el contaminante.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Paso omitido | skipped_step | high | Concluir que al aumentar $b$ el stock estacionario $P^*$ siempre se reduce monótonamente para cualquier parámetro | Un aumento en $b$ incrementa $L_1^*$ (más emisiones), pero también acelera la absorción $bP$; por tanto, para valores intermedios $P^*$ puede variar en cualquier dirección antes de caer definitivamente. |
| `D-Hab03-02` | Paso omitido | skipped_step | high | Afirmar que un aumento en $b$ hace que la pendiente de $\dot{P} = 0$ aumente en el plano $(\pi, P)$ | Dado que $b$ está en el denominador de la condición de estado estacionario $P = j(L_1)/b$, un incremento en $b$ reduce la altura de la curva y la aplana. |
| `D-Hab03-03` | Inversión de implicancia de política | conceptual_swap | high | A mayor tasa de decaimiento $b$, más probable y urgente resulta implementar una política de prohibición total ($L_1 = 0$) | Si el contaminante se degrada con rapidez (alta $b$), la naturaleza absorbe el stock eficientemente, tolerando stocks mayores $\bar{P}$ antes de justificar un cierre productivo. |
| `D-Hab03-04` | Error en la rotación del campo vectorial | conceptual_swap | high | La derivada del vector de movimiento con respecto a $b$ genera una rotación antihoraria en la parte superior de la trayectoria | Dado que $\pi < 0$ y $P > 0$, el vector $(\pi, -P)$ apunta al tercer cuadrante, induciendo un giro horario en la trayectoria óptima. |
| `D-Hab03-05` | Error de estática comparativa sobre el precio sombra | conceptual_swap | high | El aumento en $b$ deprime el precio sombra estacionario $\pi^*$, haciéndolo más negativo y contrayendo $L_1^*$ | Un contaminante menos persistente genera menor daño acumulado en valor presente, por lo que su penalización sombra se relaja ($\pi^*$ sube hacia 0) y permite más producción. |
| `D-Hab03-06` | Confusión con el caso de baja persistencia | conceptual_swap | high | En contaminantes muy persistentes como el DDT (donde $b \approx 0$), la prohibición nunca es una política óptima | Con tasas de decaimiento casi nulas ($b \approx 0$), el daño acumulativo persiste casi indefinidamente, haciendo que el umbral $\bar{P}$ sea prácticamente nulo y justificando la prohibición. |

---

### [C-04] Principio de Optimalidad de Bellman (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 12: Principio de Optimalidad de Bellman
- **Prerequisites:** Hab-03
- **Evidence Citations:** `TERCER CONTROL DE LECTURA.pdf` (page 12)

#### Description & Cognitive Model
Principio fundamental de la programación dinámica que establece que en un proceso de decisión secuencial, una política óptima tiene la propiedad de que cualesquiera que sean el estado inicial y la decisión inicial, las decisiones restantes deben constituir una política óptima con respecto al estado resultante de la primera decisión.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Independencia absoluta de etapas | conceptual_swap | high | $f_N(s) = \sum_{k=1}^N \max_{d_k} R(s_k, d_k)$ | Asumir que cada etapa puede optimizarse de forma aislada ignora que la decisión actual transforma el estado futuro disponible para las etapas subsiguientes. |
| `D-C04-02` | Miopía de optimización inmediata | conceptual_swap | high | $d^* = \arg\max_{d} R(s, d)$ | Maximizar exclusivamente el rendimiento inmediato sin considerar el valor acumulado del estado resultante no garantiza la optimalidad global. |
| `D-C04-03` | Dependencia de la trayectoria histórica previa | conceptual_swap | high | $f(s_k \mid s_1, s_2, \dots, s_{k-1})$ | El principio exige que el estado actual resuma toda la información relevante; las decisiones óptimas futuras no dependen de la historia previa que llevó a dicho estado. |
| `D-C04-04` | Confusión entre variable de estado y variable de decisión | conceptual_swap | high | $s_{k+1} = d_k$ | El estado describe la configuración del sistema (recursos disponibles), mientras que la decisión es la acción elegida que transforma dicho estado mediante la función de transición. |
| `D-C04-05` | Optimización retrospectiva errónea | conceptual_swap | high | $\max_{d_1, \dots, d_{k-1}} [f(s_k)]$ | El principio de optimalidad orienta la optimización hacia adelante sobre las decisiones remanentes condicionadas al estado alcanzado, no hacia reoptimizar el pasado. |
| `D-C04-06` | Aditividad estática de recursos constantes | conceptual_swap | high | $R_N = g(y_1) + g(y_2) + \dots + g(y_N)$ | Creer que los recursos se mantienen constantes a lo largo del proceso sin sufrir depreciación ni transformación tras cada decisión. |

---

### [H-03] Ecuación Recurrente de Asignación Óptima de Bellman (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 4: Ecuación Recurrente de Asignación Óptima de Bellman
- **Prerequisites:** C-04
- **Evidence Citations:** `TERCER CONTROL DE LECTURA.pdf` (page 4)

#### Description & Cognitive Model
Ecuación funcional para un proceso de asignación determinista de $N$ etapas: $f_N(x) = \max_{0 \le y \le x} [g(y) + h(x-y) + f_{N-1}(ay + b(x-y))]$, donde $x$ es el recurso inicial, $y$ es la cantidad asignada a la primera actividad y $a, b \in (0, 1)$ representan las tasas de recursos remanentes.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H03-01` | Omisión del recurso remanente transformado en la etapa siguiente | conceptual_swap | high | $f_N(x) = \max_{0 \le y \le x} [g(y) + h(x-y) + f_{N-1}(x)]$ | El recurso disponible en la siguiente etapa depende de las tasas de retorno $a$ y $b$ aplicadas a las asignaciones $y$ y $x-y$. |
| `D-H03-02` | Permutación de parámetros de eficiencia en la transformación | conceptual_swap | high | $f_N(x) = \max_{0 \le y \le x} [g(y) + h(x-y) + f_{N-1}(by + a(x-y))]$ | El coeficiente $a$ corresponde a la fracción conservada de la actividad $y$ asociada a $g(y)$, mientras que $b$ corresponde a $x-y$ asociada a $h(x-y)$. |
| `D-H03-03` | Rango de maximización no restringido en el dominio físico | conceptual_swap | high | $\max_{y \in \mathbb{R}} [g(y) + h(x-y) + f_{N-1}(ay + b(x-y))]$ | La asignación $y$ no puede ser negativa ni exceder la cantidad total del recurso disponible $x$. |
| `D-H03-04` | Evaluación simultánea no divisible del recurso total | conceptual_swap | high | $f_N(x) = g(x) + h(x) + f_{N-1}(ax + bx)$ | No es posible asignar el recurso total $x$ a ambas actividades al mismo tiempo; debe repartirse óptimamente entre $y$ y $x-y$. |
| `D-H03-05` | Inversión de índices temporales en la recursión | conceptual_swap | high | $f_{N-1}(x) = \max_{0 \le y \le x} [g(y) + h(x-y) + f_N(ay + b(x-y))]$ | El algoritmo resuelve retrospectivamente: $f_N$ calcula el retorno de $N$ etapas apoyándose en el retorno óptimo ya conocido de $N-1$ etapas restantes. |
| `D-H03-06` | Estructura multiplicativa en lugar de aditiva para retornos acumulados | conceptual_swap | high | $f_N(x) = \max_{0 \le y \le x} [(g(y) + h(x-y)) \cdot f_{N-1}(ay + b(x-y))]$ | El rendimiento acumulado del proceso multi-etapa es la suma del beneficio inmediato y el valor óptimo futuro, no su producto. |

---

### [C-05] Reducción de Dimensionalidad y Dualidad Valor-Política (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 4: Reducción de Dimensionalidad y Dualidad Valor-Política
- **Prerequisites:** H-03
- **Evidence Citations:** `TERCER CONTROL DE LECTURA.pdf` (page 4)

#### Description & Cognitive Model
Principio metodológico que transforma la maximización clásica simultánea de $N$ variables sobre un politopo restringido en una secuencia de $N$ problemas unidimensionales independientes de la escala temporal, sustentado en la relación biyectiva entre la función de valor $f_N(x)$ y la función de política óptima $y_N(x)$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Colapso dimensional mediante agregación estática directa | conceptual_swap | high | $\mathbb{R}^N \to \mathbb{R}^1 \quad \text{mediante suma no desacoplada}$ | La programación dinámica no fusiona las variables en una sola fórmula cerrada, sino que las desacopla en una cadena secuencial de optimizaciones unidimensionales anidadas. |
| `D-C05-02` | Asimetría unidireccional en la relación valor-política | conceptual_swap | high | $f_N(x) \Rightarrow y_N(x) \quad \text{pero} \quad y_N(x) \not\Rightarrow f_N(x)$ | Existe una dualidad simétrica: determinar la función de política permite evaluar el retorno por sustitución recursiva, tal como el valor óptimo determina la política. |
| `D-C05-03` | Exigencia de almacenamiento global de toda la trayectoria temporal | conceptual_swap | high | $\{y_1(x), y_2(x), \dots, y_N(x)\} \quad \forall N$ | Para la toma de decisiones prácticas en el estado inicial $x$, el tomador de decisiones únicamente requiere la política inmediata $y_1(x)$, no toda la secuencia futura. |
| `D-C05-04` | Asunción de derivabilidad interior en presencia de extremos de frontera | conceptual_swap | high | $\nabla R_N = 0 \iff \text{óptimo global garantizado}$ | El cálculo diferencial convencional falla porque los máximos frecuentemente se ubican en los extremos del dominio ($y=0$ o $y=x$), donde el gradiente no se anula. |
| `D-C05-05` | Aproximación ciega en funciones de valor sin explotar políticas | conceptual_swap | high | $f_k(x) \to f(x) \quad \text{por aproximación de funciones}$ | Aproximar en el espacio de políticas aprovechando la intuición económica converge de forma monótona y resulta más eficiente computacionalmente que aproximar sucesiones de funciones. |
| `D-C05-06` | Identificación errónea de la solución estacionaria con etapa única | conceptual_swap | high | $f_\infty(x) = f_1(x)$ | La solución estacionaria de horizonte infinito acumula el retorno compuesto de infinitas decisiones futuras, divergiendo sustancialmente del retorno de una etapa aislada. |

---

### [C-06] Estructura de Políticas Óptimas: Convexidad versus Concavidad (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 6: Estructura de Políticas Óptimas: Convexidad versus Concavidad
- **Prerequisites:** C-05
- **Evidence Citations:** `TERCER CONTROL DE LECTURA.pdf` (page 6)

#### Description & Cognitive Model
Caracterización cualitativa del comportamiento de la política óptima: si las funciones de retorno $g(x)$ y $h(x)$ son estrictamente convexas, la política óptima es extremal o bang-bang ($y=0$ o $y=x$); mientras que bajo concavidad estricta ($g'', h'' \le 0$) surgen soluciones interiores con monotonicidad en las etapas ($y_1 \le y_2 \le \dots$ si $b < a$).

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Interioridad errónea bajo retornos convexos crecientes | conceptual_swap | high | $g'', h'' > 0 \Rightarrow 0 < y^* < x$ | Las funciones convexas alcanzan su valor máximo en los extremos del intervalo $[0, x]$, no en un punto interior estacionario. |
| `D-C06-02` | Independencia falsa del orden de monotonicidad respecto a las tasas | conceptual_swap | high | $y_1 \le y_2 \le y_3 \le \dots \quad \forall a, b$ | La dirección del crecimiento de la asignación depende críticamente de la relación entre las tasas de depreciación: si $b > a$, la desigualdad se invierte por completo. |
| `D-C06-03` | Confusión de consecuencias de regularidad bajo concavidad | conceptual_swap | high | $g, h \text{ cóncavas} \Rightarrow f(x) \text{ no diferenciable}$ | La concavidad de las funciones de etapa se transmite a la función de valor, garantizando la regularidad y unicidad de la política óptima. |
| `D-C06-04` | Asignación de política bang-bang a rendimientos marginales decrecientes | conceptual_swap | high | $g'', h'' \le 0 \Rightarrow y^* \in \{0, x\}$ | Los rendimientos decrecientes corresponden a concavidad, lo que incentiva la diversificación simultánea entre ambas actividades en vez de una política de todo o nada. |
| `D-C06-05` | Uso de condición de primer orden sin verificación de curvatura | conceptual_swap | high | $g'(y) = h'(x-y) \Rightarrow y^* \text{ siempre maximiza}$ | Cuando las funciones de retorno son convexas, la anulación de la primera derivada ubica el punto de mínimo retorno posible, resultando en una decisión desastrosa. |
| `D-C06-06` | Suposición de asignación constante insensible a la escala del recurso | conceptual_swap | high | $y^*(x) = k \quad \forall x$ | Fijar la decisión a una constante numérica ignora la cota presupuestaria física $0 \le y \le x$ cuando el recurso $x$ varía dinámicamente. |

---

### [Hab-04] Cálculo de Umbrales de Decisión en Políticas de Potencias (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 6: Cálculo de Umbrales de Decisión en Políticas de Potencias
- **Prerequisites:** C-06
- **Evidence Citations:** `TERCER CONTROL DE LECTURA.pdf` (page 6)

#### Description & Cognitive Model
Derivación analítica del umbral crítico de estado $x_0 = \left[ \frac{c/(1-a^d)}{e/(1-b^f)} \right]^{\frac{1}{f-d}}$ para resolver ecuaciones funcionales de la forma $F(x) = \max [cx^d + F(ax), ex^f + F(bx)]$, particionando el espacio de estados entre $y=x$ para $x \le x_0$ y $y=0$ para $x \ge x_0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Omisión de la serie geométrica acumulada de retornos futuros | skipped_step | high | $x_0 = \left[ \frac{c}{e} \right]^{\frac{1}{f-d}}$ | Al calcular el valor de las ramas puras en horizonte infinito, es indispensable sumar la serie geométrica del retorno futuro compuesto. |
| `D-Hab04-02` | Inversión algebraica del exponente al despejar la variable de estado | skipped_step | high | $x_0 = \left[ \frac{c/(1-a^d)}{e/(1-b^f)} \right]^{f-d}$ | Al despejar la variable $x$ de la ecuación de indiferencia $x^{f-d} = K$, la potencia pasa al otro miembro como su exponente recíproco. |
| `D-Hab04-03` | Inversión de las regiones de decisión en el espacio de estados | conceptual_swap | high | $y=0 \text{ para } x \le x_0, \quad y=x \text{ para } x \ge x_0$ | Si $d < f$, para recursos pequeños la potencia menor domina numéricamente, haciendo óptima la asignación completa $y=x$ hasta el umbral. |
| `D-Hab04-04` | Violación de la condición de convergencia geométrica en el horizonte | conceptual_swap | high | $a^d \ge 1 \quad \text{o} \quad b^f \ge 1$ | Para que la solución del horizonte infinito tenga sentido matemático finito, los coeficientes de amortiguación deben ser estrictamente sub-unitarios. |
| `D-Hab04-05` | Intercambio erróneo de factores de descuento cruzados | conceptual_swap | high | $x_0 = \left[ \frac{e/(1-a^d)}{c/(1-b^f)} \right]^{\frac{1}{f-d}}$ | El coeficiente $c$ multiplica a la tasa $a^d$ de su propia alternativa; no puede emparejarse con la tasa $b^f$ de la opción rival. |
| `D-Hab04-06` | Planteamiento por maximización de diferencias en vez de punto de indiferencia | skipped_step | high | $x_0 = \arg\max_x \left[ \frac{c}{1-a^d} x^d - \frac{e}{1-b^f} x^f \right]$ | El umbral que delimita el cambio de política surge de la igualdad estricta de los retornos acumulados entre ambas opciones, no de su derivada nula. |

---

### [C-07] Procesos Estocásticos de Decisión y Formulación de Minería de Oro (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 10: Procesos Estocásticos de Decisión y Formulación de Minería de Oro
- **Prerequisites:** C-04
- **Evidence Citations:** `TERCER CONTROL DE LECTURA.pdf` (page 10)

#### Description & Cognitive Model
Modelado de procesos secuenciales estocásticos con riesgo de terminación catastrófica, donde la función de valor $f(x, y)$ representa el oro esperado total antes de que la máquina se destruya, expresada mediante ecuaciones condicionales: $f_A(x, y) = p_1 [r_1 x + f((1-r_1)x, y)]$ y $f_B(x, y) = p_2 [r_2 y + f(x, (1-r_2)y)]$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Omisión de la probabilidad de supervivencia en el valor futuro | conceptual_swap | high | $f_A(x, y) = p_1 r_1 x + f((1-r_1)x, y)$ | Si la máquina se destruye (con probabilidad $1-p_1$), el proceso cesa irreversiblemente, por lo que el retorno futuro debe estar ponderado por la supervivencia $p_1$. |
| `D-C07-02` | Confusión entre recurso extraído y recurso remanente en el estado | conceptual_swap | high | $f_A(x, y) = p_1 [r_1 x + f(r_1 x, y)]$ | El nuevo estado de la mina contiene la reserva remanente $(1-r_1)x$, no la porción $r_1 x$ que ya fue extraída en la etapa actual. |
| `D-C07-03` | Depreciación artificial de la mina no seleccionada | conceptual_swap | high | $f_A(x, y) = p_1 [r_1 x + f((1-r_1)x, (1-r_2)y)]$ | La operación en la mina Amerconda no afecta el volumen de oro de la mina Bonanza, cuyo recurso permanece intacto en $y$. |
| `D-C07-04` | Pretensión de enumeración exhaustiva de secuencias infinitas | conceptual_swap | high | $S \in \{A, B\}^\infty \quad \text{enumeración exhaustiva}$ | La formulación funcional condensa infinitas combinaciones de trayectorias estocásticas en una única ecuación recursiva soluble. |
| `D-C07-05` | Tratamiento determinista del horizonte de operación | conceptual_swap | high | $N = \text{constante fija de pasos}$ | El horizonte de planificación no es un número fijo predeterminado, sino una variable aleatoria gobernada por la tasa geométrica de fallas. |
| `D-C07-06` | Descuento temporal exógeno en lugar de supervivencia estocástica | conceptual_swap | high | $f(x, y) = \sum_{t=0}^\infty \beta^t R_t \quad (\beta \text{ exógeno})$ | El factor de ponderación no proviene de una tasa financiera subjetiva, sino de la probabilidad física de supervivencia de la maquinaria. |

---

### [Hab-05] Criterio de Selección por Ratio Ganancia-Pérdida en Procesos Estocásticos (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 11: Criterio de Selección por Ratio Ganancia-Pérdida en Procesos Estocásticos
- **Prerequisites:** C-07
- **Evidence Citations:** `TERCER CONTROL DE LECTURA.pdf` (page 11)

#### Description & Cognitive Model
Procedimiento de optimización para determinar la mina a operar comparando los índices de rendimiento relativo $\frac{p_1 r_1 x}{1 - p_1}$ frente a $\frac{p_2 r_2 y}{1 - p_2}$, seleccionando la mina $A$ si el primer ratio es mayor, la mina $B$ si es menor, o cualquiera si son iguales.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Comparación miope de retornos esperados ignorando la tasa de daño | skipped_step | high | $\text{Elegir } A \iff p_1 r_1 x > p_2 r_2 y$ | Comparar únicamente la ganancia inmediata esperada ignora que una mayor probabilidad de destrucción de la máquina ($1-p_1$) cancela todo beneficio futuro. |
| `D-Hab05-02` | Inversión de la dirección de eficiencia en el ratio de decisión | skipped_step | high | $\frac{1 - p_1}{p_1 r_1 x} > \frac{1 - p_2}{p_2 r_2 y} \Rightarrow \text{Elegir } A$ | El criterio óptimo busca maximizar la ganancia inmediata obtenida por unidad de riesgo asumido; invertir el cociente prescribe la peor alternativa posible. |
| `D-Hab05-03` | Uso de la probabilidad de supervivencia en el denominador | conceptual_swap | high | $\text{Ratio} = \frac{p_1 r_1 x}{p_1} = r_1 x$ | El denominador mide el costo de oportunidad esperado (probabilidad de rotura $1-p_1$), no la probabilidad de que la máquina sobreviva. |
| `D-Hab05-04` | Elección basada exclusivamente en la reserva absoluta total de mineral | conceptual_swap | high | $\text{Elegir } A \iff x > y$ | Una mina con menor depósito puede ser preferible si ofrece una tasa de extracción más favorable o un riesgo de rotura significativamente menor. |
| `D-Hab05-05` | Omisión de la actualización del estado tras el primer paso | skipped_step | high | $\text{Tras operar } A, \text{ reevaluar } \frac{p_1 r_1 x}{1 - p_1}$ | Después de cada extracción exitosa, la reserva de la mina operada se reduce a $(1-r_1)x$, lo que exige recalcular su ratio frente a la otra mina intacta. |
| `D-Hab05-06` | Fusión aditiva de ratios en lugar de evaluación por índices independientes | conceptual_swap | high | $\arg\max \left[ \frac{p_1 r_1 x}{1 - p_1} + \frac{p_2 r_2 y}{1 - p_2} \right]$ | El problema exige seleccionar una única mina a operar en cada etapa mediante una regla de índice de prioridad, no evaluar una combinación lineal conjunta. |

---
