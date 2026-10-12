# 1. Macro-Competencia Terminal Inferida
Formular, clasificar analíticamente, reducir operacionalmente y resolver con precisión cuantitativa ecuaciones en derivadas parciales de primer y segundo orden (lineales y cuasilineales) aplicadas a modelos económicos y dinámicos, aplicando el Teorema de Euler a funciones homogéneas de producción, ejecutando la separación de variables, resolviendo sistemas característicos de Charpit-Lagrange con multiplicadores algebraicos, deduciendo superficies integrales explícitas ante condiciones iniciales de Cauchy mediante inversión paramétrica, y descomponiendo operadores diferenciales de segundo orden en cascada para aislar componentes homogéneos y particulares.

# 2. Desglose Cognitivo Exhaustivo (CTA)

## A. Hechos Requeridos [H] (Facts)
- **[H-01]** `Definición de Homogeneidad e Identidad de Euler`: Una función es homogénea de grado $n$ si $f(t\mathbf{x}) = t^n f(\mathbf{x})$; la identidad de Euler establece $\sum_{i=1}^k x_i \frac{\partial f}{\partial x_i} = n f(\mathbf{x})$.
- **[H-02]** `Taxonomía de Orden, Grado y Cuasilinealidad`: El orden de una EDP es la derivada parcial de mayor orden presente; el grado es el exponente algebraico de dicha derivada una vez eliminados radicales; una EDP es cuasilineal si es lineal en las derivadas de mayor orden con coeficientes que dependen de $(x,y,u)$.
- **[H-03]** `Identidad de Verificación de Solución`: Una función $U = f(x,y)$ es solución si y solo si al sustituir formalmente sus derivadas parciales en la EDP se reduce a una identidad algebraica idénticamente nula en todo su dominio.
- **[H-04]** `Sistema Simétrico Auxiliar de Lagrange`: Para la EDP $a(x,y,u)u_x + b(x,y,u)u_y = c(x,y,u)$, el sistema característico asociado es $\frac{dx}{a} = \frac{dy}{b} = \frac{du}{c}$.
- **[H-05]** `Polinomio Característico y Discriminante de 2do Orden`: Para $a U_{xx} + b U_{xy} + c U_{yy} = d(x,y)$, la ecuación característica es $a n^2 + b n + c = 0$, con discriminante $\Delta = b^2 - 4ac$.
- **[H-06]** `Formas Canónicas Homogéneas según el Signo de Discriminante`: Clasificación canónica de la solución homogénea $U_h$ en regímenes hiperbólico (\Delta > 0), parabólico (\Delta = 0) y elíptico (\Delta < 0).
  - Si $\Delta > 0$ (Hiperbólica): $U_h = f_1(y + n_1 x) + f_2(y + n_2 x).
  - Si $\Delta = 0$ (Parabólica): $U_h = f_1(y + n x) + x f_2(y + n x).
  - Si $\Delta < 0$ (Elíptica): $U_h = \phi_1(y + (w+vi)x) + \phi_2(y + (w-vi)x)$.
- **[H-07]** `Representación por Operadores Diferenciales`: Notación $D_x \equiv \frac{\partial}{\partial x}$, $D_y \equiv \frac{\partial}{\partial y}$; el operador cuadrático $a D_x^2 + b D_x D_y + c D_y^2$ se factoriza como $(D_x - m_1 D_y)(D_x - m_2 D_y)$.

## B. Conceptos Estructurales [C] (Concepts)
- **[C-01]** `Interpretación Económica del Teorema de Euler y Agotamiento del Producto`: En mercados competitivos donde los factores reciben su producto marginal ($P_K = F_K, P_L = F_L$), el grado de homogeneidad determina si el pago total agota el producto (rendimientos constantes, $n=1$), genera déficit ($n>1$) o deja excedente ($n<1$).
  - *Distinción fina / Trampa común:* Confundir rendimientos a escala ($n = \alpha+\beta$) con rendimientos marginales decrecientes (exponente individual $\alpha < 1$).
- **[C-02]** `Geometría de Curvas Características y Superficies Integrales`: La solución de una EDP cuasilineal es una superficie $U=U(x,y)$ en $\mathbb{R}^3$ formada por una foliación de curvas características tangentes al campo vectorial $(a, b, c)$.
  - *Distinción fina / Trampa común:* Creer que las características se cruzan arbitrariamente; en puntos de regularidad forman curvas disjuntas sin autointersección.
- **[C-03]** `Principio de Separabilidad y el Rol de la Constante de Separación`: El ansatz $U(x,y)=f(x)g(y)$ solo es válido si la EDP permite aislar términos de variables independientes a cada lado de la igualdad, forzando a que ambos lados igualen una constante fija $\lambda$.
  - *Distinción fina / Trampa común:* Asumir que toda EDP es separable; coeficientes cruzados o acoplamientos impiden la separación.
- **[C-04]** `Independencia Funcional de Integrales Primeras`: Para que $\phi(m, n) = 0$ constituya la solución general de Lagrange, los gradientes $\nabla m$ y $\nabla n$ deben ser linealmente independientes (rango jacobiano 2).
  - *Distinción fina / Trampa común:* Seleccionar dos integrales primeras donde una es función trivial de la otra (ej. $n = m^2$).
- **[C-05]** `Condición de No Tangencia en el Problema de Cauchy`: El problema con condición inicial $u(x_0(s), y_0(s)) = u_0(s)$ posee solución única si y solo si la curva inicial no es tangente a las curvas características.
  - *Distinción fina / Trampa común:* Intentar imponer condiciones iniciales a lo largo de una característica, lo que provoca que no haya solución o existan infinitas.
- **[C-06]** `Partición Superposicional y Reducción en Cascada`: La solución completa de una EDP de 2do orden se descompone aditivamente en $U = U_h + U_p$; la solución particular $U_p$ puede obtenerse resolviendo dos EDPs de 1er orden consecutivas mediante el operador intermedio $V(x,y)$.
  - *Distinción fina / Trampa común:* Confundir la solución particular obtenida por operadores con la solución general, omitiendo la parte complementaria $U_h$.

## C. Habilidades Procedimentales y de Decisión [Hab] (Skills)
- **[Hab-01]** `Cálculo de Grados de Homogeneidad y Aplicación de Euler`: Evaluar formalmente $f(t\mathbf{x})$, simplificar potencias para deducir el grado $n$, y computar la suma ponderada de derivadas parciales multiplicadas por sus coordenadas.
  - *Entrada necesaria:* Función matemática $f(x,y)$ o de producción $F(K,L).
  - *Salida esperada:* Grado escalar $n$ y valor de $\sum x_i \frac{\partial f}{\partial x_i}$.
- **[Hab-02]** `Verificación Operativa de Soluciones Candidatas`: Calcular derivadas parciales sucesivas mediante regla de la cadena y producto, sustituir en el operador diferencial de la EDP y simplificar algebraicamente hasta demostrar la anulación exacta.
  - *Entrada necesaria:* EDP formal y función candidata $U(x,y).
  - *Salida esperada:* Diagnóstico riguroso de validez como solución.
- **[Hab-03]** `Desacoplamiento por Separación de Variables en EDPs Físico-Económicas`: Proponer $U=fg$, calcular derivadas, agrupar cocientes $\frac{f''}{f}$ y $\frac{g'}{g}$, igualar a la constante $\lambda$ y resolver los regímenes ordinarios resultantes según el signo de $\lambda$.
  - *Entrada necesaria:* EDP lineal homogénea separable (ej. calor o difusión).
  - *Salida esperada:* Par de EDOs desacopladas dependientes de $\lambda$.
- **[Hab-04]** `Integración Directa del Sistema Auxiliar de Lagrange`: Formular el sistema simétrico $\frac{dx}{a}=\frac{dy}{b}=\frac{du}{c}$, seleccionar pares de fracciones con variables separables, e integrar analíticamente para obtener integrales primeras $m(x,y,u)=c_1$ y $n(x,y,u)=c_2$.
  - *Entrada necesaria:* EDP cuasilineal $a u_x + b u_y = c$.
  - *Salida esperada:* Dos integrales primeras independientes $m=c_1, n=c_2$.
- **[Hab-05]** `Construcción de Integrales Primeras mediante Multiplicadores de Lagrange`: Determinar multiplicadores algebraicos $(\alpha_1, \alpha_2, \alpha_3)$ tales que $\alpha_1 a + \alpha_2 b + \alpha_3 c = 0$, integrando la forma diferencial exacta resultante $\alpha_1 dx + \alpha_2 dy + \alpha_3 du = 0$.
  - *Entrada necesaria:* Sistema auxiliar de Lagrange no separable directamente.
  - *Salida esperada:* Integral primera exacta $m(x,y,u) = c_1$.
- **[Hab-06]** `Resolución del Problema de Cauchy e Inversión Paramétrica`: Parametrizar la curva inicial en función de un parámetro $m$ en $t=0$, resolver las EDOs para $x(t), y(t), u(t)$, despejar analíticamente los parámetros libres $t$ y $m$ en términos de $(x,y)$, y sustituirlos en $u$ para aislar la solución explícita $u(x,y)$.
  - *Entrada necesaria:* EDP cuasilineal y curva inicial $u(x(s), y(s)) = u_0(s).
  - *Salida esperada:* Solución explícita unívoca $u(x,y)$.
- **[Hab-07]** `Cálculo Espectral y Ensamblado de la Solución Homogénea de 2do Orden`: Sustituir el ansatz $U=\phi(y+nx)$, resolver la ecuación cuadrática característica $an^2+bn+c=0$, evaluar el discriminante $\Delta$ y escribir la combinación lineal canónica correspondiente.
  - *Entrada necesaria:* EDP de 2do orden homogénea con coeficientes constantes.
  - *Salida esperada:* Clasificación (Hiperbólica/Parabólica/Elíptica) y solución general $U_h$.
- **[Hab-08]** `Determinación de la Solución Particular vía Factorización de Operadores`: Factorizar el polinomio en operadores diferenciales $(D_x - r_1 D_y)(D_x - r_2 D_y)U = d(x,y)$, definir la variable intermedia $V(x,y)$, resolver la primera EDP de 1er orden para $V$ por Lagrange, y luego resolver la segunda EDP para $U$.
  - *Entrada necesaria:* EDP no homogénea $a U_{xx} + b U_{xy} + c U_{yy} = d(x,y).
  - *Salida esperada:* Solución particular $U_p(x,y)$.

# 3. Puntos Ciegos del Experto y Pasos Implícitos (Expert Blindness)
| Paso Implícito / Trampa | Por qué el texto teórico lo omite | Impacto si el alumno no lo domina |
|---|---|---|
| Pérdida de la constante de integración como función arbitraria | En cálculo ordinario las constantes son escalares c | El alumno confunde la solución con una curva en vez de una superficie integral |
| Elección incorrecta de multiplicadores en Lagrange | Se exhiben los multiplicadores ya encontrados como truco | El alumno intenta integrar expresiones diferenciales que no son exactas |
| Olvidar sustituir la primera integral en la segunda ecuación de Lagrange | Se considera un paso obvio de sustitución algebraica elemental | El estudiante declara que la ecuación no tiene solución separable |
| Singularidades al despejar parámetros en el problema de Cauchy | Se prioriza la fórmula cerrada sin discutir ramas | Respuestas discontinuas en exámenes o pérdida de ramas válidas |
| Omisión de división por coeficientes al reordenar la ecuación característica | Se sobreentiende la simetría de la sustitución | El estudiante invierte las raíces y coloca coeficientes erróneos en argumentos |
| Confusión entre la solución particular Up y la general U = Uh + Up | El autor se concentra en el cálculo del operador diferencial | Pérdida de la mitad del puntaje al olvidar sumar las funciones arbitrarias |

# 4. Semillas de Automatización y Fluidez (Top's Academy)
| ID Habilidad | Micro-Competencia a Automatizar | Tipo de Ejercicio Mecánico Sugerido | Parámetros que deben variar aleatoriamente |
|---|---|---|---|
| **Hab-01** | Grado de funciones Cobb-Douglas y derivadas de Euler | Entrada Numérica directa del grado n o valor de agotamiento | Coeficientes alfa, beta en (0, 2), constante A |
| **Hab-02** | Verificación rápida de soluciones en Ux + k Uy = 0 | Opción Múltiple (7 opciones): ¿Cuál de las 7 funciones es solución? | Formas funcionales exp, sin, cos, ln, coeficientes |
| **Hab-03** | Cálculo de la constante de separación lambda en calor | Selección Múltiple de las EDOs desacopladas | Coeficiente de difusión kappa, signo de lambda |
| **Hab-04** | Integración del primer par del sistema de Lagrange dx/a = dy/b | Expresión algebraica en LaTeX de la primera integral m(x,y)=c1 | Coeficientes enteros a, b en [-8, 8], lineales x, y |
| **Hab-05** | Identificación de multiplicadores nulos en Lagrange | Selección Múltiple: Seleccionar la terna alfa que anula suma | EDPs canónicas con variables rotacionales (x-y, y-u, u-x) |
| **Hab-06** | Parametrización en t=0 para condiciones de Cauchy | Entrada directa de las condiciones x(0), y(0), u(0) en función de m | Curvas iniciales y=0, parábolas, constantes |
| **Hab-07** | Raíces características y clasificación de EDPs de 2do orden | Clasificación rápida: ¿Hiperbólica, Parabólica o Elíptica? | Coeficientes a, b, c con discriminante positivo, cero o negativo |
| **Hab-08** | Factorización de operadores diferenciales cuadráticos | Entrada algebraica de las raíces en (Dx - r1 Dy)(Dx - r2 Dy) | Coeficientes enteros factorizables |

# 5. Puentes de Transferencia hacia Problemas Complejos
- Combinación de Euler y Lagrange: permite modelar el crecimiento dinámico de firmas con múltiples factores productivos sujetos a restricciones tecnológicas continuas.
- Acoplamiento de Cauchy y Operadores de 2do Orden: conecta la teoría pura de superficies de onda con problemas de propagación económica y difusión de choques exógenos.
- Transición de Variables Separables a Series de Fourier: cimiento para resolver condiciones de frontera mixtas en dominios acotados sin sobrecarga cognitiva.