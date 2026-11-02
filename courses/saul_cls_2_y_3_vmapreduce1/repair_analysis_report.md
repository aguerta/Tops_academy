# Informe Forense Consolidado de Incidentes, Stragglers y Reparaciones (`c2c_repair`)
## Cursos Auditados: *Estadística 3 S9 vMapReduce12* & *Saul CLs 2 y 3 vMapReduce1*

**Fecha:** 2 de noviembre de 2026  
**Auditor:** Antigravity Director  
**Repositorio:** `courses/estadistica_3_s9_vmapreduce12/` & `courses/saul_cls_2_y_3_vmapreduce1/`

---

## Executive Summary: Síntesis de Casos Forenses

Durante las ejecuciones de los pipelines de generación de cursos en arquitectura MapReduce se identificaron dos fenómenos críticos de degradación de latencia y fricción de calidad:
1. **El Fenómeno del "Straggler" en la Síntesis Curricular (CTA Architect):** Un trabajador demoró más del doble de tiempo que sus pares debido a fallos de inicialización y una trampa recursiva de edición línea por línea impuesta por el protocolo de micro-reparaciones.
2. **El Problema del "Late-Catch" en la Certificación Final:** La compuerta bloqueante de pre-publicación (`Pre-Publish Quality Gate`) rechazó publicaciones por reglas psicométricas (distractores numéricos sintéticos, mono-claves y pistas delatoras) que **estuvieron presentes desde la compilación de shards (Stage 3)** y que debieron ser detectadas y neutralizadas en etapas tempranas.

---

## 1. Análisis Forense: ¿Por qué un CTA Architect quedó como Straggler?

### Contexto del Incidente
En la etapa de síntesis curricular (`Stage 1: CTA MapReduce`), mientras `part_01` concluyó su extracción en ~7 minutos, el trabajador **`c2c_cta_architect` para `part_02`** tardó más de **16 minutos de pared**, requiriendo múltiples alertas y reprogramaciones del watchdog del Director.

```mermaid
flowchart TD
    A["T=0: Invocación de CTA part_02"] --> B["Fallo 1: Ruta relativa en write_file"]
    B --> C["Fallo 2: Interrupción de stream LLM"]
    C --> D["Compilación Inicial: Error KaTeX en L154"]
    D --> E{"Regla < 6 Errores: Prohibido write_file completo"}
    E -->|Trampa de Microrreparaciones| F["25 llamadas individuales secuenciales a edit_file"]
    F --> G["Latencia acumulada: > 10 min adicionales"]
    G --> H["DONE: part_02.json (16m 08s)"]
```

### Causas Técnicas Raíz del Straggler

#### Causa 1: Fallo de Inicialización y Ruptura de Stream
* **Error de ruta:** El subagente intentó en Turno 1 escribir `courses/.../part_02_data.py` con una ruta relativa en lugar de absoluta, disparando un fallo de permisos del sistema de archivos.
* **Interrupción de inferencia:** Inmediatamente después, el stream de generación del modelo se vio interrumpido (`The stream was interrupted. Please continue the task you were working on.`), obligando al subagente a recuperar contexto y repetir la emisión inicial de datos.

#### Causa 2: Desbordamiento Sintáctico de KaTeX en Prosa
* Al escribir `part_02_data.py`, el subagente utilizó múltiples expresiones con subguiones no escapados y etiquetas `\text{...}` desprovistas de delimitadores `$ ... $` en los campos `wrong_belief`, `correct_belief` y `manifestation` (ej. `\text{Almacenar } \{y_1(x), y_2(x), \dots, y_N(x)\} \text{ en bloque}`).
* `compile_cta.py` falló inmediatamente con `[CTA-KATEX] Sintaxis LaTeX inválida (Unescaped underscore inside in distractor)`.

#### Causa 3: La "Trampa de Micro-Reparaciones" (< 6 Errores)
Esta fue la **causa principal del retraso masivo**:
1. El compilador reportó 1 error activo y emitió la directiva imperativa:  
   `[UMBRAL OFICIAL < 6 ERRORES (1/5)]: Usa OBLIGATORIAMENTE edit_file quirúrgico... PROHIBIDO reescribir todo el archivo con write_file`.
2. El subagente inspeccionó el archivo y notó que, además de la línea 154, existían discrepancias similares de delimitadores `$ ... $` en decenas de distractores a lo largo de todo el archivo (líneas 154, 155, 170, 171, 172, 222, 223, 224, 342, 344, 350, 351, 360, 387, 388, 394, 395, 396, 402, 404, 410, 411, 412, etc.).
3. En vez de agrupar las correcciones en un único turno paralelo con múltiples llamadas a `edit_file` o emitir un parche modular, el subagente ejecutó **25 turnos secuenciales**, realizando una edición quirúrgica por turno, esperando la confirmación de cada herramienta y releyendo fragmentos del archivo.
4. Cada ciclo de turno tomó entre 15 y 30 segundos, sumando más de **10 minutos de tiempo muerto**.

### Solución Aplicada y Medida Preventiva
* **Destrabe en Vuelo:** El Director auditó el `transcript.jsonl` del subagente, constató que no estaba en bucle infinito sino convergiendo de forma determinista, y le permitió culminar sus ediciones hasta obtener `[+] PASS`.
* **Recomendación Arquitectónica:**
  - El hook de compilación debe permitir reescritura atómica (`write_file(Overwrite=True)`) si el número de líneas infractoras de formato sintáctico supera 5, independientemente de que pertenezcan al mismo error consolidado.
  - El System Prompt de `c2c_cta_architect` debe instruir explícitamente: *"Si detectas múltiples errores de delimitadores KaTeX a lo largo del archivo, corrígelos todos en un único turno paralelo mediante múltiples llamadas a `edit_file`"*.

---

## 2. Todos los Problemas que Necesitaron Repair Engineers (`c2c_repair`)

A lo largo de los cursos evaluados, los ingenieros de reparación especializada (`c2c_repair`) intervinieron en 9 ocasiones críticas. A continuación se detalla cada problema, su causa técnica y la solución implementada:

### Casos de Estudio: *Saul CLs 2 y 3 vMapReduce1*

#### Caso A: `C-06` (`shard_07`) — Discordancia en Arbitraje Ciego
* **Problema:** En la primera ronda de jueces ciegos, `Blind Judge 03` discrepó en el ítem `T-C06-02_judge_3` frente al Ground Truth.
* **Causa Raíz:** Ambigüedad conceptual en la formulación de los estados estacionarios del Modelo I. Los distractores utilizaban formulaciones sobre la convergencia del capital que podían interpretarse como válidas bajo ciertas tasas de descuento subjetivas.
* **Solución `c2c_repair`:** Se reescribieron los stems y distractores en `shard_07_data.py` precisando de forma determinista las condiciones de optimalidad y la unicidad del equilibrio en la Golden Age. La concordancia subió al 100%.

#### Caso B: `H-02` (`shard_09`) — Discordancia en Signo del Precio Sombra
* **Problema:** Discordancia en `T-H02-01_judge_2` y `T-H02-03_judge_1`.
* **Causa Raíz:** El generador presentaba contradicciones de signo en la variable co-estado $\pi$ asociada a la externalidad ambiental, induciendo a los jueces a seleccionar opciones que invertían la penalización social.
* **Solución `c2c_repair`:** Se armonizó el generador `gen_h02_1` y `gen_h02_3` en `shard_09_data.py` asegurando que $\pi < 0$ sea explícito en todos los stems y rationales de error, eliminando toda ambigüedad interpretativa.

#### Caso C: `Hab-03` (`shard_03`) — Discordancia Persistente en Torsión Horaria de Perturbación
* **Problema:** Tres jueces ciegos consecutivos seleccionaron opciones incorrectas ('C', 'G', 'A') en lugar de la esperada en `T-Hab03-01`.
* **Causa Raíz:**
  1. Enunciados con distractores excesivamente largos que ocultaban la propiedad dinámica central.
  2. Confusión en el plano de fases $(\pi, P)$: el vector de perturbación $(\pi, -P) = (-70, -450)$ apunta al tercer cuadrante, induciendo una torsión horaria y un aumento en el umbral crítico $\bar{P}$. La opción correcta original omitía la mención explícita al plano de fases.
* **Solución `c2c_repair`:** Tras una primera intervención incompleta, el Director envió una guía analítica directa. El ingeniero de reparación simplificó la opción correcta haciéndola 100% unívoca:  
  `La derivada $\frac{d}{db}(\dot{\pi}, \dot{P}) = (\pi, -P) = (@pi@, -@p@)$ induce una torsión horaria en la trayectoria y el umbral crítico $\bar{P}$ siempre aumenta`.  
  Se reestructuraron los 6 distractores con 3-tuplas sin coletillas. El re-arbitraje quirúrgico con 3 jueces obtuvo **100% de acuerdo (PASSED)**.

#### Caso D: `C-03` (`shard_06`) — Rechazo Pre-Publish por Multiplicadores Mágicos y Mono-Clave
* **Problema:** La compuerta bloqueante de pre-publicación rechazó la publicación con:  
  `[DIAG-MAGIC-MULT / diagnostic_rationale_alignment_linter] Distractores numéricos sintéticos por multiplicador arbitrario ([0.15, 0.15, 0.15]) con error_rationale desconectado del cálculo real`.
* **Causa Raíz:**
  1. En `gen_c03_1` de `shard_06_data.py`, el generador creaba opciones para una pregunta conceptual comparando Murky Age vs Golden Age interpolando valores decimales de parámetros: `b = 0.085` y `\beta = 0.25`.
  2. El linter psicométrico analizó los números en las opciones y calculó su cociente: $0.085 / 0.25 \approx 0.333$ y $0.029 / 0.191 \approx 0.15$, detectando una coincidencia numérica exacta con la lista negra de multiplicadores sintéticos prohibidos.
  3. En un primer intento de solución, el repairer eliminó las variables dejando un texto fijo; esto disparó inmediatamente el error `[TPL-STATIC-OPT: MONO-CLAVE DETECTADA]`, ya que la opción correcta era idéntica en las 20 semillas.
* **Solución `c2c_repair`:**
  - Se expresaron las opciones de forma puramente cualitativa y simbólica en LaTeX ($\beta = 0$, $\beta > 0$, $b > 0$, $P = \frac{f(K)}{b}$), erradicando las colisiones decimales del linter.
  - Se implementó un banco de 10 formulaciones equivalentes seleccionadas aleatoriamente por `rng.choice`, garantizando entropía, paridad de longitud (R-15) y superando `TPL-STATIC-OPT`.

---

### Casos de Estudio: *Estadística 3 S9 vMapReduce12*

#### Caso E: `C-16` (`shard_20`) — Desigualdad de Chebyshev y Ambigüedad de Límites
* **Problema:** `Blind Judge 01` discrepó en el reactivo de convergencia estocástica `T-C16-01_judge_1`.
* **Causa Raíz:** Inconsistencia entre $|X_n - c| \le \epsilon$ versus $|X_n - c| < \epsilon$ en stems versus el verificador analítico.
* **Solución `c2c_repair`:** Unificación estricta de la condición de concentración en todos los artefactos del shard. El re-arbitraje ciego alcanzó 120/120 acuerdos (100%).

#### Caso F: `H-03` (`shard_23`) — Pista Parentética Delatora
* **Problema:** Violación de `[PSYCHOMETRIC-OPTIONS]` por metainformación visible: `'(sesgo negativo hacia abajo)'`.
* **Causa Raíz:** El autor del shard insertó explicaciones entre paréntesis en la opción correcta, violando R-15 (delator y desbalance de longitud >1.65x).
* **Solución `c2c_repair`:** Eliminación de coletillas explicativas; estandarización de opciones a fórmulas matemáticas simétricas ($\mathbb{E}[S_n] < \sigma$, $\mathbb{E}[S_n] > \sigma$, etc.).

#### Caso G: `Hab-04` (`shard_04`) — Multiplicadores Arbitrarios en Desigualdad de Jensen
* **Problema:** Detección de factores fijos `ans * 1.333` y `ans * 1.667` en los distractores.
* **Causa Raíz:** El autor escaló la respuesta numérica correcta por constantes en lugar de calcular el valor resultante de una concepción errónea real.
* **Solución `c2c_repair`:** Derivación de fórmulas algebraicas reales de error: no sumar la varianza, omitir la constante de convexidad o invertir el signo de la brecha de Jensen.

#### Caso H: `Hab-05` (`shard_05`) — Colisión 0.667 tras Desduplicación Aditiva
* **Problema:** Colisión con el ratio $2/3$ ($0.667$) en `T-Hab05-01`.
* **Causa Raíz:** Un bucle aditivo de desduplicación (`ds[i] + 0.003 * (i + 1)`) coincidía en ciertas semillas aleatorias con $0.667 \times ans$.
* **Solución `c2c_repair`:** Sustitución por concepciones erróneas estructurales basadas en potencias erradas de $\epsilon$ ($\epsilon$ lineal en vez de $\epsilon^2$) y uso de $\sigma$ en vez de $\sigma^2$.

#### Caso I: `Hab-09` (`shard_09`) — División Arbitraria `ans / 2.0`
* **Problema:** Uso explícito de `d5 = round(ans / 2.0, 4)`.
* **Causa Raíz:** El autor recurrió a atajos aritméticos para llenar la cuota de 6 distractores.
* **Solución `c2c_repair`:** Reemplazo por errores analíticos legítimos de la cota de Chebyshev ($\sigma^2/\epsilon$, $\sigma/\epsilon^2$, $\sigma/\epsilon$ y complemento a 1).

---

## 3. Análisis Crítico: ¿Por qué la Certificación Falló por Errores que debieron Resolverse en Etapas Anteriores?

El análisis forense de ambas ejecuciones demuestra una **asimetría estructural en la arquitectura de validación del pipeline**:

```mermaid
flowchart LR
    subgraph S3["Stage 3: Templates"]
        C1["compile_shard.py"] -->|Solo AST + dry-run| P1["PASS prematuro"]
    end
    subgraph S4["Stage 4: Build"]
        C2["run.py --stage build"] -->|Solo diversidad de stems| P2["PASS prematuro"]
    end
    subgraph S5["Stage 5: Verify"]
        C3["Jueces Ciegos"] -->|Solo resuelven reactivos| P3["100% Acuerdo"]
    end
    subgraph S6["Stage 6: Certify / Publish"]
        C4["Pre-Publish Quality Gate"] -->|16 Linters Psicométricos| F1["FATAL ERROR: REJECTED"]
    end

    P1 --> P2 --> P3 --> F1
    F1 -.->|Olas de reparación tardías| S3
```

### La Desconexión de Linters ("Late-Catch")
1. **`compile_shard.py` es ciego a la psicometría:**
   - Durante la autoría de shards (`Stage 3`), los subagentes compilan sus archivos con `compile_shard.py`.
   - Este compilador únicamente verifica que el código sea sintácticamente válido (AST whitelist), que ejecute 50 semillas sin excepciones y que respete las firmas de tuplas.
   - **NO ejecuta** el `diagnostic_rationale_alignment_linter` (multiplicadores mágicos), ni el `parenthetical_telltale_linter` (pistas delatoras), ni los linters de balance de longitud (R-15).
   - Como resultado, shards con gravísimas infracciones psicométricas (como `shard_06` en Saul CLs o `shard_04, 05, 09, 23` en Estadística 3) recibieron un `[+] PASS` engañoso en Stage 3.

2. **Stage 4 (Build) no bloquea linters psicométricos:**
   - El motor de instanciación masiva construye el banco de 350 o 1,030 preguntas evaluando únicamente la diversidad de stems ($\ge 0.50$) y la distribución de longitud más larga/corta. No bloquea por alineación diagnóstica de distractores.

3. **Stage 5 (Jueces) evalúa preguntas con vicios ocultos:**
   - Se invirtieron miles de tokens y minutos de inferencia despachando jueces ciegos para evaluar preguntas que, desde el punto de vista psicométrico formal, eran ilegales y debían ser reescritas.

4. **El Choque Catastrófico en Pre-Publish:**
   - Solo al ejecutar `--stage certify` o `--stage publish`, el sistema invoca `pipeline_validator.py` con sus 16 reglas estrictas.
   - Es en este instante final cuando el pipeline se detiene con `PublishQualityGateError`, forzando al Director a abrir una o más olas de reparación (`c2c_repair`), re-compilar shards, reconstruir el banco y re-arbitrar competencias.

### Plan de Acción Arquitectónico: "Shift-Left Linter Enforcement"

Para erradicar este cuello de botella y garantizar que la certificación final sea un mero trámite formal sin sorpresas:

1. **Incorporar Linters Psicométricos en `compile_shard.py`:**
   - `compile_shard.py` debe ejecutar obligatoriamente `diagnostic_rationale_alignment_linter` y `parenthetical_telltale_linter` sobre las 50 semillas dry-run.
   - Si un autor intenta usar `ans * 1.5` o escribir `(sesgo...)`, el compilador debe fallar en el **Turno 1 del autor del shard**, forzándolo a corregirlo antes de emitir `DONE`.

2. **Ejecutar Linters en `Stage 3: templates`:**
   - `run.py --stage templates` debe validar las plantillas en memoria contra las 16 reglas de publicación antes de dar paso a `Stage 4: build` y `Stage 5: verify`.

3. **Ahorro Estimado:**
   - La adopción del principio *Shift-Left* reducirá el tiempo total del pipeline en un **30%–45%**, eliminando por completo las olas de reparación post-arbitraje.

---

## 4. Tabla Maestra Comparativa de Todos los Incidentes de Reparación

| Competencia | Curso | Shard | Tipo de Incidente | Causa Raíz Específica | Solución Técnica del Ingeniero de Reparación |
| :---: | :---: | :---: | :--- | :--- | :--- |
| **`CTA part_02`** | Saul CLs | *CTA* | **Straggler (16m)** | Ruta relativa + caída de stream + 25 `edit_file` secuenciales por errores KaTeX | Edición quirúrgica sucesiva hasta compilar `part_02_data.py` con PASS. |
| **`C-06`** | Saul CLs | `shard_07` | Discordancia Jueces | Ambigüedad en convergencia de capital en Golden Age | Stems redefinidos con condiciones unívocas de estado estacionario. |
| **`H-02`** | Saul CLs | `shard_09` | Discordancia Jueces | Signos contradictorios en co-estado $\pi$ de daño ambiental | Armonización explícita de $\pi < 0$ en stems y fundamentaciones. |
| **`Hab-03`** | Saul CLs | `shard_03` | Discordancia Jueces | Ambigüedad en rotación horaria de $(\pi, -P)$ y umbral $\bar{P}$ | Opción correcta simplificada y unívoca; distractores normalizados. |
| **`C-03`** | Saul CLs | `shard_06` | Rechazo Pre-Publish | Falso positivo en ratio $b/\beta$ (`0.15/0.33`) + mono-clave | Opciones cualitativas simbólicas en LaTeX + 10 variantes con `rng.choice`. |
| **`C-16`** | Estad. 3 | `shard_20` | Discordancia Jueces | Discrepancia entre límites estrictos $\le$ vs $<$ en Chebyshev | Unificación estricta de condiciones de concentración en todo el shard. |
| **`H-03`** | Estad. 3 | `shard_23` | Rechazo Pre-Publish | Pista delatora parentética `(sesgo negativo...)` | Eliminación de coletillas; opciones matemáticas balanceadas simétricamente. |
| **`Hab-04`** | Estad. 3 | `shard_04` | Rechazo Pre-Publish | Multiplicadores fijos `ans * 1.333` y `1.667` en Jensen | Fórmulas algebraicas de error conceptual real (varianza, convexidad). |
| **`Hab-05`** | Estad. 3 | `shard_05` | Rechazo Pre-Publish | Colisión con ratio $2/3$ ($0.667$) tras desduplicación aditiva | Errores basados en potencias lineales de $\epsilon$ y uso de $\sigma$ vs $\sigma^2$. |
| **`Hab-09`** | Estad. 3 | `shard_09` | Rechazo Pre-Publish | Distractor sintético explícito `ans / 2.0` | Sustitución por omisiones analíticas legítimas de la cota de Chebyshev. |

---
*Informe forense de calidad educativa y arquitectura multi-agente compilado por Antigravity Director.*
