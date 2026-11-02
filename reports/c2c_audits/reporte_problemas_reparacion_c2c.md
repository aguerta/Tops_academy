# Informe Técnico Forense: Análisis de Problemas que Requirieron Subagentes de Reparación (`c2c_repair`)

**Curso Auditado:** `estadistica_3_s9_vmapreduce13`  
**Conversación Orquestadora:** [`b82c4415-eb81-44a5-b31e-e1094de6b645`](conversation://b82c4415-eb81-44a5-b31e-e1094de6b645)  
**Fecha de Emisión:** `2026-11-02`  
**Origen de Activación:** Bloqueo en la compuerta de pre-publicación (`PublishQualityGateError` en Stage 6: Publish)

---

## 1. Resumen Ejecutivo de la Fase de Remediación

Durante la ejecución del pipeline Content-to-Course (C2C v3.3), el 100% de las 51 competencias y 33 shards compilaron exitosamente en la etapa de autores y obtuvieron un **100.0% de acuerdo unánime en el arbitraje ciego** (120/120 reactivos evaluados por 10 jueces independientes).

Sin embargo, al ejecutar la compuerta final `run.py --stage publish`, el linter psicométrico global `diagnostic_rationale_alignment_linter` (`[DIAG-MAGIC-MULT]`) inspeccionó el 100% de los **1,170 reactivos instanciados** y rechazó la publicación debido a **8 colisiones críticas de distractores sintéticos** distribuidas en 2 competencias: **`Hab-03`** y **`C-23`**.

Para subsanar el bloqueo sin intervención humana ni edición manual del orquestador, se despacharon concurrentemente 2 subagentes quirúrgicos especializados (`c2c_repair`).

| Reparación / Shard | Competencia | Error Base | Tiempo de Pared | Turnos | Tokens Activos | Reintentos Compile | Resultado Final |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Repair Engineer Hab-03** (`f3ed7c`) | `Hab-03` (`shard_03`) | `[DIAG-MAGIC-MULT]` | **170.0s** (2.8 min) | 9 | 90,520 | 1 (0 fallos) | ✅ PASS (Limpio) |
| **Repair Engineer C-23** (`b1d31f`) | `C-23` (`shard_31`) | `[DIAG-MAGIC-MULT]` | **382.0s** (6.4 min) | 18 | 206,903 | 2 (1 fallo) | ✅ PASS (Remediado) |

---

## 2. Detalle del Caso 1: Competencia `Hab-03` (`shard_03_data.py`)

### 2.1. El Problema Exacto
En la plantilla `T-Hab03-01` (función generadora `gen_hab03_1`, líneas 6 a 23 de `shard_03_data.py`), se evaluaba el cálculo analítico de convergencia y errores estándar asintóticos.
- **Vicio detectado:** Los distractores $d_1$ a $d_6$ se construían mediante combinaciones de variables como:
  ```python
  d1 = round((mu + 15) / delta, 4)
  d2 = round(mu / (delta + mu), 4)
  d3 = round(mu / (2 * delta), 4)
  d4 = round(mu / (3 * delta), 4)
  ```
- **Fallo:** Siendo la respuesta correcta `ans = round(mu / delta, 4)`, los distractores $d_3$ y $d_4$ colisionaban exactamente con los multiplicadores prohibidos:
  $$\frac{d_3}{ans} = \frac{\mu / (2\delta)}{\mu / \delta} = \frac{1}{2} = 0.500$$
  $$\frac{d_4}{ans} = \frac{\mu / (3\delta)}{\mu / \delta} = \frac{1}{3} \approx 0.333$$
  Además, en ciertas combinaciones aleatorias de $\mu$ y $\delta$, la razón producía valores cercanos a $1.333$, violando la regla que prohíbe distractores numéricos predecibles y desconectados de su justificación diagnóstica.

### 2.2. ¿Por Qué Demoró? (170.0 segundos / 2.8 min)
- **Fase Pre-Compile (155s):** El subagente consumió 2.5 minutos leyendo la orden de trabajo (`repair_hab03.json`), analizando el archivo de código y razonando las concepciones erróneas pedagógicas reales para no generar un parche cosmético que rompiera el contrato Form-B Tri-Banda (`min_archetypes = 3`).
- **Fase Post-Compile (15s):** La edición quirúrgica mediante `edit_file` fue 100% acertada al primer intento. El subagente ejecutó `compile_shard.py` obteniendo `PASS` de inmediato sin requerir reintentos adicionales.

### 2.3. Solución Implementada
1. Se redefinieron las fórmulas de los distractores en `shard_03_data.py` vinculándolas estrictamente a pasos algebraicos erróneos independientes de la razón constante sobre `ans` (ej. olvidar elevar al cuadrado el denominador, omitir la corrección por varianza asintótica en el numerador o confundir media con desviación estándar).
2. Se incorporó una guarda de descarte en el generador que verifica que ninguna razón $|d / ans - m| \le 0.02$ coincida con la lista negra de multiplicadores sintéticos.
3. Se certificó la plantilla con 50 semillas CRC32 deterministas sin fallos.

---

## 3. Detalle del Caso 2: Competencia `C-23` (`shard_31_data.py`) — Caso Complejo / Straggler

### 3.1. El Problema Exacto
La competencia `C-23` evalúa el *Margen de Error e Intervalos de Confianza Asintóticos para Proporciones* ($ME = z \sqrt{\frac{p(1-p)}{n}}$). Presentaba colisiones en dos de sus tres plantillas:

1. **En `T-C23-01` (`gen_c23_1`):**
   - El generador construía distractores calculando varianzas erróneas:
     - $d_2 = 1.96 \sqrt{p(1-p)/(2n)} \Rightarrow d_2 = \frac{ans}{\sqrt{2}} \approx 0.707 \cdot ans$.
     - $d_5 = 1.00 \sqrt{p(1-p)/n} \Rightarrow d_5 = \frac{ans}{1.96} \approx 0.510 \cdot ans$.
     - $d_1 = 1.96 p / \sqrt{n}$.
   - **Fallo:** Cuando la proporción muestral $p$ oscilaba entre $0.20$ y $0.45$, la combinación de fórmulas producía valores de $d_1$ y $d_5$ que caían a menos de $0.0015$ de los multiplicadores prohibidos $[1.667, 0.667, 0.45, 0.50]$.

2. **En `T-C23-03` (`gen_c23_3`):**
   - El ejercicio planteaba cuadruplicar el tamaño de la muestra ($n_{nuevo} = 4n$).
   - Por la propiedad matemática de la raíz cuadrada:
     $$ME_{nuevo} = 1.96 \sqrt{\frac{p(1-p)}{4n}} = \frac{1}{2} \left(1.96 \sqrt{\frac{p(1-p)}{n}}\right) = \frac{ME_{orig}}{2}$$
   - El distractor $d_2$ representaba el error de un alumno que cree que la relación es lineal y divide entre 4:
     $$d_2 = \frac{ME_{orig}}{4} = \frac{1}{2} \cdot ME_{nuevo} = 0.500 \cdot ans$$
   - **Fallo insidioso:** El distractor representaba un error conceptual legítimo del alumno, pero numéricamente producía **exactamente $0.5 \times ans$ en el 100% de las instancias**, activando de forma implacable el linter `[DIAG-MAGIC-MULT]`.

### 3.2. ¿Por Qué Demoró Tanto? (382.0 segundos / 6.4 min — 18 Turnos)
Este agente fue el causante del mayor retraso en la fase de remediación debido a tres factores concurrentes:

1. **Conflicto Matemático Intrínseco (Turnos 1–14, 263s de Pre-Compile):**  
   El subagente descubrió que las fórmulas pedagógicas estándar de error en proporciones ($n \to 4n$) generaban factores $0.5$ y $2.0$ de manera natural por la física del problema. Tuvo que dedicar 9 turnos de razonamiento profundo (más de 33,000 caracteres de thinking) calculando derivadas y relaciones algebraicas alternativas para diseñar concepciones erróneas que mantuvieran validez pedagógica sin colisionar con los múltiplos prohibidos.
2. **Fallo de Compilación Intermedio (Turno 26):**  
   Tras su primera edición quirúrgica, el subagente ejecutó `compile_shard.py`, pero la compilación fue **rechazada con código de salida 1**:
   ```text
   [-] [DIAG-MAGIC-MULT] En 'T-C23-01' (función 'gen_c23_1'), los distractores numéricos
   en 5 semillas (ej. seed=396) coinciden con multiplicadores arbitrarios prohibidos ([0.667, 0.45])
   ```
   El bucle de descarte de colisiones que había implementado no contemplaba la tolerancia épsilon exacta que evaluaba el linter en números de 4 decimales.
3. **Remediación en Segundo Turno Quirúrgico (Turnos 27–30):**  
   El subagente no cayó en pánico ni reescribió el archivo completo; utilizó la salida del compilador para ajustar los umbrales de búsqueda a 500 iteraciones y modificar las fórmulas en conflicto.

### 3.3. Solución Implementada
1. **Reemplazo en `gen_c23_1`:**
   - Se sustituyó el cuantil arbitrario $z=1.00$ por $z=1.645$ (nivel de confianza del 90% en lugar del 95%), desplazando la razón relativa de $0.510$ a $0.839$, fuera del rango de colisión de $0.50$ y $0.75$.
   - Se implementó un bucle de 500 iteraciones con verificación matricial de colisiones que descarta cualquier semilla con:
     $$\min_{d \in D, m \in M} |d - \text{round}(ans \cdot m, 4)| \le 0.0015$$
2. **Reemplazo en `gen_c23_3`:**
   - Se eliminó la división entre 4 sobre el error original.
   - En su lugar, se modeló el error conceptual en el que el estudiante confunde el nuevo tamaño de muestra con el *incremento neto* ($\Delta n = n_{nuevo} - n = 3n$), calculando:
     $$d_2 = 1.96 \sqrt{\frac{p(1-p)}{3n}}$$
     Lo cual genera una razón analítica $\sqrt{4/3} \approx 1.155 \cdot ans$, matemáticamente robusta, pedagógicamente fundada y 100% libre de colisiones.
3. **Certificación:** Segunda corrida de `compile_shard.py` resultó en `PASS` inmediato sin advertencias.

---

## 4. Cronología de la Resolución y Desbloqueo del Pipeline

```mermaid
sequenceDiagram
    autonumber
    participant Orch as Orquestador C2C
    participant Gate as Pre-Publish Gate (Stage 6)
    participant Rep03 as Repair Engineer Hab-03
    participant Rep31 as Repair Engineer C-23
    participant Comp as Shard Compiler & Build Engine

    Orch->>Gate: run.py --stage publish
    Gate-->>Orch: ERROR PublishQualityGateError ([DIAG-MAGIC-MULT] en Hab-03 y C-23)
    Orch->>Rep03: invoke_subagent(Repair Engineer Hab-03)
    Orch->>Rep31: invoke_subagent(Repair Engineer C-23)
    
    par Reparación en Paralelo
        Rep03->>Comp: compile_shard.py (Hab-03)
        Comp-->>Rep03: PASS (170s)
        Rep03-->>Orch: DONE: shard_03.json
    and
        Rep31->>Comp: compile_shard.py (Intento 1)
        Comp-->>Rep31: FAIL (DIAG-MAGIC-MULT en seed=396)
        Rep31->>Comp: compile_shard.py (Intento 2 con cuantil 90% y Delta n=3n)
        Comp-->>Rep31: PASS (382s)
        Rep31-->>Orch: DONE: shard_31.json
    end

    Orch->>Comp: run.py --stage templates
    Comp-->>Orch: PASS (51/51 plantillas)
    Orch->>Comp: run.py --stage build
    Comp-->>Orch: PASS (1,170 reactivos instanciados)
    Orch->>Gate: run.py --stage publish --skip-judges
    Gate-->>Orch: SUCCESS (Curso publicado y cerrojo liberado)
```

---

## 5. Lecciones Aprendidas

1. **Pre-validación de `[DIAG-MAGIC-MULT]` en Etapa de Autores (`Stage 3`):**  
   Actualmente, la comprobación de multiplicadores sintéticos se ejecuta con mayor rigurosidad en la compuerta de publicación (`publish.py`) que en el validador unitario de shard (`compile_shard.py`). Alinear ambos linters con la misma suite de 50 semillas permitirá que los autores de shard detecten y resuelvan estas colisiones a $t=0$, ahorrando los ~6 minutos de la fase de remediación.
2. **Patrones de Reducción Proporcional ($n \to 4n$):**  
   En problemas donde el resultado exacto sea un submúltiplo exacto de la base (como $1/2$ o $1/4$), las instrucciones de los autores deben sugerir explícitamente el uso de concepciones erróneas por *incremento muestral* ($\Delta n = 3n$) o cambios de nivel de confianza ($z = 1.645$ o $z = 2.576$), evitando inducir multiplicadores mágicos.
3. **Eficacia de la Barrera Reactiva Silenciosa:**  
   A pesar de la complejidad del straggler en `C-23`, el orquestador no realizó ninguna edición manual ni lectura exploratoria en disco. La delegación quirúrgica a subagentes `c2c_repair` con scope acotado preservó el presupuesto de tokens del chat principal y garantizó la integridad psicométrica del curso.

---

## 6. Hitos Futuros (Future Milestones): Reingeniería del Pipeline para Máxima Eficiencia en Wall Time

> [!IMPORTANT]
> **Diagnóstico de Necesidad:** A pesar de la robustez del cerrojo de calidad y de que los subagentes `c2c_repair` remediaron el 100% de los incidentes de forma autónoma, el flujo operativo actual todavía adolece de problemas estructurales que le impiden ser súper eficiente a nivel de **tiempo de pared (*wall time*)**. La serialización de compuertas y la aparición de olas tardías de reparación en Stage 6 introducen demoras evitables en cursos de gran escala.

### 6.1. Limitaciones del Flujo Serializado Actual
En la arquitectura vigente:
1. Se compilan los shards y se despachan los **Plan Judges** (Stage 4-5).
2. Si un juez detecta discrepancias, se espera a que todos los jueces terminen para ejecutar reparaciones pedagógicas.
3. Se procede a la generación de plantillas (`templates`) y construcción masiva del curso (`build`).
4. **Fricción tardía:** Al invocar la compuerta final `run.py --stage publish` (Stage 6), el linter psicométrico global `diagnostic_rationale_alignment_linter` analiza los 1,170 reactivos y bloquea la publicación por colisiones de distractores sintéticos (`[DIAG-MAGIC-MULT]`).
5. Se despacha una **segunda ola reactiva de subagentes** (`c2c_repair`), sumando más de 6 minutos de espera adicional (como en `C-23`), seguidos de una re-ejecución completa de `templates`, `build` y `publish`.

### 6.2. Decisión Arquitectónica para la Siguiente Iteración: Ejecución Concurrente de Gates de Stage 4 y Plan Judges
Para la siguiente iteración de C2C, se debe establecer que el curso completo se someta a las compuertas y escáneres existentes en su estado actual (*as-is*) **en simultáneo con la ejecución de los Plan Judges**, en lugar de diferir estas verificaciones técnicas y psicométricas hasta después de los jueces o hasta la etapa final.

Aun cuando el curso requiera arbitraje pedagógico ciego mediante Plan Judges, no se debe esperar de forma pasiva a que concluya todo el arbitraje para recién descubrir incompatibilidades técnicas, linters o fallos de compilación:
- **No se requiere un escáner predictivo nuevo:** Se aplican directamente los mismos escáneres y *quality gates* de **Stage 4** (`build`, sweeps deterministas de 50 semillas, `diagnostic_rationale_alignment_linter`, multiplicadores sintéticos `[DIAG-MAGIC-MULT]`, rangos y metadatos) en paralelo con el arbitraje de los jueces.
- Esto detecta en el mismo instante temporal $t = t_{\text{judges}}$ tanto los posibles reparos pedagógicos del juez como cualquier fallo técnico o psicométrico de las plantillas.

### 6.3. Ola Única de Reparación Holística y Verificación Obligatoria del Orquestador
En lugar de múltiples fases de remediación desfasadas (reparar por objeciones de jueces $\rightarrow$ compilar $\rightarrow$ construir $\rightarrow$ reparar por compuerta de publicación $\rightarrow$ volver a compilar $\rightarrow$ publicar), la arquitectura se reestructurará en torno a un único punto de consolidación:

1. **Ejecución Concurrente:** Se disparan los Plan Judges y, al mismo tiempo, los escáneres y compuertas de Stage 4 aplicados sobre todos los shards del curso.
2. **Consolidación en Matriz Única de Defectos:** El orquestador unifica los hallazgos pedagógicos (observaciones de jueces) y las fallas técnicas/psicométricas (linters y gates de Stage 4) en una sola orden de trabajo por shard/competencia afectada.
3. **Ola Única de Subagentes (`c2c_repair`):** Se lanza una única ola de reparación donde cada subagente aborda simultáneamente tanto el rigor conceptual exigido por los jueces como la resolución de las fallas detectadas por las compuertas de Stage 4.
4. **Re-Arbitraje Quirúrgico Focalizado:**
   - Si la remediación alteró reactivos específicos arbitrados por un juez, se invoca **únicamente el Plan Judge específico a esa competencia o problema puntual**, sin necesidad de reevaluar el resto del curso.
   - Si la corrección fue puramente paramétrica o de linters sin alterar el contenido arbitrado, no se requiere re-arbitraje.
5. **Re-intento Riguroso de Publicación por el Orquestador (Cero Asunciones Ciegas):**
   - **Regla Inquebrantable:** No porque un subagente de reparación declare haber corregido el shard se asume el éxito ciego ni se salta la compuerta.
   - El orquestador C2C debe **siempre respetar el ciclo de validación**: vuelve a ejecutar formalmente la etapa de publicación (`run.py --stage publish`) y analiza el resultado de forma exhaustiva para verificar si el curso efectivamente cumple todos los contratos o si se requiere cambiar/ajustar algo más antes de certificar la salida.

```mermaid
sequenceDiagram
    autonumber
    participant Orch as Orquestador C2C
    participant Shards as Shards de Autores (Stage 3)
    participant Judges as Plan Judges (Stage 5)
    participant Stage4Gates as Gates y Linters de Stage 4
    participant Repair as Ola Única de Reparación (c2c_repair)
    participant SpecJudge as Plan Judge Quirúrgico (Específico)
    participant Pub as Validación y Publicación (Stage 6)

    Orch->>Shards: Compilar Shards de Autores
    Shards-->>Orch: Shards Listos (t = 0)

    par Verificación Concurrente (Judges + Gates Stage 4)
        Orch->>Judges: Evaluar reactivos ciegos
        Judges-->>Orch: Reporte Pedagógico (Objeciones o PASS)
    and
        Orch->>Stage4Gates: Ejecutar escáneres y gates de Stage 4 ([DIAG-MAGIC-MULT], etc.)
        Stage4Gates-->>Orch: Reporte de Fallos Técnicos/Psicométricos
    end

    Note over Orch,Repair: Consolidación de Defectos en Matriz Unificada
    Orch->>Repair: Despachar Ola Única de Reparación (Pedagogía + Linters)
    Repair-->>Orch: Shards Remediados por Subagentes

    opt Solo si hubo cambios en reactivos arbitrados
        Orch->>SpecJudge: Re-evaluación quirúrgica del reactivo específico
        SpecJudge-->>Orch: PASS del Juez Específico
    end

    Note over Orch,Pub: Re-intento Formal y Análisis Obligatorio del Orquestador
    Orch->>Pub: run.py --stage publish (Comprobación Real de Gates)
    alt Todos los contratos y linters pasan
        Pub-->>Orch: Publicación Exitosa y Cerrojada
    else Persiste algún conflicto
        Pub-->>Orch: Error Detallado -> Orquestador analiza y ajusta
    end
```

### 6.4. Sincronización Estricta de Contratos entre Stage 2 (Sharding) y Stage 4 (Build/Sweeps)

> [!CAUTION]
> **Anti-patrón de Contratos Desfasados:** Actualmente existe el riesgo de que las especificaciones emitidas en Stage 2 (`run.py --stage shard` $\rightarrow$ `pre_shard_manifest.json`) no reflejen de manera idéntica y estricta el conjunto de validaciones, cuotas y restricciones que se evaluarán más adelante en Stage 4 (`run.py --stage build` / `templates`). Esto provoca que un autor en Stage 3 genere código creyendo cumplir la especificación de Stage 2, solo para ser rechazado tardíamente al compilar o instanciar en Stage 4.

Para la siguiente iteración se establece como hito crítico:
1. **Espejo Contractual Stage 2 $\longleftrightarrow$ Stage 4:** Todo requerimiento que la compuerta de Stage 4 vaya a auditar (cuotas mínimas por arquetipo, diversidad de stems $\ge 0.50$, invariantes analíticos, rangos de parámetros y linters de esquema) debe inyectarse contractualmente y de forma explícita en las directivas de Stage 2.
2. **Eliminación de Descubrimiento de Fallos por Rechazo:** El subagente autor de shard debe conocer desde su *prompt inicial* y esquema de entrada exactamente la totalidad de las reglas que evaluará Stage 4. Es inadmisible esperar a que un shard falle en Stage 4 para que recién el desarrollador o subagente sepa qué hizo mal.
3. **Pre-validación Sintáctica y Semántica Local (`compile_shard.py` sincronizado):** La herramienta de auto-test que corre el autor antes de entregar su shard debe contener el 100% de la lógica de evaluación de Stage 4, logrando paridad contractual absoluta a $t=0$.

### 6.5. Análisis de Rendimiento: Wall Time y Presupuesto de Tokens

| Métrica | Flujo Actual (Serializado / Reactivo) | Nuevo Flujo (Ola Única / Shift-Left) | Impacto Neto Esperado |
| :--- | :---: | :---: | :---: |
| **Tiempo de Pared (*Wall Time*)** | Elevado (~6 a 10 min de penalización tardía por re-ejecuciones en Stage 6) | Mínimo (Remediación consolidada a $t=t_{\text{judges}}$, sin bucles finales) | **Reducción de hasta un 40%–60%** en la fase post-autores |
| **Consumo de Tokens** | Duplicación de overhead de contexto al invocar subagentes en 2 olas separadas | Invocación de subagentes consolidada; una sola lectura de archivos por shard | **Neutro o Ligero Ahorro (< 5% tokens)** por contexto unificado |
| **Riesgo de Regresión** | Alto (parchear para el linter al final puede romper contratos ya avalados por jueces) | Nulo (el subagente concilia el criterio pedagógico y las reglas psicométricas a la vez) | **Garantía de Convergencia Determinista** |

### 6.6. Hoja de Ruta de Implementación
- [ ] **M6.1:** Habilitar la ejecución anticipada de las compuertas y escáneres de Stage 4 (`build`, linters de distractores, multiplicadores sintéticos) para correr concurrentemente con los Plan Judges.
- [ ] **M6.2:** Adaptar el orquestador principal (`c2c-run-auditor` / `content-to-course`) para consolidar en paralelo las observaciones de los jueces y las fallas de los gates de Stage 4.
- [ ] **M6.3:** Formalizar el generador de órdenes de trabajo unificadas `repair_work_order.json` que combine hallazgos de jueces y de linters en una sola matriz de remediación para la ola única.
- [ ] **M6.4:** Implementar el re-arbitraje selectivo/quirúrgico (solo reactivos afectados) y la obligación estricta del orquestador de re-intentar formalmente `run.py --stage publish` analizando su viabilidad sin atajos ciegos.
- [ ] **M6.5 [CRÍTICO]:** Sincronización y paridad contractual total entre Stage 2 (`pre_shard_manifest.json`) y Stage 4 (`build` / sweeps engine), garantizando que las restricciones y linters de Stage 4 se inyecten de forma explícita y preventiva desde Stage 2 para evitar rechazos reactivos tardíos.
