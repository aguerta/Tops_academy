# Reporte de Auditoría de Calidad Técnica, Psicométrica y Pedagógica (QM / OSCQR / Path-to-Mastery v2.0)

> [!WARNING]
> **CURSO RETIRADO DE LA PLATAFORMA**: Este curso fue eliminado de la plataforma interactiva el **2026-11-18 18:51:17**. Este informe de auditoría se conserva exclusivamente como registro histórico y pedagógico ('legacy').

**Estado en Plataforma:** ELIMINADO  
**Fecha de Eliminación:** 2026-11-18 18:51:17  
- **Curso ID:** `estadistica_3_s9_vmapreduce_vlean43_v6`
- **Título:** Estadística 3 — Propiedades en Muestras Finitas y Teoría Asintótica (`vmapreduce_vlean43_v6`)
- **Total de Competencias:** 29 (1 Hecho, 18 Conceptos, 10 Habilidades)
- **Total de Reactivos:** 680 (`MC7`: 305 [44.85%], `FIB`: 216 [31.76%], `MS`: 159 [23.38%])
- **Calificación Determinista Precalculada (Linter):** `19.48 / 20.0` (*PLATINUM MASTERY*)
- **Calificación Final Auditada (Post-Verificación Semántica):** **`15.60 / 20.0`**
- **Tier de Certificación QM-OSCQR:** **ACEPTABLE (14.0 - 16.9 pts)** — *Base estructural y de evocación sólida, pero con defectos semánticos, algebraicos y diagnósticos que requieren remediación antes de certificar como Platinum*
- **Mastery Path Readiness Index (MPRI):** **`79.00 / 100.0`** (*SILVER MASTERY PATH*)
- **Risk Score de Telemetría:** `33.31`

---

> [!IMPORTANT]
> **Divergencia Crítica entre Linter Estático (`19.48/20`) y Auditoría Semántica (`15.60/20`):**
> Aunque el curso aprueba limpiamente los linters sintácticos de primera generación (logrando 100% de calibración ZPD tri-banda, 55.15% de evocación activa/discriminación con `FIB`+`MS`, 0 residuos f-string reales y un grafo DAG conexo sin ciclos), el **Loop de Verificación Semántica** descubrió cinco patologías de fondo invisibles al conteo superficial:
> 1. **Bug algebraico por concatenación de strings en pistas socráticas de `C-29`** (`Q-C29-631` y `Q-C29-632`), donde la derivada de $7x^2+10x$ se imprime como $g'(x)=27x+10$ y la de $3x^2+6x$ como $g'(x)=23x+6$ por escribir `2{a}x` en vez de `{2*a}x`.
> 2. **Desconexión diagnóstica masiva entre la fórmula numérica de los distractores y su `error_rationale`** en al menos 12 competencias (`C-04`, `C-06`, `C-07`, `C-08`, `C-10`, `C-23`, `C-25`, `C-26`, `C-27`, `C-28`, `C-29`, `Hab-03`), reciclando explicaciones teóricas del `cta.json` sobre números generados mediante operaciones aritméticas inconexas.
> 3. **Cota de probabilidad superior a $1.0$ marcada como respuesta correcta** en `Q-C02-082` (`$1.6056$`, con distractor complementario negativo `$-0.6056$`) y **colapso numérico por underflow exponencial** en `Q-Hab03-121` ($F_{X_{(1)}}(0.68) = 1 - e^{-32.64} = 1.0000$ y supervivencia $0.0000$).
> 4. **Contaminación de enunciados por inyección artificial de parámetros basura (*Parameter Stuffing*)** en `C-08`, `C-10` y `C-22` (ej. inyectar `(no r=1/9)`, `cov=15` en una muestra declarada i.i.d., o `(entorno 5, índice 16)` en una definición teórica) únicamente para alimentar variables de los distractores.
> 5. **Falsos positivos léxicos masivos en `uninterpolated_math_variable_linter` (`228` alertas)**: Se verificó que el 100% de las 228 alertas de `{Y}`, `{p}`, `{d}`, `{Var}`, `{F}`, `{X}`, `{u}` y `{n_1}` son **falsos positivos del linter** sobre macros LaTeX válidas (`\bar{Y}`, `\hat{p}`, `\xrightarrow{p}`, `\xrightarrow{d}`, `\text{Var}`, `\mathcal{F}`, `_{n_1}`).

---

## 1. Diagnóstico Forense de Telemetría y Alertas (`risk_score = 33.31`)

| Métrica / Linter en `audit_telemetry` | Valor Reportado | Veredicto Forense del Loop Semántico |
| :--- | :---: | :--- |
| `uninterpolated_math_items_count` | **228 ítems** | **100% FALSO POSITIVO LÉXICO.** El linter captura `{Y}` en `\bar{Y}`, `{p}` en `\xrightarrow{p}` y `\hat{p}`, `{d}` en `\xrightarrow{d}`, `{Var}` en `\text{Var}`, `{F}` en `\mathcal{F}` y `{n_1}` en `_{n_1}`. Cero variables de plantilla de Python sin interpolar (`fstring_placeholders_count = 0`, `template_variable_residue_count = 0`). |
| `generic_misconception_count` | **216 ítems** | **VERDADERO POSITIVO.** Coincide con los 216 ítems `fill_in_the_blank` y el reciclaje estático de `misconception_warning` por competencia. Además, varios `misconception_warning` contienen valores estáticos de otros ejemplos (ej. `Q-Hab12-421` cita $E[X^2]=(1^2+3^2)/2=5$ cuando $X \in \{14, 62\}$; `Q-Hab06-281` cita un estimador inexistente $M_B$). |
| `rationale_uniqueness_pct` | **13.5% (290/2148)** | **VERDADERO POSITIVO ESTRUCTURAL.** Cada competencia reutiliza un molde fijo de 6 justificaciones (`D-<Comp>-01` a `06`). Peor aún, en 12+ competencias el texto del `error_rationale` no describe el cálculo aritmético con el que se generó el número del distractor. |
| `domain_impossible_items_count` | **21 ítems** (`11` neg., `10` prob $>1$) | **MIXTO (16 Verdaderos Positivos + 5 Falsos Positivos de `C-11`, más casos omitidos por el linter).** En `C-11` (`Q-C11-372`, etc.) el linter confunde $\text{Var}(X)=38.00$ con una probabilidad porque el enunciado contiene $P(X=x)$. Pero en `C-01`, `Hab-01`, `H-01` y `C-11` sí existen varianzas/ECM negativos (`$-32$`, `$-48.61$`, `$-158.00$`) y probabilidades `$-5\%$` o `$131\%$`. Además, el linter no detectó que en **`Q-C02-082` la clave correcta es `$1.6056 > 1$`** para una cota de probabilidad. |
| `biased_ms_items_count` | **59 / 159 (37.11%)** | **VERDADERO POSITIVO PSICOMÉTRICO.** Más de un tercio de los reactivos `multiple_select` presentan opciones correctas significativamente más largas ($\ge 1.35\times$) que los distractores, permitiendo estrategias *test-wise*. |
| `stage5_judge_audit` | **120 / 120 (100%)** | Acuerdo nominal del 100% en la muestra juzgada, pero el juez ciego validó la aritmética cruda ($17^2/(45\cdot 4)=1.6056$) sin objetar la violación del axioma de probabilidad ($\mathbb{P} \le 1$) ni auditar las pistas socráticas o los `error_rationale`. |

---

## 2. Evaluación por Dimensiones (Rúbrica Normativa sobre 20.0 Puntos)

| Dimensión | Puntaje Determinista | Puntaje Auditado | Máximo | Estado |
| :--- | :---: | :---: | :---: | :---: |
| **D1. Arquitectura Curricular, Topología DAG y Calibración ZPD** | 4.00 | **3.80** | 4.00 | Excelente con observación menor |
| **D2. Calidad Psicométrica, Modalidad de Evocación y Anti-Gaming** | 5.00 | **3.50** | 5.00 | Aceptable con brechas psicométricas |
| **D3. Andamiaje Socrático Progresivo y Remediación Diagnóstica** | 4.48 | **3.10** | 5.00 | Aceptable con desconexión diagnóstica |
| **D4. Alineación Instruccional, Taxonomía de Bloom y Pureza de Dominio** | 4.00 | **3.30** | 4.00 | Aceptable con *parameter stuffing* |
| **D5. Accesibilidad, Ergonomía Cognitiva en UI y Sintaxis KaTeX** | 2.00 | **1.90** | 2.00 | Excelente |
| **Subtotal / Penalizaciones Duras / Total Final** | **19.48** | **15.60** (`-0.0` pen.) | **20.00** | **ACEPTABLE (14.0 - 16.9)** |

---

### Dimensión 1: Arquitectura Curricular, Topología DAG y Calibración ZPD — **3.80 / 4.0 pts**

- **Fortalezas verificadas:**
  - **Topología DAG limpia:** 29 micro-competencias conectadas en una única componente conexa (`connected_components_count = 1`), libre de ciclos (`has_cycle = false`), con profundidad máxima 7, cero aristas invertidas (`inverted_prerequisite_edges_count = 0`) y cero habilidades huérfanas de prerrequisitos.
  - **Calibración ZPD Tri-Banda al 100%:** Las 29/29 competencias cuentan con reactivos distribuidos en las tres bandas de dificultad (`easy = 167`, `medium = 205`, `hard = 308`), habilitando plenamente `calibrateByMasteryDifficulty` en el motor adaptativo de Top's Academy.
  - **Tamaño de banco robusto:** Todas las competencias tienen entre 20 y 30 reactivos (680 en total).
- **Deficiencias detectadas (`-0.20 pts`):**
  - **Inconsistencia taxonómica en `Hab-04` ("Desigualdad de Chebyshev"):** Pese a tener identificador de habilidad (`Hab-04`) y evaluar cálculo de cotas de probabilidad, fue codificada con `"category": "Concept"` y dotada de 20 reactivos en lugar de los 30 exigidos para las habilidades prácticas.
  - **Anclaje tardío de `H-01` ("Axiomas de Probabilidad de Kolmogorov"):** Aparece posicionado en el índice 14 como dependiente de `C-01` ("Sesgo, Eficiencia y ECM"), cuando ontológicamente es la raíz axiomática de `C-09`, `C-10` y `C-11`.

---

### Dimensión 2: Calidad Psicométrica, Modalidad de Evocación y Anti-Gaming — **3.50 / 5.0 pts**

- **Fortalezas verificadas:**
  - **Excelente balance multimodal:** Supera el monocultivo de opción múltiple integrando `44.85%` `multiple_choice_7_options` (305), `31.76%` `fill_in_the_blank` (216) con contrato de redondeo explícito (`fib_uncontracted_rounding_count = 0`) y `23.38%` `multiple_select` (159), alcanzando **55.15% de evocación activa o discriminación condicional**.
  - **Alta entropía de claves:** Cero competencias vulnerables a memorización visual (`memorizable_competencies_count = 0`) y cero distractores generados por multiplicadores mágicos (`magic_multiplier_distractor_items_count = 0`).
- **Hallazgos críticos y deducciones (`-1.50 pts`):**
  1. **Clave correcta con probabilidad $> 1.0$ y colapso numérico exponencial (`-0.60 pts`):**
     - En **`Q-C02-082`**, el enunciado pide: *"Para margen $\varepsilon=2$, $n=45$ y $\sigma=17$, determine la cota de Chebyshev en probabilidad"*. La opción marcada como **correcta (`opt_e`)** es **`$1.6056$`** ($17^2 / (45 \cdot 2^2) = 289/180$), y el distractor `opt_g` es **`$-0.6056$`** ($1 - 1.6056$). Esto contradice frontalmente lo que el propio curso penaliza en `Q-Hab11-391` (`D-Hab11-03`: *"Reporta $(19/11)^2 > 1$ como cota superior sin acotar por axioma de probabilidad"*).
     - En **`Q-Hab03-121`**, para $X_i \sim \text{Exp}(8)$, $n=6$ y $t=0.68$, el producto $n\theta t = 32.64$ produce $e^{-32.64} = 6.68 \times 10^{-15}$, haciendo que la clave correcta de la FDA colapse a **`$1.0000$`** (`opt_f`) y el distractor de supervivencia colapse a **`$0.0000$`** (`opt_a`). Además, tres distractores (`opt_b: $0.0009$`, `opt_e: $0.0208$`, `opt_g: $0.0026$`) insertan valores del ECM, la media $1/(n\theta)$ y la varianza en una pregunta que pide una probabilidad acumulada.
  2. **Distractores imposibles por dominio que regalan descarte trivial (`-0.50 pts`):**
     - En `C-01` (`Q-C01-003`), `Hab-01` (`Q-Hab01-022` a `025`, `035`, `046` a `050`) y `C-11` (`Q-C11-371`, `Q-C11-372`), se incluyen distractores negativos (`$-32$`, `$-48.61$`, `$-158.00$`) al pedir $\text{ECM}$ o $\text{Var}(X)$.
     - En `H-01` (`Q-H01-311`, `Q-H01-312`), al pedir $P(A \cup B)$ en porcentaje, se incluyen opciones como **`$-5\%$`**, **`$-6\%$`**, **`$131\%$`** y **`$119\%$`**.
     - En `Q-C02-081`, `Q-C02-082`, `Q-Hab04-171`, `Q-Hab04-172`, `Q-Hab11-391` y `Q-Hab11-392`, entre 2 y 3 distractores por pregunta superan $1.0$ (ej. `$40.5568$`, `$6.3684$`, `$2.9835$` en `Q-Hab11-391`), permitiendo descartar casi la mitad de las opciones sin calcular nada.
  3. **Sesgo de longitud en `multiple_select` (`37.11%`) y delación por parámetros artificiales (`-0.40 pts`):**
     - 59 de los 159 reactivos `multiple_select` (`Q-C01-017` a `020`, `Q-Hab01-036` a `040`, `Q-C04-166` a `170`, `Q-C08-246`, etc.) tienen opciones verdaderas sistemáticamente más extensas que las falsas.

---

### Dimensión 3: Andamiaje Socrático Progresivo y Remediación Diagnóstica — **3.10 / 5.0 pts**

- **Fortalezas verificadas:**
  - El 100% de los reactivos (680/680) posee 3 pistas progresivas concisas, libres del cliché Mad-Libs (`boilerplate_hints_items_count = 0`) y sin envenenamiento anti-socrático (`poisoned_hints_items_count = 0`), además de soluciones paso a paso (`missing_solutions_count = 0`).
- **Hallazgos críticos y deducciones (`-1.90 pts`):**
  1. **Desconexión Diagnóstica Severa entre Distractor y `error_rationale` en `FeedbackToast` (`-1.10 pts`):**
     - Además de una unicidad global baja (`13.5%`, 290/2148), en al menos 12 competencias el texto explicativo del `error_rationale` proviene de afirmaciones teóricas del `cta.json` que **no corresponden en absoluto con la operación aritmética usada para fabricar el número del distractor**:
       - **`Q-C04-151` (Markov):** Pide acotar $\mathbb{P}(Y \ge 72) \le 28/72 = 0.3889$ dado $Y \ge 0, \mathbb{E}[Y]=28, \operatorname{Var}(Y)=10$.
         - `opt_a` (`$0.3415 = 28/(72+10)$`) muestra al alumno: *"Permite dividir $\mathbb{E}[Y]=28$ entre $\delta \le 0$, violando la condición $\delta > 0$"* (falso: $\delta=72 > 0$ y la cifra se obtuvo sumando la varianza al denominador).
         - `opt_e` (`$0.7200 = 72/100$`) muestra: *"Aplica la cota $28/72$ sin verificar que $Y \ge 0$ casi seguramente en todo el soporte"* (falso: aplicar $28/72$ da $0.3889$, no $0.7200$, y el enunciado ya garantiza $Y \ge 0$).
       - **`Q-C06-191` (Jensen):** Pide $\mathbb{E}[X^2]$ con $\mathbb{E}[X]=25, \operatorname{Var}(X)=27$ (clave `$652$`).
         - `opt_c` (`$2704 = (25+27)^2$`) dice: *"Afirma que $S_n = \sqrt{S_n^2}$ es insesgado pese a la concavidad de la raíz y varianza $27$"* (el problema ni siquiera menciona $S_n$).
         - `opt_d` (`$754$`) dice: *"Aplica Jensen a $1/X$ sin exigir soporte en intervalo abierto"* y `opt_g` (`$675 = 25 \times 27$`) dice: *"Descarta Jensen en $g(x)=|x|$ por el vértice en $0$"*.
       - **`Q-C07-211` (Cauchy-Schwarz):** Pide $\sqrt{289 \cdot 100} = 170$. El distractor `opt_b` (`$389 = 289+100$`) dice: *"Exige discriminante $\Delta \ge 0$ para $P(t) \ge 0$"*, y `opt_d` (`$189 = 289-100$`) dice: *"Asocia la igualdad con independencia en vez de linealidad"*.
       - **`Q-C25-491` (LGN):** Pide el límite de $4\bar{Y}_n + 13$ con $\mu=10, \sigma^2=44$ (clave `$53$`). El distractor `opt_d` (`$84$`) dice: *"Exige normalidad $Y_i \sim N(\mu, \sigma^2)$ aunque basta $\mu=10$ finita y $\sigma^2=44$"* (¿cómo exigir normalidad produce el número $84$?).
       - **`Q-C26-511` (TCL):** Pide $Z_n = \frac{\sqrt{25}(48-43)}{13} = 1.9231$. El distractor `opt_a` (`$4.0698$`) dice: *"Exige simetría previa de $Y_i$ ignorando que el TCL vale con $\mu=43, \sigma=13, n=25$"* y `opt_g` (`$2.3077$`) dice: *"Toma $\bar{Y}_n \sim N(\mu, \sigma^2/n)$ como exacto para $n=25$"*.
       - **`Q-C29-631` (Método Delta):** Pide la varianza asintótica $[g'(14)]^2 \cdot 22 = 933592$. El distractor `opt_g` (`$42458$`) dice: *"Omite el valor absoluto $|g'(14)|$ dejando negativo el error estándar con varianza $22$"* (el valor `$42458$` es positivo y corresponde a $g'(14)\cdot 22$, no a un error estándar negativo).
  2. **Corrupción Algebraica en Pista Socrática 1 de `C-29` (`-0.50 pts`):**
     - En **`Q-C29-631`**, para $g(x)=7x^2+10x$, la Pista 1 instruye:
       > *"Derive primero $g(x)=7x^2+10x$ respecto a $x$ para obtener $g'(x)=27x+10$."*
     - En **`Q-C29-632`**, para $g(x)=3x^2+6x$, la Pista 1 instruye:
       > *"Derive primero $g(x)=3x^2+6x$ respecto a $x$ para obtener $g'(x)=23x+6$."*
     - El autor de la plantilla escribió `2{a}x` en vez de `{2*a}x`, concatenando el exponente `2` con el coeficiente `a` ($2$ con $7 \to 27$; $2$ con $3 \to 23$). Un alumno que siga la pista obtendrá una derivada falsa y fallará sus intentos en `PracticeSession.tsx`.
  3. **`misconception_warning` con datos estáticos de otros problemas (`-0.30 pts`):**
     - En `Q-Hab12-421` ($X \in \{14, 62\}$) y `Q-Hab12-422` ($X \in \{5, 49\}$), la advertencia dice: *"Eleve cada realización al cuadrado antes de promediar para hallar $E[X^2] = (1^2+3^2)/2 = 5$"*.
     - En `Q-Hab06-281` y `Q-Hab06-282` ($\hat{\mu}_n = \bar{Y}_n + c/n$), la advertencia habla de un estimador ajeno: *"Verifique además $\lim_{n\to\infty}\text{Var}(M_B)=\sigma_Y^2\frac{1-a}{1+a}>0$"*.

---

### Dimensión 4: Alineación Instruccional, Taxonomía de Bloom y Pureza de Dominio — **3.30 / 4.0 pts**

- **Fortalezas verificadas:**
  - **Cero contaminación inter-dominio:** `cross_domain_prefix_items_count = 0` y `vacuous_quantifier_items_count = 0`. Todo el vocabulario pertenece legítimamente a Inferencia Estadística y Teoría Asintótica.
  - **Cobertura de niveles superiores en habilidades:** 320/320 reactivos de habilidades están en niveles `Apply`, `Analyze` o `Evaluate`.
- **Deficiencias detectadas (`-0.70 pts`):**
  1. **Artificialidad de enunciados por *Parameter Stuffing* (`-0.50 pts`):**
     - Para satisfacer validadores de interpolación de variables en los distractores, varios enunciados inyectan cláusulas parásitas o contradictorias con la teoría:
       - **`Q-C08-231`:** *"En la norma $L^{9}$ con $0<4<9$, $\|U\|_{9}=20$ y $\|V\|_{9}=30$ (no $r=1/9$), obtenga la cota de $\|U+V\|_{9}$"*. Ni $0<4<9$ ni $r=1/9$ intervienen en $\|U+V\|_9 \le 20+30=50$.
       - **`Q-C10-351` / `Q-C10-352`:** *"Con muestra i.i.d. de tamaño $n=6$, $\sigma^2=156$, $\mu=40$, $\bar{y}=31$, covarianza $36$ y sesgo $8$, halle $\text{Var}(\bar{Y}_n)$"*. Declarar simultáneamente que una muestra es i.i.d. y darle un dato *"covarianza $36$"* confunde gravemente el modelado estadístico.
       - **`Q-C22-451` / `Q-C22-452`:** *"Para $X_n$ con límite casi seguro $15$ (entorno $5$, índice $16$), seleccione la caracterización válida"*. Inyectar `(entorno 5, índice 16)` en una pregunta de definición cuya respuesta es `$P(\lim_{n\to\infty} X_n = 15)=1$` es artificioso y delata a los distractores que usan `5` y `16`.
  2. **Desalineación puntual de etiquetas Bloom (`-0.20 pts`):**
     - En `C-27`, `C-28` y `C-29` (`Q-C27-591`, `Q-C28-611`, `Q-C29-631`), problemas de cálculo algebraico y derivación multipaso fueron etiquetados como `"bloom": "Understand"` en lugar de `"Apply"`.

---

### Dimensión 5: Accesibilidad, Ergonomía Cognitiva en UI y Sintaxis KaTeX — **1.90 / 2.0 pts**

- **Fortalezas verificadas:**
  - **Sintaxis KaTeX 100% íntegra:** `unclosed_braces_count = 0`, `triple_dollars_count = 0`, `double_braces_count = 0`, `unbalanced_dollars_count = 0`.
  - **Ergonomía móvil impecable:** `prose_in_katex_text_items_count = 0` y `raw_identifier_math_items_count = 0`. Las tarjetas de opciones son compactas y legibles.
  - **Descarte confirmado de las 228 alertas de `uninterpolated_math_variable_linter`:** Todas corresponden a macros estándar de LaTeX (`\bar{Y}`, `\hat{p}`, `\xrightarrow{p}`, `\xrightarrow{d}`, `\text{Var}`, `\mathcal{F}`, `_{n_1}`).
- **Observación menor (`-0.10 pts`):**
  - El bug `g'(x)=27x+10` / `23x+6` dentro de expresiones KaTeX en las pistas de `C-29` y ligera heterogeneidad de macro para el operador varianza (`\text{Var}`, `\operatorname{Var}`, `\mathrm{Var}`).

---

## 3. Mastery Path Readiness Index (`MPRI`: 79.00 / 100.0 — SILVER MASTERY PATH)

| Pilar de Preparación para el Dominio (Path-to-Mastery v2.0) | Puntaje Determinista | Puntaje Auditado | Máximo | Diagnóstico en el Viaje del Estudiante |
| :--- | :---: | :---: | :---: | :--- |
| **1. `zpd_adaptive_progression`** | 20.00 | **19.00** | 20.0 | Progresión `easy` $\to$ `medium` $\to$ `hard` activa en 29/29 competencias; ajustar categoría/conteo de `Hab-04` y etiqueta Bloom en `C-27` a `C-29`. |
| **2. `retrieval_modality_and_anti_gaming`** | 20.00 | **15.00** | 20.0 | Excelente proporción `FIB`+`MS` (55.15%), pero vulnerado por sesgo de longitud en 37.11% de `MS`, cotas $>1$ en clave (`Q-C02-082`) y distractores negativos/imposibles. |
| **3. `socratic_scaffolding_lifeline`** | 25.00 | **19.50** | 25.0 | Pistas concisas y útiles en general, pero el bug `2{a}x` en la Pista 1 de `C-29` induce al fallo directo bajo la regla *3-Strikes*. |
| **4. `diagnostic_remediation_alignment`** | 11.93 | **7.50** | 15.0 | Punto más débil del curso: alta tasa de `error_rationale` teóricos desconectados de la fórmula aritmética del distractor en 12+ competencias y unicidad del 13.5%. |
| **5. `dag_and_interleaving_topology`** | 10.00 | **9.50** | 10.0 | DAG conexo y acíclico de profundidad 7; reubicar `H-01` como prerrequisito raíz de probabilidad. |
| **6. `cognitive_ergonomics_and_framing`** | 10.00 | **8.50** | 10.0 | KaTeX limpio y sin desbordamiento móvil, penalizado por *parameter stuffing* (`(no r=1/9)`, `cov=36` en muestra i.i.d.) en enunciados. |
| **TOTAL MPRI** | **96.93** | **79.00** | **100.0** | **SILVER MASTERY PATH (70-84): Apto con remediación focalizada antes de certificar como Gold/Platinum.** |

---

## 4. Plan de Remediación Prioritario y Reglas Candidatas (`/learn`)

### Acciones de Remediación en el Curso (`estadistica_3_s9_vmapreduce_vlean43_v6`)
1. **[CRÍTICO — `C-29`] Corregir bug de concatenación `2{a}x` en Pista 1 del Método Delta (`Q-C29-631` a `650`):** Reemplazar `f"g'(x)=2{a}x+{b}"` por `f"g'(x)={2*a}x+{b}"` para que la derivada de $7x^2+10x$ sea $14x+10$ (y no $27x+10$).
2. **[CRÍTICO — `C-02` y `Hab-03`] Restringir rangos paramétricos en cotas de Chebyshev y FDA Exponencial:**
   - En `C-02` (`Q-C02-082`, etc.), imponer la restricción de generador $\sigma^2 / (n\varepsilon^2) < 1$ (o truncar explícitamente $\min\{1, \sigma^2/(n\varepsilon^2)\}$) para evitar claves correctas de probabilidad $>1$ (`$1.6056$`) y complementos negativos (`$-0.6056$`).
   - En `Hab-03` (`Q-Hab03-121`), acotar $n\theta t \in [0.3, 4.5]$ para evitar que $1 - e^{-n\theta t}$ colapse numéricamente a `$1.0000$` y reemplazar los distractores que calculan esperanza/varianza por errores reales de probabilidad acumulada.
3. **[ALTO — 12+ Competencias] Alinear cada `error_rationale` con la operación matemática exacta del distractor:** En `C-04`, `C-06`, `C-07`, `C-08`, `C-10`, `C-23`, `C-25`, `C-26`, `C-27`, `C-28`, `C-29` y `Hab-03`, reescribir los `error_rationale` para que expliquen el error algebraico real que produce el número mostrado (ej. en `Q-C06-191`, explicar que `$2704$` proviene de elevar $(E[X]+\text{Var}(X))^2$, en vez de hablar de $S_n = \sqrt{S_n^2}$).
4. **[MEDIO — `C-08`, `C-10`, `C-22`] Eliminar *Parameter Stuffing* de los enunciados:** Quitar muletillas artificiales como `(no r=1/9)` en `C-08`, `cov=36, sesgo=8` en muestras i.i.d. de `C-10`, y `(entorno 5, índice 16)` en definiciones de `C-22`.
5. **[MEDIO — `MS` y `Hab-01`/`C-11`/`H-01`] Equilibrar longitud de opciones en `multiple_select` y eliminar distractores negativos en magnitudes cuadráticas:** Nivelar la extensión de los distractores en los 59 ítems `MS` sesgados y sustituir varianzas/ECM/probabilidades negativas por errores de escala positivos plausibles.

### Nuevas Reglas de Linter Descubiertas para `standardized_audit_engine.py`
1. **`LINT-LATEX-MACRO-WHITELIST-FIX` (`info`):** Excluir en `uninterpolated_math_variable_linter` cualquier `{...}` precedido inmediatamente por un comando LaTeX (`\\[a-zA-Z]+`) o por subíndice/superíndice (`[_^]`), eliminando los 228 falsos positivos sobre `\bar{Y}`, `\xrightarrow{p}`, `\text{Var}`, `\mathcal{F}` y `_{n_1}`.
2. **`LINT-STRING-CONCAT-COEFF-DERIVATIVE` (`critical`):** Detectar en enunciados, pistas o soluciones el patrón `g'\(x\)\s*=\s*2[2-9]x` cuando la función cuadrática original es `[2-9]x\^2`, atrapando concatenaciones accidentales de strings `2{a}x` en vez de `{2*a}x`.
3. **`LINT-PROBABILITY-BOUND-GT-ONE-KEY` (`critical`):** Auditar que en cualquier reactivo cuyo enunciado pida una probabilidad o cota de probabilidad (`cota.*probabilidad|determine\s+\\mathbb\{P\}|calcule\s+P\(`), la opción marcada como `is_correct: true` pertenezca estrictamente a $(0, 1)$ (o $[0, 100]\%$).
4. **`LINT-STEM-PARAMETER-STUFFING` (`warning`):** Detectar paréntesis artificiales de inyección de parámetros inconexos en el enunciado (`\(no\s+[a-z]\s*=|\(datos\s+.*cov=|\(entorno\s+\d+,\s*índice\s+\d+\)`).

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "estadistica_3_s9_vmapreduce_vlean43_v6",
    "unit_title": "Estadistica 3 S9 Vmapreduce Vlean43 V6",
    "detected_objective": "Dominio y aplicación analítica integral de propiedades de estimadores en muestras finitas (sesgo, varianza, eficiencia, ECM), desigualdades probabilísticas (Markov, Chebyshev, Jensen, Cauchy-Schwarz) y teoría asintótica (convergencia en probabilidad, media cuadrática, casi segura, distribución, LGN, TCL, Teorema de la Aplicación Continua, Slutsky y Método Delta).",
    "total_competencies": 29,
    "total_questions": 680
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 3.8,
      "max": 4.0,
      "feedback": "Estructura curricular de 29 competencias (680 ítems) con DAG acíclico y conexo (profundidad 7, 0 aristas invertidas) y calibración ZPD tri-banda (easy/medium/hard) en 29/29 competencias. Deducción menor (-0.2) por codificar Hab-04 ('Desigualdad de Chebyshev') con categoría 'Concept' y 20 ítems en vez de 30, y por ubicar H-01 ('Axiomas de Kolmogorov') como hijo de C-01 en lugar de raíz fundacional."
    },
    "assessment_quality": {
      "score": 3.5,
      "max": 5.0,
      "feedback": "Excelente mix multimodal (MC7=44.85%, FIB=31.76%, MS=23.38%; 55.15% evocación activa/discriminación) y alta entropía de respuestas. Se deducen -1.5 pts por: 1) Clave correcta con cota de probabilidad > 1.0 ($1.6056) y distractor negativo (-0.6056) en Q-C02-082, más colapso numérico exponencial a $1.0000 / $0.0000 en Q-Hab03-121; 2) Distractores imposibles por dominio (ECM/varianzas negativas en C-01, Hab-01, C-11 y probabilidades de -5% o 131% en H-01); 3) Sesgo de longitud en el 37.11% (59/159) de los ítems multiple_select."
    },
    "scaffolding_hints": {
      "score": 3.1,
      "max": 5.0,
      "feedback": "El 100% de los 680 ítems cuenta con 3 pistas escalonadas y solución paso a paso sin boilerplate genérico. Se deducen -1.9 pts por: 1) Desconexión diagnóstica masiva en FeedbackToast en 12+ competencias (C-04, C-06, C-07, C-08, C-10, C-23, C-25, C-26, C-27, C-28, C-29, Hab-03) donde el error_rationale recicla teoría del cta.json que no corresponde a la fórmula aritmética del distractor (unicidad global de 13.5%); 2) Bug algebraico por concatenación de strings 2{a}x en la Pista 1 de C-29 (Q-C29-631 indica g'(x)=27x+10 para 7x^2+10x; Q-C29-632 indica g'(x)=23x+6 para 3x^2+6x); 3) 216 misconception_warning genéricos o con números hardcodeados de otros ejemplos (ej. Q-Hab12-421, Q-Hab06-281)."
    },
    "instructional_alignment": {
      "score": 3.3,
      "max": 4.0,
      "feedback": "100% de habilidades en niveles superiores de Bloom (Apply/Analyze/Evaluate) y 0 prefijos de dominios ajenos. Se deducen -0.7 pts por inyección artificial de parámetros basura ('parameter stuffing') en enunciados para forzar interpolación en distractores (ej. '(no r=1/9)' en Q-C08-231, 'covarianza 36 y sesgo 8' en muestras i.i.d. de Q-C10-351, y '(entorno 5, índice 16)' en Q-C22-451) y por etiquetar cálculos algebraicos de C-27, C-28 y C-29 como 'Understand'."
    },
    "technical_ergonomics": {
      "score": 1.9,
      "max": 2.0,
      "feedback": "Sintaxis KaTeX limpia (0 llaves rotas, 0 triples dólares, 0 prosa desbordante en \\text{}). Se verificó que el 100% de las 228 alertas de uninterpolated_math_variable_linter son falsos positivos léxicos sobre argumentos de macros LaTeX válidas (\\bar{Y}, \\hat{p}, \\xrightarrow{p}, \\xrightarrow{d}, \\text{Var}, \\mathcal{F}, _{n_1}). Deducción mínima (-0.1) por el typo algebraico 2{a}x dentro de KaTeX en las pistas de C-29."
    }
  },
  "penalties_applied": [],
  "raw_subtotal": 15.6,
  "final_score": 15.6,
  "quality_tier": "ACEPTABLE (14-16.9)",
  "mastery_path_readiness": {
    "mpri_score": 79.0,
    "mpri_max": 100.0,
    "mpri_tier": "SILVER MASTERY PATH (70-84): Apto con remediación focalizada en rationales y plantillas",
    "pillars": {
      "zpd_adaptive_progression": { "score": 19.0, "max": 20.0 },
      "retrieval_modality_and_anti_gaming": { "score": 15.0, "max": 20.0 },
      "socratic_scaffolding_lifeline": { "score": 19.5, "max": 25.0 },
      "diagnostic_remediation_alignment": { "score": 7.5, "max": 15.0 },
      "dag_and_interleaving_topology": { "score": 9.5, "max": 10.0 },
      "cognitive_ergonomics_and_framing": { "score": 8.5, "max": 10.0 }
    },
    "student_journey_verdict": "El curso ofrece una progresión ZPD tri-banda real y una excelente combinación de evocación activa (FIB 31.76% + MS 23.38%), pero la experiencia de remediación en PracticeSession.tsx y FeedbackToast.tsx se ve comprometida por justificaciones de error teóricas desconectadas de la aritmética de los distractores, un bug de concatenación en la derivada de la Pista 1 en C-29 (27x+10 en lugar de 14x+10), y casos de cotas de probabilidad > 1.0 en la clave correcta (Q-C02-082)."
  },
  "discovered_lint_rules": [
    {
      "rule_id": "LINT-LATEX-MACRO-WHITELIST-FIX",
      "severity": "info",
      "regex_pattern": "(?<!\\\\[a-zA-Z]+)(?<!_)(?<!\\^)\\{[A-Za-z_][A-Za-z0-9_]*\\}",
      "description": "Excluir en uninterpolated_math_variable_linter las llaves precedidas por comandos LaTeX (\\bar{Y}, \\hat{p}, \\xrightarrow{p}, \\text{Var}, \\mathcal{F}) o sub/superíndices (_{n_1}) para eliminar los 228 falsos positivos léxicos.",
      "evidence_items": ["Q-C01-012", "Q-C03-111", "Q-C08-236", "Q-C09-346", "Q-Hab14-547"]
    },
    {
      "rule_id": "LINT-STRING-CONCAT-COEFF-DERIVATIVE",
      "severity": "critical",
      "regex_pattern": "g'\\(x\\)\\s*=\\s*2[2-9]x",
      "description": "Detecta concatenación accidental de strings '2{a}x' en lugar de '{2*a}x' al mostrar la derivada de polinomios cuadráticos ax^2+bx en pistas o soluciones.",
      "evidence_items": ["Q-C29-631", "Q-C29-632"]
    },
    {
      "rule_id": "LINT-PROBABILITY-BOUND-GT-ONE-KEY",
      "severity": "critical",
      "regex_pattern": "(cota.*probabilidad|determine\\s+\\\\mathbb\\{P\\}|calcule\\s+P\\()",
      "description": "Verifica que cuando el enunciado solicita una probabilidad o cota de probabilidad, la opción correcta (is_correct=true) no supere 1.0 ni colapse a 1.0000 por underflow exponencial.",
      "evidence_items": ["Q-C02-082", "Q-Hab03-121"]
    },
    {
      "rule_id": "LINT-STEM-PARAMETER-STUFFING",
      "severity": "warning",
      "regex_pattern": "(\\(no\\s+r=1/\\d+\\)|\\(datos\\s+.*cov=|\\(entorno\\s+\\d+,\\s*índice\\s+\\d+\\))",
      "description": "Detecta inyección artificial de parámetros irrelevantes o contradictorios entre paréntesis en el enunciado para forzar su aparición en los distractores.",
      "evidence_items": ["Q-C08-231", "Q-C08-232", "Q-C10-351", "Q-C10-352", "Q-C22-451", "Q-C22-452"]
    }
  ],
  "remediation_actions": [
    "Corregir en la plantilla de C-29 (Método Delta) la expresión f-string de la Pista 1 cambiando '2{a}x' por '{2*a}x' (actualmente imprime g'(x)=27x+10 para 7x^2+10x en Q-C29-631 y g'(x)=23x+6 para 3x^2+6x en Q-C29-632).",
    "Restringir los parámetros (n, sigma, varepsilon) en C-02 y Hab-04/Hab-11 para que sigma^2/(n*varepsilon^2) < 1 (o acotar explícitamente con min(1, ...)), eliminando claves correctas > 1 como $1.6056 en Q-C02-082 y complementos negativos como -0.6056.",
    "Acotar el producto n*theta*t en Hab-03 (Mínimo Exponencial) al rango [0.3, 4.5] para evitar que la FDA 1 - exp(-n*theta*t) colapse a $1.0000 (Q-Hab03-121), y reemplazar los distractores que calculan media/varianza/ECM por errores reales en el cálculo de la probabilidad.",
    "Reescribir los error_rationale en C-04, C-06, C-07, C-08, C-10, C-23, C-25, C-26, C-27, C-28 y C-29 para que expliquen la operación aritmética exacta que generó el valor del distractor, eliminando el pegado de frases teóricas inconexas del cta.json.",
    "Eliminar el 'parameter stuffing' de los enunciados en C-08 ('(no r=1/9)'), C-10 ('covarianza 36 y sesgo 8' en muestras i.i.d.) y C-22 ('(entorno 5, índice 16)').",
    "Nivelar la longitud de los distractores en los 59 reactivos multiple_select detectados por ms_length_bias_linter y sustituir los distractores negativos en magnitudes no negativas (ECM, varianza, probabilidad) por errores plausibles positivos."
  ]
}
```

</details>
