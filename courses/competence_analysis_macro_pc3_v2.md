# Cognitive Task Analysis (CTA): Macro Pc3 V2

- **Course ID:** `macro_pc3_v2`
- **Macro-Competency:** Dominio y aplicación analítica integral de Macro Pc3 V2
- **Structure:** 14 total competencies (3 Facts, 7 Concepts, 4 Skills) with 84 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `H-01` | Condición de Estabilidad Macroeconómica del Gasto Agregado | Fact | Remember | Unidad 4: Condición de Estabilidad Macroeconómica del Gasto Agregado | - | 6 |
| `C-01` | Pendiente y Desplazamientos de la Curva IS en Economía Cerrada | Concept | Understand | Unidad 6: Pendiente y Desplazamientos de la Curva IS en Economía Cerrada | H-01 | 6 |
| `C-02` | Equilibrio del Mercado Monetario y Pendiente de la Curva LM | Concept | Understand | Unidad 6: Equilibrio del Mercado Monetario y Pendiente de la Curva LM | H-01 | 6 |
| `C-03` | Casos Extremos de la Curva LM: Trampa de Liquidez y Caso Clásico | Concept | Analyze | Unidad 7: Casos Extremos de la Curva LM: Trampa de Liquidez y Caso Clásico | C-02 | 6 |
| `Hab-01` | Derivación Analítica del Equilibrio Simultáneo IS-LM y Multiplicadores de Política | Skill | Apply | Unidad 7: Derivación Analítica del Equilibrio Simultáneo IS-LM y Multiplicadores de Política | C-01, C-02 | 6 |
| `C-04` | Efecto Desplazamiento (Crowding-Out) y Acomodación Monetaria | Concept | Analyze | Unidad 8: Efecto Desplazamiento (Crowding-Out) y Acomodación Monetaria | C-01, C-02 | 6 |
| `Hab-02` | Medición de Brechas Horizontales y Calibración Numérica BCRP | Skill | Apply | Unidad 9: Medición de Brechas Horizontales y Calibración Numérica BCRP | Hab-01, C-04 | 6 |
| `H-02` | Tipo de Cambio Real Bilateral y Tasa de Variación Logarítmica | Fact | Remember | Unidad 12: Tipo de Cambio Real Bilateral y Tasa de Variación Logarítmica | - | 6 |
| `Hab-03` | Evaluación Numérica de Desviaciones de la Paridad del Poder Adquisitivo (PPA) | Skill | Apply | Unidad 14: Evaluación Numérica de Desviaciones de la Paridad del Poder Adquisitivo (PPA) | H-02 | 6 |
| `C-05` | Valor Agregado vs. Valor Bruto en Apertura Comercial: Caso Japonés | Concept | Analyze | Unidad 2: Valor Agregado vs. Valor Bruto en Apertura Comercial: Caso Japonés | H-02 | 6 |
| `C-06` | Causalidad Acumulativa de Myrdal y Economía de los Flujos Migratorios | Concept | Analyze | Unidad 10: Causalidad Acumulativa de Myrdal y Economía de los Flujos Migratorios | C-05 | 6 |
| `H-03` | Paridad Descubierta de Tasas de Interés (UIP) | Fact | Remember | Unidad 15: Paridad Descubierta de Tasas de Interés (UIP) | H-02 | 6 |
| `C-07` | Curva IS en Economía Abierta y Doble Canal de Transmisión | Concept | Analyze | Unidad 15: Curva IS en Economía Abierta y Doble Canal de Transmisión | C-01, H-02, H-03 | 6 |
| `Hab-04` | Estática Comparativa de Shocks Macroeconómicos en Economía Abierta con Tipo Flexible | Skill | Evaluate | Unidad 16: Estática Comparativa de Shocks Macroeconómicos en Economía Abierta con Tipo Flexible | C-07, Hab-01 | 6 |

---

## Detailed Competency Specifications

### [H-01] Condición de Estabilidad Macroeconómica del Gasto Agregado (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 4: Condición de Estabilidad Macroeconómica del Gasto Agregado
- **Prerequisites:** None
- **Evidence Citations:** `jijas.pdf` (page 4)

#### Description & Cognitive Model
La condición de estabilidad macroeconómica exige que la propensión marginal total a gastar sea estrictamente menor que la unidad, $c_1 + d_1 < 1$, garantizando un denominador positivo $1 - c_1 - d_1 > 0$ en el multiplicador keynesiano $\alpha = \frac{1}{1 - c_1 - d_1}$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Violación de estabilidad | conceptual_swap | high | $c_1 + d_1 \ge 1$ | Si la suma supera la unidad, cualquier incremento autónomo generaría un proceso divergente o explosivo del producto. |
| `D-H01-02` | Omisión de la inversión inducida | conceptual_swap | high | $\alpha = \frac{1}{1 - c_1}$ | El multiplicador con inversión inducida por ventas debe incorporar tanto la propensión a consumir como la sensibilidad a la renta. |
| `D-H01-03` | Signo invertido en acelerador | conceptual_swap | high | $1 - c_1 + d_1$ | El acelerador de la inversión expande el gasto ante aumentos del producto, por lo que resta en el denominador ampliando el multiplicador. |
| `D-H01-04` | Confusión con tasa impositiva | conceptual_swap | high | $\alpha = \frac{1}{(1 - c_1)(1 - t)}$ | En el modelo con impuestos fijos $T = \bar{T}$, el efecto impositivo no altera la pendiente inducida por la renta. |
| `D-H01-05` | Confusión con sensibilidad a la tasa | conceptual_swap | high | $\alpha = \frac{1}{1 - c_1 - d_2}$ | El parámetro $d_2$ mide la sensibilidad de la inversión a la tasa de interés, no a la renta agregada. |
| `D-H01-06` | Inversión de desigualdad | conceptual_swap | high | $c_1 + d_1 = 0$ | Tanto el consumo como la inversión tienen respuestas positivas a la renta en economías viables. |

---

### [C-01] Pendiente y Desplazamientos de la Curva IS en Economía Cerrada (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 6: Pendiente y Desplazamientos de la Curva IS en Economía Cerrada
- **Prerequisites:** H-01
- **Evidence Citations:** `jijas.pdf` (page 6)

#### Description & Cognitive Model
La curva IS representa las combinaciones de producto $Y$ y tasa de interés $i$ que equilibran el mercado de bienes ($Y = Z$). Su ecuación directa es $Y = \alpha A - \alpha d_2 i$, con pendiente negativa en el plano $(Y, i)$ dada por $\frac{\partial i}{\partial Y} = -\frac{1 - c_1 - d_1}{d_2} < 0$, desplazándose horizontalmente en $\Delta Y = \alpha \Delta A$ ante variaciones del gasto autónomo.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Pendiente invertida | conceptual_swap | high | $\frac{\partial i}{\partial Y} > 0$ | Un alza en la tasa de interés encarece el financiamiento y deprime la inversión, requiriendo menor producto para vaciar el mercado de bienes. |
| `D-C01-02` | Error en desplazamiento horizontal | conceptual_swap | high | $\Delta Y = \Delta A$ | El desplazamiento horizontal de la curva IS a tasa constante está magnificado por el multiplicador keynesiano. |
| `D-C01-03` | Aplanamiento erróneo | conceptual_swap | high | $d_2 \to 0 \Rightarrow \text{plana}$ | Una alta sensibilidad de la inversión a la tasa ($d_2 \to \infty$) hace que la curva IS sea casi horizontal en el plano cartesiano. |
| `D-C01-04` | Confusión con gasto autónomo | conceptual_swap | high | $\Delta A = \Delta G + c_1 \Delta T$ | Los impuestos reducen el ingreso disponible y por ende el consumo autónomo resta en una proporción $c_1$. |
| `D-C01-05` | Inversión de ejes en la pendiente | conceptual_swap | high | $\frac{\partial Y}{\partial i} = \text{pendiente en plano }(Y,i)$ | Con la tasa $i$ en el eje vertical y el producto $Y$ en el horizontal, la pendiente geométrica es la inversa de la derivada de $Y$ respecto a $i$. |
| `D-C01-06` | Efecto de la propensión marginal | conceptual_swap | high | $c_1 \uparrow \Rightarrow \text{curva más empinada}$ | A mayor propensión a consumir, mayor es el multiplicador $\alpha$ y menor es la magnitud de la pendiente, aplanando la curva IS. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Nivel de precios constante en el corto plazo $P = \bar{P}$ | Permite equiparar variaciones nominales con reales en la tasa de interés e inversión. | - |
| `A-C01-02` | - | Capacidad ociosa y ajuste pasivo de la producción por la demanda | Asegura que el producto se determine estrictamente por el gasto agregado planeado. | - |

---

### [C-02] Equilibrio del Mercado Monetario y Pendiente de la Curva LM (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 6: Equilibrio del Mercado Monetario y Pendiente de la Curva LM
- **Prerequisites:** H-01
- **Evidence Citations:** `jijas.pdf` (page 6)

#### Description & Cognitive Model
La curva LM refleja el equilibrio en el mercado monetario donde la oferta real de dinero iguala la demanda de saldos reales: $\frac{M}{P} = f_1 Y - f_2 i$. En el plano $(Y, i)$, su pendiente es positiva, $\frac{\partial i}{\partial Y} = \frac{f_1}{f_2} > 0$, desplazándose a la derecha y hacia abajo ante incrementos de la oferta monetaria real en una magnitud $\Delta Y = \frac{1}{f_1}\Delta(M/P)$ a tasa constante.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Signo de la pendiente | conceptual_swap | high | $\frac{\partial i}{\partial Y} = -\frac{f_1}{f_2}$ | Un mayor producto eleva la demanda de dinero por transacción; ante oferta fija, la tasa de interés debe subir para reequilibrar el mercado. |
| `D-C02-02` | Desplazamiento monetario | conceptual_swap | high | $\Delta Y = f_2 \Delta(M/P)$ | El desplazamiento horizontal a tasa constante depende de la sensibilidad de la demanda de dinero a la renta $f_1$. |
| `D-C02-03` | Confusión de motivos de demanda | conceptual_swap | high | $f_2 \text{ motivo transacción}$ | El parámetro $f_1$ acompaña a $Y$ (transacción y precaución) y $f_2$ mide el costo de oportunidad respecto a bonos. |
| `D-C02-04` | Dirección del choque monetario | conceptual_swap | high | $\Delta(M/P) > 0 \Rightarrow \text{desplaza arriba a la izquierda}$ | Una inyección de liquidez reduce la tasa de interés de equilibrio para cualquier nivel de producto. |
| `D-C02-05` | Sensibilidad a la tasa nula | conceptual_swap | high | $f_2 \to 0 \Rightarrow \text{LM horizontal}$ | Cuando la demanda no responde a la tasa de interés, la pendiente $f_1/f_2$ tiende a infinito, volviendo la LM vertical. |
| `D-C02-06` | Efecto de precios sobre LM | conceptual_swap | high | $P \uparrow \Rightarrow \text{expande LM}$ | Un aumento de precios erosiona los saldos reales $M/P$, contrayendo la curva monetaria hacia la izquierda y arriba. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | Oferta monetaria exógenamente controlada por la autoridad central | Permite aislar choques de liquidez sin endogeneidad bancaria inmediata. | - |
| `A-C02-02` | - | Elección de cartera restringida a dinero y bonos | Garantiza que el equilibrio del mercado de dinero vacíe simultáneamente el de bonos por Ley de Walras. | - |

---

### [C-03] Casos Extremos de la Curva LM: Trampa de Liquidez y Caso Clásico (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 7: Casos Extremos de la Curva LM: Trampa de Liquidez y Caso Clásico
- **Prerequisites:** C-02
- **Evidence Citations:** `jijas.pdf` (page 7)

#### Description & Cognitive Model
En la trampa de liquidez ($f_2 \to \infty$), la curva LM es horizontal con $\frac{\partial i}{\partial Y} = 0$, otorgando máxima eficacia a la política fiscal ($\Delta Y = \alpha \Delta A$) y esterilidad a la política monetaria. En el caso clásico ($f_2 \to 0$), la LM es vertical con $\frac{\partial i}{\partial Y} \to \infty$, anulando el impacto fiscal sobre el producto ($\Delta Y = 0$) y maximizando la efectividad monetaria con crowding-out total.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Inversión de casos extremos | conceptual_swap | high | $\text{Trampa liquidez: LM vertical}$ | En la trampa de liquidez el público retiene cualquier incremento monetario, dejando la tasa inmóvil y la curva totalmente plana. |
| `D-C03-02` | Eficacia fiscal en caso clásico | conceptual_swap | high | $\text{text Caso clásico: política fiscal expan}$ | Con LM vertical, el gasto público desplaza en idéntica cuantía a la inversión privada al disparar la tasa de interés. |
| `D-C03-03` | Eficacia monetaria en trampa de liquidez | conceptual_swap | high | $\text{Expansión monetaria reactiva el producto}$ | En la trampa de liquidez la tasa de interés ya se encuentra en su piso mínimo y la compra de bonos no estimula la inversión. |
| `D-C03-04` | Comportamiento de la tasa en trampa de liquidez | conceptual_swap | high | $i \text{ cae drásticamente ante } \Delta G$ | Al no subir la tasa de interés en la trampa de liquidez, no existe desincentivo alguno a la inversión privada. |
| `D-C03-05` | Parámetro en el caso clásico | conceptual_swap | high | $f_1 \to \infty \text{ define caso clásico}$ | El caso cuantitativista o clásico se caracteriza porque la demanda de dinero es insensible a la tasa de interés ($f_2 \to 0$). |
| `D-C03-06` | Multiplicador de equilibrio en trampa de liquidez | conceptual_swap | high | $\alpha_A < \alpha$ | Al no existir retroalimentación contractiva por alza de tasas, el multiplicador general coincide exactamente con el simple de la IS. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | Tasa de interés cercana al límite inferior efectivo cero en trampa de liquidez | Fundamenta la perfecta sustitución entre dinero y activos financieros seguros. | - |
| `A-C03-02` | - | Velocidad de circulación estable en el enfoque clásico cuantitativo | Asegura la proporcionalidad estricta entre oferta monetaria y transacciones nominales. | - |

---

### [Hab-01] Derivación Analítica del Equilibrio Simultáneo IS-LM y Multiplicadores de Política (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 7: Derivación Analítica del Equilibrio Simultáneo IS-LM y Multiplicadores de Política
- **Prerequisites:** C-01, C-02
- **Evidence Citations:** `jijas.pdf` (page 7)

#### Description & Cognitive Model
Derivar la solución analítica del sistema $2 \times 2$ igualando las curvas IS y LM para obtener el producto de equilibrio $Y^* = \alpha_A A + \alpha_M \frac{M}{P}$, donde $\alpha_A = \frac{f_2}{(1 - c_1 - d_1)f_2 + d_2 f_1} = \frac{1}{(1 - c_1 - d_1) + d_2(f_1 / f_2)}$ y $\alpha_M = \frac{d_2}{(1 - c_1 - d_1)f_2 + d_2 f_1}$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Omisión de retroalimentación monetaria | skipped_step | high | $Y^* = \frac{1}{1 - c_1 - d_1} A$ | Ignorar la interacción monetaria sobredimensiona el multiplicador fiscal al asumir una tasa de interés invariable. |
| `D-Hab01-02` | Error algebraico en denominador común | skipped_step | high | $\text{Denominador} = (1 - c_1 - d_1)f_1 + d_2 f_2$ | Al multiplicar por $d_2 f_2$, los coeficientes cruzados agrupan $f_2$ con el término autónomo de la IS y $d_2$ con el de la LM. |
| `D-Hab01-03` | Inversión de multiplicadores | conceptual_swap | high | $\alpha_A \text{ intercambiado con } \alpha_M$ | El impacto fiscal es proporcional a $f_2$ (amortigua alzas de tasa), mientras que el monetario depende de $d_2$ (canal de inversión). |
| `D-Hab01-04` | Confusión en unidades monetarias | conceptual_swap | high | $\alpha_M M \text{ sin deflactar por } P$ | El equilibrio macroeconómico requiere el volumen de saldos reales de dinero $M/P$, no el acervo nominal. |
| `D-Hab01-05` | Omisión del parámetro acelerador | skipped_step | high | $d_1 = 0 \text{ en denominador}$ | La inversión inducida por el producto incrementa el efecto multiplicador y debe restarse en el término de filtraciones. |
| `D-Hab01-06` | Signo erróneo en la tasa de interés | conceptual_swap | high | $i^* \text{ cae ante choque fiscal}$ | El aumento del producto eleva la demanda transaccional de liquidez, presionando al alza la tasa de interés de equilibrio. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Determinante del sistema no nulo $(1 - c_1 - d_1)f_2 + d_2 f_1 > 0$ | Garantiza la existencia de una solución única y estable para $(Y^*, i^*)$. | - |
| `A-Hab01-02` | - | Ajuste instantáneo en el mercado de activos frente al mercado de bienes | Permite que la economía permanezca sobre la curva LM mientras transita hacia el equilibrio general. | - |

---

### [C-04] Efecto Desplazamiento (Crowding-Out) y Acomodación Monetaria (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 8: Efecto Desplazamiento (Crowding-Out) y Acomodación Monetaria
- **Prerequisites:** C-01, C-02
- **Evidence Citations:** `jijas.pdf` (page 8)

#### Description & Cognitive Model
El crowding-out mide la pérdida de producto inducida por el alza en la tasa de interés que desincentiva la inversión privada tras un choque fiscal: $\text{Pérdida} = \Delta Y_{\text{sin } \Delta i} - \Delta Y^* = (\alpha - \alpha_A)\Delta A > 0$. Para neutralizar este efecto y mantener $\Delta i = 0$, el banco central debe aplicar una regla de acomodación monetaria inyectando liquidez por $\Delta(M/P) = \frac{f_1}{1 - c_1 - d_1}\Delta A = f_1 \Delta Y_{\text{sin } \Delta i}$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Magnitud errónea de acomodación | conceptual_swap | high | $\Delta(M/P) = \Delta A$ | La acomodación debe expandir la oferta monetaria en exactamente la nueva demanda transaccional generada por la expansión plena del producto. |
| `D-C04-02` | Signo del efecto desplazamiento | conceptual_swap | high | $\alpha_A > \alpha$ | La retroalimentación financiera siempre eleva la tasa de interés reduciendo la inversión frente al modelo keynesiano puro. |
| `D-C04-03` | Efecto en la inversión con acelerador | conceptual_swap | high | $I \text{ cae invariablemente ante } \Delta G > 0$ | El aumento de ventas expande la inversión vía acelerador $d_1$, pudiendo compensar o mitigar el encarecimiento crediticio $d_2 \Delta i$. |
| `D-C04-04` | Confusión con regla de Taylor | conceptual_swap | high | $\text{Acomodación exige subir la tasa}$ | La acomodación busca deliberadamente evitar el freno de la tasa para alcanzar la máxima expansión del producto $\alpha \Delta A$. |
| `D-C04-05` | Crowding-out completo en condiciones estándar | conceptual_swap | high | $\alpha_A = 0 \text{ en economía normal}$ | El crowding-out total solo ocurre en el caso clásico con LM vertical ($f_2 = 0$), no con sensibilidades estándar. |
| `D-C04-06` | Sensibilidad que maximiza el crowding-out | conceptual_swap | high | $d_2 \to 0 \Rightarrow \text{máximo crowding-out}$ | A mayor sensibilidad crediticia $d_2$, un pequeño aumento en la tasa deprime intensamente el gasto privado de capital. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | Estabilidad en la preferencia por liquidez del público | Asegura que el dinero inyectado reduzca o estabilice la tasa de interés y no sea atesorado imprevisiblemente. | - |
| `A-C04-02` | - | Horizonte de rigidez de precios donde no opera inflación inmediata | Permite que la expansión monetaria de acomodación altere los saldos reales de forma efectiva. | - |

---

### [Hab-02] Medición de Brechas Horizontales y Calibración Numérica BCRP (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 9: Medición de Brechas Horizontales y Calibración Numérica BCRP
- **Prerequisites:** Hab-01, C-04
- **Evidence Citations:** `jijas.pdf` (page 9)

#### Description & Cognitive Model
Calcular la brecha horizontal entre curvas IS ($\Delta Y|_{i=\text{cte}} = \alpha \Delta A$) y LM ($\Delta Y|_{i=\text{cte}} = \frac{1}{f_1}\Delta(M/P)$), y cuantificar los multiplicadores generales de equilibrio con parámetros empíricos del BCRP para la economía peruana ($c_1 \approx 0.6226, d_1 \approx 0.2461, d_2 \approx 2.4821, f_1 \approx 1.0, f_2 \approx 0.0010$).

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Error en cálculo del multiplicador simple | skipped_step | high | $\alpha = \frac{1}{1 - 0.6226} \approx 2.65$ | Omitir el coeficiente acelerador subestima dramáticamente la expansión potencial del producto a tasa fija. |
| `D-Hab02-02` | Confusión en escala de sensibilidad monetaria | skipped_step | high | $f_2 = 1.0 \text{ en lugar de } 0.001$ | En las unidades del modelo empírico la demanda de dinero a la tasa es muy inelástica, arrojando una razón $f_1/f_2 = 1000$. |
| `D-Hab02-03` | Error en brecha horizontal de la IS | conceptual_swap | high | $\text{Brecha IS} = \Delta A / \alpha$ | La distancia horizontal que se desplaza la curva a tasa constante es el multiplicador keynesiano por el choque autónomo. |
| `D-Hab02-04` | Cálculo erróneo de choque tributario | skipped_step | high | $\Delta A = -\Delta T$ | El impacto en gasto autónomo ante un alza de impuestos está filtrado por la propensión marginal a consumir. |
| `D-Hab02-05` | Estimación del multiplicador fiscal general | conceptual_swap | high | $\alpha_A \approx 7.61$ | El fuerte término de retroalimentación monetaria ($d_2 f_1 / f_2 \approx 2482.1$) comprime drásticamente el multiplicador fiscal general. |
| `D-Hab02-06` | Inversión de brecha LM | conceptual_swap | high | $\text{Brecha LM} = f_1 \Delta(M/P)$ | El desplazamiento horizontal de la LM a tasa constante requiere dividir el cambio monetario entre la sensibilidad al ingreso $f_1$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Parámetros estructurales invariantes ante choques fiscales de magnitud moderada | Garantiza la estabilidad lineal de la matriz de coeficientes del modelo. | - |
| `A-Hab02-02` | - | Transmisión crediticia fluida según las elasticidades calibradas | Asegura la correspondencia entre las tasas de política y el costo de financiamiento de la inversión. | - |

---

### [H-02] Tipo de Cambio Real Bilateral y Tasa de Variación Logarítmica (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 12: Tipo de Cambio Real Bilateral y Tasa de Variación Logarítmica
- **Prerequisites:** None
- **Evidence Citations:** `jijas.pdf` (page 12)

#### Description & Cognitive Model
El tipo de cambio real $\epsilon = \frac{E \cdot P^*}{P}$ mide el precio relativo de los bienes extranjeros expresados en términos de bienes nacionales; su tasa de variación porcentual se aproxima diferenciando logarítmicamente como $\frac{\Delta\epsilon}{\epsilon} \approx \frac{\Delta E}{E} + \pi^* - \pi$, donde $\pi$ y $\pi^*$ son las inflaciones local y externa.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H02-01` | Inversión de precios en tipo real | conceptual_swap | high | $\epsilon = \frac{E \cdot P}{P^*}$ | El producto del tipo nominal por el nivel de precios foráneo convierte los precios externos a moneda local, dividiéndose entre los nacionales. |
| `D-H02-02` | Signo de inflaciones en variación logarítmica | conceptual_swap | high | $\frac{\Delta\epsilon}{\epsilon} \approx \frac{\Delta E}{E} + \pi - \pi^*$ | La inflación interna $P$ figura en el denominador restando poder de compra a la divisa foránea. |
| `D-H02-03` | Confusión entre tipo nominal y real | conceptual_swap | high | $\text{text Devaluación nominal siempre implica}$ | Una alta inflación doméstica neutraliza o revierte la devaluación nominal, encareciendo los bienes locales en términos reales. |
| `D-H02-04` | Convención de cotización invertida | conceptual_swap | high | $E = \text{unidades de divisa por sol}$ | Bajo la convención estándar adoptada, un alza de $E$ significa devaluación o depreciación nominal de la moneda doméstica. |
| `D-H02-05` | Error en producto multiplicativo | conceptual_swap | high | $\frac{\Delta\epsilon}{\epsilon} \approx \frac{\Delta E}{E} \cdot (\pi^* / \pi)$ | La diferenciación de $\ln \epsilon = \ln E + \ln P^* - \ln P$ transforma cocientes en sumas y restas lineales de tasas. |
| `D-H02-06` | Apreciación real y encarecimiento | conceptual_swap | high | $\epsilon \uparrow \Rightarrow \text{apreciación real}$ | Un tipo de cambio real más alto significa que la canasta importada se encarece frente a la producción local. |

---

### [Hab-03] Evaluación Numérica de Desviaciones de la Paridad del Poder Adquisitivo (PPA) (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 14: Evaluación Numérica de Desviaciones de la Paridad del Poder Adquisitivo (PPA)
- **Prerequisites:** H-02
- **Evidence Citations:** `jijas.pdf` (page 14)

#### Description & Cognitive Model
Calcular el tipo de cambio real bilateral entre bienes comerciables mediante la conversión monetaria al tipo de cambio nominal ($\epsilon = \frac{P_{\text{extranjero en moneda local}}}{P_{\text{nacional}}}$) y diagnosticar situaciones de sobrevaluación o subvaluación cambiaria (ejemplo Blanchard Mercedes-Benz vs. Jaguar).

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Inversión en la conversión monetaria | skipped_step | high | $P_{\text{Mercedes en £}} = 50\,000 \times 1.15 = 57\,500 £$ | Si la libra cotiza a $1.15 €$, un monto en euros debe dividirse entre el tipo de cambio para expresarse en libras esterlinas. |
| `D-Hab03-02` | Razón de precios invertida | skipped_step | high | $\epsilon_{\text{Mercedes/Jaguar}} = \frac{30\,000 £}{43\,478.26 £} \approx 0.69$ | El tipo de cambio real del Mercedes respecto al Jaguar mide cuántos Jaguars equivalen a un Mercedes, situando a este último en el numerador. |
| `D-Hab03-03` | Diagnóstico erróneo de arbitraje | conceptual_swap | high | $\epsilon = 1.44 \Rightarrow \text{el bien extranjero es más barato}$ | Un ratio real de $1.44$ indica que comprar el vehículo importado exige un 44% más de esfuerzo adquisitivo que el nacional. |
| `D-Hab03-04` | Omisión de costos de transporte y aranceles | conceptual_swap | high | $\text{text Desviación de PPA implica arbitraje}$ | La presencia de costos de transacción y barreras no arancelarias impide la igualación perfecta de precios internacionales. |
| `D-Hab03-05` | Confusión con el tipo nominal de arbitraje | skipped_step | high | $E_{\text{PPA}} = \frac{30\,000}{50\,000} = 0.60 €/£$ | El tipo de cambio nominal que igualaría los precios absolutos es el cociente del precio en euros sobre el precio en libras. |
| `D-Hab03-06` | Interpretación del tipo de cambio inverso | conceptual_swap | high | $\epsilon_{\text{Jaguar/Mercedes}} = 1.44$ | Desde la perspectiva alemana, un Jaguar británico cuesta el 69% del precio de un Mercedes nacional. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | Homogeneidad en las especificaciones funcionales básicas de los bienes comparados | Permite contrastar valoraciones relativas en mercados de competencia imperfecta. | - |
| `A-Hab03-02` | - | Ausencia de controles prohibitivos a las operaciones de cambio de divisas | Asegura la vigencia de la cotización nominal observada de mercado. | - |

---

### [C-05] Valor Agregado vs. Valor Bruto en Apertura Comercial: Caso Japonés (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 2: Valor Agregado vs. Valor Bruto en Apertura Comercial: Caso Japonés
- **Prerequisites:** H-02
- **Evidence Citations:** `jijas.pdf` (page 2)

#### Description & Cognitive Model
El índice de apertura comercial bruta $ACX = \frac{X}{Y}$ puede superar el $100\%$ sin violar identidades contables porque el PBI ($Y$) mide valor agregado interno mientras las exportaciones ($X$) registran el valor de venta bruto con insumos importados. En contraste, las exportaciones netas $XN = X - IM$ nunca exceden al PBI; economías grandes y diversificadas como Japón presentan $ACX$ bajo ($\approx 15\%$) al absorber internamente gran parte de su cadena productiva.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Paradoja contable inexistente | conceptual_swap | high | $X > Y \text{ es matemáticamente imposible}$ | Un país que ensambla componentes importados caros puede exportar un monto bruto superior a todo su producto generado internamente. |
| `D-C05-02` | Confusión entre exportaciones brutas y netas | conceptual_swap | high | $X - IM \text{ puede superar el 100\% del PBI}$ | El saldo comercial neto representa una fracción del valor agregado y físicamente no puede sobrepasar el producto total. |
| `D-C05-03` | Interpretación del caso japonés | conceptual_swap | high | $\text{text Japón tiene bajo ACX text por ser u}$ | A pesar de ser una superpotencia exportadora, el enorme mercado doméstico japonés consume la gran mayoría de su producción. |
| `D-C05-04` | Impacto del tamaño geográfico en apertura | conceptual_swap | high | $\text{Países gigantes tienen mayor } ACX \text{ que países pequeños}$ | Los centros de redistribución logística y economías de pequeña escala dependen masivamente del comercio exterior frente a países continentales. |
| `D-C05-05` | Uso de logaritmos en exportaciones netas | conceptual_swap | high | $\ln(X - IM) \text{ es aplicable en series con déficit}$ | Las exportaciones netas presentan valores negativos durante etapas de déficit, invalidando el cálculo de logaritmos naturales. |
| `D-C05-06` | Rezagos temporales de exportaciones peruanas | conceptual_swap | high | $\text{text Las exportaciones peruanas impactan}$ | El sector exportador requiere un periodo sostenido de cinco años consecutivos para consolidar su efecto multiplicador en la economía peruana. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Diferenciación estricta entre valor de facturación bruta y valor añadido contable | Evita la doble contabilización en las matrices de insumo-producto. | - |
| `A-C05-02` | - | Registro aduanero estandarizado de bienes en frontera a precios FOB y CIF | Garantiza la consistencia métrica entre agregados del PBI y flujos de comercio exterior. | - |

---

### [C-06] Causalidad Acumulativa de Myrdal y Economía de los Flujos Migratorios (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 10: Causalidad Acumulativa de Myrdal y Economía de los Flujos Migratorios
- **Prerequisites:** C-05
- **Evidence Citations:** `jijas.pdf` (page 10)

#### Description & Cognitive Model
La teoría de causalidad acumulativa de Myrdal explica que las disparidades salariales generan flujos migratorios impulsados por ilusión salarial que desatienden el costo de vida foráneo. En el país receptor, shocks migratorios no absorbidos durante fases contractivas causan 'artritis esclerósica laboral', deprimiendo salarios no calificados, impulsando la informalidad y presionando las finanzas públicas vía mayor gasto en orden y bienes públicos.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Ilusión salarial versus costo de vida | conceptual_swap | high | $\text{text La decisión migratoria optimiza el }$ | Los migrantes suelen comparar salarios nominales brutos sin descontar alquileres elevados, seguros obligatorios y presión tributaria. |
| `D-C06-02` | Efecto migratorio en fase recesiva | conceptual_swap | high | $\text{text La oferta laboral se absorbe automá}$ | En recesión, la incapacidad de absorber excedentes laborales deriva en informalidad y aumento de gasto estatal en contención. |
| `D-C06-03` | Impacto tributario de trabajadores informales | conceptual_swap | high | $\text{text El migrante informal no genera ning}$ | Aunque evadan la tributación directa sobre ingresos, pagan impuestos indirectos sobre todos los bienes y servicios gravados que adquieren. |
| `D-C06-04` | Presión sobre el deflactor del PBI | conceptual_swap | high | $\text{text Mayor población reduce la inflación}$ | Si la demanda de bienes y servicios se expande más rápido que la capacidad instalada y la infraestructura pública, se genera presión en el deflactor. |
| `D-C06-05` | Mecanismo de fuga de divisas | conceptual_swap | high | $\text{text Las remesas fortalecen las reservas}$ | El envío periódico de ahorros al país de origen drena liquidez y divisas del flujo circular del ingreso receptor. |
| `D-C06-06` | Dilema de política pública fiscal | conceptual_swap | high | $\text{text Deportar masivamente carece de cost}$ | Filtrar e integrar formalmente a los migrantes incrementa la recaudación tributaria directa y reduce costes de persecución. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Rigidez a la baja de salarios en el sector formal y segmentación laboral | Fundamenta la canalización del excedente de mano de obra hacia actividades informales. | - |
| `A-C06-02` | - | Existencia de externalidades y congestión en la provisión de bienes públicos | Explica el incremento en los costos de mantenimiento y reposición de infraestructura estatal. | - |

---

### [H-03] Paridad Descubierta de Tasas de Interés (UIP) (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 15: Paridad Descubierta de Tasas de Interés (UIP)
- **Prerequisites:** H-02
- **Evidence Citations:** `jijas.pdf` (page 15)

#### Description & Cognitive Model
La condición exacta de arbitraje financiero internacional iguala los rendimientos esperados en moneda común: $1 + i_t = (1 + i^*_t)\frac{E_t}{E^e_{t+1}}$, cuya aproximación lineal es $i_t \approx i^*_t + \frac{E^e_{t+1} - E_t}{E_t}$, implicando que un alza en la tasa de interés local provoca una apreciación nominal inmediata de la divisa nacional ($E_t \downarrow$) dada una expectativa futura $E^e_{t+1}$ constante.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H03-01` | Relación inversa entre tasas y tipo de cambio spot | conceptual_swap | high | $i_t \uparrow \Rightarrow E_t \uparrow \text{ (depreciación inmediata)}$ | Un mayor rendimiento de los bonos locales atrae capitales financieros que demandan moneda nacional, apreciándola de inmediato. |
| `D-H03-02` | Inversión en el cociente de tipos de cambio | conceptual_swap | high | $1 + i_t = (1 + i^*_t) \frac{E^e_{t+1}}{E_t}$ | El inversor convierte soles a dólares hoy al tipo $1/E_t$, gana $1+i^*_t$ y reconvierte a soles futuros a $E^e_{t+1}$. |
| `D-H03-03` | Signo de la expectativa de depreciación | conceptual_swap | high | $i_t \approx i^*_t - \frac{E^e_{t+1} - E_t}{E_t}$ | Si se espera que la moneda extranjera se encarezca ($E^e_{t+1} > E_t$), la tasa doméstica debe compensar ofreciendo un diferencial positivo. |
| `D-H03-04` | Omisión de la tasa externa | conceptual_swap | high | $i_t = \frac{E^e_{t+1} - E_t}{E_t}$ | El arbitraje exige sumar la tasa de rendimiento libre de riesgo extranjera al cambio esperado de la cotización. |
| `D-H03-05` | Confusión con paridad cubierta | conceptual_swap | high | $\text{text UIP utiliza el tipo de cambio forwa}$ | La paridad descubierta asume exposición al riesgo basada en expectativas racionales o subjetivas futuras, no en coberturas a plazo. |
| `D-H03-06` | Impacto de expectativas futuras sobre el contado | conceptual_swap | high | $E^e_{t+1} \uparrow \Rightarrow E_t \downarrow$ | Una expectativa de depreciación futura desalienta hoy la tenencia de moneda doméstica, depreciándola en el período actual. |

---

### [C-07] Curva IS en Economía Abierta y Doble Canal de Transmisión (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 15: Curva IS en Economía Abierta y Doble Canal de Transmisión
- **Prerequisites:** C-01, H-02, H-03
- **Evidence Citations:** `jijas.pdf` (page 15)

#### Description & Cognitive Model
En economía abierta bajo tipo de cambio flexible, la demanda agregada incorpora las exportaciones netas $NX(Y, Y^*, \epsilon)$ sujetas a la condición Marshall-Lerner. La tasa de interés opera mediante un doble canal contractivo: el canal directo de inversión ($i \uparrow \Rightarrow I \downarrow$) y el canal cambiario-comercial ($i \uparrow \Rightarrow E \downarrow \Rightarrow \epsilon \downarrow \Rightarrow NX \downarrow$), volviendo a la curva IS abierta sustancialmente más plana que en autarquía.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Pendiente relativa de la IS abierta | conceptual_swap | high | $\text{text La curva IS abierta es más empinada}$ | Ante una variación de tasas, el producto reacciona con mayor intensidad en economía abierta porque al ajuste en inversión se suma el del comercio exterior. |
| `D-C07-02` | Falla de la condición Marshall-Lerner | conceptual_swap | high | $\epsilon \downarrow \Rightarrow NX \uparrow \text{ en condiciones estándar}$ | Bajo Marshall-Lerner, la pérdida de competitividad de las exportaciones supera el abaratamiento de importaciones, deteriorando $NX$. |
| `D-C07-03` | Dirección del canal cambiario | conceptual_swap | high | $\text{i uparrow Rightarrow text deprecia la mo}$ | Mayores tasas atraen capitales foráneos apreciando el tipo de cambio y encareciendo la producción nacional frente al resto del mundo. |
| `D-C07-04` | Omisión del producto extranjero | conceptual_swap | high | $Y^* \uparrow \Rightarrow NX \downarrow$ | El crecimiento económico de los socios comerciales expande sus compras de bienes nacionales, desplazando la curva IS hacia la derecha. |
| `D-C07-05` | Efecto de propensión a importar en multiplicador | conceptual_swap | high | $\text{text La apertura comercial amplía el mul}$ | Las importaciones constituyen una filtración adicional del flujo circular de la renta que atenúa el impacto del gasto autónomo. |
| `D-C07-06` | Inversión privada frente a apreciación | conceptual_swap | high | $\text{text El canal cambiario sustituye entera}$ | La tasa de interés continúa encareciendo el crédito corporativo a la vez que la apreciación cambiaria resta demanda externa a las firmas. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Cumplimiento de la condición Marshall-Lerner en el horizonte de análisis | Garantiza que una depreciación real mejore la balanza comercial superando el efecto precio adverso. | - |
| `A-C07-02` | - | Régimen cambiario de flotación limpia sin bandas ni fijaciones bilaterales | Permite que el arbitraje de la UIP ajuste instantáneamente el valor de cotización de la divisa. | - |

---

### [Hab-04] Estática Comparativa de Shocks Macroeconómicos en Economía Abierta con Tipo Flexible (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 16: Estática Comparativa de Shocks Macroeconómicos en Economía Abierta con Tipo Flexible
- **Prerequisites:** C-07, Hab-01
- **Evidence Citations:** `jijas.pdf` (page 16)

#### Description & Cognitive Model
Determinar la dirección de ajuste y equilibrio general de $Y$, $i$, $E$, $C$, $I$ y $NX$ en el modelo Mundell-Fleming con flotación limpia ante shocks fiscales ($\Delta G > 0$), monetarios ($\Delta M > 0$), externos ($\Delta Y^* > 0, \Delta i^* > 0$) y de expectativas cambiarias ($\Delta E^e > 0$).

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Eficacia fiscal bajo tipo flexible y perfecta movilidad | skipped_step | high | $\Delta G > 0 \Rightarrow \Delta Y > 0 \text{ con fuerte expansión sostenida}$ | La expansión fiscal presiona al alza la tasa de interés atrayendo capitales masivos; la apreciación cambiaria destruye $NX$ compensando el impulso fiscal. |
| `D-Hab04-02` | Potencia de la política monetaria | skipped_step | high | $\text{Delta M > 0 Rightarrow text política ine}$ | La baja de tasas provoca salida de capitales y depreciación cambiaria, potenciando las exportaciones y expandiendo decididamente el producto. |
| `D-Hab04-03` | Shock de aumento en tasa internacional | conceptual_swap | high | $\text{Delta i * > 0 Rightarrow text aprecia la}$ | El encarecimiento del rendimiento foráneo deprecia la moneda doméstica, abaratando los productos exportables e impulsando la demanda agregada. |
| `D-Hab04-04` | Impacto en consumo e inversión tras shock fiscal | conceptual_swap | high | $\Delta G > 0 \Rightarrow I \uparrow \text{ inequívocamente}$ | El producto expande el consumo, pero la mayor tasa de interés penaliza la inversión contrarrestando el efecto acelerador. |
| `D-Hab04-05` | Shock de expectativas cambiarias alcistas | conceptual_swap | high | $\Delta E^e > 0 \Rightarrow \text{deprime el producto al generar incertidumbre}$ | Esperar una devaluación futura deprecia de inmediato la cotización al contado, estimulando las exportaciones netas contemporáneas. |
| `D-Hab04-06` | Comportamiento del saldo comercial ante expansión de demanda externa | conceptual_swap | high | $\Delta Y^* > 0 \Rightarrow NX \downarrow \text{ por mayor compra de insumos}$ | El mayor ingreso extranjero tracciona directamente las exportaciones domésticas aumentando la actividad local. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Alta movilidad internacional de capitales privados sin controles cuantitativos | Permite que los diferenciales de rentabilidad muevan intensamente la cotización cambiaria. | - |
| `A-Hab04-02` | - | Estabilidad en las funciones de demanda por importaciones de los socios externos | Asegura la transmisión positiva de las expansiones del PBI mundial hacia las ventas domésticas. | - |

---
