# 1. Macro-Competencia Terminal Inferida
Formular, reducir matricialmente, resolver cuantitativamente y diagnosticar cualitativamente la dinámica local y global de sistemas acoplados bidimensionales de ecuaciones diferenciales ordinarias (lineales y no lineales autónomos) en modelos macroeconómicos y de crecimiento, deduciendo estados estacionarios de largo plazo, trayectorias analíticas explícitas según la estructura de sus valores propios y regímenes de estabilidad asintótica o ciclicidad persistente.

# 2. Desglose Cognitivo Exhaustivo (CTA)

## A. Hechos Requeridos [H] (Facts)
- **[H-01]** `Polinomio Característico Canónico 2x2`: $p(\lambda) = \lambda^2 - \text{tr}(A)\lambda + \det(A) = 0$, donde para $A = \begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix}$, $\text{tr}(A) = a_{11} + a_{22}$ y $\det(A) = a_{11}a_{22} - a_{12}a_{21}$.
- **[H-02]** `Fórmula Cuadrática Espectral y Discriminante`: $\lambda_{1,2} = \frac{\text{tr}(A) \pm \sqrt{\Delta}}{2}$, con discriminante $\Delta = [\text{tr}(A)]^2 - 4\det(A)$.
- **[H-03]** `Inversa Matricial de Dimensión 2x2`: $A^{-1} = \frac{1}{\det(A)}\begin{bmatrix} a_{22} & -a_{12} \\ -a_{21} & a_{11} \end{bmatrix}$, válida si y solo si $\det(A) \neq 0$.
- **[H-04]** `Solución Particular Constante`: $X_p = -A^{-1}B$ para sistemas no homogéneos $\dot{X} = AX + B$ donde $B$ es un vector invariante en el tiempo y $\det(A) \neq 0$.
- **[H-05]** `Base Real para Autovalores Complejos Conjugados`: Si $\lambda_{1,2} = a \pm bi$ con autovector $v = r \pm si$, la solución complementaria es $X_h(t) = c_1 e^{at}[r\cos(bt) - s\sin(bt)] + c_2 e^{at}[s\cos(bt) + r\sin(bt)]$.
- **[H-06]** `Definición de Autovector Generalizado`: Para raíz real repetida $\lambda$ con deficiencia geométrica, el vector generalizado satisface $(A - \lambda I)v_2 = v_1$, generando la solución $X(t) = c_1 e^{\lambda t}v_1 + c_2 e^{\lambda t}(v_2 + v_1 t)$.
- **[H-07]** `Matriz Jacobiana Local 2x2`: $J(x,y) = \begin{bmatrix} \frac{\partial f}{\partial x} & \frac{\partial f}{\partial y} \\ \frac{\partial g}{\partial x} & \frac{\partial g}{\partial y} \end{bmatrix}$ para sistemas autónomos no lineales $\dot{x} = f(x,y)$, $\dot{y} = g(x,y)$.
- **[H-08]** `Álgebra de Tasas de Variación Proporcional`: $\frac{d}{dt}\ln(u/v) = \frac{\dot{u}}{u} - \frac{\dot{v}}{v}$ y $\frac{d}{dt}\ln(uv) = \frac{\dot{u}}{u} + \frac{\dot{v}}{v}$, requeridas para modelos de ratios distributivos y de empleo.

## B. Conceptos Estructurales [C] (Concepts)
- **[C-01]** `Principio de Superposición y Partición de Soluciones`: La trayectoria temporal se descompone en $X(t) = X_h(t) + X_p(t)$, donde $X_h(t)$ modela la dinámica transitoria hacia o desde el origen y $X_p(t)$ ancla la posición de largo plazo o tendencia estructural.
  - *Distinción fina / Trampa común:* $X_p$ no siempre es estático; si el término no homogéneo depende del tiempo ($B(t)$), el equilibrio es una trayectoria móvil y no un punto de reposo.
- **[C-02]** `Tipología Topológica en el Plano Traza-Determinante`: Si $\det(A) < 0$, las raíces tienen signos opuestos (Punto Silla); si $\det(A) > 0$ y $\text{tr}(A) < 0$, estabilidad asintótica local (Nodo Estable si $\Delta \ge 0$, Foco Estable si $\Delta < 0$); si $\det(A) > 0$ y $\text{tr}(A) = 0$, Centro armónico con órbitas cerradas periódicas.
  - *Distinción fina / Trampa común:* Confundir estabilidad marginal con asintótica; un centro ($	ext{tr}(A)=0$) no converge a un punto, preserva órbitas perpetuas.
- **[C-03]** `Frontera de Linealización y No Hiperbolicidad`: En sistemas no lineales, la aproximación local vía $J(x^*,y^*)$ preserva la topología solo en equilibrios hiperbólicos ($\text{Re}(\lambda) \neq 0$).
  - *Distinción fina / Trampa común:* En modelos como Lotka-Volterra o ciclos de Goodwin, el Jacobiano en el equilibrio arroja $	ext{tr}(J^*)=0$; linealmente predice un centro, pero la no linealidad subyacente exige constatar que las trayectorias no se transformen en espirales degeneradas.
- **[C-04]** `Desacoplamiento Causal Unidireccional (Bloque Triangular)`: En matrices dinámicas triangulares (como en el modelo Solow-Polución con $J_{12} = 0$), los autovalores coinciden con la diagonal.
  - *Distinción fina / Trampa común:* Calcular el discriminante completo de forma innecesaria en lugar de leer directamente los autovalores de los elementos de la diagonal principal.
- **[C-05]** `Leyes de Movimiento por Exceso de Demanda`: En formulaciones de ajuste IS-LM o macro dinámicas, las variables de estado evolucionan proporcionalmente a brechas de mercado ($D_t - O_t$ o $L^d_t - L^o_t$) reguladas por parámetros de velocidad de ajuste $c_1, c_2, v, \mu$.
  - *Distinción fina / Trampa común:* Omitir que las velocidades de ajuste determinan la velocidad de convergencia o amortiguamiento, pero no alteran la posición del equilibrio estático de largo plazo.

## C. Habilidades Procedimentales y de Decisión [Hab] (Skills)
- **[Hab-01]** `Reducción Estructural a Forma Matricial Compacta`: Sustituir ecuaciones de comportamiento e identidades contables/estáticas dentro de las leyes de movimiento temporal para aislar $\dot{X} = AX + B$.
  - *Entrada necesaria:* Funciones de consumo, inversión, demanda de dinero y ecuaciones diferenciales de brecha.
  - *Salida esperada:* Matriz $A_{2\times 2}$ y vector de forzamiento $B_{2\times 1}$ parametrizados.
- **[Hab-02]** `Inversión Algebraica Simbólica para Estados Estacionarios`: Computar analíticamente $-A^{-1}B$ o igualar $f(x,y)=0, g(x,y)=0$ para aislar coordenadas de equilibrio de largo plazo.
  - *Entrada necesaria:* Matriz $A$ invertible y vector constante $B$ (o ecuaciones no lineales igualadas a cero).
  - *Salida esperada:* Expresiones analíticas del vector de equilibrio $(Y^E, r^E)$ o $(K^*, P^*)$.
- **[Hab-03]** `Diagnóstico Espectral Directo mediante Traza, Determinante y Discriminante`: Evaluar algebraicamente los signos de $\text{tr}(A)$, $\det(A)$ y $\Delta$ para categorizar el régimen dinámico sin calcular los autovectores.
  - *Entrada necesaria:* Matriz $A_{2\times 2}$ o Jacobiano $J^*$.
  - *Salida esperada:* Diagnóstico categórico (ej., 'Foco asintóticamente estable con trayectoria oscilatoria amortiguada').
- **[Hab-04]** `Resolución de Subespacios Propios para Trayectorias Explícitas`: Resolver el sistema algebraico homogéneo $(A - \lambda_i I)v_i = 0$ para autovalores reales distintos o complejos, normalizando vectores base.
  - *Entrada necesaria:* Matriz $A$ y raíces características $\lambda_1, \lambda_2$.
  - *Salida esperada:* Vectores propios $v_1, v_2$ y solución general parametrizada con constantes arbitrarias $c_1, c_2$.
- **[Hab-05]** `Ajuste por Coeficientes Indeterminados en Sistemas No Homogéneos`: Plantear una propuesta polinomial $X_p(t) = A_1 t + A_0$ para forzamientos no constantes y derivar el sistema algebraico acoplado.
  - *Entrada necesaria:* Sistema dinámico $\dot{X} = AX + B(t)$ donde $B(t)$ es función lineal de $t$.
  - *Salida esperada:* Vectores de constantes $A_1$ y $A_0$ resueltos.
- **[Hab-06]** `Linealización Diferencial Alrededor del Estado Estacionario`: Diferenciar parcialmente sistemas no lineales y evaluar las derivadas en el punto interior positivo $(x^*, y^*)$.
  - *Entrada necesaria:* Funciones de flujo $f(x,y), g(x,y)$ y punto crítico no nulo.
  - *Salida esperada:* Matriz jacobiana evaluada $J^*$ y sistema traslatorio $\dot{X} \approx J^*(X - X^*)$.
- **[Hab-07]** `Conversión Log-Diferencial de Variables Ratio`: Pasar de definiciones de nivel a tasas de crecimiento para derivar ecuaciones de estado no lineales acopladas.
  - *Entrada necesaria:* Definición de tasa de empleo $v = L/N$ o participación salarial $u = w/a$ junto con las tasas de crecimiento de sus componentes.
  - *Salida esperada:* Ecuaciones diferenciales canónicas $\dot{v} = v(...)$ y $\dot{u} = u(...)$ tipo Lotka-Volterra.

# 3. Puntos Ciegos del Experto y Pasos Implícitos (Expert Blindness)
| Paso Implícito / Trampa | Por qué el texto teórico lo omite | Impacto si el alumno no lo domina |
|---|---|---|
| Eliminación algebraica de derivadas implícitas | El autor asume que el alumno domina la sustitución hacia atrás antes de escribir la matriz | El estudiante no logra obtener los coeficientes de la segunda fila y falla en deducir el sistema |
| Evaluación de condiciones iniciales sobre el nivel total vs desviación | Enfoque centrado en la solución complementaria; se sobreentiende la traslación | El alumno evalúa X(0) en Xh(0) olvidando restar Xp invalidando las constantes |
| Desacoplamiento inmediato de matrices triangulares | El experto reconoce que los autovalores de una matriz triangular son su diagonal | Pérdida de tiempo y errores al calcular el determinante simbólico completo |
| Condiciones de validez económica en denominadores | Foco puramente algebraico en la inversión matricial, asumiendo parámetros razonables | Incapacidad de interpretar casos donde el sistema diverge o genera equilibrios negativos |
| Pérdida de la validez de linealización ante centros | Se asumen conocidas las limitaciones de Hartman-Grobman para equilibrios no hiperbólicos | El alumno asume que cualquier Jacobiano con traza cero es necesariamente un centro estable |

# 4. Semillas de Automatización y Fluidez (Top's Academy)
| ID Habilidad | Micro-Competencia a Automatizar | Tipo de Ejercicio Mecánico Sugerido | Parámetros que deben variar aleatoriamente |
|---|---|---|---|
| **Hab-03** | Lectura instantánea de traza y determinante para tipificar dinámicas 2x2 | Opción múltiple: Clasificar si es Punto Silla, Foco Estable, Nodo Inestable o Centro | Entradas de A en [-8, 8], alternando signos |
| **Hab-02** | Cálculo numérico directo de equilibrios constantes X* = -A^{-1}B | Entrada numérica directa: computar (x*, y*) | Coeficientes enteros de A con det(A) en [-5, 5] no nulo, B en [-10, 10] |
| **Hab-06** | Ensamblado y evaluación de matrices Jacobianas en el equilibrio | Completar matriz: derivadas parciales evaluadas en (x*, y*) | Parámetros de captura y tasas de crecimiento en (0, 2) |
| **Hab-04** | Construcción de autovectores para raíces reales | Respuesta corta: Determinar vector base v = [1, k]^T | Matriz triangular o simétrica con autovalor entero dado |
| **Hab-07** | Derivada temporal logarítmica de combinaciones de factores | Emparejamiento algebraico: transformar d/dt ln(u/v) a forma expandida | Exponentes de productividad, tasas exógenas |
| **Hab-05** | Igualación de vectores en coeficientes indeterminados | Resolución algebraica guiada: igualar coeficientes de grado 1 y grado 0 | Parámetros escalares y elementos de matriz invertible |

# 5. Puentes de Transferencia hacia Problemas Complejos
- Descompresión en Estática Comparativa Dinámica: Al automatizar la inversión matricial 2x2 y el cálculo espectral con matrices paramétricas densas (como en el IS-LM dinámico o el modelo macro de previsión perfecta), el estudiante libera memoria de trabajo para concentrarse en la interpretación de los multiplicadores dinámicos y el impacto de políticas de estabilización.
- Construcción Fluida del Diagrama de Fases Global: El dominio previo de la linealización jacobiana local permite al alumno trazar rápidamente las rectas tangentes de las variedades en torno a cada punto crítico, facilitando el empalme topológico de trayectorias no lineales en modelos ecológicos o distributivos complejos (Goodwin y Lotka-Volterra).
- Manejo Riguroso de la Condición de Punto Silla en Macroeconomía Moderna: La fluidez en identificar el caso det(A) < 0 resulta indispensable para abordar sistemas con variables de salto versus variables de estado predeterminadas; esto permite aislar de manera sistemática la variedad estable unidimensional descartando trayectorias divergentes.