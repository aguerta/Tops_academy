# Informe Técnico Forense: Registro Histórico Consolidado de Problemas que Requirieron Subagentes de Reparación (`c2c_repair`)

**Repositorio Central de Auditorías C2C:** `reports/c2c_audits/reporte_problemas_reparacion_c2c.md`  
**Fecha de Actualización:** `2026-11-02`  
**Arquitectura del Pipeline:** C2C v3.3 (Hardened MapReduce Architecture)  

---

## Índice de Contenidos
1. [Resumen Ejecutivo Multi-Curso](#1-resumen-ejecutivo-multi-curso)
2. [Curso 1: Saul PC Sistemas de Ecuaciones vMapReduce1 (`saul_pc_sistemas_de_ecuaciones_vmapreduce1`)](#2-curso-1-saul-pc-sistemas-de-ecuaciones-vmapreduce1)
   - [2.1. Ola 1: Reparaciones por Discordancias en Arbitraje Ciego (Stage 5)](#21-ola-1-reparaciones-por-discordancias-en-arbitraje-ciego-stage-5)
     - [Caso 1.1: Competencia `Hab-19` (`shard_19_data.py`)](#caso-11-competencia-hab-19-shard_19_datapy---reactivo-sin-contexto-suficiente)
     - [Caso 1.2: Competencia `C-01` (`shard_24_data.py`)](#caso-12-competencia-c-01-shard_24_datapy---ambigüedad-en-definición-de-orden-de-sistema)
     - [Caso 1.3: Competencia `C-18` (`shard_36_data.py`)](#caso-13-competencia-c-18-shard_36_datapy---discordancia-en-relación-dimensional)
   - [2.2. Ola 2: Reparaciones por Bloqueo en Compuerta Pre-Publish (Stage 6)](#22-ola-2-reparaciones-por-bloqueo-en-compuerta-pre-publish-stage-6)
     - [Caso 1.4: Competencia `H-02` (`shard_32_data.py`)](#caso-14-competencia-h-02-shard_32_datapy---multiplicadores-sintéticos-en-curva-de-phillips)
     - [Caso 1.5: Competencia `Hab-23` (`shard_23_data.py`)](#caso-15-competencia-hab-23-shard_23_datapy---colisión-con-cota-de-estabilidad-de-cournot)
3. [Curso 2: Estadística 3 S9 vMapReduce13 (`estadistica_3_s9_vmapreduce13`)](#3-curso-2-estadística-3-s9-vmapreduce13)
   - [Caso 2.1: Competencia `Hab-03` (`shard_03_data.py`)](#caso-21-competencia-hab-03-shard_03_datapy---razones-constantes-sobre-ans)
   - [Caso 2.2: Competencia `C-23` (`shard_31_data.py`)](#caso-22-competencia-c-23-shard_31_datapy---conflicto-matemático-intrínseco-n---4n)
4. [Matriz Taxonómica Comparativa de Errores y Linters](#4-matriz-taxonómica-comparativa-de-errores-y-linters)
5. [Protocolo de Desbloqueo y Directivas Antiestancamiento](#5-protocolo-de-desbloqueo-y-directivas-antiestancamiento)
6. [Hitos de Reingeniería para Eliminación de Olas Tardías](#6-hitos-de-reingeniería-para-eliminación-de-olas-tardías)

---

## 1. Resumen Ejecutivo Multi-Curso

Este documento recopila de manera forense y sistemática **todos los problemas detectados en las distintas ejecuciones del pipeline C2C que requirieron la intervención de ingenieros de reparación quirúrgica (`c2c_repair`)**, documentando:
- La causa raíz exacta a nivel de código fuente y modelo conceptual.
- El síntoma o linter que activó la alarma.
- La solución matemática, pedagógica y de implementación adoptada por cada subagente.
- El tiempo de resolución y las lecciones aprendidas para evitar regresiones.

### Tabla Comparativa de Ejecuciones con Remediación

| Curso | Total Comps / Shards | Ítems en Banco | Fase de Activación | Subagentes `c2c_repair` | Causa Principal | Estado Final |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`saul_pc_sistemas_de_ecuaciones_vmapreduce1`** | 56 / 40 | 1,350 | • Stage 5 (Jueces)<br>• Stage 6 (Quality Gate) | **5 subagentes**<br>(`Hab-19`, `C-01`, `C-18`, `H-02`, `Hab-23`) | • Ambigüedad en stems de orden y contexto de solución particular.<br>• Colisión con multiplicadores prohibidos (`[DIAG-MAGIC-MULT]`). | ✅ Publicado (100% PASS) |
| **`estadistica_3_s9_vmapreduce13`** | 51 / 33 | 1,170 | • Stage 6 (Quality Gate) | **2 subagentes**<br>(`Hab-03`, `C-23`) | • Distractores con razones constantes sobre `ans`.<br>• Conflicto matemático intrínseco en reducción proporcional ($n \to 4n$). | ✅ Publicado (100% PASS) |

---

## 2. Curso 1: Saul PC Sistemas de Ecuaciones vMapReduce1

**Identificador:** `saul_pc_sistemas_de_ecuaciones_vmapreduce1`  
**Conversación Orquestadora:** [`d2bdb524-f682-4e86-b7a3-a13d5e708bf9`](conversation://d2bdb524-f682-4e86-b7a3-a13d5e708bf9)  
**Dominio Temático:** Sistemas de Ecuaciones Diferenciales Ordinarias (EDOs) y en Diferencias (EEDs), Estabilidad Dinámica, Autovalores y Modelos Económicos (Phillips-Phelps, Duopolio de Cournot).

---

### 2.1. Ola 1: Reparaciones por Discordancias en Arbitraje Ciego (Stage 5)

En la etapa de verificación ciega concurrente con 10 jueces (`c2c_judge`), se evaluaron 120 reactivos estratificados sin claves de respuesta. El arbitraje determinó una tasa de acuerdo inicial del **96.7% (116/120)**, registrando 4 discordancias que bloquearon la certificación inmediata en 3 competencias: `Hab-19`, `C-01` y `C-18`.

```
======================================================================
[AUX STAGE: JUDGE-COMPARE] Comparing blind judge evaluations vs Ground Truth
======================================================================
  [+] Judge comparison finished with status: DISCORDANCES
  [+] Agreement rate: 96.7% (116/120)
  [!] Disagreements detected: 4
      * [T-Hab19-03_judge_1] template=T-Hab19-03 (Hab-19)
      * [T-C01-01_judge_1] template=T-C01-01 (C-01)
      * [T-C01-03_judge_2] template=T-C01-03 (C-01)
      * [T-C18-01_judge_2] template=T-C18-01 (C-18)
```

---

#### Caso 1.1: Competencia `Hab-19` (`shard_19_data.py`) — Reactivo sin Contexto Suficiente

- **Subagente:** `Repair Engineer Hab-19` (`47cdc4d8-0971-491c-946b-dde9c9e3c9f6`)
- **Plantilla Afectada:** `T-Hab19-03` (Tipo: `fill_in_the_blank`)
- **Archivo Objetivo:** `courses/saul_pc_sistemas_de_ecuaciones_vmapreduce1/work/shards/shard_19_data.py`
- **Diagnóstico del Fallo:**
  - El evaluador independiente emitió: `BLOCKED: Reactivo carece de contexto` en lugar del valor numérico esperado `136`.
- **Causa Raíz:**
  La plantilla evaluaba la solución temporal $X_t = X_{h,t} + X_{p,t}$ de un sistema acoplado en diferencias finitas. Las variantes de stem en `s3` y `s2` daban por sentada la tasa de forzamiento exógeno y omitían explicitar las ecuaciones dinámicas completas del sistema o la forma de ensayo de la solución particular, obligando al juez a adivinar las hipótesis implícitas del generador. Al no disponer de un enunciado autosuficiente, el protocolo del juez ciego dictó correctamente el bloqueo del ítem.
- **Solución Implementada por el Repair Engineer:**
  1. Se reescribieron quirúrgicamente los stems de `s3` y `s2` en `shard_19_data.py` utilizando `edit_file`.
  2. Se explicitó la formulación matemática integral: la matriz de transición simétrica $A$, el vector de términos independientes $B(t) = B_0 \cdot \mu^t$, el forzamiento exponencial y la forma de la solución particular ensayada $X_{p,t} = K \mu^t$.
  3. Se mantuvo el verificador analítico `ver_hab19_3(res)` validando que la solución particular satisficiera $( \mu I - A ) K = B_0$.
  4. Certificación: `compile_shard.py` arrojó `PASS` en 50 semillas deterministas sin advertencias.

---

#### Caso 1.2: Competencia `C-01` (`shard_24_data.py`) — Ambigüedad en Definición de Orden de Sistema

- **Subagente:** `Repair Engineer C-01` (`a7b7ccf5-712b-4ab4-beb4-0fafc891533b`)
- **Plantillas Afectadas:** `T-C01-01` y `T-C01-03` (Tipo: `multiple_choice_7_options`)
- **Archivo Objetivo:** `courses/saul_pc_sistemas_de_ecuaciones_vmapreduce1/work/shards/shard_24_data.py`
- **Diagnóstico del Fallo:**
  - En `T-C01-01_judge_1`: Juez seleccionó `'F'` (letra F) esperando `'E'` ($n = 29$).
  - En `T-C01-03_judge_2`: Juez seleccionó `'A'` (letra A) esperando `'B'` ($n = 23$).
- **Causa Raíz:**
  Conflicto semántico en la definición curricular del orden de un sistema de EDOs. En sistemas donde distintas ecuaciones tienen órdenes dispares (ej. $y_1^{(29)} + y_2'' = 0$ y $y_2' + y_1 = 0$), el curso define en su CTA que el **orden del sistema es la derivada de mayor orden que figure en cualquiera de sus ecuaciones** ($\max_{j,k} \{ \text{orden de } y_j^{(k)} \} = 29$).  
  Sin embargo, los enunciados de `T-C01-01` y `T-C01-03` formulaban la pregunta de manera ambigua, permitiendo que el evaluador ciego interpretara el orden del sistema como la **dimensión del espacio de estados equivalente** (la suma de los órdenes máximos de cada variable dependiente: $29 + 2 = 31$, o $23 + 5 + 4 = 32$), seleccionando las opciones distractoras que reflejaban dicha suma.
- **Solución Implementada por el Repair Engineer:**
  1. Se editaron quirúrgicamente los stems de `C-01` en `shard_24_data.py` para precisar sin ambigüedad: *"determine el orden formal del sistema de ecuaciones diferenciales, definido canónicamente como el orden de la derivada más alta que aparece en cualquiera de sus ecuaciones constituyentes"*.
  2. Se ajustaron los distractores para mantener diagnóstica la confusión entre orden máximo vs suma de órdenes, pero eliminando la posibilidad de interpretación dual del enunciado.
  3. Certificación: `compile_shard.py` validó las 3 plantillas (`T-C01-01`, `T-C01-02`, `T-C01-03`) arrojando `PASS` con estricta adherencia Form-B Tri-Banda.

---

#### Caso 1.3: Competencia `C-18` (`shard_36_data.py`) — Discordancia en Relación Dimensional

- **Subagente:** `Repair Engineer C-18` (`54dd361b-0df5-452d-bec5-e380b60cfccf`)
- **Plantilla Afectada:** `T-C18-01` (Tipo: `multiple_choice_7_options`)
- **Archivo Objetivo:** `courses/saul_pc_sistemas_de_ecuaciones_vmapreduce1/work/shards/shard_36_data.py`
- **Diagnóstico del Fallo:**
  - El juez seleccionó `'B'` en lugar de `'E'` ($m = 53p$).
- **Causa Raíz:**
  En la reducción matricial de sistemas de orden superior a sistemas de primer orden, el número total de variables de estado viene dado por la suma de órdenes $m = \sum n_i$. En el generador de `T-C18-01`, una opción distractora formulaba una notación sintáctica muy similar a la correcta respecto al producto $n \cdot p$, lo que generó colisión en la interpretación de los subíndices de la matriz compañera.
- **Solución Implementada por el Repair Engineer:**
  1. Se refinó la expresión algebraica de las opciones en `shard_36_data.py` distinguiendo nítidamente el número de ecuaciones dependientes del orden de cada ecuación.
  2. Se certificaron las 3 plantillas de la competencia con `compile_shard.py` obteniendo `PASS`.

---

### 2.2. Ola 2: Reparaciones por Bloqueo en Compuerta Pre-Publish (Stage 6)

Tras resolver las 4 discordancias y re-arbitrar con éxito el 100% de las plantillas, el orquestador intentó la publicación formal mediante `run.py --stage publish`. En este punto, la compuerta psicométrica estricta `PublishQualityGateError` abortó la publicación:

```
ERROR: Publish Quality Gate Rejected Publication:
  - Critical audit issues detected (2): 
    [diagnostic_rationale_alignment_linter] Distractores numéricos sintéticos por multiplicador arbitrario ([1.333, 1.667]) con error_rationale desconectado del cálculo real.
    [diagnostic_rationale_alignment_linter] Distractores numéricos sintéticos por multiplicador arbitrario ([0.45, 1.333]) con error_rationale desconectado del cálculo real.
  - Affected Shards: shard_23, shard_32
  - Competencies: H-02, Hab-23
```

---

#### Caso 1.4: Competencia `H-02` (`shard_32_data.py`) — Multiplicadores Sintéticos en Curva de Phillips

- **Subagente:** `Repair Engineer H-02` (`46c43464-6e1c-4321-ac77-80cfa11fec1f`)
- **Plantilla Afectada:** `T-H02-01` (Función generadora: `gen_h02_1`, L205)
- **Linter Infraccionado:** `[DIAG-MAGIC-MULT / diagnostic_rationale_alignment_linter]`
- **Archivo Objetivo:** `courses/saul_pc_sistemas_de_ecuaciones_vmapreduce1/work/shards/shard_32_data.py`
- **Diagnóstico del Fallo:**
  El generador construía distractores numéricos para la tasa de inflación efectiva $p = (\alpha - T) - \beta U + g\pi$ escalando el valor correcto `ans` por constantes fijas o colisionando numéricamente con los factores prohibidos `[1.333, 1.667]` ($4/3$ y $5/3$).
- **Incidente de Estancamiento (Straggler):**
  Durante los primeros 5 minutos, el subagente se desvió de su scope leyendo exhaustivamente fragmentos de `cta.json`. El Director de Proyecto intervino mediante `send_message`, prohibiendo lecturas externas y ordenando la edición directa sobre `shard_32_data.py`.
- **Solución Implementada:**
  1. Inmediatamente tras la directiva, el subagente ejecutó `edit_file` sobre `shard_32_data.py`.
  2. Sustituyó cualquier factor multiplicativo sobre `ans` por cálculos derivados de concepciones erróneas auténticas:
     - Error en signo de desempleo: $p_1 = (\alpha - T) + \beta U + g\pi$.
     - Omisión de la tasa de productividad: $p_2 = \alpha - \beta U + g\pi$.
     - Traspaso unitario erróneo de expectativas ($g = 1$ en vez de $g < 1$).
     - Confusión entre tasa y nivel de precios.
  3. Agregó un filtro en la desduplicación garantizando que $|d - round(ans \cdot m, 3)| > 0.0015$ para todo $m \in \{1.333, 1.667, \dots\}$.
  4. Certificación: `compile_shard.py` otorgó `PASS`.

---

#### Caso 1.5: Competencia `Hab-23` (`shard_23_data.py`) — Colisión con Cota de Estabilidad de Cournot

- **Subagente:** `Repair Engineer Hab-23` (`9b16a916-f37f-401a-ad66-7abf9940aa8f`)
- **Plantilla Afectada:** `T-Hab23-01` (Función generadora: `gen_hab23_1`, L3..L38)
- **Linter Infraccionado:** `[DIAG-MAGIC-MULT / diagnostic_rationale_alignment_linter]`
- **Archivo Objetivo:** `courses/saul_pc_sistemas_de_ecuaciones_vmapreduce1/work/shards/shard_23_data.py`
- **Diagnóstico del Fallo:**
  En el duopolio de Cournot con velocidad de ajuste simétrica $d$, la matriz de transición es $A = \begin{bmatrix} 1-d & -d/2 \\ -d/2 & 1-d \end{bmatrix}$ con autovalores $\lambda_1 = 1 - d/2$ y $\lambda_2 = 1 - 3d/2$. La estabilidad exige $|\lambda_2| < 1 \Rightarrow 0 < d < 4/3$.  
  El generador incluía distractores con valores derivados de $1 - d$ (para $d = 0.55 \Rightarrow 0.45$) y cotas que igualaban $4/3 \approx 1.333$. El linter psicométrico detectó que los distractores coincidían con las razones prohibidas `[0.45, 1.333]`.
- **Incidente de Estancamiento (Straggler):**
  Al igual que en `H-02`, el subagente demoró intentando parsear `cta.json`. Fue destrabado con el mensaje analítico del Director.
- **Solución Implementada:**
  1. Modificó `shard_23_data.py` reestructurando los distractores de `gen_hab23_1`.
  2. Los errores se reformularon en términos cualitativos y algebraicos rigurosos:
     - Confundir la estabilidad simultánea con la estabilidad del autovalor no restrictivo ($0 < d < 4$).
     - Signos erróneos en las pendientes de las curvas de reacción rivales ($+d/2$ en lugar de $-d/2$).
     - Autovalores desacoplados falsos $(1-d, 1+d)$.
  3. Se eliminaron todas las operaciones que producían razones coincidentes con $0.45$ y $1.333$.
  4. Certificación: `compile_shard.py` emitió `PASS` de inmediato.

---

## 3. Curso 2: Estadística 3 S9 vMapReduce13

**Identificador:** `estadistica_3_s9_vmapreduce13`  
**Conversación Orquestadora:** [`b82c4415-eb81-44a5-b31e-e1094de6b645`](conversation://b82c4415-eb81-44a5-b31e-e1094de6b645)  
**Dominio Temático:** Estadística Inferencial Asintótica, Estimadores MCO/IV, Convergencia en Probabilidad, Teorema Central del Límite e Intervalos de Confianza para Proporciones.

---

### Caso 2.1: Competencia `Hab-03` (`shard_03_data.py`) — Razones Constantes sobre `ans`

- **Subagente:** `Repair Engineer Hab-03` (`f3ed7c`)
- **Tiempo de Resolución:** 170.0 segundos (2.8 min) — 9 turnos
- **Plantilla Afectada:** `T-Hab03-01` (`gen_hab03_1`, L6..L23)
- **Linter Infraccionado:** `[DIAG-MAGIC-MULT]`
- **El Problema:**
  Los distractores $d_3$ y $d_4$ se generaban mediante:
  $$d_3 = \text{round}(\mu / (2\delta), 4) \quad \text{y} \quad d_4 = \text{round}(\mu / (3\delta), 4)$$
  Dado que la respuesta correcta era $ans = \text{round}(\mu / \delta, 4)$, las razones resultantes eran algebraicamente idénticas a constantes prohibidas:
  $$\frac{d_3}{ans} = 0.500 \quad \text{y} \quad \frac{d_4}{ans} = 0.333$$
- **Solución Implementada:**
  Se sustituyeron las fórmulas por pasos erróneos de derivación asintótica (omisión de la corrección por varianza asintótica en el numerador, confusión entre desviación estándar y varianza $\delta^2$). Se agregó una guarda que verifica $|d / ans - m| > 0.02$. Certificado en primer intento.

---

### Caso 2.2: Competencia `C-23` (`shard_31_data.py`) — Conflicto Matemático Intrínseco ($n \to 4n$)

- **Subagente:** `Repair Engineer C-23` (`b1d31f`)
- **Tiempo de Resolución:** 382.0 segundos (6.4 min) — 18 turnos (Straggler crítico)
- **Plantillas Afectadas:** `T-C23-01` y `T-C23-03`
- **Linter Infraccionado:** `[DIAG-MAGIC-MULT]`
- **El Problema:**
  En el cálculo del margen de error para proporciones ($ME = z \sqrt{\frac{p(1-p)}{n}}$):
  1. En `T-C23-01`: Cuando la proporción oscilaba entre $0.20$ y $0.45$, combinaciones de varianzas erróneas generaban razones accidentales cercanas a $0.50$ y $0.75$.
  2. En `T-C23-03`: Al cuadruplicar la muestra ($n \to 4n$), el error correcto se reduce a la mitad ($ME_{nuevo} = ME / 2$). El distractor pedagógico legítimo de asumir linealidad dividiendo entre 4 producía:
     $$d = \frac{ME}{4} = \frac{1}{2} \cdot ans = 0.500 \cdot ans$$
     Colisionaba de forma matemática inevitable con el factor $0.50$.
- **Solución Implementada:**
  1. En `gen_c23_1`: Se reemplazó el cuantil $z=1.00$ por $z=1.645$ (confianza al 90%), desplazando la razón a $0.839$, fuera del rango de colisión.
  2. En `gen_c23_3`: Se sustituyó la división entre 4 por el error conceptual de calcular el margen considerando únicamente el *incremento muestral* ($\Delta n = 4n - n = 3n$), generando una razón $\sqrt{4/3} \approx 1.155 \cdot ans$, matemáticamente rica y libre de colisiones.

---

## 4. Matriz Taxonómica Comparativa de Errores y Linters

| Código de Error / Linter | Mecanismo de Detección | Causa Subyacente Típica | Solución Canónica Demostrada |
| :--- | :--- | :--- | :--- |
| **`[DIAG-MAGIC-MULT]`** | `diagnostic_rationale_alignment_linter` analiza 50 semillas; calcula $\min \|d - ans \cdot m\|$ contra lista negra $\{0.333, 0.5, 0.667, 0.75, 1.25, 1.333, 1.5, 1.667, \dots\}$. | • Creación perezosa de distractores multiplicando `ans` por constantes.<br>• Coincidencia accidental por la física/matemática del problema ($n \to 4n \Rightarrow 1/2$, o cotas como $4/3$). | • Modelar el distractor mediante la fórmula del paso algebraico equivocado real.<br>• Cambiar parámetros estructurales ($z=1.645$, $\Delta n = 3n$) para desplazar la razón lejos de los múltiplos prohibidos. |
| **`BLOCKED: Reactivo carece de contexto`** | Subagente `c2c_judge` (evaluador ciego) no puede resolver el problema desde primeros principios. | Enunciado incompleto en stems; omisión de matrices dinámicas, tasas exógenas o condiciones iniciales necesarias para el cálculo. | Reescribir stems explicitando formalmente el modelo matemático, parámetros exógenos y formas funcionales completas. |
| **`Discordancia de Arbitraje (Judge vs GT)`** | Comparación estricta entre respuesta de jueces ciegos y clave generada (`judge-compare`). | Ambigüedad en definiciones conceptuales (ej. orden máximo de derivación vs dimensión del espacio de estados). | Clarificar en el stem la convención curricular exacta evaluada sin delatar la respuesta ni usar coletillas delatoras. |
| **`Straggler por Scope-Creep`** | Watchdog del Director detecta inactividad o consumo de tiempo excesivo en fase pre-compile. | Subagente de reparación lee archivos masivos (`cta.json`, `course.json`) fuera de su scope autorizado. | Envío inmediato de directiva analítica `send_message` instruyendo edición directa con `edit_file` y compilación local. |

---

## 5. Protocolo de Desbloqueo y Directivas Antiestancamiento

Durante la ejecución de reparaciones en ambos cursos, se consolidó la **Regla de Intervención del Director**:

1. **Watchdog Activo a los 7–10 Minutos:**
   Si un subagente `c2c_repair` supera los 5–7 minutos sin reportar `DONE:`, el Director audita de inmediato su `transcript.jsonl`.
2. **Detección Temprana de Lecturas Prohibidas:**
   Si el transcript revela que el subagente está leyendo archivos globales como `cta.json` (más de 300 KB) o intentando parsear el curso completo, el Director emite de inmediato un mensaje analítico:
   ```python
   send_message(
       Recipient=cid,
       Message="ALERTA: Tienes PROHIBIDO leer cta.json. Ve directo al grano: edita con edit_file la función [fn] en [shard_data.py], aplica las fórmulas algebraicas reales, ejecuta compile_shard.py y reporta DONE."
   )
   ```
3. **Efectividad Comprobada:**
   En los casos de `H-02` y `Hab-23` en el curso de sistemas de ecuaciones, la directiva destrabó ambos subagentes, logrando que completaran la edición y la compilación exitosa en menos de 2 minutos tras recibir el mensaje.

---

## 6. Hitos de Reingeniería para Eliminación de Olas Tardías

Para evitar que las reparaciones ocurran de manera tardía en Stage 6, se ratifican los siguientes hitos de reingeniería arquitectónica:

1. **Shift-Left de `[DIAG-MAGIC-MULT]` a Stage 3 (Autores):**
   Incorporar la verificación exhaustiva de multiplicadores sintéticos (50 semillas) directamente en `compile_shard.py`, para que el autor del shard detecte y corrija las colisiones antes de entregar su archivo, eliminando la necesidad de despachar `c2c_repair` en la compuerta final.
2. **Ejecución Concurrente de Gates de Stage 4 y Jueces Ciegos (Stage 5):**
   Disparar en paralelo los Plan Judges y los escáneres psicométricos globales de Stage 4. Si se detectan objeciones de jueces y colisiones de linters, se consolidan en una **única matriz de reparación por shard**, ejecutando una sola ola consolidada de subagentes `c2c_repair`.
3. **Re-Arbitraje Quirúrgico Exclusivo:**
   Si una reparación altera el contenido pedagógico evaluado por un juez, se re-evalúa únicamente esa competencia puntual mediante un juez quirúrgico individual, sin re-despachar lotes masivos de 10 jueces.
4. **Validación Formal Obligatoria del Orquestador:**
   El Director nunca asume el éxito ciego tras el reporte de un subagente; siempre re-ejecuta formalmente el ciclo de compilación, construcción y compuerta de publicación (`run.py --stage publish`) para certificar la integridad psicométrica del banco.
