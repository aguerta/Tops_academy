# Cognitive Task Analysis: Estadística III - Modelo de Regresión Lineal

## Resumen Ejecutivo del Curso
- **Course ID:** `estadistica3_regresion`
- **Título:** Estadística III: Modelo de Regresión Lineal
- **Macro-Competencia:** Formulación, estimación matricial MCO, análisis geométrico de proyección, descomposición ANOVA e inferencia clásica en el modelo de regresión lineal general.
- **Total de Competencias:** 6 (1 Hecho [H], 2 Conceptos [C], 3 Habilidades Procedimentales [Hab])
- **Total de Distractores Fundidos:** 36 (6 distractores por competencia con 100% de diagnósticos psicométricos)

---

## 1. Taxonomía de Competencias y Triada del Conocimiento

| ID | Tipo | Nombre | Nivel Bloom | Requisitos Previos | Total Distractores |
|---|---|---|---|---|---|
| **H-01** | Hecho | Supuestos Clásicos y Fundamentos Matriciales del MRLC | Remember | Ninguno | 6 |
| **C-01** | Concepto | Geometría y Álgebra de Proyección: Matrices P, M y M0 | Understand | H-01 | 6 |
| **C-02** | Concepto | Formas Funcionales, Efectos Marginales y Elasticidades | Understand | H-01 | 6 |
| **Hab-01** | Habilidad | Estimación MCO Matricial, Ajuste y Residuos | Apply | H-01, C-01 | 6 |
| **Hab-02** | Habilidad | Descomposición ANOVA, Coeficiente de Determinación ($R^2$) y Varianza Residual ($s^2$) | Apply | C-01, Hab-01 | 6 |
| **Hab-03** | Habilidad | Inferencia Estadística: Contrastes t-Student, F-Fisher y P-Valores | Analyze | Hab-01, Hab-02 | 6 |

---

## 2. Descripción Detallada de Competencias

### [H-01] Supuestos Clásicos y Fundamentos Matriciales del MRLC
- **Descripción:** Identificación de los supuestos clásicos de Gauss-Markov ($E(u|X)=0$, $\operatorname{Var}(u|X)=\sigma^2 I_n$, $\operatorname{rango}(X)=k$), dimensiones conformables ($Y \in \mathbb{R}^{n \times 1}$, $X \in \mathbb{R}^{n \times k}$, $\beta \in \mathbb{R}^{k \times 1}$) y condición MELI/BLUE.
- **Evidencia:** `EST3_LEC01_26_2.pdf` p. 9, `EST3_LEC03_26_2.pdf` p. 4, `EST3_LEC03_26_2.pdf` p. 5.

### [C-01] Geometría y Álgebra de Proyección: Matrices P, M y M0
- **Descripción:** Propiedades de las matrices de proyección ortogonal: Hat Matrix $P = X(X'X)^{-1}X'$ (proyecta $Y$ sobre $\operatorname{col}(X)$, $\operatorname{tr}(P)=k$, simétrica e idempotente), Matriz Aniquiladora $M = I_n - P$ ($MX = 0$, $\operatorname{tr}(M)=n-k$) y Matriz de Centrado $M_0 = I_n - \frac{1}{n}\iota\iota'$ ($\operatorname{tr}(M_0)=n-1$).
- **Evidencia:** `EST3_LEC03_26_2.pdf` p. 17, 18, 20.

### [C-02] Formas Funcionales, Efectos Marginales y Elasticidades
- **Descripción:** Distinción analítica entre modelos Lineal, Doble-Log (elasticidad constante $\beta_2$), Log-Lin (semielasticidad $100\beta_2$), Lin-Log (cambio absoluto $\beta_2/100$), Cuadrático ($X^* = -\beta_1/(2\beta_2)$) y Recíproco (asíntota de saturación $\beta_1$).
- **Evidencia:** `EST3_LEC02_26_2.pdf` p. 20, 21, 22, 23, 25.

### [Hab-01] Estimación MCO Matricial, Ajuste y Residuos
- **Descripción:** Cálculo procedimental de la matriz de momentos $X'X$, su determinante e inversa $(X'X)^{-1}$, el vector de producto cruzado $X'Y$, el estimador $\hat{\beta} = (X'X)^{-1}X'Y$, el vector de predicción $\hat{Y} = X\hat{\beta}$ y los residuos muestrales $e = Y - \hat{Y}$.
- **Evidencia:** `EST3_LEC01_26_2.pdf` p. 7, `EST3_LEC03_26_2.pdf` p. 10, `Stats3 10-10.pdf` p. 1.

### [Hab-02] Descomposición ANOVA, Coeficiente de Determinación ($R^2$) y Varianza Residual ($s^2$)
- **Descripción:** Cálculo de las sumas de cuadrados matriciales: $STC = Y'M_0 Y$, $SRC = e'e$, $SEC = \hat{Y}'M_0 \hat{Y}$, verificación de la identidad $STC = SEC + SRC$, determinación de $R^2 = 1 - \frac{SRC}{STC}$ y estimación de la varianza del error $s^2 = \frac{e'e}{n-k}$.
- **Evidencia:** `EST3_LEC03_26_2.pdf` p. 21, `Stats3 10-10.pdf` p. 2, `EST3_LEC01_26_2.pdf` p. 8.

### [Hab-03] Inferencia Estadística: Contrastes t-Student, F-Fisher y P-Valores
- **Descripción:** Cálculo de errores estándar de los coeficientes $SE(\hat{\beta}_j) = \sqrt{s^2 c_{jj}}$, estadístico individual $t_{\mathrm{calc}} = \frac{\hat{\beta}_j - \beta_{j0}}{SE(\hat{\beta}_j)}$, estadístico de significancia global $F = \frac{SEC/(k-1)}{SRC/(n-k)} = \frac{R^2/(k-1)}{(1-R^2)/(n-k)}$, comparación con valores críticos y reglas de decisión basadas en p-valores.
- **Evidencia:** `EST3_LEC01_26_2.pdf` p. 11, 12, `EST3_LEC03_26_2.pdf` p. 23, 25, 27.
