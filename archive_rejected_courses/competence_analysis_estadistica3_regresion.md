# Cognitive Task Analysis (CTA) - Estadística III: Econometría y Modelo de Regresión Lineal
**Course ID:** `estadistica3_regresion`  
**Macro-competency:** Dominar la especificación matemática, estimación MCO en notación matricial, propiedades estadísticas y asintóticas de Gauss-Markov, álgebra geométrica de proyecciones, descomposición ANOVA de sumas de cuadrados, inferencia de hipótesis lineales y diagnóstico econométrico integral.

---

# Sesión 1: Especificación del Modelo Lineal General, Notación Matricial y Estimación MCO

## [H-01] Especificación Matricial y Dimensionalidad del Modelo Lineal General (Hecho [H])
- **Unit Index:** 0
- **Bloom Taxonomy:** Remember
- **Prerequisites:** Ninguno (Fundacional)
- **Evidence:** `EST3_LEC01_26_2.pdf` (pág. 5)

### Descripción Matemática
Formulación canónica del Modelo Lineal General en forma matricial $\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$, donde $\mathbf{y} \in \mathbb{R}^{n \times 1}$ es el vector de observaciones de la variable dependiente, $\mathbf{X} \in \mathbb{R}^{n \times K}$ es la matriz de diseño cuyos regresores incluyen el vector unitario $\boldsymbol{\iota}_n$ en la primera columna si hay constante, $\boldsymbol{\beta} \in \mathbb{R}^{K \times 1}$ es el vector de parámetros desconocidos, y $\boldsymbol{\varepsilon} \in \mathbb{R}^{n \times 1}$ es el vector de perturbaciones estocásticas.

### Ejemplos en Corpus
- Extrapolando a n observaciones y K parámetros: y = X*beta + epsilon con y (n x 1), X (n x K), beta (K x 1), epsilon (n x 1).

### Distractores Fusionados (3)
#### `D-H-01-01` - Inconformabilidad dimensional entre matriz de diseño y vector de coeficientes
- **Tipo de Error:** `notation` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `EST3_LEC01_26_2.pdf` (pág. 5)
- **Creencia Errónea:** Creer que el vector de parámetros beta es un vector fila (1 x K) en lugar de un vector columna (K x 1), intentando multiplicar X (n x K) por beta (1 x K).
- **Creencia Correcta:** En la especificación matricial estándar, beta es estrictamente un vector columna de orden (K x 1), permitiendo la conformabilidad del producto matricial X*beta de orden (n x 1).
- **Detonante (Trigger):** Escribir la multiplicación de regresores y coeficientes en forma matricial compacta.
- **Manifestación:** Dimensiones no conformables en X*beta que impiden la suma vectorial con epsilon.
- **Pauta de Remediación:** *Recuerda que para multiplicar matrices A (n x p) y B (q x m) se requiere p = q. Dado que X es (n x K), beta debe ser columna (K x 1).*

#### `D-H-01-02` - Omisión del vector unitario en la matriz de diseño para modelos con intercepto
- **Tipo de Error:** `conceptual_swap` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `EST3_LEC01_26_2.pdf` (pág. 5)
- **Creencia Errónea:** Omitir la primera columna de unos (vector unitario iota) en X cuando el modelo teórico contiene intercepto beta_0.
- **Creencia Correcta:** Para modelar un intercepto constante beta_0, la primera columna de la matriz X debe ser un vector columna de unos de dimensión n x 1.
- **Detonante (Trigger):** Construir la matriz de diseño X a partir de un conjunto de datos brutos con constante.
- **Manifestación:** Matriz X de orden n x (K-1) que fuerza una regresión que pasa por el origen y produce estimadores sesgados.
- **Pauta de Remediación:** *Verifica siempre que la columna 1 de la matriz de diseño X contenga exclusivamente unos para capturar la constante beta_0.*

#### `D-H-01-03` - Tratamiento escalar del término de perturbación en el sistema matricial
- **Tipo de Error:** `unit_or_scale` | **Severidad:** `medium` | **Origen:** `inferred`
- **Evidencia:** `EST3_LEC01_26_2.pdf` (pág. 5)
- **Creencia Errónea:** Tratar la perturbación epsilon como un escalar invariable epsilon en lugar de un vector estocástico n x 1.
- **Creencia Correcta:** Cada una de las n observaciones posee su propia perturbación individual epsilon_i, por lo que epsilon es un vector n x 1 en el espacio muestral.
- **Detonante (Trigger):** Sumar el error a la parte determinística X*beta en notación matricial.
- **Manifestación:** Suma inválida de una matriz o vector (n x 1) con un escalar epsilon.
- **Pauta de Remediación:** *Recuerda que la perturbación poblacional es un vector columna epsilon = [epsilon_1, ..., epsilon_n]' con una dimensión por observación.*

---

## [C-01] Supuestos Clásicos de Gauss-Markov y Ortogonalidad Regresor-Error (Concepto [C])
- **Unit Index:** 1
- **Bloom Taxonomy:** Understand
- **Prerequisites:** `H-01`
- **Evidence:** `EST3_LEC01_26_2.pdf` (pág. 9)

### Descripción Matemática
Conjunto de supuestos fundamentales del Modelo de Regresión Lineal Clásico (MRLC): 1) Linealidad en parámetros; 2) Rango columna completo $\text{rango}(\mathbf{X}) = K < n$ (ausencia de multicolinealidad perfecta); 3) Muestreo aleatorio; 4) Exogeneidad estricta $E[\boldsymbol{\varepsilon}|\mathbf{X}] = \mathbf{0}_{n \times 1}$ que garantiza $E[\mathbf{X}'\boldsymbol{\varepsilon}] = \mathbf{0}$; 5) Homocedasticidad y no autocorrelación $\text{Var}(\boldsymbol{\varepsilon}|\mathbf{X}) = \sigma^2 \mathbf{I}_n$.

### Ejemplos en Corpus
- Supuestos clásicos: Linealidad, rango completo rango(X)=K, esperanza condicional nula E(epsilon|X)=0, y Var(epsilon|X)=sigma^2*I_n.

### Distractores Fusionados (3)
#### `D-C-01-01` - Confusión entre media incondicional nula y exogeneidad estricta condicional
- **Tipo de Error:** `conceptual_swap` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `EST3_LEC01_26_2.pdf` (pág. 9)
- **Creencia Errónea:** Creer que la condición E[epsilon] = 0 es suficiente para garantizar la insesgadez del estimador MCO sin requerir E[epsilon|X] = 0.
- **Creencia Correcta:** La media incondicional nula E[epsilon] = 0 solo indica ausencia de sesgo sistemático global, pero la exogeneidad estricta E[epsilon|X] = 0 es indispensable para que los regresores no transmitan información sobre el error.
- **Detonante (Trigger):** Evaluar las condiciones requeridas para demostrar el valor esperado del estimador MCO.
- **Manifestación:** Asumir falsamente que MCO es insesgado ante regresores endógenos correlacionados con epsilon.
- **Pauta de Remediación:** *Exige siempre exogeneidad condicional E[epsilon|X] = 0; la media incondicional nula no previene la endogeneidad Cov(X, epsilon) != 0.*

#### `D-C-01-02` - Atribución errónea de normalidad a los supuestos de Gauss-Markov
- **Tipo de Error:** `overgeneralization` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `EST3_LEC01_26_2.pdf` (pág. 9)
- **Creencia Errónea:** Creer que el Teorema de Gauss-Markov requiere que los errores epsilon sigan una distribución normal condicional N(0, sigma^2*I_n).
- **Creencia Correcta:** El Teorema de Gauss-Markov solo requiere los momentos de primer y segundo orden (media cero, varianza constante y no autocorrelación); la normalidad solo se precisa para inferencia en muestras pequeñas (tests t y F).
- **Detonante (Trigger):** Enumerar los supuestos estrictamente necesarios para que MCO sea el estimador MELI (BLUE).
- **Manifestación:** Descalificar la eficiencia MELI de MCO cuando los residuos presentan asimetría o curtosis no normal.
- **Pauta de Remediación:** *Distingue entre propiedades de Gauss-Markov (MELI/BLUE), que no exigen normalidad, e inferencia exacta pivotal (t y F), que sí la exige.*

#### `D-C-01-03` - Equiparación de la ortogonalidad muestral con la exogeneidad poblacional
- **Tipo de Error:** `boundary_case` | **Severidad:** `high` | **Origen:** `inferred`
- **Evidencia:** `EST3_LEC01_26_2.pdf` (pág. 9)
- **Creencia Errónea:** Creer que la propiedad matemática X'e = 0 demuestra empíricamente que se cumple el supuesto teórico E[X'epsilon] = 0.
- **Creencia Correcta:** X'e = 0 es una consecuencia algebraica puramente mecánica de las condiciones de primer orden de MCO, independientemente de si X y epsilon están correlacionados en la población.
- **Detonante (Trigger):** Interpretar la relación entre los residuos calculados e y los regresores X.
- **Manifestación:** Afirmar que un modelo no sufre de endogeneidad porque la correlación entre X y los residuos e es exactamente cero.
- **Pauta de Remediación:** *Recuerda que X'e = 0 es una identidad algebraica forzada por MCO; no es un contraste del supuesto poblacional E[epsilon|X] = 0.*

---

## [Hab-01] Derivación Matricial del Estimador MCO y Ecuaciones Normales (Habilidad [Hab])
- **Unit Index:** 2
- **Bloom Taxonomy:** Apply
- **Prerequisites:** `H-01`, `C-01`
- **Evidence:** `EST3_LEC01_26_2.pdf` (pág. 7)

### Descripción Matemática
Procedimiento algebraico para derivar el estimador MCO: 1) Formulación de la función objetivo escalar $S(\hat{\boldsymbol{\beta}}) = \mathbf{e}'\mathbf{e} = (\mathbf{y} - \mathbf{X}\hat{\boldsymbol{\beta}})'(\mathbf{y} - \mathbf{X}\hat{\boldsymbol{\beta}}) = \mathbf{y}'\mathbf{y} - 2\hat{\boldsymbol{\beta}}'\mathbf{X}'\mathbf{y} + \hat{\boldsymbol{\beta}}'\mathbf{X}'\mathbf{X}\hat{\boldsymbol{\beta}}$; 2) Cálculo del vector gradiente $\frac{\partial S}{\partial \hat{\boldsymbol{\beta}}} = -2\mathbf{X}'\mathbf{y} + 2\mathbf{X}'\mathbf{X}\hat{\boldsymbol{\beta}}$; 3) Igualación a cero para obtener el sistema de ecuaciones normales $\mathbf{X}'\mathbf{X}\hat{\boldsymbol{\beta}} = \mathbf{X}'\mathbf{y}$; 4) Verificación de la condición de segundo orden (Hessiana definida positiva $2\mathbf{X}'\mathbf{X} > 0$); 5) Despeje unívoco $\hat{\boldsymbol{\beta}} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$.

### Ejemplos en Corpus
- Minimizamos S(beta_hat) = e'e = (y - X*beta_hat)'(y - X*beta_hat), expandiendo dS/dbeta_hat = -2X'y + 2X'X*beta_hat = 0, beta_hat = (X'X)^(-1)X'y.

### Distractores Fusionados (6)
#### `D-Hab-01-01` - Error de transposición o regla de la cadena en el gradiente matricial
- **Tipo de Error:** `sign_error` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `EST3_LEC01_26_2.pdf` (pág. 7)
- **Creencia Errónea:** Creer que la derivada de beta'*X'*y respecto a beta es beta'*X' o y'*X en lugar de X'*y.
- **Creencia Correcta:** Por cálculo vectorial, la derivada del escalar a'*beta respecto al vector columna beta es el vector columna a; por tanto, para a = X'*y, la derivada es X'*y.
- **Detonante (Trigger):** Calcular la derivada parcial de la forma bilineal transpuesta en la expansión cuadrática de los residuos.
- **Manifestación:** Gradiente no conformable con dimensiones transpuestas que impide despejar beta_hat.
- **Pauta de Remediación:** *Aplica la regla de derivación vectorial: d(a'x)/dx = a y d(x'Ax)/dx = 2Ax cuando A es simétrica.*

#### `D-Hab-01-02` - Inversión sin validación de rango columna completo de X
- **Tipo de Error:** `skipped_step` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `EST3_LEC01_26_2.pdf` (pág. 7)
- **Creencia Correcta:** La matriz X'X de orden K x K es invertible si y solo si X tiene rango columna completo (rango(X) = K).
- **Paso Omitido (Expert Blindness):** Verificar explícitamente que rango(X) = K antes de multiplicar por la inversa (X'X)^(-1).
- **Detonante (Trigger):** Despejar beta_hat premultiplicando las ecuaciones normales X'X*beta_hat = X'y.
- **Manifestación:** Intentar invertir una matriz singular cuando existe multicolinealidad perfecta o cuando n < K.
- **Pauta de Remediación:** *Antes de premultiplicar por (X'X)^(-1), verifica que las columnas de X sean linealmente independientes (rango columna pleno).*

#### `D-Hab-01-03` - Omisión de la comprobación de la condición de segundo orden (Hessiana)
- **Tipo de Error:** `skipped_step` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `EST3_LEC01_26_2.pdf` (pág. 7)
- **Creencia Correcta:** Para garantizar un mínimo global estricto, la matriz Hessiana d^2S / dbeta dbeta' = 2X'X debe ser estrictamente definida positiva.
- **Paso Omitido (Expert Blindness):** Comprobar que la segunda derivada matricial 2X'X es definida positiva para descartar puntos de ensilladura o máximos.
- **Detonante (Trigger):** Finalizar la derivación MCO al igualar el gradiente a cero.
- **Manifestación:** Aceptar soluciones de primer orden sin certificar que la curvatura de la función residual corresponde a un mínimo global.
- **Pauta de Remediación:** *Calcula la Hessiana 2X'X y justifica que z'(2X'X)z = 2||Xz||^2 > 0 para todo z != 0 si rango(X) = K.*

#### `D-Hab-01-04` - Distribución indebida de la inversa en matrices no cuadradas
- **Tipo de Error:** `procedural_slip` | **Severidad:** `high` | **Origen:** `inferred`
- **Evidencia:** `EST3_LEC01_26_2.pdf` (pág. 7)
- **Creencia Errónea:** Intentar distribuir la inversa de un producto escribiendo (X'X)^(-1) = X^(-1)*(X')^(-1) cuando X es rectangular (n x K con n > K).
- **Creencia Correcta:** X es una matriz rectangular de orden n x K; la inversa ordinaria solo existe para matrices cuadradas. Por tanto, X'X (K x K) no puede descomponerse en inversas individuales de X.
- **Detonante (Trigger):** Simplificar algebraicamente la expresión del estimador (X'X)^(-1)*X'*y.
- **Manifestación:** Expresión inválida X^(-1)*(X')^(-1)*X'*y = X^(-1)*y que genera un colapso algebraico.
- **Pauta de Remediación:** *Recuerda que una matriz rectangular no tiene inversa tradicional; la matriz invertible es el producto simétrico X'X de K x K.*

#### `D-Hab-01-05` - Conmutación inválida en el producto matricial de MCO
- **Tipo de Error:** `procedural_slip` | **Severidad:** `high` | **Origen:** `inferred`
- **Evidencia:** `EST3_LEC01_26_2.pdf` (pág. 7)
- **Creencia Errónea:** Escribir beta_hat = X'y*(X'X)^(-1) asumiendo conmutatividad en el álgebra matricial.
- **Creencia Correcta:** La multiplicación matricial no es conmutativa. Para despejar beta_hat de X'X*beta_hat = X'y, debe premultiplicarse por izquierda por (X'X)^(-1).
- **Detonante (Trigger):** Despejar algebraicamente el vector beta_hat del sistema de ecuaciones normales.
- **Manifestación:** Producto matricial X'y*(X'X)^(-1) con dimensiones no conformables (K x 1) por (K x K).
- **Pauta de Remediación:** *En álgebra matricial AB != BA. Multiplica siempre por la izquierda en ambos miembros para despejar la incógnita.*

#### `D-Hab-01-06` - Omisión de la transposición al formular la suma de residuos al cuadrado
- **Tipo de Error:** `notation` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `EST3_LEC01_26_2.pdf` (pág. 7)
- **Creencia Errónea:** Formular la suma de residuos al cuadrado en notación vectorial como e*e o e*e' en lugar de e'*e.
- **Creencia Correcta:** La suma escalar de cuadrados de un vector columna e (n x 1) es el producto interno e'*e = sum(e_i^2). El producto e*e' genera una matriz de orden n x n.
- **Detonante (Trigger):** Escribir la función objetivo cuadrática S(beta) en notación matricial.
- **Manifestación:** Obtención de una matriz n x n en lugar de un escalar a minimizar, o error de dimensiones no conformables e*e.
- **Pauta de Remediación:** *Verifica que el producto interno de dos vectores columna u y v sea u'*v (escalar 1 x 1); v*u' es un producto exterior (matriz n x n).*

---


# Sesión 2: Estimación MCO en Forma Matricial, Teorema de Gauss-Markov y Formas Funcionales

## [H-02] Álgebra de Ponderadores k_i y Representación Lineal del Estimador (Hecho [H])
- **Unit Index:** 3
- **Bloom Taxonomy:** Remember
- **Prerequisites:** `Hab-01`
- **Evidence:** `EST3_LEC02_26_2.pdf` (pág. 13)

### Descripción Matemática
Definición del ponderador determinístico $k_i \equiv \frac{x_i}{\sum_{j=1}^n x_j^2} = \frac{X_i - \bar{X}}{\sum_{j=1}^n (X_j - \bar{X})^2}$, el cual satisface las identidades algebraicas exactas: $\sum_{i=1}^n k_i = 0$, $\sum_{i=1}^n k_i X_i = 1$, y $\sum_{i=1}^n k_i^2 = \frac{1}{\sum x_i^2}$, permitiendo expresar el estimador de la pendiente como combinación lineal de las observaciones dependientes: $\hat{\beta}_2 = \sum_{i=1}^n k_i Y_i$.

### Ejemplos en Corpus
- Definimos k_i = x_i / sum(x_j^2), sum(k_i)=0, sum(k_i*X_i)=1, sum(k_i^2) = 1/sum(x_i^2), por tanto beta_hat_2 = sum(k_i*Y_i).

### Distractores Fusionados (3)
#### `D-H-02-01` - Creencia errónea de que la suma de ponderadores k_i es unitaria
- **Tipo de Error:** `conceptual_swap` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `EST3_LEC02_26_2.pdf` (pág. 13)
- **Creencia Errónea:** Creer que sum(k_i) = 1 por analogía superficial con ponderaciones de promedios ponderados tradicionales.
- **Creencia Correcta:** Dado que el numerador de k_i son los desvíos respecto a la media (x_i = X_i - bar(X)), la suma de los desvíos es idénticamente nula: sum(k_i) = sum(x_i)/sum(x_i^2) = 0.
- **Detonante (Trigger):** Simplificar sumatorias que involucran k_i multiplicando por constantes como beta_1.
- **Manifestación:** Término espurio beta_1 sum(k_i) = beta_1 en la deducción de la insesgadez, sugiriendo sesgo en beta_hat_2.
- **Pauta de Remediación:** *Recuerda siempre la propiedad fundamental de los desvíos respecto a la media: sum(X_i - bar(X)) = 0, por lo que sum(k_i) = 0.*

#### `D-H-02-02` - Tratamiento de los ponderadores k_i como variables aleatorias
- **Tipo de Error:** `overgeneralization` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `EST3_LEC02_26_2.pdf` (pág. 13)
- **Creencia Errónea:** Tratar k_i como variable estocástica dependiente del error aleatorio u_i.
- **Creencia Correcta:** Bajo el supuesto de regresores no estocásticos (o condicionando respecto a X), k_i es una función determinística fija dependiente únicamente de los valores muestrales de X.
- **Detonante (Trigger):** Calcular la esperanza matemática condicional E[sum(k_i*u_i)|X].
- **Manifestación:** Intentar calcular covarianzas complejas Cov(k_i, u_i) en lugar de extraer k_i fuera del operador de esperanza.
- **Pauta de Remediación:** *Al condicionar por X, las cantidades que dependen únicamente de X (como k_i y bar(X)) se comportan algebraicamente como constantes.*

#### `D-H-02-03` - Cálculo erróneo de la suma cuadrática sum(k_i^2)
- **Tipo de Error:** `procedural_slip` | **Severidad:** `high` | **Origen:** `inferred`
- **Evidencia:** `EST3_LEC02_26_2.pdf` (pág. 13)
- **Creencia Errónea:** Creer que sum(k_i^2) = (sum(k_i))^2 = 0^2 = 0.
- **Creencia Correcta:** La suma de los cuadrados sum(k_i^2) es estrictamente positiva: sum((x_i/sum(x_j^2))^2) = sum(x_i^2)/(sum(x_i^2))^2 = 1/sum(x_i^2) > 0.
- **Detonante (Trigger):** Calcular la varianza de beta_hat_2 aplicando el operador de varianza a la suma lineal sum(k_i*Y_i).
- **Manifestación:** Varianza nula Var(beta_hat_2) = 0 o división por cero en la deducción de la precisión muestral.
- **Pauta de Remediación:** *Distingue siempre entre el cuadrado de una suma (sum(a_i))^2 y la suma de cuadrados sum(a_i^2); sum(k_i^2) = 1/sum(x_i^2).*

---

## [C-02] Propiedades de MCO: Insesgadez, Teorema de Gauss-Markov (BLUE) y Consistencia (Concepto [C])
- **Unit Index:** 4
- **Bloom Taxonomy:** Understand
- **Prerequisites:** `H-02`, `C-01`
- **Evidence:** `EST3_LEC02_26_2.pdf` (pág. 16)

### Descripción Matemática
Demostración y consecuencias de las propiedades estadísticas clave de $\hat{\beta}_2$: 1) Insesgadez $E[\hat{\beta}_2|X] = \beta_2 \implies \text{Sesgo}(\hat{\beta}_2) = 0$ sustentada en $E[u_i|X] = 0$; 2) Eficiencia (Teorema de Gauss-Markov), que establece que para cualquier estimador lineal insesgado alternativo $\tilde{\beta}_2 = \sum c_i Y_i$, $\text{Var}(\tilde{\beta}_2|X) = \text{Var}(\hat{\beta}_2|X) + \sigma^2 \sum d_i^2 \ge \text{Var}(\hat{\beta}_2|X)$; 3) Consistencia asintótica $\text{plim}_{n \to \infty} \hat{\beta}_2 = \beta_2$ asegurada por la desigualdad de Chebyshev cuando la varianza de la muestra acota positivamente $S_X^2$.

### Ejemplos en Corpus
- Teorema de Gauss-Markov: Var(beta_tilde) = Var(beta_hat) + sigma^2*sum(d_i^2) >= Var(beta_hat), minima varianza si d_i=0. Consistencia: plim beta_hat = beta.

### Distractores Fusionados (3)
#### `D-C-02-01` - Confusión entre insesgadez en muestra finita y consistencia asintótica
- **Tipo de Error:** `conceptual_swap` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `EST3_LEC02_26_2.pdf` (pág. 18)
- **Creencia Errónea:** Creer que un estimador insesgado es automáticamente consistente independientemente del comportamiento de la muestra de X.
- **Creencia Correcta:** La insesgadez no garantiza consistencia; se requiere además que la varianza tienda a cero (o que la variabilidad de X no colapse), es decir, lim sum(x_i^2) = infinito a medida que n -> infinito.
- **Detonante (Trigger):** Analizar la convergencia en probabilidad de un estimador econométrico cuando n tiende a infinito.
- **Manifestación:** Afirmar consistencia sin verificar la condición lim Var(beta_hat) = 0 o la cota inferior de la varianza muestral S_X^2.
- **Pauta de Remediación:** *La insesgadez es una propiedad de la media para cualquier tamaño de muestra fijo; la consistencia exige convergencia de la distribución al valor puntual cuando n -> inf.*

#### `D-C-02-02` - Generalización indebida de la eficiencia MELI hacia estimadores no lineales
- **Tipo de Error:** `overgeneralization` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `EST3_LEC02_26_2.pdf` (pág. 16)
- **Creencia Errónea:** Creer que el estimador MCO posee la menor varianza posible entre absolutamente todos los estimadores insesgados, incluso los no lineales.
- **Creencia Correcta:** Gauss-Markov demuestra la optimalidad de varianza mínima estrictamente dentro de la subclase de estimadores lineales en Y (MELI / BLUE). Estimadores no lineales insesgados pueden superar su precisión si se conocen distribuciones específicas.
- **Detonante (Trigger):** Definir el alcance de la palabra 'Mejor' en la sigla MELI / BLUE.
- **Manifestación:** Negar la posibilidad de que estimadores no lineales superen a MCO en eficiencia sin asumir normalidad.
- **Pauta de Remediación:** *MELI significa Mejor Estimador Lineal Insesgado; su cota mínima de varianza está restringida a combinaciones lineales de Y.*

#### `D-C-02-03` - Olvido de la condición de insesgadez para el estimador alternativo en Gauss-Markov
- **Tipo de Error:** `boundary_case` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `EST3_LEC02_26_2.pdf` (pág. 16)
- **Creencia Errónea:** Creer que la demostración de Gauss-Markov compara MCO contra estimadores con sesgo que pudieran tener menor varianza.
- **Creencia Correcta:** La comparación se realiza estrictamente frente a estimadores insesgados, lo que impone las restricciones sum(d_i) = 0 y sum(d_i*X_i) = 0 sobre la perturbación d_i.
- **Detonante (Trigger):** Plantear la varianza del estimador lineal alternativo beta_tilde = sum(k_i + d_i)Y_i.
- **Manifestación:** Anular incorrectamente los términos cruzados de covarianza sin utilizar las restricciones sum(d_i)=0 y sum(d_i*X_i)=0.
- **Pauta de Remediación:** *Recuerda que los estimadores con sesgo (como Ridge) pueden tener menor varianza que MCO; Gauss-Markov solo aplica a estimadores insesgados.*

---

## [Hab-02] Transformación e Interpretación de Formas Funcionales No Lineales (Habilidad [Hab])
- **Unit Index:** 5
- **Bloom Taxonomy:** Apply
- **Prerequisites:** `C-02`
- **Evidence:** `EST3_LEC02_26_2.pdf` (pág. 25)

### Descripción Matemática
Procedimiento para formular, linealizar e interpretar modelos de regresión no lineales en variables: 1) Modelo Lin-Log ($Y = \beta_1 + \beta_2 \ln X + u$): efecto marginal $\frac{dY}{dX} = \frac{\beta_2}{X}$, variación relativa $\Delta Y \approx \frac{\beta_2}{100} (100 \frac{\Delta X}{X})$; 2) Modelo Log-Lin ($\ln Y = \beta_1 + \beta_2 X + u$): efecto relativo $100 \frac{\Delta Y}{Y} \approx (100 \beta_2) \Delta X$; 3) Modelo Log-Log ($\ln Y = \beta_1 + \beta_2 \ln X + u$): elasticidad constante $\beta_2$; 4) Modelo Cuadrático ($Y = \beta_0 + \beta_1 X + \beta_2 X^2 + u$): efecto marginal variable $\frac{dY}{dX} = \beta_1 + 2\beta_2 X$ y punto de inflexión/vértice $X^* = -\frac{\beta_1}{2\beta_2}$; 5) Modelo Recíproco ($Y = \beta_1 + \beta_2 \frac{1}{X} + u$): efecto marginal $-\frac{\beta_2}{X^2}$ y asíntota $\lim_{X \to \infty} E(Y|X) = \beta_1$.

### Ejemplos en Corpus
- Lin-Log: Un cambio de 1% en X genera cambio de beta_2/100 unidades en Y. Log-Lin: cambio de 1 unidad en X genera (100*beta_2)% en Y. Cuadratico: dY/dX = beta_1 + 2*beta_2*X, vertice X* = -beta_1/(2*beta_2).

### Distractores Fusionados (6)
#### `D-Hab-02-01` - Intercambio conceptual entre efectos absolutos y relativos en modelos semilogarítmicos
- **Tipo de Error:** `conceptual_swap` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `EST3_LEC02_26_2.pdf` (pág. 19)
- **Creencia Errónea:** Interpretar el coeficiente beta_2 en un modelo Lin-Log como un cambio porcentual directo en Y ante una variación unitaria en X.
- **Creencia Correcta:** En el modelo Lin-Log (Y en niveles, X en logaritmo), beta_2 cuantifica que un incremento de 1% en X genera una variación absoluta de beta_2/100 unidades en Y.
- **Detonante (Trigger):** Interpretar verbalmente el resultado de un modelo econométrico con especificación Lin-Log.
- **Manifestación:** Reportar un cambio de beta_2% en Y en vez de beta_2/100 unidades físicas de Y.
- **Pauta de Remediación:** *Recuerda la regla mnemotécnica: la variable que tiene logaritmo se lee en porcentaje (1%), y la que está en niveles se lee en unidades originales.*

#### `D-Hab-02-02` - Omisión del factor de escala 100 en la tasa de crecimiento del modelo Log-Lin
- **Tipo de Error:** `unit_or_scale` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `EST3_LEC02_26_2.pdf` (pág. 20)
- **Creencia Errónea:** Afirmar que un cambio de 1 unidad en X modifica Y en beta_2% en lugar de (100*beta_2)%.
- **Creencia Correcta:** Dado que d(ln Y)/dX = (1/Y)(dY/dX) = beta_2, la variación porcentual 100*(Delta Y/Y) requiere multiplicar beta_2 por 100.
- **Detonante (Trigger):** Convertir el coeficiente de una regresión Log-Lin en una tasa porcentual de crecimiento.
- **Manifestación:** Subestimar el impacto relativo por un factor de 100 (por ejemplo, interpretar 0.05 como 0.05% en vez de 5%).
- **Pauta de Remediación:** *Multiplica siempre por 100 el coeficiente de un regresor en niveles cuando la variable dependiente está expresada en logaritmo natural.*

#### `D-Hab-02-03` - Omisión del cálculo del punto crítico en modelos polinomiales cuadráticos
- **Tipo de Error:** `skipped_step` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `EST3_LEC02_26_2.pdf` (pág. 22)
- **Creencia Correcta:** En un modelo cuadrático Y = beta_0 + beta_1*X + beta_2*X^2, el efecto marginal dY/dX = beta_1 + 2*beta_2*X cambia de signo en el vértice X* = -beta_1 / (2*beta_2).
- **Paso Omitido (Expert Blindness):** Calcular explícitamente el punto de inflexión X* = -beta_1 / (2*beta_2) para delimitar los rangos de efectos marginales positivos y negativos.
- **Detonante (Trigger):** Interpretar el coeficiente lineal beta_1 en un modelo que incluye también el término cuadrático X^2.
- **Manifestación:** Reportar que el efecto marginal de X es constante e igual a beta_1 en todo el dominio.
- **Pauta de Remediación:** *En modelos cuadráticos nunca interpretes beta_1 de forma aislada; calcula la derivada completa dY/dX = beta_1 + 2*beta_2*X y su vértice.*

#### `D-Hab-02-04` - Omisión del signo negativo al derivar el efecto marginal del modelo recíproco
- **Tipo de Error:** `sign_error` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `EST3_LEC02_26_2.pdf` (pág. 23)
- **Creencia Errónea:** Creer que la derivada de 1/X respecto a X es positiva e igual a 1/X^2.
- **Creencia Correcta:** La derivada de X^(-1) es -X^(-2) = -1/X^2; por tanto, el efecto marginal es -beta_2 / X^2.
- **Detonante (Trigger):** Calcular la derivada de la función de regresión recíproca Y = beta_1 + beta_2*(1/X).
- **Manifestación:** Signo invertido en la pendiente marginal, afirmando crecimiento en lugar de rendimientos decrecientes hacia la asíntota.
- **Pauta de Remediación:** *Aplica la regla de potencias: d(X^(-1))/dX = -1 * X^(-2) = -1/X^2. No olvides arrastrar el signo negativo.*

#### `D-Hab-02-05` - Omisión de la comprobación del signo del coeficiente cuadrático para la concavidad
- **Tipo de Error:** `skipped_step` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `EST3_LEC02_26_2.pdf` (pág. 22)
- **Creencia Correcta:** La naturaleza del vértice (máximo o mínimo) depende estrictamente del signo de beta_2: si beta_2 < 0 es un máximo local; si beta_2 > 0 es un mínimo local.
- **Paso Omitido (Expert Blindness):** Evaluar la segunda derivada d^2Y/dX^2 = 2*beta_2 para certificar si el punto crítico corresponde a un máximo o mínimo económico.
- **Detonante (Trigger):** Interpretar el punto de retorno en una curva de salarios por experiencia o producción cuadrática.
- **Manifestación:** Calificar como nivel de saturación máxima un punto que en realidad es un mínimo de costos (o viceversa).
- **Pauta de Remediación:** *Verifica el signo de beta_2: si es negativo, la parábola abre hacia abajo (máximo); si es positivo, abre hacia arriba (mínimo).*

#### `D-Hab-02-06` - Falla en la derivación del límite de Box-Cox cuando lambda tiende a cero
- **Tipo de Error:** `boundary_case` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `EST3_LEC02_26_2.pdf` (pág. 24)
- **Creencia Errónea:** Evaluar la transformación de Box-Cox directamente sustituyendo lambda = 0 en (Y^lambda - 1)/lambda, concluyendo que queda indefinida (0/0).
- **Creencia Correcta:** Cuando lambda -> 0, se aplica la regla de L'Hôpital respecto a lambda para obtener lim_{lambda -> 0} (Y^lambda - 1)/lambda = ln(Y).
- **Detonante (Trigger):** Determinar la forma funcional resultante de la parametrización de Box-Cox en el punto límite lambda = 0.
- **Manifestación:** Afirmar que la transformación de Box-Cox no puede representar el modelo logarítmico cuando lambda es exactamente cero.
- **Pauta de Remediación:** *Aplica L'Hôpital derivando respecto a lambda: d(exp(lambda*ln Y) - 1)/dlambda = ln(Y)*Y^lambda; al evaluar en 0 resulta ln(Y).*

---


# Sesión 3: Estimación de la Varianza del Error, Descomposición ANOVA, R^2 e Inferencia F y t

## [H-03] Álgebra de Proyecciones: Hat Matrix P, Aniquiladora M y Matriz Centradora M^0 (Hecho [H])
- **Unit Index:** 6
- **Bloom Taxonomy:** Remember
- **Prerequisites:** `Hab-01`
- **Evidence:** `EST3_LEC03_26_2.pdf` (pág. 17)

### Descripción Matemática
Estructura y propiedades algebraicas fundamentales de los proyectores ortogonales: 1) Hat Matrix $\mathbf{P} = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}' \in \mathbb{R}^{n \times n}$ tal que $\hat{\mathbf{Y}} = \mathbf{P}\mathbf{Y}$, $\mathbf{P}' = \mathbf{P}$, $\mathbf{P}^2 = \mathbf{P}$, $\mathbf{P}\mathbf{X} = \mathbf{X}$, $\text{traza}(\mathbf{P}) = k$; 2) Matriz aniquiladora o generadora de residuos $\mathbf{M} = \mathbf{I}_n - \mathbf{P}$ tal que $\hat{\mathbf{u}} = \mathbf{M}\mathbf{Y} = \mathbf{M}\mathbf{u}$, $\mathbf{M}' = \mathbf{M}$, $\mathbf{M}^2 = \mathbf{M}$, $\mathbf{M}\mathbf{X} = \mathbf{0}$, $\mathbf{P}\mathbf{M} = \mathbf{0}$, $\text{traza}(\mathbf{M}) = n - k$; 3) Matriz centradora $\mathbf{M}^0 = \mathbf{I}_n - \frac{1}{n}\boldsymbol{\iota}\boldsymbol{\iota}'$ tal que $\mathbf{M}^0 \boldsymbol{\iota} = \mathbf{0}$, $\mathbf{M}^0 \hat{\mathbf{u}} = \hat{\mathbf{u}}$ y $\text{traza}(\mathbf{M}^0) = n - 1$.

### Ejemplos en Corpus
- P = X(X'X)^(-1)X', M = I - P, M^0 = I - (1/n)*iota*iota'. Propiedades: P'=P, P^2=P, M'=M, M^2=M, PM=0, traza(P)=k, traza(M)=n-k.

### Distractores Fusionados (3)
#### `D-H-03-01` - Cálculo erróneo de la traza de la Hat Matrix creyendo que equivale a n
- **Tipo de Error:** `conceptual_swap` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `EST3_LEC03_26_2.pdf` (pág. 17)
- **Creencia Errónea:** Creer que traza(P) = n porque P es una matriz de dimensiones n x n.
- **Creencia Correcta:** Por la propiedad cíclica del operador traza, traza(P) = traza(X(X'X)^(-1)X') = traza((X'X)^(-1)X'X) = traza(I_k) = k.
- **Detonante (Trigger):** Calcular los grados de libertad asociados al hiperplano de predicción o espacio columna de X.
- **Manifestación:** Asignar n grados de libertad a la proyección, concluyendo erróneamente que traza(M) = 0.
- **Pauta de Remediación:** *Aplica la propiedad cíclica de la traza traza(AB) = traza(BA). Al ciclar X' se obtiene traza(I_k) = k.*

#### `D-H-03-02` - Creencia errónea de que la matriz aniquiladora M es no singular
- **Tipo de Error:** `boundary_case` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `EST3_LEC03_26_2.pdf` (pág. 18)
- **Creencia Errónea:** Intentar calcular la inversa ordinaria M^(-1) de la matriz aniquiladora de residuos.
- **Creencia Correcta:** M es un proyector ortogonal de rango n - k < n; por tanto, tiene k autovalores nulos y su determinante es estrictamente cero (es singular).
- **Detonante (Trigger):** Intentar despejar Y a partir de los residuos M*Y = u_hat.
- **Manifestación:** Error de singularidad al ejecutar o proponer M^(-1) en deducciones algebraicas.
- **Pauta de Remediación:** *Recuerda que toda matriz idempotente distinta de la identidad es singular (det(M)=0) porque proyecta sobre un subespacio propio.*

#### `D-H-03-03` - Confusión en la ortogonalidad entre P y M
- **Tipo de Error:** `sign_error` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `EST3_LEC03_26_2.pdf` (pág. 19)
- **Creencia Errónea:** Creer que P*M = I_n o que P*M = P en lugar de la matriz nula de ceros.
- **Creencia Correcta:** Dado que M = I - P y P es idempotente (P^2 = P), P*M = P(I - P) = P - P^2 = P - P = 0_{n x n}.
- **Detonante (Trigger):** Expandir productos cruzados de valores ajustados y residuos (PY)'*(MY).
- **Manifestación:** Falla en la cancelación del producto cruzado Y'*P'*M*Y, impidiendo la descomposición ortogonal de Pitágoras.
- **Pauta de Remediación:** *P y M proyectan sobre subespacios ortogonales complementarios; su producto siempre es idénticamente la matriz nula 0.*

---

## [C-03] Descomposición Ortogonal de Sumas de Cuadrados (ANOVA) y Coeficiente R^2 (Concepto [C])
- **Unit Index:** 7
- **Bloom Taxonomy:** Understand
- **Prerequisites:** `H-03`
- **Evidence:** `EST3_LEC03_26_2.pdf` (pág. 21)

### Descripción Matemática
Fundamento teórico de la partición de la varianza total: En modelos con constante, el vector unitario $\boldsymbol{\iota} \in \text{Col}(\mathbf{X})$, lo que asegura que $\mathbf{M}^0 \mathbf{M} = \mathbf{M}$ y $\mathbf{M}^0 \hat{\mathbf{u}} = \hat{\mathbf{u}}$. Esto anula los productos cruzados entre valores ajustados centrados y residuos, demostrando el Teorema de Pitágoras centrado: $\text{STC} = \text{SEC} + \text{SRC}$ (donde $\text{STC} = \mathbf{Y}'\mathbf{M}^0 \mathbf{Y}$, $\text{SEC} = \hat{\mathbf{Y}}'\mathbf{M}^0 \hat{\mathbf{Y}}$, $\text{SRC} = \hat{\mathbf{u}}'\hat{\mathbf{u}}$). El coeficiente de determinación clásico se define como $R^2 = \frac{\text{SEC}}{\text{STC}} = 1 - \frac{\text{SRC}}{\text{STC}}$.

### Ejemplos en Corpus
- STC = SEC + SRC: Y'M^0Y = Y_hat'M^0Y_hat + u_hat'u_hat. Coeficiente de determinación: R^2 = SEC/STC = 1 - SRC/STC.

### Distractores Fusionados (3)
#### `D-C-03-01` - Generalización de la descomposición centrada STC = SEC + SRC a modelos sin constante
- **Tipo de Error:** `boundary_case` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `EST3_LEC03_26_2.pdf` (pág. 21)
- **Creencia Errónea:** Asumir que STC = SEC + SRC se cumple siempre, incluso si el modelo econométrico carece de término constante.
- **Creencia Correcta:** Si el modelo no incluye constante, el vector iota no pertenece a Col(X), por lo que sum(u_hat_i) != 0 y el producto cruzado Y_hat'M^0*u_hat != 0; en consecuencia, STC != SEC + SRC y R^2 puede ser negativo.
- **Detonante (Trigger):** Calcular o interpretar el R^2 centrado en una regresión forzada a pasar por el origen.
- **Manifestación:** Obtención de un R^2 centrado negativo o inconsistente que no suma 1 con SRC/STC.
- **Pauta de Remediación:** *Recuerda que la ortogonalidad entre Y_hat y los residuos centrados exige que la suma de residuos sea cero, propiedad garantizada solo si hay intercepto.*

#### `D-C-03-02` - Interpretación causal del coeficiente de determinación R^2
- **Tipo de Error:** `overgeneralization` | **Severidad:** `medium` | **Origen:** `inferred`
- **Evidencia:** `EST3_LEC03_26_2.pdf` (pág. 21)
- **Creencia Errónea:** Creer que un R^2 alto demuestra una relación de causalidad directa entre los regresores y la variable dependiente.
- **Creencia Correcta:** R^2 únicamente mide la proporción de la variabilidad muestral lineal de Y explicada por X; no demuestra causalidad ni exime de problemas de endogeneidad o regresión espuria.
- **Detonante (Trigger):** Interpretar el valor empírico de R^2 obtenido de una regresión con series no estacionarias o variables omitidas.
- **Manifestación:** Afirmar causalidad económica certera basándose únicamente en un valor de R^2 > 0.90.
- **Pauta de Remediación:** *R^2 es una medida de ajuste lineal descriptivo muestral, no una prueba de validez estructural ni de causalidad.*

#### `D-C-03-03` - Inversión entre las razones de variabilidad al definir R^2
- **Tipo de Error:** `procedural_slip` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `EST3_LEC03_26_2.pdf` (pág. 21)
- **Creencia Errónea:** Definir R^2 como SRC/STC o como 1 - SEC/STC.
- **Creencia Correcta:** R^2 representa la fracción explicada: SEC/STC. La fracción residual no explicada es SRC/STC, por lo que R^2 = 1 - SRC/STC.
- **Detonante (Trigger):** Escribir la fórmula del coeficiente de determinación en función de las sumas de cuadrados.
- **Manifestación:** Calcular 1 - R^2 en lugar de R^2, invirtiendo la bondad de ajuste del modelo.
- **Pauta de Remediación:** *Recuerda: R^2 mide la bondad explicada (SEC/STC). Mientras menor sea la suma residual SRC, más cercano a 1 será R^2.*

---

## [Hab-03] Estimación Insesgada de la Varianza del Error s^2 mediante la Traza de M (Habilidad [Hab])
- **Unit Index:** 8
- **Bloom Taxonomy:** Apply
- **Prerequisites:** `H-03`
- **Evidence:** `EST3_LEC03_26_2.pdf` (pág. 18)

### Descripción Matemática
Procedimiento riguroso para derivar y calcular el estimador insesgado de la varianza del error $\sigma^2$: 1) Expresión de la suma residual como forma cuadrática $\hat{\mathbf{u}}'\hat{\mathbf{u}} = (\mathbf{M}\mathbf{u})'(\mathbf{M}\mathbf{u}) = \mathbf{u}'\mathbf{M}'\mathbf{M}\mathbf{u} = \mathbf{u}'\mathbf{M}\mathbf{u}$; 2) Aplicación del operador traza sobre el escalar $E[\hat{\mathbf{u}}'\hat{\mathbf{u}}] = E[\text{traza}(\mathbf{u}'\mathbf{M}\mathbf{u})]$; 3) Permutación cíclica $E[\text{traza}(\mathbf{M}\mathbf{u}\mathbf{u}')] = \text{traza}(\mathbf{M}E[\mathbf{u}\mathbf{u}']) = \text{traza}(\mathbf{M}\sigma^2 \mathbf{I}_n) = \sigma^2 \text{traza}(\mathbf{M})$; 4) Sustitución de $\text{traza}(\mathbf{M}) = n - k$, resultando $E[\hat{\mathbf{u}}'\hat{\mathbf{u}}] = \sigma^2 (n - k)$; 5) Definición del estimador insesgado $s^2 = \frac{\hat{\mathbf{u}}'\hat{\mathbf{u}}}{n - k}$ tal que $E[s^2] = \sigma^2$.

### Ejemplos en Corpus
- u_hat'u_hat = u'Mu, E(u_hat'u_hat) = sigma^2*traza(M) = sigma^2*(n-k), s^2 = u_hat'u_hat / (n-k), Var_hat(beta_hat|X) = s^2*(X'X)^(-1).

### Distractores Fusionados (6)
#### `D-Hab-03-01` - División por el tamaño muestral n en lugar de los grados de libertad residuales n - k
- **Tipo de Error:** `unit_or_scale` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `EST3_LEC03_26_2.pdf` (pág. 18)
- **Creencia Errónea:** Calcular el estimador insesgado de la varianza dividiendo la suma residual entre n en vez de n - k.
- **Creencia Correcta:** Dividir entre n produce el estimador de máxima verosimilitud (MLE), el cual es sesgado en muestras pequeñas con sesgo E[sigma_MLE^2] = sigma^2 (n-k)/n. El estimador insesgado MCO exige dividir entre n - k.
- **Detonante (Trigger):** Calcular la varianza residual muestral s^2 a partir de la suma de residuos al cuadrado u_hat'u_hat.
- **Manifestación:** Subestimación sistemática de la varianza residual por un factor de (n - k)/n.
- **Pauta de Remediación:** *Resta siempre el número total de parámetros estimados k del tamaño muestral n al calcular la varianza residual insesgada s^2.*

#### `D-Hab-03-02` - Omisión de la permutación cíclica en la traza de la forma cuadrática
- **Tipo de Error:** `skipped_step` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `EST3_LEC03_26_2.pdf` (pág. 18)
- **Creencia Correcta:** Para ingresar el operador de esperanza hacia el producto u*u', se debe aplicar la propiedad cíclica traza(u'Mu) = traza(Muu').
- **Paso Omitido (Expert Blindness):** Permutar cíclicamente los términos en el operador traza para transformar la forma cuadrática u'Mu en traza(M*uu').
- **Detonante (Trigger):** Demostrar algebraicamente el valor esperado de la forma cuadrática u'Mu.
- **Manifestación:** Incapacidad de factorizar la matriz de varianza poblacional sigma^2*I_n fuera del producto vectorial.
- **Pauta de Remediación:** *Recuerda que para cualquier vector u y matriz M, u'Mu = traza(u'Mu) = traza(Muu') por la propiedad cíclica.*

#### `D-Hab-03-03` - Uso de grados de libertad univariados n - 1 en regresión múltiple
- **Tipo de Error:** `procedural_slip` | **Severidad:** `high` | **Origen:** `inferred`
- **Evidencia:** `EST3_LEC03_26_2.pdf` (pág. 18)
- **Creencia Errónea:** Dividir entre n - 1 creyendo que solo se pierde un grado de libertad al estimar la media.
- **Creencia Correcta:** En regresión múltiple se estiman k parámetros (constante más k - 1 pendientes), por lo que se consumen k grados de libertad, dejando n - k.
- **Detonante (Trigger):** Calcular el denominador de s^2 en un modelo con múltiples regresores.
- **Manifestación:** Varianza residual artificialmente pequeña e inflación espuria de los estadísticos t de significancia.
- **Pauta de Remediación:** *En regresión lineal múltiple con k coeficientes, el número de grados de libertad residuales es estrictamente n - k.*

#### `D-Hab-03-04` - Confusión entre la varianza residual s^2 y el error estándar de la regresión s
- **Tipo de Error:** `unit_or_scale` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `EST3_LEC03_26_2.pdf` (pág. 18)
- **Creencia Errónea:** Utilizar la varianza residual s^2 directamente dentro del denominador del estadístico t sin extraer la raíz cuadrada.
- **Creencia Correcta:** El error estándar de la regresión es la desviación típica s = sqrt(s^2). Los errores estándar de los coeficientes requieren SE(beta_j) = sqrt(s^2 * c_jj) = s * sqrt(c_jj).
- **Detonante (Trigger):** Construir los errores estándar de los parámetros a partir de la matriz de varianza-covarianza.
- **Manifestación:** Errores estándar de orden cuadrático que distorsionan severamente los estadísticos de prueba.
- **Pauta de Remediación:** *Asegúrate de tomar la raíz cuadrada de la varianza residual s^2 para obtener el error estándar de la regresión s.*

#### `D-Hab-03-05` - Omisión de la comprobación del rango de M ante colinealidad no detectada
- **Tipo de Error:** `skipped_step` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `EST3_LEC03_26_2.pdf` (pág. 18)
- **Creencia Correcta:** Los grados de libertad residuales son formalmente rango(M) = n - rango(X); si rango(X) < k, la división por n - k es incorrecta.
- **Paso Omitido (Expert Blindness):** Verificar que rango(X) = k para garantizar que rango(M) = n - k antes de dividir.
- **Detonante (Trigger):** Calcular la varianza residual en bases de datos con posibles redundancias lineales.
- **Manifestación:** Grados de libertad residuales mal calculados cuando existen variables explicativas perfectamente colineales.
- **Pauta de Remediación:** *Asegúrate de que no existan variables colineales para que la pérdida de grados de libertad sea exactamente k.*

#### `D-Hab-03-06` - Suposición de varianza homocedástica constante para cada residuo individual
- **Tipo de Error:** `overgeneralization` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `EST3_LEC03_26_2.pdf` (pág. 18)
- **Creencia Errónea:** Creer que Var(u_hat_i|X) = sigma^2 para todo i.
- **Creencia Correcta:** Aunque las perturbaciones poblacionales son homocedásticas (Var(u_i)=sigma^2), los residuos MCO no lo son: Var(u_hat|X) = sigma^2 * M, lo que implica Var(u_hat_i|X) = sigma^2 * (1 - p_ii), variando según el leverage p_ii.
- **Detonante (Trigger):** Evaluar la varianza individual de un residuo de regresión u_hat_i.
- **Manifestación:** Ignorar el impacto del apalancamiento (leverage) p_ii en el análisis de residuos y detección de outliers.
- **Pauta de Remediación:** *Recuerda que u_hat = Mu, por lo que Var(u_hat) = sigma^2*M. La varianza del residuo i-ésimo es sigma^2*(1 - p_ii), no sigma^2.*

---

## [Hab-04] Inferencia Estadística en Muestras Finitas: Contrastes t-Student y F-Fisher (Habilidad [Hab])
- **Unit Index:** 9
- **Bloom Taxonomy:** Apply
- **Prerequisites:** `C-03`, `Hab-03`
- **Evidence:** `EST3_LEC03_26_2.pdf` (pág. 23)

### Descripción Matemática
Procedimiento completo para realizar pruebas de hipótesis sobre parámetros del modelo lineal: 1) Test $t$-Student de significancia individual: $H_0: \beta_j = \beta_{j0}$ vs. $H_1: \beta_j \neq \beta_{j0}$, estadístico $t = \frac{\hat{\beta}_j - \beta_{j0}}{\text{SE}(\hat{\beta}_j)} = \frac{\hat{\beta}_j - \beta_{j0}}{\sqrt{s^2 c_{jj}}} \sim t_{(n-k)}$, donde $c_{jj} = [(X'X)^{-1}]_{jj}$; 2) Test $F$-Fisher de significancia global: $H_0: \beta_2 = \dots = \beta_k = 0$, estadístico $F = \frac{\text{SEC}/(k-1)}{\text{SRC}/(n-k)} = \frac{R^2/(k-1)}{(1 - R^2)/(n-k)} \sim F_{(k-1, n-k)}$; 3) Decisión con regla crítica o $p$-valor: rechazar $H_0$ si $|t| > t_{\text{crit}}$, si $F > F_{\text{crit}}$, o si $p\text{-valor} \le \alpha$.

### Ejemplos en Corpus
- Test t: t_calc = (beta_hat_j - 0)/SE(beta_hat_j) ~ t_(n-k). Test F: F = [R^2/(k-1)] / [(1-R^2)/(n-k)] ~ F_(k-1, n-k). Rechazar H0 si p-valor <= alpha.

### Distractores Fusionados (6)
#### `D-Hab-04-01` - Inversión de los grados de libertad del numerador y denominador en el test F
- **Tipo de Error:** `procedural_slip` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `EST3_LEC03_26_2.pdf` (pág. 25)
- **Creencia Errónea:** Contrastar el estadístico F contra una distribución crítica F(n - k, k - 1) en lugar de F(k - 1, n - k).
- **Creencia Correcta:** Los grados de libertad del numerador corresponden al número de restricciones probadas (k - 1 para significancia global), y los del denominador a los residuos (n - k).
- **Detonante (Trigger):** Buscar el valor crítico de tablas para la prueba F de significancia global.
- **Manifestación:** Adopción de un umbral crítico totalmente distorsionado que lleva a decisiones erróneas sobre el rechazo de H0.
- **Pauta de Remediación:** *Recuerda: gl1 (numerador) = número de restricciones = k - 1; gl2 (denominador) = grados de libertad residuales = n - k.*

#### `D-Hab-04-02` - Omisión de la duplicación de la cola en el cálculo del p-valor bilateral del test t
- **Tipo de Error:** `skipped_step` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `EST3_LEC03_26_2.pdf` (pág. 27)
- **Creencia Correcta:** Para una hipótesis bilateral H1: beta_j != beta_{j0}, el p-valor es 2 * P(T >= |t_calc|). Omitir el factor 2 corresponde a una prueba unilateral.
- **Paso Omitido (Expert Blindness):** Multiplicar por 2 la probabilidad de cola superior al contrastar una hipótesis alternativa bilateral.
- **Detonante (Trigger):** Calcular o contrastar el p-valor asociado a un estadístico t bilateral.
- **Manifestación:** Reportar un p-valor que es la mitad del real, provocando rechazos espurios de la hipótesis nula.
- **Pauta de Remediación:** *En contrastes bilaterales H1: beta_j != 0, multiplica siempre por 2 el área de la cola: p-valor = 2 * P(T >= |t|).*

#### `D-Hab-04-03` - Uso de los elementos diagonales de X'X en vez de los de (X'X)^(-1)
- **Tipo de Error:** `conceptual_swap` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `EST3_LEC03_26_2.pdf` (pág. 23)
- **Creencia Errónea:** Calcular la varianza del coeficiente como s^2 * [X'X]_{jj} en lugar de s^2 * [(X'X)^(-1)]_{jj}.
- **Creencia Correcta:** La matriz de covarianza de beta_hat es sigma^2*(X'X)^(-1); por tanto, la varianza individual proviene de la diagonal de la matriz invertida c_jj.
- **Detonante (Trigger):** Calcular los errores estándar de los estimadores a partir de matrices muestrales.
- **Manifestación:** Errores estándar completamente equivocados que impiden la construcción correcta del estadístico t.
- **Pauta de Remediación:** *Usa siempre los elementos diagonales de la matriz invertida (X'X)^(-1), nunca los de la matriz original X'X.*

#### `D-Hab-04-04` - Inversión de la regla de decisión basada en p-valor
- **Tipo de Error:** `sign_error` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `EST3_LEC03_26_2.pdf` (pág. 28)
- **Creencia Errónea:** Rechazar la hipótesis nula cuando el p-valor es mayor que el nivel de significancia alpha (p > alpha).
- **Creencia Correcta:** La regla universal de decisión es rechazar H0 si y solo si p-valor <= alpha. Si p-valor > alpha, no existe evidencia suficiente para rechazar H0.
- **Detonante (Trigger):** Concluir el test de hipótesis comparando el p-valor reportado frente a alpha = 0.05.
- **Manifestación:** Rechazar variables que no tienen significancia estadística o mantener variables nulas.
- **Pauta de Remediación:** *Mnemotecnia clásica: 'Si el p-valor es bajo, H0 debe caer' (rechazar H0 si p-valor <= alpha).*

#### `D-Hab-04-05` - Omisión de la exclusión del intercepto en los grados de libertad del numerador de F
- **Tipo de Error:** `skipped_step` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `EST3_LEC03_26_2.pdf` (pág. 25)
- **Creencia Correcta:** La prueba de significancia global solo contrasta las pendientes explicativas (beta_2 = ... = beta_k = 0), excluyendo la constante. Por tanto, el número de restricciones es k - 1, no k.
- **Paso Omitido (Expert Blindness):** Restar 1 parámetro correspondiente a la constante para fijar gl1 = k - 1 en el numerador de F.
- **Detonante (Trigger):** Calcular el estadístico F de significancia global a partir del R^2.
- **Manifestación:** Estadístico F subestimado calculado como [R^2/k] / [(1 - R^2)/(n - k)].
- **Pauta de Remediación:** *En la significancia global se evalúan únicamente las k - 1 pendientes; no se incluye el intercepto en la hipótesis nula.*

#### `D-Hab-04-06` - Afirmación de certeza poblacional nula ante el no rechazo de H0
- **Tipo de Error:** `overgeneralization` | **Severidad:** `low` | **Origen:** `source`
- **Evidencia:** `EST3_LEC03_26_2.pdf` (pág. 24)
- **Creencia Errónea:** Afirmar que no rechazar H0: beta_j = 0 demuestra con total certeza que el verdadero parámetro poblacional es idénticamente cero.
- **Creencia Correcta:** El no rechazo de H0 solo indica ausencia de evidencia muestral suficiente para descartar el valor nulo al nivel alpha; no demuestra que beta_j sea exactamente cero.
- **Detonante (Trigger):** Redactar la conclusión empírica de una prueba t donde |t_calc| < t_crit.
- **Manifestación:** Aseveraciones categóricas erróneas de que la variable no tiene ninguna relación con Y en la población.
- **Pauta de Remediación:** *Usa la redacción estadística adecuada: 'No se rechaza H0' o 'No existe evidencia estadísticamente significativa de un efecto'.*

---


# Sesión 4: Restricciones Lineales Generales, Formas Cuadráticas y Diagnóstico Econométrico

## [H-04] Formulación Matricial de Restricciones Lineales Generales R*beta = r (Hecho [H])
- **Unit Index:** 10
- **Bloom Taxonomy:** Remember
- **Prerequisites:** `Hab-04`
- **Evidence:** `stats 3 3-10.png` (pág. 0)

### Descripción Matemática
Estructura formal para contrastar q restricciones lineales simultáneas sobre el vector de parámetros: $H_0: \mathbf{R}\boldsymbol{\beta} = \mathbf{r}$ frente a $H_1: \mathbf{R}\boldsymbol{\beta} \neq \mathbf{r}$, donde $\mathbf{R} \in \mathbb{R}^{q \times k}$ es la matriz de restricciones con rango fila completo $\text{rango}(\mathbf{R}) = q \le k$, y $\mathbf{r} \in \mathbb{R}^{q \times 1}$ es el vector de valores hipotéticos. El estadístico de Wald/Fisher toma la forma cuadrática $F = \frac{(\mathbf{R}\hat{\boldsymbol{\beta}} - \mathbf{r})' [\mathbf{R}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{R}']^{-1} (\mathbf{R}\hat{\boldsymbol{\beta}} - \mathbf{r})}{q \cdot s^2} \sim F_{(q, n-k)}$.

### Ejemplos en Corpus
- Contraste de restricciones: H0: R*beta = r con R (q x k) de rango q. F = (R*beta_hat - r)'[R(X'X)^(-1)R']^(-1)(R*beta_hat - r) / (q * s^2) ~ F(q, n-k).

### Distractores Fusionados (3)
#### `D-H-04-01` - Especificación de una matriz de restricciones R con filas linealmente dependientes
- **Tipo de Error:** `boundary_case` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `stats 3 3-10.png` (pág. 0)
- **Creencia Errónea:** Plantear matrices de restricciones donde una fila es combinación lineal de otra, asumiendo que el estadístico F puede resolverse normalmente.
- **Creencia Correcta:** La matriz R debe tener rango fila pleno (rango(R) = q); de lo contrario, la matriz R(X'X)^(-1)R' de orden q x q es singular y no puede invertirse.
- **Detonante (Trigger):** Formular hipótesis simultáneas redundantes en el contraste de restricciones conjuntas.
- **Manifestación:** Imposibilidad de invertir R(X'X)^(-1)R' en el cálculo del estadístico F.
- **Pauta de Remediación:** *Verifica siempre que las q restricciones formuladas sean independientes entre sí para que rango(R) = q.*

#### `D-H-04-02` - Inversión dimensional de la matriz de restricciones R
- **Tipo de Error:** `notation` | **Severidad:** `medium` | **Origen:** `inferred`
- **Evidencia:** `stats 3 3-10.png` (pág. 0)
- **Creencia Errónea:** Tratar la matriz R como de dimensión k x q en lugar de q x k.
- **Creencia Correcta:** Cada fila de R representa una restricción lineal y cada columna corresponde a uno de los k coeficientes del modelo; por tanto, R es q x k.
- **Detonante (Trigger):** Multiplicar la matriz de restricciones R por el vector de parámetros beta (k x 1).
- **Manifestación:** Dimensiones incompatibles en el producto R*beta.
- **Pauta de Remediación:** *Recuerda: tantas filas como restricciones haya (q), y tantas columnas como parámetros tenga el modelo (k).*

#### `D-H-04-03` - Ignorancia de las covarianzas entre parámetros al contrastar restricciones conjuntas
- **Tipo de Error:** `conceptual_swap` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `stats 3 3-10.png` (pág. 0)
- **Creencia Errónea:** Evaluar la significancia conjunta de dos coeficientes realizando dos pruebas t independientes y concluyendo sin considerar la covarianza Cov(beta_i, beta_j).
- **Creencia Correcta:** La prueba conjunta F utiliza la matriz completa R(X'X)^(-1)R', la cual incorpora explícitamente las covarianzas muestrales entre los estimadores.
- **Detonante (Trigger):** Contraste de hipótesis sobre la suma o igualdad de coeficientes (ej. beta_1 + beta_2 = 1).
- **Manifestación:** Aceptar erróneamente la nula al sumar varianzas ignorando el término de covarianza 2*Cov(beta_1, beta_2).
- **Pauta de Remediación:** *Usa la forma matricial cuadrática del test F para asegurar la correcta incorporación de las covarianzas entre parámetros.*

---

## [C-04] Teorema de Saturación Muestral (n = k) e Inferencia en Formas Cuadráticas (Concepto [C])
- **Unit Index:** 11
- **Bloom Taxonomy:** Understand
- **Prerequisites:** `H-04`, `Hab-03`
- **Evidence:** `stats 3 3-10.png` (pág. 2)

### Descripción Matemática
Análisis matemático del caso límite saturado cuando el número de observaciones es exactamente igual al número de parámetros ($n = k$): La matriz $\mathbf{X}$ es cuadrada ($n \times n$) e invertible, lo que colapsa el estimador a $\hat{\boldsymbol{\beta}} = \mathbf{X}^{-1}\mathbf{Y}$, anulando idénticamente los residuos $\hat{\mathbf{u}} = \mathbf{Y} - \mathbf{X}(\mathbf{X}^{-1}\mathbf{Y}) = \mathbf{0}_{n \times 1}$, arrojando un ajuste perfecto $R^2 = 1$ y $0$ grados de libertad residuales ($n - k = 0$). Como consecuencia del Teorema de Cochran, la forma cuadrática $\frac{\hat{\mathbf{u}}'\hat{\mathbf{u}}}{\sigma^2} = \frac{\mathbf{u}'\mathbf{M}\mathbf{u}}{\sigma^2} \sim \chi^2_{(n-k)}$, imposibilitando la inferencia estadística al quedar indeterminada la varianza residual $s^2 = 0/0$.

### Ejemplos en Corpus
- Caso n=k: X es cuadrada e invertible, beta_hat = X^(-1)Y, u_hat = 0, R^2 = 1, gl = n-k = 0, s^2 queda indeterminado.

### Distractores Fusionados (3)
#### `D-C-04-01` - Interpretación de ajuste perfecto como éxito econométrico en muestras saturadas
- **Tipo de Error:** `conceptual_swap` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `stats 3 3-10.png` (pág. 2)
- **Creencia Errónea:** Creer que obtener R^2 = 1 en una muestra con n = k observaciones representa un modelo con excelente capacidad predictiva general.
- **Creencia Correcta:** Un R^2 = 1 cuando n = k es un artificio puramente algebraico de un sistema lineal con solución exacta; no hay grados de libertad para contrastar hipótesis ni para estimar la varianza del error.
- **Detonante (Trigger):** Analizar los resultados de una regresión donde el tamaño muestral n coincide con el número de variables k.
- **Manifestación:** Recomendar la adopción del modelo asumiendo ajuste óptimo en lugar de advertir la ausencia de grados de libertad.
- **Pauta de Remediación:** *Recuerda que con n = k simplemente estás resolviendo un sistema de ecuaciones lineales sin redundancia estocástica: gl = 0 y s^2 no existe.*

#### `D-C-04-02` - Intento de cálculo de estadísticos t y F en el caso saturado n = k
- **Tipo de Error:** `boundary_case` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `stats 3 3-10.png` (pág. 2)
- **Creencia Errónea:** Intentar calcular el estadístico t dividiendo por s = 0 y obteniendo valores supuestamente infinitos.
- **Creencia Correcta:** Dado que s^2 = u_hat'u_hat / (n - k) = 0 / 0, el estimador de la varianza está algebraicamente indeterminado, haciendo imposible el cálculo de estadísticos t y F.
- **Detonante (Trigger):** Calcular pruebas de hipótesis en un modelo con n = k.
- **Manifestación:** Reportar erróneamente estadísticos t = infinito y rechazo de todas las hipótesis nulas.
- **Pauta de Remediación:** *Verifica siempre que n > k para disponer de al menos un grado de libertad residual para la inferencia estadística.*

#### `D-C-04-03` - Identificación de los residuos calculados con las perturbaciones poblacionales
- **Tipo de Error:** `conceptual_swap` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `stats 3 3-10.png` (pág. 2)
- **Creencia Errónea:** Creer que u_hat = 0 cuando n = k implica que las perturbaciones poblacionales u_i son exactamente cero.
- **Creencia Correcta:** u_hat es una variable muestral forzada a cero por la saturación dimensional (u_hat = M*u = 0 porque M = 0), pero las perturbaciones latentes u_i siguen siendo no nulas con varianza sigma^2 > 0.
- **Detonante (Trigger):** Deducir las propiedades de las perturbaciones inobservables en el caso saturado.
- **Manifestación:** Afirmar erróneamente que los datos no tienen ruido estocástico cuando n = k.
- **Pauta de Remediación:** *Distingue siempre entre el error poblacional inobservable u y el residuo MCO u_hat = Mu.*

---

## [Hab-05] Diagnóstico e Interpretación Econométrica de Salidas EViews (Habilidad [Hab])
- **Unit Index:** 12
- **Bloom Taxonomy:** Analyze
- **Prerequisites:** `Hab-04`, `C-03`
- **Evidence:** `stats 3 3-10.png` (pág. 6)

### Descripción Matemática
Procedimiento de lectura, diagnóstico e inferencia econométrica integral a partir de tablas de regresión tipo EViews: 1) Análisis de coeficientes individuales: estimación puntual, error estándar (`Std. Error`), estadístico `t-Statistic` y regla del `p-valor` (`Prob.`); 2) Diagnóstico de bondad de ajuste: interpretación de `R-squared` ($R^2$), penalización por grados de libertad en `Adjusted R-squared` ($\bar{R}^2 = 1 - (1 - R^2)\frac{n-1}{n-k}$), y escala en `S.E. of regression` ($s = \sqrt{\text{SRC}/(n-k)}$); 3) Contraste de significancia conjunta: interpretación de `F-statistic` y `Prob(F-statistic)`; 4) Diagnóstico de autocorrelación serial básica mediante el estadístico `Durbin-Watson stat` ($d \approx 2$ ausencia de correlación).

### Ejemplos en Corpus
- Tabla EViews (Inmobiliario n=11, k=5): Coeficientes significativos al 1% (Prob < 0.01), F-stat = 459.75 con Prob = 0.000000, R^2 = 0.9967, Durbin-Watson = 1.7968.

### Distractores Fusionados (6)
#### `D-Hab-05-01` - Diagnóstico erróneo de insignificancia en presencia de multicolinealidad severa
- **Tipo de Error:** `conceptual_swap` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `stats 3 3-10.png` (pág. 6)
- **Creencia Errónea:** Concluir que los regresores carecen de relación con Y al observar estadísticos t no significativos de forma aislada, ignorando un F-statistic altamente significativo y un R^2 elevado.
- **Creencia Correcta:** La combinación de un test F global altamente significativo con tests t individuales no significativos y R^2 alto es el síntoma clásico de multicolinealidad severa, no de falta de relación teórica.
- **Detonante (Trigger):** Interpretar una salida econométrica donde el F global es significativo pero varios tests t individuales no lo son.
- **Manifestación:** Eliminar erróneamente todas las variables colineales del modelo creyendo que ninguna es relevante.
- **Pauta de Remediación:** *Ante R^2 alto y F significativo con t individuales bajos, diagnostica multicolinealidad antes de descartar variables.*

#### `D-Hab-05-02` - Omisión de la verificación del estadístico Durbin-Watson antes de validar la inferencia
- **Tipo de Error:** `skipped_step` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `stats 3 3-10.png` (pág. 6)
- **Creencia Correcta:** Un estadístico Durbin-Watson sustancialmente alejado de 2 (ej. d < 1) evidencia autocorrelación serial de primer orden, lo que invalida la inferencia basada en los tests t y F estándar de MCO.
- **Paso Omitido (Expert Blindness):** Examinar el estadístico Durbin-Watson para confirmar d cercano a 2 antes de dar por válidos los p-valores de la tabla.
- **Detonante (Trigger):** Analizar la significancia de coeficientes en regresiones de series de tiempo.
- **Manifestación:** Aceptar conclusiones de significancia basadas en tests t cuyos errores estándar están severamente subestimados por autocorrelación.
- **Pauta de Remediación:** *Verifica que el estadístico Durbin-Watson esté próximo a 2 (rango habitual 1.8 a 2.2) para asegurar que los errores estándar no estén sesgados.*

#### `D-Hab-05-03` - Confusión entre el error estándar del parámetro y el error estándar de la regresión
- **Tipo de Error:** `conceptual_swap` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `stats 3 3-10.png` (pág. 6)
- **Creencia Errónea:** Confundir la fila 'Std. Error' de un coeficiente con el estadístico global 'S.E. of regression'.
- **Creencia Correcta:** 'Std. Error' es la desviación típica estimada del estimador individual SE(beta_j) = s * sqrt(c_jj); 'S.E. of regression' es la desviación típica estimada de las perturbaciones s = sqrt(SRC/(n-k)).
- **Detonante (Trigger):** Extraer el error estándar de la regresión para calcular intervalos de confianza o varianzas residuales.
- **Manifestación:** Uso de SE(beta_j) en lugar de s al calcular formas cuadráticas o varianzas residuales.
- **Pauta de Remediación:** *Distingue entre SE(beta_j) (precisión de un coeficiente individual) y S.E. of regression (dispersión típica del error del modelo).*

#### `D-Hab-05-04` - Interpretación del Prob(F-statistic) como probabilidad nula exacta
- **Tipo de Error:** `notation` | **Severidad:** `low` | **Origen:** `source`
- **Evidencia:** `stats 3 3-10.png` (pág. 6)
- **Creencia Errónea:** Afirmar que Prob(F-statistic) = 0.000000 significa que la probabilidad de que los coeficientes sean nulos es exactamente cero en términos absolutos.
- **Creencia Correcta:** 0.000000 es un truncamiento visual de software que denota un p-valor infinitesimal menor a 0.000001; nunca representa una probabilidad matemática de cero absoluto.
- **Detonante (Trigger):** Interpretar el valor p del estadístico F en salidas de software econométrico.
- **Manifestación:** Conclusiones dogmáticas de certeza absoluta en lugar de rechazo probabilístico al 99.9%.
- **Pauta de Remediación:** *Interpreta 0.000000 en EViews como p-valor < 0.0001 (altamente significativo al 99.9%).*

#### `D-Hab-05-05` - Omisión de la comparación entre R^2 y R^2 ajustado para detectar sobreajuste
- **Tipo de Error:** `skipped_step` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `stats 3 3-10.png` (pág. 6)
- **Creencia Correcta:** Una gran discrepancia entre R^2 y R^2 ajustado evidencia que se han agregado regresores irrelevantes que consumen grados de libertad sin aportar variabilidad explicativa genuina.
- **Paso Omitido (Expert Blindness):** Comparar la magnitud de R^2 frente a R^2 ajustado para evaluar si la inclusión de variables adicionales penaliza la parsimonia del modelo.
- **Detonante (Trigger):** Evaluar la especificación del modelo comparando alternativas con diferente número de variables explicativas.
- **Manifestación:** Seleccionar modelos sobreparametrizados basándose exclusivamente en un R^2 ligeramente mayor.
- **Pauta de Remediación:** *Usa el R^2 ajustado para comparar modelos con distinto número de regresores, ya que penaliza la pérdida de grados de libertad.*

#### `D-Hab-05-06` - Interpretación errónea del signo de un coeficiente sin contrastar con la teoría económica
- **Tipo de Error:** `conceptual_swap` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `stats 3 3-10.png` (pág. 6)
- **Creencia Errónea:** Asumir que un coeficiente con signo negativo es erróneo sin verificar el fundamento sustantivo de la relación empírica.
- **Creencia Correcta:** El signo de un coeficiente debe contrastarse con la teoría del dominio (por ejemplo, en el mercado inmobiliario, una mayor antigüedad de la vivienda debe tener signo negativo sobre el precio).
- **Detonante (Trigger):** Analizar la coherencia económica de los coeficientes estimados en la tabla EViews.
- **Manifestación:** Descalificar incorrectamente variables con signos negativos teóricamente esperados (como ANTIGUEDAD en precios).
- **Pauta de Remediación:** *Contrasta siempre el signo estimado frente a la hipótesis económica teórica antes de calificarlo como contraintuitivo.*

---


# Sesión 5: Notas de Inferencia Conjunta, Modelos con y sin Constante y Predicción de Y

## [Hab-06] Algoritmo de Cálculo Matricial Completo de P, Y_hat, Residuos y Formas Cuadráticas en Muestras Reducidas (Habilidad [Hab])
- **Unit Index:** 13
- **Bloom Taxonomy:** Apply
- **Prerequisites:** `H-03`, `Hab-01`
- **Evidence:** `Stats3 10-10.pdf` (pág. 1)

### Descripción Matemática
Procedimiento de cálculo matricial manual para muestras pequeñas ($n = 3, k = 2$): 1) Construcción y producto cruzado $\mathbf{X}'\mathbf{X} = \begin{bmatrix} n & \sum X \\ \sum X & \sum X^2 \end{bmatrix}$; 2) Cálculo del determinante $\det(\mathbf{X}'\mathbf{X}) = ad - bc$ y matriz inversa $(\mathbf{X}'\mathbf{X})^{-1} = \frac{1}{\det} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$; 3) Construcción de la Hat Matrix $\mathbf{P} = \mathbf{X}(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'$; 4) Predicción del vector de respuesta $\hat{\mathbf{Y}} = \mathbf{P}\mathbf{Y}$ y vector de residuos $\mathbf{e} = \mathbf{Y} - \hat{\mathbf{Y}}$; 5) Construcción de la matriz centradora $\mathbf{M}^0 = \mathbf{I}_n - \frac{1}{n}\boldsymbol{\iota}\boldsymbol{\iota}'$; 6) Cómputo numérico exacto de sumas de cuadrados $\text{STC} = \mathbf{Y}'\mathbf{M}^0 \mathbf{Y}$, $\text{SEC} = \hat{\boldsymbol{\beta}}'\mathbf{X}'\mathbf{M}^0 \mathbf{X}\hat{\boldsymbol{\beta}}$, $\text{SRC} = \mathbf{e}'\mathbf{e}$, estadístico $F$ y matriz $\widehat{\text{Var}}(\hat{\boldsymbol{\beta}}) = s^2 (\mathbf{X}'\mathbf{X})^{-1}$.

### Ejemplos en Corpus
- Ejemplo n=3, Y=[3,5,6]', X=[[1,1],[1,2],[1,3]]': X'X=[[3,6],[6,14]], det=6, (X'X)^(-1)=(1/6)*[[14,-6],[-6,3]], beta_hat=[5/3, 3/2]', STC=14/3, SEC=9/2, SRC=1/6, F=27.

### Distractores Fusionados (6)
#### `D-Hab-06-01` - Error de signo en los elementos fuera de la diagonal al invertir matrices 2x2
- **Tipo de Error:** `sign_error` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `Stats3 10-10.pdf` (pág. 1)
- **Creencia Errónea:** Invertir la matriz 2x2 cambiando los signos de la diagonal principal o manteniendo positivos los elementos cruzados.
- **Creencia Correcta:** La inversa de una matriz 2x2 [[a, b], [c, d]] intercambia la diagonal principal [[d, ...], [..., a]] y niega los elementos fuera de la diagonal [[..., -b], [-c, ...]].
- **Detonante (Trigger):** Calcular la matriz inversa (X'X)^(-1) para un modelo bivariado.
- **Manifestación:** Matriz (X'X)^(-1) incorrecta que altera los signos de los coeficientes estimados y covarianza.
- **Pauta de Remediación:** *Para matriz [[a,b],[c,d]], la inversa es (1/det)*[[d, -b],[-c, a]]. Intercambia diagonal principal y cambia de signo los elementos cruzados.*

#### `D-Hab-06-02` - Error en la formulación de la matriz centradora M^0 para orden n
- **Tipo de Error:** `procedural_slip` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `Stats3 10-10.pdf` (pág. 2)
- **Creencia Errónea:** Calcular M^0 restando 1/n a toda la matriz identidad, en vez de restar la matriz de unos dividida entre n ( (1/n)*iota*iota' ).
- **Creencia Correcta:** M^0 = I_n - (1/n)*iota*iota'; los elementos diagonales son 1 - 1/n = (n-1)/n, y los elementos fuera de la diagonal son estrictamente -1/n.
- **Detonante (Trigger):** Construir numéricamente la matriz centradora M^0 para un tamaño muestral específico.
- **Manifestación:** Matriz no idempotente que altera el cálculo de la suma total de cuadrados STC.
- **Pauta de Remediación:** *Construye M^0 poniendo (n-1)/n en la diagonal principal y -1/n en todos los elementos fuera de la diagonal.*

#### `D-Hab-06-03` - Omisión de la comprobación de simetría en la Hat Matrix calculada
- **Tipo de Error:** `skipped_step` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `Stats3 10-10.pdf` (pág. 1)
- **Creencia Correcta:** La matriz P = X(X'X)^(-1)X' debe ser estrictamente simétrica (P_ij = P_ji); cualquier discrepancia numérica evidencia un error en la multiplicación matricial.
- **Paso Omitido (Expert Blindness):** Verificar la simetría numérica P = P' tras realizar las multiplicaciones matriciales intermedias.
- **Detonante (Trigger):** Multiplicar X*(X'X)^(-1) por X' para obtener la Hat Matrix.
- **Manifestación:** Obtención de una matriz P asimétrica que conduce a predicciones y descomposiciones de varianza erróneas.
- **Pauta de Remediación:** *Comprueba que P_12 = P_21, P_13 = P_31, etc. La Hat Matrix calculada debe ser siempre exactamente simétrica.*

#### `D-Hab-06-04` - Inversión del orden en la resta de los residuos
- **Tipo de Error:** `sign_error` | **Severidad:** `low` | **Origen:** `source`
- **Evidencia:** `Stats3 10-10.pdf` (pág. 1)
- **Creencia Errónea:** Calcular el vector de residuos como e = Y_hat - Y en lugar de e = Y - Y_hat.
- **Creencia Correcta:** Por definición formal de MCO, el residuo es el valor observado menos el valor ajustado: e = Y - Y_hat.
- **Detonante (Trigger):** Calcular el vector de residuos a partir de las predicciones de la variable dependiente.
- **Manifestación:** Signos invertidos en todos los residuos individuales, afectando la dirección de los errores de predicción.
- **Pauta de Remediación:** *El residuo es lo observado menos lo ajustado: e = Y - Y_hat.*

#### `D-Hab-06-05` - Omisión de la verificación de suma de residuos nula antes de calcular STC
- **Tipo de Error:** `skipped_step` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `Stats3 10-10.pdf` (pág. 1)
- **Creencia Correcta:** En modelos con constante, la suma de los residuos debe ser exactamente cero: sum(e_i) = 0. Si no es cero, hubo un error de cálculo aritmético en beta_hat.
- **Paso Omitido (Expert Blindness):** Sumar los residuos individuales sum(e_i) para verificar que sea exactamente cero antes de proceder al análisis ANOVA.
- **Detonante (Trigger):** Finalizar la obtención del vector de residuos e.
- **Manifestación:** Arrastre de errores aritméticos no detectados hacia la suma de cuadrados y estadísticos de inferencia.
- **Pauta de Remediación:** *Verifica siempre sum(e_i) = 0 tras calcular los residuos en cualquier modelo con intercepto.*

#### `D-Hab-06-06` - Conclusión errónea de insignificancia global comparando contra el valor crítico t en lugar de F
- **Tipo de Error:** `conceptual_swap` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `Stats3 10-10.pdf` (pág. 3)
- **Creencia Errónea:** Comparar el estadístico F_calc = 27 contra un valor crítico de 1.96 o 4 en lugar del valor crítico F_tab(1, 1) = 39.86.
- **Creencia Correcta:** El estadístico F_calc se contrasta exclusivamente con tablas de la distribución F de Fisher con (k-1, n-k) grados de libertad. Para n=3 y k=2, F_crit(1, 1) al 10% es aproximadamente 40.
- **Detonante (Trigger):** Tomar la decisión estadística sobre la significancia global del modelo en muestras muy reducidas.
- **Manifestación:** Rechazar erróneamente H0 creyendo que F = 27 es significativo porque es mayor a 4.
- **Pauta de Remediación:** *En muestras pequeñas los valores críticos de F(1, 1) son sumamente altos (aprox. 40 al 10%); compara siempre con la distribución F correspondiente.*

---

## [C-05] Sensibilidad de la Bondad de Ajuste R^2 y R^2 Ajustado en Presencia y Ausencia de Término Constante (Concepto [C])
- **Unit Index:** 14
- **Bloom Taxonomy:** Understand
- **Prerequisites:** `C-03`, `Hab-06`
- **Evidence:** `Stats3 10-10.pdf` (pág. 7)

### Descripción Matemática
Fundamento teórico y distorsiones del coeficiente de determinación al suprimir el término independiente (modelo sin constante $Y_i = \alpha_1 X_i + u_i$): 1) La condición de primer orden $\sum e_i = 0$ ya no se verifica de forma general, imposibilitando la anulación de productos cruzados centrados; 2) La descomposición $\text{STC} = \text{SEC} + \text{SRC}$ calculada respecto a la media $\bar{Y}$ colapsa, pudiendo arrojar $R^2 < 0$; 3) El $R^2$ no centrado ($R_{\text{raw}}^2 = \frac{\sum \hat{Y}_i^2}{\sum Y_i^2}$) no es comparable con el $R^2$ centrado de modelos con intercepto; 4) El coeficiente ajustado $\bar{R}^2 = 1 - (1 - R^2)\frac{n-1}{n-k}$ penaliza drásticamente cuando los grados de libertad residuales $n - k$ son reducidos.

### Ejemplos en Corpus
- Modelo con constante vs sin constante: En modelo sin constante sum(e_i) != 0, STC != SEC + SRC centrado, y R^2 centrado puede ser negativo o no comparable.

### Distractores Fusionados (3)
#### `D-C-05-01` - Comparación directa del R^2 no centrado frente al R^2 centrado clásico
- **Tipo de Error:** `conceptual_swap` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `Stats3 10-10.pdf` (pág. 7)
- **Creencia Errónea:** Creer que un modelo sin constante con R_raw^2 = 0.98 es superior a un modelo con constante que tiene R^2 = 0.90.
- **Creencia Correcta:** El R^2 sin centrar mide la variación alrededor de cero, mientras que el R^2 centrado mide la variación respecto a la media bar(Y). No son métricas conmensurables.
- **Detonante (Trigger):** Comparar la bondad de ajuste entre una especificación con constante y otra sin constante.
- **Manifestación:** Elección errónea del modelo sin constante por una falsa ilusión de mayor ajuste explicativo.
- **Pauta de Remediación:** *Nunca compares directamente el R^2 de un modelo sin constante con el de un modelo con constante; las bases de variabilidad total difieren.*

#### `D-C-05-02` - Suposición de residuos de media cero en modelos sin intercepto
- **Tipo de Error:** `boundary_case` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `Stats3 10-10.pdf` (pág. 7)
- **Creencia Errónea:** Creer que sum(u_hat_i) = 0 es una propiedad universal de MCO válida en todo modelo lineal.
- **Creencia Correcta:** sum(u_hat_i) = 0 proviene exclusivamente de la ecuación normal asociada al intercepto dS/dbeta_1 = 0; si no hay constante en el modelo, la suma de residuos generalmente no es cero.
- **Detonante (Trigger):** Analizar las propiedades de los residuos en un modelo estimado sin término independiente.
- **Manifestación:** Aplicar propiedades de centrado y simplificaciones algebraicas inválidas a los residuos.
- **Pauta de Remediación:** *Recuerda que sum(u_hat_i) = 0 solo se cumple si la matriz de diseño X contiene un vector constante de unos.*

#### `D-C-05-03` - Ignorancia del impacto de la penalización de grados de libertad en R^2 ajustado
- **Tipo de Error:** `overgeneralization` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `Stats3 10-10.pdf` (pág. 5)
- **Creencia Errónea:** Creer que el R^2 ajustado siempre aumenta al agregar una nueva variable explicativa.
- **Creencia Correcta:** R^2 ajustado solo aumenta si el aporte marginal de la nueva variable compensa la pérdida de grados de libertad (equivalente a que el estadístico t individual sea en valor absoluto mayor a 1).
- **Detonante (Trigger):** Evaluar la evolución de R^2 ajustado al incorporar regresores adicionales.
- **Manifestación:** Concluir que agregar variables siempre mejora el modelo, cuando en realidad R^2 ajustado puede disminuir.
- **Pauta de Remediación:** *R^2 ajustado penaliza fuertemente la pérdida de grados de libertad; solo se incrementa si el estadístico t del regresor supera 1 en magnitud.*

---

## [Hab-07] Contraste Empírico de Modelos con y sin Intercepto y Predicción Condicional Puntual (Habilidad [Hab])
- **Unit Index:** 15
- **Bloom Taxonomy:** Apply
- **Prerequisites:** `C-05`, `Hab-06`
- **Evidence:** `Stats3 10-10.pdf` (pág. 9)

### Descripción Matemática
Procedimiento de estimación, diagnóstico de significancia individual y predicción puntual comparativa: 1) Estimación del modelo sin constante $\hat{\alpha}_1 = \frac{\sum X_i Y_i}{\sum X_i^2}$; 2) Estimación del modelo con constante $\hat{\beta}_2 = \frac{\sum (X_i - \bar{X})(Y_i - \bar{Y})}{\sum (X_i - \bar{X})^2}$ e intercepto $\hat{\beta}_1 = \bar{Y} - \hat{\beta}_2 \bar{X}$; 3) Estimación de varianzas residuales y errores estándar específicos para cada parámetro; 4) Contraste de hipótesis individual con grados de libertad ajustados ($n - 2$ con constante vs. $n - 1$ sin constante); 5) Predicción puntual de la media condicional $\hat{Y}_0 = \hat{\beta}_1 + \hat{\beta}_2 X_0$ para un valor fijado de la variable explicativa.

### Ejemplos en Corpus
- Ejercicio n=4: sum(X)=98, sum(Y)=12.7. Con constante: Y_hat = 1.1333 + 0.0833*X. Sin constante: Y_hat = 0.13*X. Predicción puntual para X=20: Y_hat = 1.1333 + 0.0833(20) = 2.80.

### Distractores Fusionados (6)
#### `D-Hab-07-01` - Uso de desvíos centrados al estimar la pendiente del modelo sin constante
- **Tipo de Error:** `conceptual_swap` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `Stats3 10-10.pdf` (pág. 7)
- **Creencia Errónea:** Calcular la pendiente sin intercepto usando sum(x_i*y_i)/sum(x_i^2) en lugar de sum(X_i*Y_i)/sum(X_i^2).
- **Creencia Correcta:** En el modelo sin constante, la condición de primer orden minimiza sum((Y_i - alpha*X_i)^2), lo que deriva en sum(X_i*Y_i)/sum(X_i^2), sin sustraer las medias.
- **Detonante (Trigger):** Calcular la pendiente estimada en una regresión lineal sin término independiente.
- **Manifestación:** Estimación errónea de la pendiente sin intercepto, haciéndola coincidir con la pendiente del modelo con constante.
- **Pauta de Remediación:** *En modelos sin constante usa valores brutos sin centrar: alpha_hat = sum(X*Y) / sum(X^2).*

#### `D-Hab-07-02` - Omisión del intercepto al calcular la predicción puntual en modelos con constante
- **Tipo de Error:** `skipped_step` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `Stats3 10-10.pdf` (pág. 9)
- **Creencia Correcta:** La predicción puntual de la media condicional en un modelo con constante exige sumar el intercepto: Y_hat_0 = beta_hat_1 + beta_hat_2 * X_0.
- **Paso Omitido (Expert Blindness):** Sumar el término constante estimado beta_hat_1 al producto marginal beta_hat_2 * X_0 para obtener la predicción puntual completa.
- **Detonante (Trigger):** Calcular la predicción puntual de Y para un valor fijado X_0.
- **Manifestación:** Pronóstico Y_hat_0 = beta_hat_2 * X_0 que omite el nivel base de la función de regresión.
- **Pauta de Remediación:** *Asegúrate de sumar el intercepto beta_hat_1 al pronosticar: Y_hat_0 = beta_hat_1 + beta_hat_2 * X_0.*

#### `D-Hab-07-03` - Uso erróneo de grados de libertad en la varianza residual del modelo sin intercepto
- **Tipo de Error:** `procedural_slip` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `Stats3 10-10.pdf` (pág. 8)
- **Creencia Errónea:** Dividir la suma residual entre n - 2 en un modelo sin constante creyendo que siempre se pierden 2 grados de libertad.
- **Creencia Correcta:** Al estimar un modelo con un solo parámetro (k = 1, solo la pendiente), los grados de libertad residuales son n - k = n - 1.
- **Detonante (Trigger):** Calcular el estimador de la varianza residual s^2 en un modelo sin intercepto.
- **Manifestación:** Subestimación de los grados de libertad y consecuente sobrestimación de la varianza del error.
- **Pauta de Remediación:** *Resta únicamente el número de parámetros efectivamente estimados: en un modelo sin constante k = 1, por lo que gl = n - 1.*

#### `D-Hab-07-04` - Inversión del cociente de la pendiente en la estimación sin constante
- **Tipo de Error:** `procedural_slip` | **Severidad:** `high` | **Origen:** `source`
- **Evidencia:** `Stats3 10-10.pdf` (pág. 7)
- **Creencia Errónea:** Calcular alpha_hat = sum(X_i^2) / sum(X_i*Y_i) invirtiendo el numerador y denominador.
- **Creencia Correcta:** La condición de primer orden iguala sum(X_i*(Y_i - alpha*X_i)) = 0, despejando alpha = sum(X_i*Y_i) / sum(X_i^2).
- **Detonante (Trigger):** Despejar la fórmula del estimador MCO sin intercepto.
- **Manifestación:** Pendiente estimada invertida que colapsa la escala del modelo.
- **Pauta de Remediación:** *La covarianza de la muestra va en el numerador y la variabilidad del regresor en el denominador: sum(XY)/sum(X^2).*

#### `D-Hab-07-05` - Omisión de la verificación del rango de soporte muestral en la predicción puntual
- **Tipo de Error:** `skipped_step` | **Severidad:** `medium` | **Origen:** `source`
- **Evidencia:** `Stats3 10-10.pdf` (pág. 9)
- **Creencia Correcta:** La predicción lineal es válida dentro o muy cerca del rango muestral observado [X_min, X_max]; extrapolar a valores lejanos asumiendo linealidad sin evaluar soporte genera errores de predicción severos.
- **Paso Omitido (Expert Blindness):** Verificar que el punto de predicción X_0 se encuentra dentro del rango de soporte muestral para asegurar la confiabilidad del pronóstico.
- **Detonante (Trigger):** Pronosticar Y para un valor de X muy distante de la media muestral bar(X).
- **Manifestación:** Pronósticos inverosímiles o fuera del dominio físico de la variable sin advertencia de extrapolación lejana.
- **Pauta de Remediación:** *Comprueba si X_0 pertenece al rango muestral [X_min, X_max]; la varianza del error de predicción crece cuadráticamente con (X_0 - bar(X))^2.*

#### `D-Hab-07-06` - Confusión entre predicción de la media condicional y predicción de un valor individual
- **Tipo de Error:** `conceptual_swap` | **Severidad:** `high` | **Origen:** `inferred`
- **Evidencia:** `Stats3 10-10.pdf` (pág. 9)
- **Creencia Errónea:** Creer que la varianza del error de predicción de un valor individual Y_0 es idéntica a la varianza de la media condicional E[Y|X_0].
- **Creencia Correcta:** La predicción de un individuo particular incluye la incertidumbre de la perturbación futura u_0 (sigma^2), sumando sigma^2 [1 + 1/n + (X_0 - bar(X))^2 / sum(x_i^2)], mientras que la media condicional solo tiene sigma^2 [1/n + (X_0 - bar(X))^2 / sum(x_i^2)].
- **Detonante (Trigger):** Construir intervalos de confianza para la predicción versus intervalos de predicción individual.
- **Manifestación:** Intervalos de predicción para un individuo artificialmente estrechos que subestiman el riesgo estocástico.
- **Pauta de Remediación:** *Distingue entre pronosticar la media condicional E[Y|X_0] y pronosticar un individuo Y_0 = E[Y|X_0] + u_0 (este último suma la varianza residual s^2).*

---
