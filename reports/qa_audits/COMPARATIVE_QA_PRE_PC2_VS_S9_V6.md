# Auditoría Comparativa Profunda (QA): `estadistica_3_pre_pc2` vs. `estadistica_3_s9_vmapreduce_vlean43_v6`

- **Fecha de Auditoría:** 2026-11-15
- **Marco Normativo:** Quality Matters (QM), OSCQR, Bloom 2-Sigma Mastery Learning y Path-to-Mastery v2.0 (`StandardizedAuditEngine` + Verificación Forense Cruzada)
- **Reportes Individuales Base:**
  - [estadistica_3_pre_pc2_qa_report.md](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/estadistica_3_pre_pc2_qa_report.md)
  - [estadistica_3_s9_vmapreduce_vlean43_v6_qa_report.md](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/estadistica_3_s9_vmapreduce_vlean43_v6_qa_report.md)

---

## 1. Síntesis Ejecutiva y Veredicto Escéptico

Ambos cursos aprueban con holgura los linters sintácticos de primera generación (logrando **20.00 / 20.0** y **19.48 / 20.0** en el *Fast Deterministic Pass*, con 100% de calibración ZPD tri-banda `easy`/`medium`/`hard`, 0 llaves KaTeX rotas, 0 residuos f-string y >55% de práctica activa `FIB`+`MS`). Sin embargo, al someter el 100% de sus bancos de reactivos a una **auditoría forense cruzada y escéptica**, emergen diferencias estructurales profundas entre ambos pipelines:

1. **En calidad psicométrica de reactivos y fidelidad diagnóstica de `error_rationale` (Dimensiones 2 y 3), `estadistica_3_pre_pc2` es claramente superior (`17.70 / 20.0` global; `17.65 / 20.0` en temas compartidos) frente a `estadistica_3_s9_vmapreduce_vlean43_v6` (`15.60 / 20.0`):**
   - En `estadistica_3_pre_pc2`, casi la totalidad de los `error_rationale` en problemas de cálculo numérico explican **la operación aritmética exacta** que originó el valor del distractor (con la única excepción de `C-12`), y no existen claves correctas que violen el axioma de probabilidad ($\mathbb{P} \le 1$) ni colapsos exponenciales a `1.0000` / `0.0000`.
   - En `estadistica_3_s9_vmapreduce_vlean43_v6`, al menos **12 competencias** (`C-04`, `C-06`, `C-07`, `C-08`, `C-10`, `C-23`, `C-25`, `C-26`, `C-27`, `C-28`, `C-29`, `Hab-03`) sufren **desconexión diagnóstica severa**: los distractores son números generados por perturbaciones aritméticas, pero sus `error_rationale` pegan afirmaciones teóricas estáticas del `cta.json` que no tienen relación con el número mostrado en pantalla. Además, presenta errores matemáticos críticos en claves correctas (`Q-C02-082` marca `$1.6056$` y `Q-C02-084` marca `$2.9091$` como cotas de probabilidad correctas; `Hab-03` colapsa a `$1.0000$` en 4 reactivos por underflow exponencial $e^{-32.64}$) y un bug de concatenación en la Pista 1 de `C-29` (`g'(x)=27x+10` para $7x^2+10x$).
2. **En deduplicación curricular (Stage-2 MapReduce Reducer) y limpieza de anti-gaming de linter, `estadistica_3_s9_vmapreduce_vlean43_v6` supera a `estadistica_3_pre_pc2`:**
   - Sobre exactamente los mismos dos documentos de Semana 9 (`01_semana_9_apuntes.pdf` + `02_EST3_LEC07_26.2_V2.pdf`), `s9_vmapreduce_vlean43_v6` fusionó correctamente los traslapes entre apuntes y diapositivas en **29 competencias canónicas (680 reactivos)**. En cambio, `pre_pc2` dejó **37 competencias (890 reactivos)** para esos mismos dos documentos (con **7 pares duplicados** como Markov `C-05`+`Hab-10` y Chebyshev `Hab-03`+`C-17`, más **3 clústeres duplicados adicionales** en las unidades de Semana 10).
   - `pre_pc2` contiene **dos artificios de compilador que engañaron al linter estático**:
     1. **Contaminación del 100% de los `fill_in_the_blank` (`556/556` ítems):** Todos los reactivos FIB de las 57 competencias de `pre_pc2` tienen hardcodeada como `common_misconception_warning` la fórmula cruda `"$\mathrm{Sesgo}(\hat{\theta}_n)=\theta-\mathbb{E}[\hat{\theta}_n]$"` de `C-01`, lo que evadió la regex de frases genéricas (`generic_misconception_count = 0`) pero muestra una fórmula de sesgo sin contexto en temas de TCL, MCO, White o Hausman.
     2. **Inflación de unicidad de `error_rationale` mediante 16 prefijos rotativos (`57.90%` del banco):** `pre_pc2` antepone etiquetas rotativas (*"Error conceptual:"*, *"Confusión teórica:"*, *"Fallo de cálculo:"*, *"Desvío algebraico:"*, etc.) al mismo esqueleto de rationale, inflando la métrica del linter de **`29.45%` real** (`1,111/3,772`) a **`56.18%` nominal** (`2,119/3,772`).

---

## 2. Parte I: Comparación Global (Todos los Temas de Ambos Cursos)

| Métrica / Dimensión Auditada | `estadistica_3_pre_pc2` (Global: 4 PDFs) | `estadistica_3_s9_vmapreduce_vlean43_v6` (Global: 2 PDFs) | Ventaja / Veredicto Forense |
| :--- | :---: | :---: | :--- |
| **Volumen Curricular** | **57 comps / 1,390 ítems** (`0` H, `32` C, `25` Hab) | **29 comps / 680 ítems** (`1` H, `18` C, `10` Hab) | `Pre PC2` cubre Semanas 9 y 10; `S9 V6` cubre Semana 9 |
| **Score Determinista (Linter)** | `20.00 / 20.0` (`MPRI: 99.91`) | `19.48 / 20.0` (`MPRI: 96.93`) | Empate técnico superficial (ambos con sesgos de linter) |
| **Score Auditado Calibrado (/20.0)** | **17.70 / 20.0** (`EXCELENTE`) | **15.60 / 20.0** (`ACEPTABLE`) | **`Pre PC2` (+2.10 pts)** |
| **MPRI Auditado Calibrado (/100.0)** | **89.5 / 100.0** (`GOLD`) | **79.0 / 100.0** (`SILVER`) | **`Pre PC2` (+10.5 pts)** |
| **D1. Arquitectura y DAG (`/4.0`)** | **3.60 / 4.0** (10 pares/clústeres duplicados entre PDFs; 0 `Fact`) | **3.80 / 4.0** (Deduplicación limpia en 29 nodos; `Hab-04` como `Concept`) | **`S9 V6` (+0.20 pts)** por mejor fusión MapReduce Stage-2 |
| **D2. Calidad Psicométrica (`/5.0`)** | **4.50 / 5.0** (62.2% FIB+MS; 0 claves $>1$; 44.2% MS length bias) | **3.50 / 5.0** (55.2% FIB+MS; claves $>1$ en `C-02`, underflow `Hab-03`, 16 neg.) | **`Pre PC2` (+1.00 pt)** por sanidad de dominios numéricos |
| **D3. Andamiaje y Diagnóstico (`/5.0`)** | **4.10 / 5.0** (Rationales alineados; 29.45% unicidad real; 556 FIB contaminados) | **3.10 / 5.0** (12+ comps con rationales desconectados; 13.5% unicidad; bug `27x` en `C-29`) | **`Pre PC2` (+1.00 pt)** por alineación aritmética de `FeedbackToast` |
| **D4. Alineación Instruccional (`/4.0`)** | **3.70 / 4.0** (98.9% Hab en Apply+; 0.4% parameter stuffing) | **3.30 / 4.0** (100% Hab en Apply+; parameter stuffing `cov=36` en i.i.d., `(no r=1/9)`) | **`Pre PC2` (+0.40 pts)** por enunciados más naturales |
| **D5. Ergonomía y KaTeX (`/2.0`)** | **1.80 / 2.0** (9 ítems con float `e-0X` en KaTeX; `*` en `Hab-14`) | **1.90 / 2.0** (0 floats `e-0X`; 228 alertas de `{Y}` son 100% falsos positivos de `\bar{Y}`) | **`S9 V6` (+0.10 pts)** por formato numérico más limpio en KaTeX |
| **Unicidad Nominal vs. Real de Rationales** | `56.18%` nominal $\to$ **`29.45%` real** (`19.5` esqueletos/comp) | `13.50%` nominal $\to$ **`13.50%` real** (`10.0` esqueletos/comp) | **`Pre PC2` (2.18x más variedad real)** pese a usar prefijos sintéticos |
| **Pistas con Parámetros del Enunciado** | `732 / 1,390` (**52.7%**) — prom. `65.3` chars | `403 / 680` (**59.3%**) — prom. `70.2` chars | **`S9 V6` (+6.6 pts %)** pistas ligeramente más específicas al ítem |

---

## 3. Parte II: Comparación Justa 1 a 1 (Unidades Compartidas: Propiedades Finitas + Teoría Asintótica / Semana 9)

Para eliminar la distorsión causada por las 20 competencias exclusivas de Semana 10 en `estadistica_3_pre_pc2` (`C-29` a `Hab-26`: MCO Asintótico, Matriz Sándwich/White, Wald/F, Hausman, Atenuación y Método Delta en Regresión, que suman 500 preguntas), aislamos exactamente el subconjunto compartido de **Unidades 1 y 2** (basado en `01_semana_9_apuntes.pdf` y `02_EST3_LEC07_26.2_V2.pdf`):

- **`estadistica_3_pre_pc2` (Subconjunto Compartido Unidades 1 y 2):** Primeras **37 competencias** (`C-01` a `Hab-16`), **890 preguntas** (`MC7`: 346 [38.9%], `FIB`: 342 [38.4%], `MS`: 202 [22.7%]).
- **`estadistica_3_s9_vmapreduce_vlean43_v6` (Curso Completo):** **29 competencias** (`C-01` a `Hab-16`), **680 preguntas** (`MC7`: 305 [44.9%], `FIB`: 216 [31.8%], `MS`: 159 [23.4%]).

### 3.1. Métricas Head-to-Head en el Subconjunto Compartido (Unidades 1 y 2)

| Indicador Forense (Solo Unidades Compartidas) | `Pre PC2` (Unidades 1 y 2: 37 comps) | `S9 V6` (Unidades 1 y 2: 29 comps) | Diferencia / Interpretación Analítica |
| :--- | :---: | :---: | :--- |
| **Competencias Extraídas de los Mismos 2 PDFs** | `37` (`22` Concept, `15` Skill) | `29` (`1` Fact, `18` Concept, `10` Skill) | `Pre PC2` dejó **8 competencias redundantes sin fusionar** (+210 ítems extra) |
| **Total de Preguntas en Unidades Compartidas** | `890` | `680` | `+210` preguntas en `Pre PC2` por desdoblamiento de nodos |
| **Proporción de Evocación Activa (`FIB` + `MS`)** | **61.1%** (`38.4%` FIB + `22.7%` MS) | **55.1%** (`31.8%` FIB + `23.4%` MS) | **`Pre PC2` (+6.0%)** exige más cálculo directo sin opciones (`FIB`) |
| **MC7 Puramente Numéricos** | `75.5%` | `91.8%` | `Pre PC2` combina MC7 numéricos y simbólicos; `S9 V6` mecaniza más a números |
| **Unicidad Real de Esqueletos `error_rationale` (Sin Prefijos)** | **`26.65%`** (`661 / 2,480` — `17.9` por comp) | **`13.50%`** (`290 / 2,148` — `10.0` por comp) | **`Pre PC2` casi duplica (1.97x)** la diversidad real de diagnóstico |
| **Fidelidad Aritmética del `error_rationale`** | **36 / 37 comps alineadas (97.3%)** (solo falla `C-12`) | **17 / 29 comps alineadas (58.6%)** (fallan 12 comps) | **Diferencia decisiva a favor de `Pre PC2`** |
| **Claves Correctas con Probabilidad $>1.0$ o Underflow `1.0000`** | **0 ítems** | **6 ítems** (`Q-C02-082`, `Q-C02-084`, 4 en `Hab-03`) | **`Pre PC2`** acotó correctamente los dominios paramétricos |
| **Distractores Negativos en Varianza / ECM / Probabilidad** | **0 ítems** en MC7 numérico | **16 ítems** (`C-01`, `Hab-01`, `C-11`, `H-01`) | **`Pre PC2`** evita distractores negativos descartables a simple vista |
| **Sesgo de Longitud en `multiple_select` (`>1.08x`)** | **37.6%** (`76 / 202`, ratio prom. `1.041x`) | **37.1%** (`59 / 159`, ratio prom. `1.055x`) | **Empate exacto (~37%)** en las unidades compartidas (el 44.2% global de `Pre PC2` proviene del 56.6% en Semana 10) |
| **Pistas que Citan Parámetros del Enunciado** | `451 / 890` (**50.7%**) — prom. `63.4` chars | `403 / 680` (**59.3%**) — prom. `70.2` chars | **`S9 V6` (+8.6%)** interpola más datos del problema en las pistas |
| **Contaminación de `misconception_warning` en FIB** | **342 / 342 (100%)** tienen `$\mathrm{Sesgo}=\theta-\mathbb{E}[\hat{\theta}]$` | **216 / 216 (100%)** tienen `"Verifique cuidadosamente..."` | Ambos fallan en FIB, pero **`Pre PC2` inyecta una fórmula falsa de `C-01`** |
| **Errores de Concatenación (`2{a}`) en Texto Matemático** | `Q-C05-141/142` (`263`), `Q-C06-191/192` (`412`, `26^2`) en rationales | `Q-C29-631/632` (`g'(x)=27x+10`, `23x+6`) en **Pista 1** | Más grave en **`S9 V6`** porque sabotea la Pista 1 en pleno intento del alumno |
| **Calificación Auditada en Unidades Compartidas (/20.0)** | **17.65 / 20.0** (`EXCELENTE`) | **15.60 / 20.0** (`ACEPTABLE`) | **`Pre PC2` gana por +2.05 pts** en comparación justa 1 a 1 |

---

### 3.2. Mapa Biyectivo 1 a 1 de los 27 Clústeres Temáticos Compartidos

La siguiente tabla empareja el 100% de las **29 competencias de `S9 V6`** con el 100% de las **37 competencias compartidas de `Pre PC2`**, comparando su volumen, diversidad real de rationales (despojando prefijos sintéticos) y hallazgos forenses:

| # | Clúster Temático Compartido | `S9 V6` (IDs / Qs / Esqueletos Rationale) | `Pre PC2` (IDs / Qs / Esqueletos Rationale) | Comparación Forense 1 a 1 |
| :-: | :--- | :--- | :--- | :--- |
| **01** | **Sesgo, Insesgadez y Eficiencia Relativa** | `C-01` (`20q`: 12/4/4) — `18/80` (`22.5%`) | `C-01, Hab-08, C-13` (`70q`: 27/25/18) — `58/198` (`29.3%`) | `S9 V6` fusionó 3 nodos en 1 pero dejó `$-10$` para ECM en `Q-C01-003`. `Pre PC2` fragmenta en 3 nodos y deja fórmula cruda en FIB `C-01`. |
| **02** | **Descomposición del Error Cuadrático Medio (ECM)** | `Hab-01` (`30q`: 20/5/5) — `32/130` (`24.6%`) | `C-02, Hab-09` (`50q`: 18/20/12) — `55/132` (`41.7%`) | `S9 V6` tiene 10 ítems con distractores de ECM negativos (`-32`, `-103`, `-110`). `Pre PC2` duplica el tema en 2 nodos pero sin ECM negativos en MC7 numérico. |
| **03** | **Momentos de Media y Cuasivarianza ($n-1$)** | `Hab-02` (`30q`: 15/8/7) — `12/104` (`11.5%`) | `Hab-01, C-14` (`50q`: 18/20/12) — `20/132` (`15.2%`) | `Pre PC2` tiene sustitución parcial `\frac{n-1}{3}\sigma^2` en Pista 1 de `C-14` y contradicción aritmética en `Q-Hab01-041` (`67/18 = 67.0000`). `S9 V6` es más limpio aquí. |
| **04** | **Sucesiones, Conv. en Probabilidad y Consistencia** | `C-02` (`20q`: 12/4/4) — `18/80` (`22.5%`) | `C-03, C-15` (`40q`: 20/10/10) — `52/140` (`37.1%`) | **Fallo crítico en `S9 V6`**: `Q-C02-082` tiene clave correcta `$1.6056 > 1$` y `Q-C02-084` tiene `$2.9091 > 1$` para una cota de probabilidad. `Pre PC2` es matemáticamente impecable. |
| **05** | **Conv. en Media $r$-ésima y Consistencia vía ECM** | `C-03` (`20q`: 10/5/5) — `12/70` (`17.1%`) | `C-04, Hab-12` (`50q`: 18/20/12) — `50/132` (`37.9%`) | `Pre PC2` ofrece el doble de riqueza diagnóstica en rationales, aunque `Q-Hab12-621` conserva números fijos (`5/n`, `25/n^2`) en `misconception_warning`. |
| **06** | **Mínimo Muestral Exponencial ($X_{(1)}$)** | `Hab-03` (`30q`: 8/15/7) — `6/62` (`9.7%`) | `Hab-02` (`30q`: 8/15/7) — `10/62` (`16.1%`) | **Fallo crítico en `S9 V6`**: 4 ítems (`Q-Hab03-121, 124, 126, 127`) colapsan a `$1.0000$` por usar $\theta \in [3,10]$ ($e^{-32.64}\approx 0$) y mezclan ECM/varianza como distractores de probabilidad. `Pre PC2` usa $\theta=0.11$ sin underflow. |
| **07** | **Desigualdad de Markov** | `C-04` (`20q`: 10/5/5) — `12/70` (`17.1%`) | `C-05, Hab-10` (`50q`: 18/20/12) — `54/132` (`40.9%`) | En `S9 V6` (`Q-C04-151`) los rationales están desconectados de la aritmética (`"viola \delta > 0"` para $28/(72+10)$). En `Pre PC2` explican el cálculo real, pero duplica el tema en `C-05`+`Hab-10` y concatena `263` en `Q-C05-141`. |
| **08** | **Desigualdad de Chebyshev** | `Hab-04, Hab-11` (`50q`: 20/19/11) — `24/142` (`16.9%`) | `Hab-03, C-17` (`50q`: 25/13/12) — `35/174` (`20.1%`) | Ambos cursos desdoblan Chebyshev en 2 nodos (50 preguntas). `S9 V6` etiquetó erróneamente `Hab-04` como `Concept` (20q) e incluyó varios distractores $>1.0$; `Pre PC2` tiene 5 floats `e-0X` en `C-17`. |
| **09** | **Desigualdad de Jensen** | `C-06` (`20q`: 10/5/5) — `12/70` (`17.1%`) | `C-06` (`20q`: 10/5/5) — `44/70` (`62.9%`) | En `S9 V6` (`Q-C06-191`) los rationales hablan de $S_n=\sqrt{S_n^2}$, $1/X$ y $|x|$ en un cálculo de $E[X^2]=25^2+27$. En `Pre PC2` están 100% alineados al polinomio cuadrático (con typo menor `(412+10)^2`). |
| **10** | **Sesgo por No Linealidad** | `Hab-12` (`30q`: 8/15/7) — `6/62` (`9.7%`) | `Hab-04` (`30q`: 8/22/0) — `6/48` (`12.5%`) | En `S9 V6` `Q-Hab12-421` tiene warning hardcodeado `(1^2+3^2)/2=5`. En `Pre PC2` `Hab-04` carece de ítems `MS` (0/30) pero sus MC7 simbólicos están bien alineados. |
| **11** | **Desigualdad de Cauchy-Schwarz** | `C-07` (`20q`: 10/5/5) — `6/70` (`8.6%`) | `C-07` (`20q`: 10/5/5) — `16/70` (`22.9%`) | En `S9 V6` (`Q-C07-211`) el distractor $289+100=389$ dice *"Exige discriminante $\Delta \ge 0$"*. En `Pre PC2` (`Q-C07-241`) explica exactamente *"suma $45+26=71$ en lugar de multiplicarlos"*. |
| **12** | **Jerarquía de Convergencias** | `C-08` (`20q`: 10/5/5) — `12/70` (`17.1%`) | `C-08` (`20q`: 10/5/5) — `21/70` (`30.0%`) | `S9 V6` inyecta `(no r=1/9)` en el enunciado (`Q-C08-231`) y pega teoría desconectada en rationales. `Pre PC2` evalúa una cota de Markov de orden 3 en `Q-C08-261` pero con rationales coherentes. |
| **13** | **Contraejemplo Probabilidad vs. Momentos** | `Hab-05` (`30q`: 8/15/7) — `6/62` (`9.7%`) | `Hab-05` (`30q`: 8/15/7) — `10/62` (`16.1%`) | Ambos modelan correctamente la sucesión con valores extremos $n^2$ con probabilidad $1/n$; `Pre PC2` explica mejor la desviación aritmética de cada distractor. |
| **14** | **Insesgadez vs. Consistencia y Estimadores Alt.** | `Hab-06` (`30q`: 18/6/6) — `18/120` (`15.0%`) | `C-09, Hab-06` (`50q`: 18/27/5) — `22/118` (`18.6%`) | `S9 V6` cita un estimador inexistente $M_B$ en el warning de `Q-Hab06-281`. `Pre PC2` sustituyó parcialmente $n=11$ en la pista `"Tome $a^{11}\to 0$ cuando $n\to\infty$"` (`Q-Hab06-331`). |
| **15** | **Espacio de Probabilidad y Axiomas de Kolmogorov** | `H-01` (`20q`: 10/5/5) — `6/70` (`8.6%`) | `C-10` (`20q`: 10/5/5) — `16/70` (`22.9%`) | Ambos ubican tardíamente Kolmogorov a mitad del curso. `S9 V6` incluye probabilidades imposibles (`-5%`, `131%`) en `Q-H01-311` y lo cuelga de `C-01` (Sesgo). `Pre PC2` mantiene opciones en $[0,1]$. |
| **16** | **Variable Aleatoria y Distribución Inducida** | `C-09` (`20q`: 10/5/5) — `6/70` (`8.6%`) | `C-11` (`20q`: 10/5/5) — `16/70` (`22.9%`) | `Pre PC2` explica con mayor precisión los errores de suma de masas de probabilidad en preimágenes. |
| **17** | **Muestra Aleatoria i.i.d. y Estimador** | `C-10` (`20q`: 10/5/5) — `8/70` (`11.4%`) | `C-12` (`20q`: 10/5/5) — `10/70` (`14.3%`) | Punto débil en ambos: `S9 V6` (`Q-C10-351`) inyecta *"covarianza 36 y sesgo 8"* en una muestra declarada i.i.d.; `Pre PC2` (`Q-C12-401`) desconecta los distractores de $\bar{y}=815/42$ de sus rationales verbales. |
| **18** | **Esperanza y Varianza de Variable Aleatoria** | `C-11` (`20q`: 10/5/5) — `14/70` (`20.0%`) | `Hab-07` (`30q`: 8/15/7) — `10/62` (`16.1%`) | `Pre PC2` la clasifica acertadamente como `Skill` (`Hab-07`, 30q) sin varianzas negativas. `S9 V6` la deja como `Concept` (`C-11`, 20q) e incluye varianzas negativas (`-158.00`). |
| **19** | **Convergencia Casi Segura ($\xrightarrow{a.s.}$)** | `C-22` (`20q`: 10/5/5) — `8/70` (`11.4%`) | `C-22` (`20q`: 10/5/5) — `16/70` (`22.9%`) | Ambos inyectan parámetros decorativos en enunciados de definición: `(entorno 5, índice 16)` en `S9 V6` (`Q-C22-451`) y `con tolerancia \epsilon=0.6 desde n=41` en `Pre PC2` (`Q-C22-651`). |
| **20** | **Convergencia en Distribución ($\xrightarrow{d}$)** | `C-23` (`20q`: 10/5/5) — `6/70` (`8.6%`) | `C-23` (`20q`: 10/5/5) — `10/70` (`14.3%`) | En `Pre PC2` los MC7 evalúan la definición simbólica formal; en `S9 V6` fuerzan cálculos numéricos de cuantiles normales con rationales teóricos desconectados. |
| **21** | **Ley de los Grandes Números (LGN)** | `C-25` (`20q`: 10/5/5) — `6/70` (`8.6%`) | `C-25` (`20q`: 10/5/5) — `16/70` (`22.9%`) | En `S9 V6` (`Q-C25-491`) el distractor `$84$` dice *"Exige normalidad $Y_i \sim N(\mu,\sigma^2)$"*. En `Pre PC2` cada distractor explica el error algebraico lineal exacto. |
| **22** | **Teorema Central del Límite (TCL)** | `C-26` (`20q`: 10/5/5) — `6/70` (`8.6%`) | `C-26` (`20q`: 10/5/5) — `16/70` (`22.9%`) | En `S9 V6` (`Q-C26-511`) los distractores `$4.0698$` y `$2.3077$` dan excusas teóricas (*"Exige simetría previa"*). En `Pre PC2` (`Q-C26-711`) diagnostican exactamente qué hizo mal el alumno al estandarizar $Z_n$. |
| **23** | **Cálculo de Probabilidades con el TCL** | `Hab-14` (`30q`: 8/15/7) — `6/62` (`9.7%`) | `Hab-13` (`30q`: 8/15/7) — `10/62` (`16.1%`) | Muy parejos; ambos evalúan estandarización y simetría de colas normales con buena progresión tri-banda. |
| **24** | **Inferencia Asintótica para Proporciones** | `Hab-15` (`30q`: 8/15/7) — `6/62` (`9.7%`) | `Hab-14` (`30q`: 8/15/7) — `10/62` (`16.1%`) | Ambos sólidos; `Pre PC2` tiene un detalle cosmético menor en `Q-Hab14-761` (usa `*` en vez de `\cdot` en una opción simbólica). |
| **25** | **Teorema de la Aplicación Continua (CMT)** | `C-27` (`20q`: 10/5/5) — `6/70` (`8.6%`) | `C-27` (`20q`: 10/5/5) — `16/70` (`22.9%`) | En `Pre PC2` se integra el contraste directo entre CMT ($\operatorname{plim} g(\hat{\theta}) = g(\theta)$) y Jensen ($\mathbb{E}[g(\hat{\theta})] \neq g(\theta)$) con rationales aritméticos exactos. |
| **26** | **Teorema de Slutsky y Contraste con Varianza Est.** | `C-28` (`20q`: 10/5/5) — `6/70` (`8.6%`) | `C-28, Hab-15` (`50q`: 18/20/12) — `52/132` (`39.4%`) | `Pre PC2` dedica una habilidad completa (`Hab-15`, 30q) al contraste $t$ asintótico con varianza estimada vía Slutsky, logrando 8.6x más esqueletos diagnósticos que `S9 V6`. |
| **27** | **Método Delta y Error Estándar / IC** | `C-29, Hab-16` (`50q`: 18/20/12) — `12/132` (`9.1%`) | `Hab-16` (`30q`: 8/15/7) — `10/62` (`16.1%`) | En `S9 V6`, `Hab-16` está muy bien logrado, pero `C-29` tiene el **bug grave de concatenación `2{a}x` en la Pista 1** (`g'(x)=27x+10` para $7x^2+10x$). `Pre PC2` (`Hab-16`) no tiene errores de derivación en pistas. |

---

## 4. Conclusión y Recomendación de Ingeniería Curricular

1. **¿Cuál curso tiene mayor calidad real hoy?**
   - **`estadistica_3_pre_pc2` (`17.70 / 20.0` global; `17.65 / 20.0` en Unidades 1 y 2)** supera con claridad a **`estadistica_3_s9_vmapreduce_vlean43_v6` (`15.60 / 20.0`)** tanto en la evaluación global como en la comparación justa 1 a 1 de los temas compartidos (**+2.05 puntos** sobre 20 y **+10.5 puntos MPRI**). Su ventaja decisiva radica en que los distractores numéricos están respaldados por `error_rationale` que explican la operación aritmética real del error y sus generadores respetan las cotas de dominio ($0 \le \mathbb{P} \le 1$, varianzas/ECM no negativos y tasas exponenciales sin underflow).
2. **¿Qué debe tomar `estadistica_3_pre_pc2` de `estadistica_3_s9_vmapreduce_vlean43_v6`?**
   - La **consolidación curricular del Stage-2 MapReduce Reducer** de `S9 V6`: fusionar los 7 pares duplicados en las Unidades 1 y 2 (y los 3 clústeres duplicados en las Unidades 3 y 4) reduciría `estadistica_3_pre_pc2` de 57 a ~44 competencias verdaderamente ortogonales, evitando que el alumno resuelva dos veces bancos idénticos de Markov (`C-05` y `Hab-10`) o Chebyshev (`Hab-03` y `C-17`).
3. **Saneamiento inmediato recomendado en `estadistica_3_pre_pc2`:**
   - Reemplazar el `common_misconception_warning` hardcodeado (`$\mathrm{Sesgo}(\hat{\theta}_n)=\theta-\mathbb{E}[\hat{\theta}_n]$`) en los 556 ítems FIB por la advertencia específica de cada competencia, eliminar los prefijos rotativos artificiales de los `error_rationale`, y corregir la concatenación sin `\cdot` en `C-39` (`20.5`), `C-06` (`412`) y `C-05` (`263`).
4. **Saneamiento inmediato recomendado en `estadistica_3_s9_vmapreduce_vlean43_v6`:**
   - Corregir el f-string `2{a}x` $\to$ `{2*a}x` en la Pista 1 de `C-29`, acotar $\sigma^2/(n\varepsilon^2) < 1$ en `C-02` (`Q-C02-082/084`) y $n\theta t \le 4.5$ en `Hab-03` (`Q-Hab03-121`), y reescribir los `error_rationale` de las 12 competencias donde se pegaron textos teóricos del `cta.json` sin relación con la fórmula aritmética del distractor.
