# Cognitive Task Analysis (CTA): Econometria Violaciones Supuestos

- **Course ID:** `econometria_violaciones_supuestos`
- **Macro-Competency:** Dominio y aplicación analítica integral de Econometria Violaciones Supuestos
- **Structure:** 14 total competencies (0 Facts, 6 Concepts, 8 Skills) with 84 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Supuestos del Modelo Lineal General y Propiedad BLUE | Concept | Understand | Unidad 2: Supuestos del Modelo Lineal General y Propiedad BLUE | - | 6 |
| `C-02` | Naturaleza y Consecuencias de la Heterocedasticidad | Concept | Understand | Unidad 3: Naturaleza y Consecuencias de la Heterocedasticidad | C-01 | 6 |
| `C-03` | Detección de Heterocedasticidad mediante Pruebas Auxiliares | Skill | Analyze | Unidad 4: Detección de Heterocedasticidad mediante Pruebas Auxiliares | C-02 | 6 |
| `C-04` | Corrección de Heterocedasticidad con Errores Robustos y MCG | Skill | Apply | Unidad 7: Corrección de Heterocedasticidad con Errores Robustos y MCG | C-02, C-03 | 6 |
| `C-05` | Autocorrelación de Errores: Causas y Patrones Temporales | Concept | Understand | Unidad 8: Autocorrelación de Errores: Causas y Patrones Temporales | C-01 | 6 |
| `C-06` | Diagnóstico de Autocorrelación: Durbin-Watson y Breusch-Godfrey | Skill | Analyze | Unidad 9: Diagnóstico de Autocorrelación: Durbin-Watson y Breusch-Godfrey | C-05 | 6 |
| `C-07` | Evaluación de Inestabilidad Paramétrica mediante la Prueba de Chow | Skill | Apply | Unidad 11: Evaluación de Inestabilidad Paramétrica mediante la Prueba de Chow | C-01 | 6 |
| `C-08` | Modelado de Quiebres Estructurales con Variables Dummy e Interacciones | Skill | Apply | Unidad 12: Modelado de Quiebres Estructurales con Variables Dummy e Interacciones | C-07 | 6 |
| `C-09` | Multicolinealidad: Detección mediante Factor de Inflación de Varianza (VIF) | Concept | Analyze | Unidad 15: Multicolinealidad: Detección mediante Factor de Inflación de Varianza (VIF) | C-01 | 6 |
| `C-10` | Diagnóstico de Normalidad de Residuos mediante el Test de Jarque-Bera | Skill | Analyze | Unidad 17: Diagnóstico de Normalidad de Residuos mediante el Test de Jarque-Bera | C-01 | 6 |
| `C-11` | Endogeneidad por Variables Omitidas y Dirección del Sesgo | Concept | Understand | Unidad 18: Endogeneidad por Variables Omitidas y Dirección del Sesgo | C-01 | 6 |
| `C-12` | Error de Medición Clásico y Sesgo de Atenuación | Concept | Analyze | Unidad 19: Error de Medición Clásico y Sesgo de Atenuación | C-11 | 6 |
| `C-13` | Contrastes de Endogeneidad: Test de Hausman y Durbin-Wu-Hausman | Skill | Apply | Unidad 20: Contrastes de Endogeneidad: Test de Hausman y Durbin-Wu-Hausman | C-11, C-12 | 6 |
| `C-14` | Estimación por Variables Instrumentales y Mínimos Cuadrados en Dos Etapas (MC2E) | Skill | Apply | Unidad 22: Estimación por Variables Instrumentales y Mínimos Cuadrados en Dos Etapas (MC2E) | C-11, C-13 | 6 |

---

## Detailed Competency Specifications

### [C-01] Supuestos del Modelo Lineal General y Propiedad BLUE (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 2: Supuestos del Modelo Lineal General y Propiedad BLUE
- **Prerequisites:** None
- **Evidence Citations:** `Nota_academica_Econometria.pdf` (page 2)

#### Description & Cognitive Model
En el Modelo Lineal General $Y_i = \beta_0 + \sum_{j=1}^k \beta_j X_{ji} + u_i$, el estimador de Mínimos Cuadrados Ordinarios (MCO) es el Mejor Estimador Lineal Insesgado (BLUE por el teorema de Gauss-Markov) si se satisfacen: linealidad en parámetros, exogeneidad estricta $E(u_i|X) = 0$, homocedasticidad $Var(u_i|X) = \sigma^2$, no autocorrelación $Cov(u_i, u_j|X) = 0$ ($i \neq j$) y ausencia de multicolinealidad perfecta.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Confusión de Insesgadez con Eficiencia | conceptual_swap | high | $\text{Creer que un estimador insesgado tiene necesariamente la varianza mínima posible}$ | Recuerda que un estimador puede centrarse en el valor verdadero pero tener una dispersión innecesariamente grande si se viola la homocedasticidad. |
| `D-C01-02` | Creencia de que Homocedasticidad Garantiza Insesgadez | conceptual_swap | high | $\text{Pensar que la varianza constante } Var(u_i|X) = \sigma^2 \text{ asegura que } E(\hat{\beta}) = \beta$ | La homocedasticidad afecta la matriz de covarianzas y la eficiencia, pero no el valor esperado del estimador. |
| `D-C01-03` | Suposición de que MCO Minimiza la Varianza sin Restricción Lineal | conceptual_swap | high | $\text{Considerar que MCO tiene menor varianza que cualquier función no lineal de los datos}$ | El acrónimo BLUE incluye la L de Linear; la cota de mínima varianza aplica exclusivamente dentro de los estimadores lineales. |
| `D-C01-04` | Atribución de Inconsistencia a Cualquier Violación de Gauss-Markov | conceptual_swap | high | $\text{Asumir que toda violación de Gauss-Markov vuelve a los estimadores inconsistentes asintóticamente}$ | Solo la violación de la exogeneidad (endogeneidad) destruye la consistencia de MCO; las fallas en la varianza solo afectan la eficiencia y los errores estándar. |
| `D-C01-05` | Confusión entre Linealidad en Variables y Linealidad en Parámetros | conceptual_swap | high | $\text{Creer que un modelo con términos cuadráticos } X^2 \text{ o logaritmos viola los supuestos del MLG}$ | La regresión lineal clásica requiere que la derivada respecto a cada parámetro $\beta_j$ no dependa de ningún otro parámetro. |
| `D-C01-06` | Identificación Errónea de Exogeneidad Débil como Suficiente para BLUE | conceptual_swap | high | $\text{Pensar que la correlación contemporánea nula } Cov(X_i, u_i) = 0 \text{ basta para las propiedades en muestras pequeñas}$ | La condición de media condicional nula es más estricta que la correlación nula no condicionada y es indispensable para la insesgadez exacta. |

---

### [C-02] Naturaleza y Consecuencias de la Heterocedasticidad (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 3: Naturaleza y Consecuencias de la Heterocedasticidad
- **Prerequisites:** C-01
- **Evidence Citations:** `Nota_academica_Econometria.pdf` (page 3)

#### Description & Cognitive Model
La heterocedasticidad ocurre cuando la varianza condicional de las perturbaciones no es constante a través de las observaciones, $Var(u_i|X_i) = \sigma_i^2 \neq \sigma^2$. Es causada por omisión de variables, disparidades de escala, valores atípicos o cambios estructurales. Si se cumple $E(u_i|X_i) = 0$, los coeficientes MCO continúan siendo insesgados y consistentes, pero pierden la propiedad de varianza mínima (BLUE), y los errores estándar clásicos calculados con $\hat{\sigma}^2(X'X)^{-1}$ quedan sesgados e inválidos para contrastes $t$ y $F$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Creencia de que la Heterocedasticidad Genera Sesgo en Coeficientes MCO | conceptual_swap | high | $\text{Afirmar que } E(\hat{\beta}_{MCO}) \neq \beta \text{ debido a que } Var(u_i|X_i) \neq \sigma^2$ | Revisa la demostración algebraica de la insesgadez: la varianza de los errores no interviene en la esperanza de los coeficientes, solo en su matriz de covarianzas. |
| `D-C02-02` | Suposición de que Errores Estándar MCO Siempre Sobreestiman la Varianza Real | conceptual_swap | high | $\text{Creer que la fórmula clásica de MCO siempre infla los errores estándar}$ | La dirección del sesgo de la matriz de varianzas clásica depende de cómo se distribuyen las varianzas de los errores respecto a los regresores. |
| `D-C02-03` | Confusión entre Escala de Regresores y Violación de Linealidad | conceptual_swap | high | $\text{Interpretar que la mayor dispersión en empresas grandes implica que el modelo generador no es lineal}$ | Las diferencias de escala entre observaciones modifican la variabilidad del residuo, pero no necesariamente la forma lineal de la media condicional. |
| `D-C02-04` | Creencia de que Muestras Grandes Corrigen Automáticamente la Ineficiencia de MCO | conceptual_swap | high | $\text{Asumir que al aumentar } N \to \infty\text{, MCO recupera la eficiencia de varianza mínima}$ | El aumento muestral garantiza convergencia en probabilidad al valor verdadero, pero no elimina la pérdida de precisión relativa frente a un estimador ponderado. |
| `D-C02-05` | Asunción de que el R-cuadrado Refleja la Presencia de Heterocedasticidad | conceptual_swap | high | $\text{Interpretar un } R^2 \text{ bajo como evidencia concluyente de heterocedasticidad}$ | Un modelo puede tener un ajuste lineal excelente ($R^2$ alto) y presentar simultáneamente heterocedasticidad severa en sus colas. |
| `D-C02-06` | Ignorancia del Impacto de Heterocedasticidad sobre Intervalos de Confianza | conceptual_swap | high | $\text{Creer que los intervalos de confianza del 95\% mantienen su nivel nominal de cobertura bajo heterocedasticidad}$ | Si la varianza del estimador está mal estimada, los valores críticos de la distribución $t$ no producen la cobertura probabilística deseada. |

---

### [C-03] Detección de Heterocedasticidad mediante Pruebas Auxiliares (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 4: Detección de Heterocedasticidad mediante Pruebas Auxiliares
- **Prerequisites:** C-02
- **Evidence Citations:** `Nota_academica_Econometria.pdf` (page 4)

#### Description & Cognitive Model
Contrastar la presencia de heterocedasticidad evaluando hipótesis nula $H_0: \sigma_i^2 = \sigma^2$ (homocedasticidad) frente a $H_1: \sigma_i^2 \neq \sigma^2$ mediante pruebas auxiliares: Breusch-Pagan-Godfrey con regresión auxiliar $\hat{\varepsilon}_i^2 = \alpha_0 + \sum_{j=1}^k \alpha_j X_{ji} + v_i$ y estadístico $LM = \frac{SEC}{2(\hat{\sigma}^2)^2} \sim \chi^2(k)$; Test de Harvey con ajuste Gamma; Test de Glejser sobre $|\hat{\varepsilon}_i|$; y Test de White general $nR^2 \sim \chi^2(p)$ con términos cruzados y cuadráticos.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Omitir Cuadrados y Productos Cruzados en el Test de White | skipped_step | high | $\text{Estimar la regresión auxiliar de White únicamente con los regresores en nivel } X_j$ | La ventaja del test de White radica en capturar no linealidades en la varianza; sin los términos cuadráticos y cruzados se reduce a una prueba lineal restringida. |
| `D-C03-02` | Confusión de los Grados de Libertad de la Distribución Chi-Cuadrado | skipped_step | high | $\text{Comparar el estadístico } LM \text{ contra } \chi^2(N) \text{ o } \chi^2(N-k) \text{ en lugar del número de regresores auxiliares } p$ | Revisa la formulación de los contrastes de multiplicadores de Lagrange: los grados de libertad son las restricciones impuestas bajo la hipótesis nula. |
| `D-C03-03` | Uso Inadecuado de Residuos Sin Elevar al Cuadrado en Breusch-Pagan | conceptual_swap | high | $\text{Regresar los residuos en nivel } \hat{\varepsilon}_i \text{ sobre los regresores en la etapa auxiliar}$ | La condición de primer orden de MCO hace que los residuos brutos sean ortogonales a los regresores; para modelar la dispersión se requiere $\hat{\varepsilon}_i^2$. |
| `D-C03-04` | Inversión de la Regla de Decisión para el p-valor en H0 de Homocedasticidad | conceptual_swap | high | $\text{Rechazar la homocedasticidad cuando el } p\text{-valor es mayor al nivel de significancia } \alpha = 0.05$ | La hipótesis nula postula varianza constante; un $p$-valor alto indica que no hay suficiente evidencia para descartar la homocedasticidad. |
| `D-C03-05` | Interpretación Errónea del Estadístico LM de Glejser como Prueba de Autocorrelación | conceptual_swap | high | $\text{Asociar la regresión de } |\hat{\varepsilon}_i| \text{ con la correlación temporal entre residuos}$ | El test de Glejser es una prueba de heterocedasticidad basada en valores absolutos, no un contraste dinámico de perturbaciones temporales. |
| `D-C03-06` | Atribución Errónea de Mayor Potencia al Test de White con Exceso de Regresores | conceptual_swap | high | $\text{Creer que incluir docenas de productos cruzados siempre mejora la detección de heterocedasticidad}$ | A mayor cantidad de términos cruzados, el estadístico $\chi^2$ pierde grados de libertad efectivos y potencia para identificar patrones específicos. |

---

### [C-04] Corrección de Heterocedasticidad con Errores Robustos y MCG (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 7: Corrección de Heterocedasticidad con Errores Robustos y MCG
- **Prerequisites:** C-02, C-03
- **Evidence Citations:** `Nota_academica_Econometria.pdf` (page 7)

#### Description & Cognitive Model
Implementar estrategias de corrección frente a heterocedasticidad: estimación con matriz de covarianzas robusta de White/Huber-White ($Var(\hat{\beta}) = (X'X)^{-1} X' \hat{\Omega} X (X'X)^{-1}$ donde $\hat{\Omega} = \text{diag}(\hat{\varepsilon}_i^2)$), transformaciones de variables (logaritmos en niveles para estabilizar la dispersión) y Mínimos Cuadrados Generalizados / Ponderados (MCG/WLS) transformando las variables por $1/\sigma_i$ para restaurar la eficiencia BLUE.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Creencia de que Errores Robustos de White Modifican los Coeficientes Estimados | skipped_step | high | $\text{Esperar que la estimación robusta produzca coeficientes } \hat{\beta} \text{ numéricamente distintos a MCO}$ | Los errores estándar robustos modifican el denominador del estadístico $t$, pero el estimador puntual $\hat{\beta}$ sigue proviniendo de $(X'X)^{-1}X'Y$. |
| `D-C04-02` | Aplicación de MCO tras Ponderación Incorrecta en Mínimos Cuadrados Ponderados | skipped_step | high | $\text{Ponderar el modelo multiplicando por } \sigma_i \text{ en lugar de dividir por la desviación estándar del error}$ | Para lograr varianza unitaria $Var(u_i/\sigma_i) = 1$, el factor de escala debe ser el inverso de la desviación estándar condicional. |
| `D-C04-03` | Suposición de que Errores Robustos Corrigen el Sesgo de Endogeneidad | conceptual_swap | high | $\text{Aplicar errores estándar robustos pretendiendo subsanar la correlación entre regresores y perturbación}$ | Ninguna corrección de errores estándar puede eliminar el sesgo estructural en los coeficientes cuando los regresores son endógenos. |
| `D-C04-04` | Omisión de la Transformación Inversa al Predecir con Modelos Logarítmicos | conceptual_swap | high | $\text{Calcular el valor predicho del nivel como } \hat{Y} = \exp(\widehat{\ln Y}) \text{ sin corrección por varianza}$ | La exponencial de la media condicional del logaritmo no es igual a la media condicional de la variable original debido a la convexidad exponencial. |
| `D-C04-05` | Creencia de que MCG es Factible sin Conocer ni Estimar la Estructura de Omega | conceptual_swap | high | $\text{Aplicar Mínimos Cuadrados Generalizados exactos sin especificar la función de varianza } \sigma_i^2$ | Si la matriz de varianzas $\Omega$ contiene parámetros desconocidos, debe modelarse y estimarse consistentemente antes de transformar el sistema. |
| `D-C04-06` | Interpretación Equivocada del Aumento o Disminución del Error Estándar Robusto | conceptual_swap | high | $\text{Asumir que el error estándar robusto siempre es mayor que el error estándar clásico de MCO}$ | La fórmula robusta se ajusta a la dispersión empírica de los residuos ponderados por los regresores; puede corregir tanto sobreestimaciones como subestimaciones. |

---

### [C-05] Autocorrelación de Errores: Causas y Patrones Temporales (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 8: Autocorrelación de Errores: Causas y Patrones Temporales
- **Prerequisites:** C-01
- **Evidence Citations:** `Nota_academica_Econometria.pdf` (page 8)

#### Description & Cognitive Model
La autocorrelación ocurre cuando las perturbaciones aleatorias de diferentes observaciones presentan correlación temporal o espacial, $Cov(u_t, u_s|X) \neq 0$ para $t \neq s$. Es frecuente en series de tiempo por inercia o persistencia de variables económicas, omisión de variables relevantes con dinamismo temporal o especificaciones dinámicas incorrectas (falta de rezagos). Si los regresores son estrictamente exógenos, los estimadores MCO siguen siendo insesgados y consistentes, pero pierden eficiencia; además, los errores estándar clásicos suelen estar subestimados, inflando ficticiamente los estadísticos $t$ y $F$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Creencia de que la Autocorrelación Sesga los Coeficientes MCO | conceptual_swap | high | $\text{Sostener que } E(\hat{\beta}_{MCO}) \neq \beta \text{ debido a que } Cov(u_t, u_{t-1}) \neq 0$ | Al igual que en heterocedasticidad, la estructura de covarianza de los errores no afecta el valor esperado de los estimadores lineales bajo exogeneidad. |
| `D-C05-02` | Confusión entre Inercia en Variables y Autocorrelación en el Término de Error | conceptual_swap | high | $\text{Creer que si la variable dependiente } Y_t \text{ tiene tendencia, el modelo necesariamente presenta autocorrelación}$ | Una serie temporal puede tener inercia natural; si el modelo explicativo incorpora dicha tendencia adecuadamente, los residuos pueden ser ruido blanco incorrelacionado. |
| `D-C05-03` | Suposición de que Errores Estándar MCO Sobreestiman la Precisión en Presencia de Autocorrelación Positiva | conceptual_swap | high | $\text{Pensar que la autocorrelación positiva amplía los errores estándar de MCO, haciendo el test conservador}$ | Cuando los errores consecutivos covarían positivamente, el MCO clásico sobreestima la cantidad de información independiente en la muestra, produciendo una falsa sensación de precisión. |
| `D-C05-04` | Identificación Errónea de Autocorrelación como Causa de Inconsistencia Asintótica | conceptual_swap | high | $\text{Afirmar que con muestras grandes los coeficientes MCO convergen a un valor erróneo debido a la autocorrelación}$ | La consistencia se pierde únicamente si los errores correlacionados interactúan con variables endógenas o rezagos de $Y$; en modelos estrictamente exógenos, $\hat{\beta} \xrightarrow{p} \beta$. |
| `D-C05-05` | Creencia de que una Gráfica Residual Aleatoria Indica Autocorrelación Severa | conceptual_swap | high | $\text{Interpretar oscilaciones rápidas y cruces continuos del eje cero como evidencia de correlación serial positiva}$ | La autocorrelación positiva se visualiza mediante agrupamientos de residuos positivos seguidos de agrupamientos de residuos negativos. |
| `D-C05-06` | Confusión entre Autocorrelación de Primer Orden y Autocorrelación Serial General | conceptual_swap | high | $\text{Asumir que toda autocorrelación en series temporales se limita a una relación autorregresiva de orden 1 (AR1)}$ | Procesos económicos trimestrales o mensuales a menudo muestran correlación en múltiplos de rezagos específicos que no son capturados por análisis de orden uno. |

---

### [C-06] Diagnóstico de Autocorrelación: Durbin-Watson y Breusch-Godfrey (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 9: Diagnóstico de Autocorrelación: Durbin-Watson y Breusch-Godfrey
- **Prerequisites:** C-05
- **Evidence Citations:** `Nota_academica_Econometria.pdf` (page 9)

#### Description & Cognitive Model
Evaluar la correlación serial mediante pruebas estadísticas formales: el estadístico de Durbin-Watson $DW = \frac{\sum_{t=2}^n (u_t - u_{t-1})^2}{\sum_{t=1}^n u_t^2} \approx 2(1-\rho)$ con $DW \approx 2 \implies \rho \approx 0$ (ideal), $DW \approx 0 \implies \rho \approx 1$ (positiva) y $DW \approx 4 \implies \rho \approx -1$ (negativa), contrastado contra cotas críticas $d_L$ y $d_U$; y el test de Breusch-Godfrey de orden $p$ con regresión auxiliar $\hat{u}_t = \sum \beta_j X_{jt} + \sum_{s=1}^p \rho_s \hat{u}_{t-s} + \varepsilon_t$ y estadístico $LM = (n-p)R_{aux}^2 \sim \chi^2(p)$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Aplicación del Test de Durbin-Watson en Modelos con Regresores Autorregresivos Rezago | skipped_step | high | $\text{Utilizar el estadístico } DW \text{ en una ecuación que incluye la variable dependiente rezagada } Y_{t-1} \text{ como regresor}$ | Cuando $Y_{t-1}$ está en el modelo, el supuesto de independencia entre regresores y perturbaciones pasadas se incumple para $DW$, inutilizando sus tablas. |
| `D-C06-02` | Mala Interpretación de la Zona de Indecisión del Test de Durbin-Watson | skipped_step | high | $\text{Aceptar la hipótesis nula si } DW \text{ se ubica entre la cota inferior } d_L \text{ y la cota superior } d_U$ | Las cotas de Durbin-Watson contemplan zonas donde la distribución depende de la matriz $X$, requiriendo pruebas complementarias para tomar una decisión concluyente. |
| `D-C06-03` | Inversión del Signo de la Autocorrelación ante Valores de DW Cercanos a 0 y 4 | conceptual_swap | high | $\text{Interpretar } DW \approx 0 \text{ como evidencia de autocorrelación negativa y } DW \approx 4 \text{ como positiva}$ | Sustituye $\rho = 1$ en la fórmula aproximada $2(1-\rho)$ para verificar que valores cercanos a cero corresponden a fuerte persistencia positiva. |
| `D-C06-04` | Omisión de los Residuos Rezagados de Orden Superior en la Regresión Auxiliar de Breusch-Godfrey | conceptual_swap | high | $\text{Incluir únicamente el primer rezago } \hat{u}_{t-1} \text{ en Breusch-Godfrey cuando se sospecha autocorrelación estacional}$ | El test de Breusch-Godfrey permite probar hipótesis conjuntas sobre múltiples rezagos; debe seleccionarse el orden $p$ coherente con la periodicidad de los datos. |
| `D-C06-05` | Confusión entre el Número de Observaciones Efectivas (n-p) y Muestrales Totales n | conceptual_swap | high | $\text{Calcular el estadístico LM multiplicando el } R_{aux}^2 \text{ por el tamaño muestral total } n \text{ sin descontar los rezagos perdidos}$ | Al rezagar los residuos se pierden los primeros $p$ periodos muestrales; el tamaño efectivo de la muestra auxiliar se reduce a $n-p$. |
| `D-C06-06` | Asunción de que DW = 2 Descarta Autocorrelaciones Estacionales de Órdenes Mayores | conceptual_swap | high | $\text{Concluir ausencia total de dependencia temporal en datos trimestrales únicamente porque } DW = 2.01$ | El estadístico $DW$ no tiene potencia para detectar patrones de dependencia que operan a frecuencias superiores a un desfase. |

---

### [C-07] Evaluación de Inestabilidad Paramétrica mediante la Prueba de Chow (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 11: Evaluación de Inestabilidad Paramétrica mediante la Prueba de Chow
- **Prerequisites:** C-01
- **Evidence Citations:** `Nota_academica_Econometria.pdf` (page 11)

#### Description & Cognitive Model
Contrastar la estabilidad de los parámetros entre submuestras independientes (o antes y después de un quiebre conocido en series de tiempo, o entre grupos como género en corte transversal): partición $n = n_1 + n_2$, hipótesis nula $H_0: \beta^1 = \beta^2$ frente a $H_1: \beta^1 \neq \beta^2$. El estadístico de Chow se calcula mediante $F = \frac{(SSRC - SSRU)/g}{SSRU / df_u} \sim F(g, df_u)$, donde $SSRC$ es la suma de cuadrados de residuos del modelo restringido, $SSRU = SSR_1 + SSR_2$, $g = k$ es el número de restricciones y $df_u = (n_1 - k) + (n_2 - k) = n - 2k$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Resta Invertida de Sumas de Cuadrados de Residuos Restringida y No Restringida | skipped_step | high | $\text{Calcular el numerador de la prueba F como } (SSRU - SSRC)/g \text{ obteniendo un valor negativo}$ | La imposición de restricciones nunca reduce la suma de residuos al cuadrado; por ende, $SSRC$ es siempre el término mayor en la resta. |
| `D-C07-02` | Cálculo Erróneo de los Grados de Libertad del Modelo No Restringido | skipped_step | high | $\text{Usar } n - k \text{ como grados de libertad del denominador en lugar de } n - 2k \text{ (o } df_1 + df_2\text{)}$ | Cada submuestra consume $k$ grados de libertad independientes; el modelo combinado no restringido gasta el doble de parámetros. |
| `D-C07-03` | Asunción de que el Test de Chow Identifica la Fecha Exacta de Quiebre Desconocida | conceptual_swap | high | $\text{Utilizar la prueba de Chow estándar para encontrar endógenamente el punto de cambio estructural}$ | Probar múltiples puntos de quiebre con Chow estándar invalida la distribución $F$ clásica debido al problema de inferencia no estándar y búsqueda de datos. |
| `D-C07-04` | Creencia de que Varianzas Distintas entre Grupos No Afectan la Validez de la Prueba de Chow Clásica | conceptual_swap | high | $\text{Ejecutar el test de Chow asumiendo que es válido aun si } \sigma_1^2 \neq \sigma_2^2 \text{ entre los subperiodos}$ | Si la varianza del error cambia entre regímenes, se debe recurrir al test de Wald robusto o generalizaciones de Chow con varianzas dispares. |
| `D-C07-05` | Omisión de la Constante al Contar los Parámetros Restringidos g | conceptual_swap | high | $\text{Fijar } g = k - 1 \text{ suponiendo que la prueba de estabilidad solo aplica a las pendientes}$ | A menos que explícitamente solo se pruebe estabilidad de pendientes manteniendo el intercepto común, la prueba clásica evalúa el vector completo de $k$ coeficientes. |
| `D-C07-06` | Interpretación de Rechazo de H0 como Validación de Estabilidad | conceptual_swap | high | $\text{Concluir que los parámetros son estables cuando el } p\text{-valor del test de Chow es menor a 0.05}$ | La hipótesis nula representa la estabilidad ($\beta_1 = \beta_2$); un rechazo exige estimar modelos separados o introducir variables dummy de quiebre. |

---

### [C-08] Modelado de Quiebres Estructurales con Variables Dummy e Interacciones (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 12: Modelado de Quiebres Estructurales con Variables Dummy e Interacciones
- **Prerequisites:** C-07
- **Evidence Citations:** `Nota_academica_Econometria.pdf` (page 12)

#### Description & Cognitive Model
Especificar y estimar modelos que incorporan quiebres estructurales o heterogeneidad grupal mediante variables dicotómicas: quiebre en intercepto mediante $Y_t = \alpha_0 + \alpha_1 X_t + \gamma_1 D_t + \varepsilon_t$, y quiebre simultáneo en intercepto y pendiente mediante $Y_t = \alpha_0 + \gamma_1 D_t + \alpha_1 X_t + \gamma_2 (X_t \times D_t) + \varepsilon_t$. En este último, el efecto marginal en el periodo base ($D_t=0$) es $\frac{\partial Y}{\partial X} = \alpha_1$, mientras que en el periodo alternativo ($D_t=1$) es $\alpha_1 + \gamma_2$, evaluando la significancia del cambio de pendiente con el contraste individual sobre $\gamma_2$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Caer en la Trampa de las Variables Dummy por Inclusión de Todas las Categorías con Intercepto | skipped_step | high | $\text{Incluir una variable dummy para cada categoría o régimen simultáneamente con el intercepto general } \beta_0$ | Para evitar la trampa de la dummy, se debe omitir una categoría como grupo base de referencia o estimar el modelo sin intercepto general. |
| `D-C08-02` | Confundir Quiebre de Pendiente con Cambio de Intercepto | skipped_step | high | $\text{Incluir solo la variable dummy aditiva } \gamma_1 D_t \text{ pretendiendo modelar un cambio en la sensibilidad marginal ante } X_t$ | Una dummy simple traslada el nivel medio de la regresión hacia arriba o abajo; para cambiar la inclinación de la recta es indispensable la interacción. |
| `D-C08-03` | Omisión del Efecto Base al Calcular el Efecto Marginal del Segundo Periodo | conceptual_swap | high | $\text{Interpretar el coeficiente de interacción } \gamma_2 \text{ como la pendiente total del segundo grupo o periodo}$ | El parámetro de interacción no es el efecto autónomo del segundo grupo, sino el incremento o decremento relativo respecto al coeficiente de referencia. |
| `D-C08-04` | Interpretación Errónea del Coeficiente de Interacción como Coeficiente Autónomo | conceptual_swap | high | $\text{Evaluar la pendiente del grupo base utilizando el término de interacción } \gamma_2$ | En la submuestra de control o régimen base, la variable indicadora toma valor cero, neutralizando por completo el término multiplicativo. |
| `D-C08-05` | Asignación Inversa de la Codificación Binaria de la Variable Dummy | conceptual_swap | high | $\text{Interpretar el signo de } \gamma_1 \text{ asumiendo que el grupo base es el que toma el valor 1 en la dummy}$ | Verifica siempre la etiqueta de valor de la variable dicotómica: el grupo de comparación por omisión es aquel donde la variable toma el valor cero. |
| `D-C08-06` | Creencia de que el Test t sobre el Intercepto Dummy Evalúa el Cambio en la Pendiente | conceptual_swap | high | $\text{Usar el estadístico } t \text{ de } \gamma_1 \text{ para contrastar si la elasticidad o propensión marginal cambió tras la crisis}$ | Cada parámetro captura una dimensión geométrica distinta: la dummy sola prueba diferencias de nivel medio, mientras que la interacción prueba diferencias de inclinación. |

---

### [C-09] Multicolinealidad: Detección mediante Factor de Inflación de Varianza (VIF) (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 15: Multicolinealidad: Detección mediante Factor de Inflación de Varianza (VIF)
- **Prerequisites:** C-01
- **Evidence Citations:** `Nota_academica_Econometria.pdf` (page 15)

#### Description & Cognitive Model
La multicolinealidad es la alta correlación lineal entre dos o más variables explicativas en el modelo de regresión. No viola ningún supuesto de Gauss-Markov si no es perfecta: los estimadores MCO siguen siendo insesgados, consistentes y BLUE. No obstante, infla las varianzas y errores estándar de los coeficientes: $Var(\hat{\beta}_j) = \frac{\sigma^2}{\sum (X_{ji} - \bar{X}_j)^2} \times VIF_j$, donde el Factor de Inflación de Varianza es $VIF_j = \frac{1}{1 - R_j^2}$, siendo $R_j^2$ el coeficiente de determinación de la regresión de $X_j$ sobre las demás explicativas. Regla práctica: $VIF > 5$ genera preocupación y $VIF > 10$ indica multicolinealidad severa, produciendo estadísticos $t$ individuales insignificantes a pesar de un $R^2$ global elevado.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Creencia de que la Multicolinealidad Viola la Insesgadez de los Estimadores MCO | conceptual_swap | high | $\text{Sostener que } E(\hat{\beta}_j) \neq \beta_j \text{ debido a que dos variables explicativas están fuertemente correlacionadas}$ | La multicolinealidad es un problema muestral de deficiencia en la precisión de la información (alta covarianza), no una violación de exogeneidad. |
| `D-C09-02` | Afirmación de que Multicolinealidad Implica Inconsistencia Asintótica | conceptual_swap | high | $\text{Creer que en muestras infinitas los coeficientes no convergen a los verdaderos valores debido a multicolinealidad imperfecta}$ | Con más datos muestrales se aporta información adicional que reduce la dispersión de los estimadores, preservando plenamente la consistencia. |
| `D-C09-03` | Confusión entre Tolerancia (1 - Rj2) y Factor de Inflación de Varianza (VIF) | conceptual_swap | high | $\text{Interpretar un valor de } VIF = 0.1 \text{ como señal de multicolinealidad severa}$ | Recuerda que el VIF es el inverso de la tolerancia; a mayor correlación auxiliar, la tolerancia tiende a cero y el VIF se dispara hacia el infinito. |
| `D-C09-04` | Creencia de que Correlaciones Bivariadas Bajas Descartan Multicolinealidad | conceptual_swap | high | $\text{Examinar únicamente la matriz de correlaciones de Pearson por pares de variables para descartar multicolinealidad}$ | El análisis por pares es insuficiente en modelos múltiples; el cálculo del VIF a través de regresiones auxiliares es indispensable para detectar dependencias lineales conjuntas. |
| `D-C09-05` | Suposición de que Eliminar Variables Correlacionadas Nunca Induce Sesgo por Omisión | conceptual_swap | high | $\text{Eliminar automáticamente una variable con alto VIF sin considerar su relevancia económica teórica}$ | Existe un dilema técnico: tolerar mayor varianza en los estimadores o inducir sesgo de variable omitida; la teoría económica debe guiar la decisión de exclusión. |
| `D-C09-06` | Interpretación de un R2 Global Alto con Coeficientes No Significativos como Falla de Muestreo | conceptual_swap | high | $\text{Atribuir a un error de cálculo que el estadístico } F \text{ global sea altamente significativo pero todos los } t \text{ individuales no lo sean}$ | El conjunto de variables explica conjuntamente la variable dependiente de forma contundente, pero la correlación mutua impide aislar el impacto individual de cada una. |

---

### [C-10] Diagnóstico de Normalidad de Residuos mediante el Test de Jarque-Bera (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 17: Diagnóstico de Normalidad de Residuos mediante el Test de Jarque-Bera
- **Prerequisites:** C-01
- **Evidence Citations:** `Nota_academica_Econometria.pdf` (page 17)

#### Description & Cognitive Model
Evaluar el supuesto de normalidad en las perturbaciones del modelo econométrico mediante los momentos muestrales de asimetría $S$ y curtosis $K$, contrastando $H_0: u_i \sim \mathcal{N}(0, \sigma^2)$ frente a $H_1: u_i \text{ no normal}$. El estadístico de Jarque-Bera se define como $JB = \frac{T-k}{6}\left[S^2 + \frac{(K-3)^2}{4}\right] \sim \chi^2(2)$, donde bajo normalidad $S = 0$ y $K = 3$. Regla de decisión: para $\alpha = 0.05$ con valor crítico $\chi^2(0.05, 2) = 5.99$, se rechaza la normalidad si $JB \ge 5.99$, comprometiendo las pruebas exactas $t$ y $F$ en muestras pequeñas.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C10-01` | Uso de la Curtosis Total K en lugar del Exceso de Curtosis (K-3) en el Estadístico JB | skipped_step | high | $\text{Calcular el término de curtosis como } \frac{K^2}{4} \text{ en vez de } \frac{(K-3)^2}{4}$ | La distribución normal teórica tiene curtosis poblacional igual a 3; la fórmula estandariza el exceso de curtosis elevando al cuadrado su diferencia respecto a 3. |
| `D-C10-02` | Asignación Incorrecta de los Grados de Libertad de la Distribución Chi-Cuadrado | skipped_step | high | $\text{Comparar el estadístico } JB \text{ contra una } \chi^2(T-k) \text{ o } \chi^2(k) \text{ en lugar de } \chi^2(2)$ | Independientemente del número de regresores o datos, el contraste evalúa exactamente dos coeficientes de forma (asimetría y curtosis). |
| `D-C10-03` | Inversión de la Regla de Decisión para el Estadístico Jarque-Bera y el Valor Crítico 5.99 | conceptual_swap | high | $\text{Concluir que los residuos son normales cuando } JB \ge 5.99$ | Un estadístico grande indica que la asimetría o el exceso de curtosis están muy lejos de los valores de una normal teórica. |
| `D-C10-04` | Suposición de que la No Normalidad de Errores Invalida MCO en Grandes Muestras Asintóticas | conceptual_swap | high | $\text{Afirmar que si } JB \ge 5.99\text{, las pruebas } t \text{ y } F \text{ no pueden interpretarse bajo ninguna circunstancia}$ | El supuesto de normalidad en las perturbaciones es crucial para la validez de las distribuciones $t$ y $F$ en muestras finitas, pero la inferencia asintótica permanece válida en grandes muestras. |
| `D-C10-05` | Omisión del Ajuste por Grados de Libertad (T-k) en Muestras Finitas | conceptual_swap | high | $\text{Multiplicar los momentos por el tamaño muestral bruto } T \text{ en muestras pequeñas sin descontar los } k \text{ parámetros estimados}$ | Cuando los momentos se calculan a partir de residuos estimados y no de errores verdaderos, se debe considerar el número de regresores $k$ ajustados. |
| `D-C10-06` | Interpretación de Asimetría Negativa como Exceso de Curtosis Positivo | conceptual_swap | high | $\text{Confundir una distribución con cola izquierda pesada (asimetría } S < 0\text{) con una distribución leptocúrtica ( } K > 3\text{)}$ | Cada momento mide propiedades geométricas independientes: la asimetría refleja la dirección de la cola más larga, y la curtosis la concentración o grosor de ambas colas. |

---

### [C-11] Endogeneidad por Variables Omitidas y Dirección del Sesgo (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 18: Endogeneidad por Variables Omitidas y Dirección del Sesgo
- **Prerequisites:** C-01
- **Evidence Citations:** `Nota_academica_Econometria.pdf` (page 18)

#### Description & Cognitive Model
La endogeneidad surge cuando una o más variables explicativas se correlacionan con la perturbación, $E(X_i u_i) \neq 0$, provocando que el estimador MCO sea sesgado e inconsistente. En el caso de omisión de una variable relevante $w$ en el modelo $y = \alpha + \beta x + \gamma w + \varepsilon$, al estimar por MCO la ecuación corta $y = \alpha + \beta x + v$ (donde $v = \gamma w + \varepsilon$), el valor esperado del estimador es $E[\hat{\beta}_{MCO}] = \beta + \gamma \frac{Cov(x,w)}{Var(x)}$. La dirección del sesgo viene dada por $\text{sign}(\text{sesgo}) = \text{sign}(\gamma) \times \text{sign}(Cov(x,w))$: es positivo si ambos tienen igual signo y negativo si tienen signos opuestos.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C11-01` | Creencia de que el Sesgo por Variable Omitida Desaparece al Aumentar el Tamaño de Muestra | conceptual_swap | high | $\text{Afirmar que con } N \to \infty \text{ el estimador MCO converge al verdadero } \beta \text{ a pesar de omitir } w$ | El sesgo persiste intacto en el infinito muestral porque la correlación estructural entre el regresor y el error no se diluye con más observaciones. |
| `D-C11-02` | Error en la Determinación del Signo del Sesgo ante Factores de Signos Opuestos | conceptual_swap | high | $\text{Concluir que el sesgo es positivo cuando } \gamma < 0 \text{ y } Cov(x,w) > 0$ | Multiplica algebraicamente los signos: el signo del sesgo es estrictamente el producto del signo del impacto marginal $\gamma$ por el signo de la relación $\text{Cov}(x,w)$. |
| `D-C11-03` | Suposición de que Omitir una Variable Incorrelacionada con el Regresor Causa Sesgo | conceptual_swap | high | $\text{Creer que excluir una variable relevante } w \text{ siempre sesga } \hat{\beta} \text{ aun cuando } Cov(x,w) = 0$ | Para que exista sesgo en $\hat{\beta}$, la variable omitida debe cumplir dos condiciones simultáneas: afectar a $y$ ($\gamma \neq 0$) y estar correlacionada con $x$ ($\text{Cov}(x,w) \neq 0$). |
| `D-C11-04` | Confusión entre Sesgo de Coeficientes y Pérdida de Eficiencia en MCO | conceptual_swap | high | $\text{Identificar la omisión de variables simplemente como una falta de precisión que infla las varianzas}$ | El sesgo desplaza el centro de la distribución muestral lejos del parámetro poblacional verdadero; no puede solucionarse ajustando la dispersión. |
| `D-C11-05` | Creencia de que Incluir Controles Irrelevantes Elimina el Sesgo de Endogeneidad | conceptual_swap | high | $\text{Saturar el modelo con cualquier variable disponible para garantizar que no haya variables omitidas}$ | La inclusión de variables debe justificarse teóricamente; incorporar variables que están determinadas conjuntamente con el resultado puede crear nuevo sesgo. |
| `D-C11-06` | Asunción de que el Estimador MCO Sobrestima el Parámetro cuando gamma es Positivo y Covarianza es Negativa | conceptual_swap | high | $\text{Afirmar que si } \gamma > 0 \text{ y } Cov(x,w) < 0\text{, el valor estimado } \hat{\beta} \text{ es mayor que } \beta$ | Cuando el sesgo es negativo, el estimador MCO arroja un valor sistemáticamente menor que el parámetro poblacional real. |

---

### [C-12] Error de Medición Clásico y Sesgo de Atenuación (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 19: Error de Medición Clásico y Sesgo de Atenuación
- **Prerequisites:** C-11
- **Evidence Citations:** `Nota_academica_Econometria.pdf` (page 19)

#### Description & Cognitive Model
Cuando una variable explicativa continua verdadera $x^*$ no es directamente observable y se mide con error clásico $x = x^* + u$ (con $E(u)=0$, $u \perp x^*$ y $u \perp \varepsilon$), al estimar $y = \alpha + \beta x + (\varepsilon - \beta u)$, se genera correlación entre el regresor observado y el error efectivo: $Cov(x, \varepsilon - \beta u) = -\beta Var(u) \neq 0$. El valor esperado del estimador MCO es $E[\hat{\beta}] = \lambda \beta$, donde $\lambda = \frac{Var(x^*)}{Var(x^*) + Var(u)} \in (0, 1)$ es el factor de atenuación. Consecuencia: MCO subestima sistemáticamente la magnitud del efecto de $x^*$, sesgando el coeficiente hacia cero independientemente del signo de $\beta$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C12-01` | Creencia de que el Error de Medición en la Variable Explicativa Mantiene la Consistencia de MCO | conceptual_swap | high | $\text{Asumir que al aumentar la muestra } N \to \infty\text{, el ruido } u \text{ se cancela y } \hat{\beta} \xrightarrow{p} \beta$ | La varianza del error de medición permanece constante en la población; la proporción de varianza de ruido $\text{Var}(u)$ no disminuye con el tamaño muestral. |
| `D-C12-02` | Afirmación de que el Sesgo de Atenuación Puede Invertir el Signo del Parámetro Verdadero | conceptual_swap | high | $\text{Creer que el sesgo clásico de atenuación puede transformar un } \beta > 0 \text{ en una estimación negativa } E[\hat{\beta}] < 0$ | El factor $\lambda$ es un número estrictamente positivo; por ende, escala el parámetro achicando su valor absoluto, pero jamás cruza el cero. |
| `D-C12-03` | Confusión entre Error de Medición en el Regresor y Error en la Variable Dependiente | conceptual_swap | high | $\text{Creer que medir con error la variable } Y \text{ genera sesgo de atenuación en los coeficientes}$ | El sesgo de atenuación es exclusivo del error de medición en las variables explicativas; en la variable dependiente solo reduce la precisión del ajuste. |
| `D-C12-04` | Suposición de que el Factor de Atenuación lambda Aumenta al Crecer la Varianza del Error | conceptual_swap | high | $\text{Afirmar que a mayor ruido de medición } Var(u)\text{, mayor es el factor } \lambda$ | Revisa la fracción: el error de medición está en el denominador; mientras más ruidosa sea la variable, menor es la fracción de señal sobre ruido total. |
| `D-C12-05` | Creencia de que Muestras Infinitas Eliminan el Factor de Atenuación | conceptual_swap | high | $\text{Confundir el promedio muestral de los errores con la varianza poblacional del término de ruido}$ | El TLC asegura que el estimador tiene una distribución normal en torno a su límite probabilístico, pero ese límite es $\lambda \beta$, no $\beta$. |
| `D-C12-06` | Asunción de que un Error de Medición No Clásico Genera Estrictamente Atenuación | conceptual_swap | high | $\text{Generalizar el resultado } E[\hat{\beta}] = \lambda \beta \text{ a casos donde } u \text{ se correlaciona con } x^*$ | La atenuación hacia cero está matemáticamente condicionada a la ortogonalidad entre el error de medición y la variable latente verdadera. |

---

### [C-13] Contrastes de Endogeneidad: Test de Hausman y Durbin-Wu-Hausman (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 20: Contrastes de Endogeneidad: Test de Hausman y Durbin-Wu-Hausman
- **Prerequisites:** C-11, C-12
- **Evidence Citations:** `Nota_academica_Econometria.pdf` (page 20)

#### Description & Cognitive Model
Evaluar formalmente la exogeneidad de los regresores mediante el test de especificación de Hausman y la prueba de Durbin-Wu-Hausman (DWH). Hipótesis: $H_0: \text{regresores son exógenos (MCO es consistente y eficiente)}$ frente a $H_1: \text{regresores son endógenos (MCO es inconsistente; VI es consistente)}$. La prueba de Hausman compara el vector de coeficientes: $\chi^2 = (\hat{\beta}_{IV} - \hat{\beta}_{MCO})' [Var(\hat{\beta}_{IV}) - Var(\hat{\beta}_{MCO})]^{-1} (\hat{\beta}_{IV} - \hat{\beta}_{MCO}) \sim \chi^2(k^*)$. En la implementación operativa DWH, se estima la primera etapa del regresor potencialmente endógeno sobre instrumentos y controles, se extraen los residuos $\hat{v}$, y se evalúa su significancia al incluirlos como regresor en la ecuación estructural original.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C13-01` | Inversión del Orden de Estimadores en la Comparación del Test de Hausman | skipped_step | high | $\text{Ejecutar en software la comparación especificando el modelo MCO en primer lugar y el modelo VI en segundo lugar}$ | La matriz de diferencia de covarianzas se calcula como $V_{IV} - V_{MCO}$, la cual es semidefinida positiva solo cuando el estimador consistente y menos eficiente va primero. |
| `D-C13-02` | Omisión de la Inclusión de Residuos de Primera Etapa en la Ecuación Estructural DWH | skipped_step | high | $\text{Estimar la primera etapa pero incluir los valores ajustados } \hat{X} \text{ en lugar de los residuos } \hat{v} \text{ en la prueba DWH}$ | La hipótesis de exogeneidad equivale a probar si el coeficiente del residuo auxiliar $\hat{v}$ en la ecuación estructural es estadísticamente igual a cero. |
| `D-C13-03` | Interpretación del Rechazo de H0 en Hausman como Validación de Exogeneidad de MCO | conceptual_swap | high | $\text{Concluir que los regresores son exógenos cuando el } p\text{-valor del test de Hausman es } < 0.05$ | La hipótesis nula afirma que la diferencia no es sistemática (exogeneidad); al rechazarla se confirma que MCO está sesgado e inconsistente. |
| `D-C13-04` | Creencia de que el Test de Hausman Puede Ejecutarse sin un Instrumento Válido | conceptual_swap | high | $\text{Intentar contrastar endogeneidad mediante Hausman sin haber identificado instrumentos exógenos y relevantes previa estimación}$ | El test de Hausman no diagnostica si el instrumento es bueno; asume que el estimador IV es consistente para evaluar si MCO difiere de él. |
| `D-C13-05` | Confusión entre la Hipótesis Nula de Exogeneidad y la Prueba de Sobreidentificación | conceptual_swap | high | $\text{Interpretar el test de Hausman como una prueba de que los instrumentos son válidos y ortogonales al error}$ | Son pruebas con propósitos distintos: Hausman responde '¿es endógeno el regresor?', mientras que Sargan responde '¿son válidos los instrumentos sobrantes?'. |
| `D-C13-06` | Asunción de que una Matriz de Varianzas No Definida Positiva en Hausman Confirma Exogeneidad | conceptual_swap | high | $\text{Concluir que no hay endogeneidad si el software reporta que la diferencia de covarianzas no es definida positiva}$ | En muestras finitas la matriz $V_{IV} - V_{MCO}$ puede no ser positiva definida debido a errores de aproximación; en tal caso la prueba DWH en regresión directa es obligatoria. |

---

### [C-14] Estimación por Variables Instrumentales y Mínimos Cuadrados en Dos Etapas (MC2E) (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 22: Estimación por Variables Instrumentales y Mínimos Cuadrados en Dos Etapas (MC2E)
- **Prerequisites:** C-11, C-13
- **Evidence Citations:** `Nota_academica_Econometria.pdf` (page 22)

#### Description & Cognitive Model
Implementar el método de Variables Instrumentales (VI) y Mínimos Cuadrados en Dos Etapas (MC2E / 2SLS) para corregir endogeneidad. Condiciones para un instrumento válido $Z$: relevancia ($Cov(Z, X) \neq 0$, comprobado con estadístico $F > 10$ en primera etapa) y exogeneidad/exclusión ($Cov(Z, \varepsilon) = 0$). Procedimiento de dos etapas: 1) Estimar la regresión del regresor endógeno sobre todos los instrumentos excluidos y controles exógenos para obtener valores predichos $\hat{X}$; 2) Estimar la regresión de $Y$ sobre $\hat{X}$ y controles exógenos. Corrección obligatoria de la matriz de covarianzas en segunda etapa utilizando los residuos estructurales calculados con los datos originales $X$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C14-01` | Uso Directo de Residuos de la Segunda Etapa Manual sin Corregir la Varianza del Error | skipped_step | high | $\text{Estimar MC2E ejecutando manualmente dos regresiones MCO secuenciales y utilizar los errores estándar de la segunda regresión}$ | El software especializado (como ivregress) reemplaza automáticamente $\hat{X}$ por los datos originales $X$ al evaluar los residuos finales para calcular $\sigma^2$ correctamente. |
| `D-C14-02` | Omisión de Variables Exógenas Incluidas en la Ecuación de Primera Etapa | skipped_step | high | $\text{Regresar la variable endógena } X \text{ únicamente sobre el instrumento excluido } Z \text{ sin incluir los controles exógenos } W$ | Si omites los controles exógenos en la primera etapa, el valor predicho $\hat{X}$ no será ortogonal a la perturbación de la segunda etapa, reintroduciendo endogeneidad. |
| `D-C14-03` | Uso de Instrumentos Débiles sin Evaluar el Estadístico F de Primera Etapa | conceptual_swap | high | $\text{Utilizar un instrumento asumiendo validez solo porque teóricamente tiene sentido, sin verificar que } F > 10$ | La regla empírica de Staiger y Stock exige que el estadístico $F$ de significancia conjunta de los instrumentos excluidos en la primera etapa supere 10 para descartar sesgo severo por instrumentos débiles. |
| `D-C14-04` | Creencia de que los Estimadores MC2E son Más Eficientes que MCO cuando los Regresores son Exógenos | conceptual_swap | high | $\text{Preferir siempre la estimación MC2E sobre MCO aun cuando los regresores sean perfectamente exógenos}$ | El estimador IV debe utilizarse únicamente cuando hay endogeneidad demostrada; usarlo innecesariamente sacrifica gran precisión estadística. |
| `D-C14-05` | Asunción de que la Condición de Exogeneidad del Instrumento Puede Verificarse Estadísticamente en Modelos Justo-Identificados | conceptual_swap | high | $\text{Pretender contrastar formalmente con una prueba de hipótesis que } Cov(Z, \varepsilon) = 0 \text{ cuando hay exactamente un instrumento para un regresor endógeno}$ | La prueba de sobreidentificación de Sargan requiere que haya más instrumentos que regresores endógenos ($m > k$); con un solo instrumento, el modelo está saturado y el residuo es exactamente ortogonal por construcción. |
| `D-C14-06` | Interpretación Errónea de la Ecuación de Primera Etapa como la Ecuación Estructural de Interés | conceptual_swap | high | $\text{Interpretar el coeficiente del instrumento en la primera etapa como el efecto causal sobre la variable dependiente final } Y$ | La primera etapa es un paso intermedio para descomponer la variación de $X$ en una componente exógena y una endógena; los parámetros de interés residen en la ecuación estructural corregida. |

---
