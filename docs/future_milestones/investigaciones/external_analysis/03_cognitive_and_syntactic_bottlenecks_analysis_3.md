El análisis del código de la pipeline (`content-to-course`) y de las trazas empíricas de ejecución (`e8ab9fd6` y `c4802280`, donde **95.8% del tiempo total es pura inferencia del LLM** y solo **4.2% es ejecución de herramientas locales**, acumulando hasta **519 turnos** y **60M de tokens con caché** para 530 preguntas) muestra que la ineficiencia de output y latencia no proviene de la lentitud de Python, sino de **7 causas raíces estructurales y cognitivas** que fuerzan al LLM a operar en bucles multi-turno de prueba y error.

### Resumen Cuantitativo de las Trazas Auditadas

| Métrica / Indicador Forense | Corrida `e8ab9fd6` (3 Shards) | Corrida `c4802280` (4 Shards) | Impacto en Latencia / Output |
| --- | --- | --- | --- |
| **Tiempo en Inferencia LLM vs. Tools** | 95.8% LLM / 4.2% Tools | 95.8% LLM / 4.2% Tools | El cuello de botella es el número de turnos y generación de tokens, no el CPU local |
| **Turnos en Autores de Shards (`Stage 3`)** | 56 a 104 turnos por autor | 86 a 146 turnos por autor | Presupuesto teórico de $\le 25$ turnos desbordado por micro-bucles secuenciales |
| **Duración de `Stage 3` (Camino Crítico)** | 27.95 min (`shard_01`) | 32.70 min (`shard_01` y `shard_04`) | Define más del 65% del *wall-time* real de toda la pipeline |
| **Errores de Herramientas / Validación** | 62 errores registrados | 88 errores registrados | Cada fallo invalida el flujo y suma rondas completas de re-lectura de contexto |
| **Tokens Totales Leídos en Caché** | 26.14M tokens | 56.04M tokens | Crecimiento cuadrático $O(T^2)$ por re-enviar el historial en cada micro-turno |

### 1. Colisión de 4 Capas de Escapado y Sintaxis (Python $\to$ f-string $\to$ Plantilla `{var}` $\to$ JSON $\to$ KaTeX)

El LLM debe escribir código Python (`generate_py`) embebido como un *string* dentro de un JSON (o dentro de un script Python que escribe un JSON), el cual a su vez usa f-strings de Python para interpolar fórmulas LaTeX/KaTeX que luego pasan por un motor propio de sustitución (`format_template_string` en `engine/assemble.py`).

* **Conflicto sintáctico de llaves (`{}`):** En f-strings de Python, una llave literal de LaTeX requiere duplicarse (`{{`), pero el validador (`validate_katex_syntax` en `engine/invariants.py` y `R-20` en `src/validator/rules.py`) penaliza cualquier llave doble residual (`{{` o `}}`) y cualquier llave simple `{var}` que no esté precedida por un comando LaTeX o declarada en `vars`.
* **Corrupción silenciosa de secuencias de escape:** Si el autor omite un prefijo `r"..."` en un solo string, secuencias LaTeX como `\frac`, `\beta`, `\tau` o `\nabla` se convierten en caracteres de control ASCII (`\x0c`, `\x08`, `\t`, `\n`), detonando fallos en el escáner léxico (`check_latex_escape_corruption` en `engine/sandbox.py`).
* **Efecto en el LLM:** Los modelos generativos sufren alta tasa de error al mantener simultáneamente el conteo de llaves y barras invertidas en 4 niveles de anidación, provocando decenas de ciclos de rechazo por `R-20` (`Unbalanced Math Delimiters`, `Unsubstituted Template Variables` y `KaTeX Double Curly Braces`).

### 2. La Paradoja entre el Límite de `max_output_tokens` y el "Sharding Amortizado"

En `plan_shards.py`, la pipeline agrupa **7 a 8 competencias por shard** para amortizar los tokens de entrada del prompt del sistema. Sin embargo, esto crea una trampa irresoluble en un solo turno de salida:

* **Peso real de salida por shard:** Cada competencia exige $\ge 6$ plantillas paramétricas (2 MC7 con 6 distractores cada una, 2 FIB, 2 MS con `error_rationale`, 3 a 5 `stem_variants`, `generate_py`, `cross_check_py`, 3 `hints` y `solution`). Un archivo de 1 competencia (`Hab-01.json`) pesa **~18 a 28 KB (~5,000–7,000 tokens)**.
* **Imposibilidad física de emisión atómica:** Emitir 7 u 8 competencias de golpe requiere generar **~160 KB de código denso (~40,000–45,000 tokens de salida)** en un solo turno, lo que excede el `max_output_tokens` del modelo y trunca la respuesta a mitad de generación (como ocurrió en `Direct CTA Architect` en el paso 27 de `e8ab9fd6` y en `Shard Author shard_02` en el paso 40 de `c4802280`).
* **Contradicción en `prompt_shard_author.md`:** Para evitar el truncamiento, el prompt ordena construir las plantillas *"en bloques de COMO MÁXIMO 1 o 2 competencias a la vez"*, pero al mismo tiempo exige *"Autoría Atómica en 1 script"* y *"prohibido micro-bucles"*. Obligado a particionar su escritura en bloques de 1–2 competencias, el agente inevitablemente multiplica sus turnos (`shard01_part1.py` ... `part4.py`, `gen_c07.py` ... `gen_hab07.py`) y cae en bucles de 86 a 146 turnos.

### 3. Restricciones Psicométricas Estocásticas Acopladas sobre 50 Semillas (`check_templates.py`)

El LLM no escribe preguntas estáticas; escribe un generador estocástico (`def generate(rng)`) que `check_templates.py` evalúa ejecutando un barrido determinista de **50 semillas** (`num_dry_run_seeds=50`) más la simulación de cuota de producción (20 o 30 preguntas en `check_competency_diversity`). Para que una plantilla pase, **el 100% de las 50 semillas** debe cumplir simultáneamente restricciones acopladas que un LLM no puede calcular mentalmente mientras genera texto:

* **Cota psicométrica de longitud por ítem (`R-15`):** En las 50 semillas, la longitud en caracteres del string renderizado de la respuesta correcta `len(correct)` debe caer dentro de $[0.80 \times \min(\text{len}(D)),\, 1.20 \times \max(\text{len}(D))]$. Basta que una semilla genere un número de 1 dígito en `correct` y de 3 dígitos en un distractor para que falle `R-15`.
* **No-colisión dinámica de distractores (`TPL-D4`):** En las 50 semillas, las 6 fórmulas de perturbación algebraica de los distractores deben producir strings estrictamente distintos entre sí y distintos de `correct`. Cuando dos perturbaciones coinciden para una semilla específica (ej. $a = b$ o multiplicación por $0$ o $1$), el validador rechaza la plantilla.
* **Gate de diversidad estructural enmascarada (`TPL-VAR` $\ge 0.50$):** `engine/diversity.py` reemplaza todos los números, fracciones `\frac{...}{...}` y matrices por tokens estáticos `[NUM]`, `[FRAC]`, `[BMATRIX]` antes de medir unicidad (`unique_masked / total >= 0.50`). Si el autor varía los números en `generate_py` pero no crea suficientes estructuras sintácticas distintas en `stem_variants` (por ejemplo, si una competencia tiene 30 ítems de cuota y las plantillas suman menos de 15 estructuras sintácticas post-máscara), `TPL-VAR` falla aunque todas las preguntas tengan números distintos.

### 4. Inflación Cuadrática de Contexto y Truncamiento del Feedback Diagnóstico

Cuando un autor de shard entra en el ciclo de validación y corrección, se activa un efecto bola de nieve en latencia y tokens:

* **Crecimiento $O(T^2)$ del historial conversacional:** En `c4802280`, los 4 autores acumularon entre 86 y 146 turnos cada uno, leyendo **54.2 millones de tokens de caché** y **2.6 millones de tokens de entrada activos**. A partir del turno 40, cada turno de inferencia procesa decenas de miles de tokens de intentos fallidos previos, degradando la atención del modelo y haciendo cada respuesta más lenta.
* **Ceguera por recorte a 15 errores en `check_templates.py`:** Aunque se eliminaron los `break` tempranos dentro de las funciones de validación para acumular errores, el CLI de `check_templates.py` (líneas 1361–1364) trunca la salida impresa a los primeros 15 errores (`for e in errors[:15]: ... and N more errors`). Como un solo error en una plantilla se replica en las 50 semillas del dry-run, **una sola plantilla rota llena los 15 slots de salida**, ocultando los errores de las demás plantillas del shard y forzando al agente a jugar al "juego del topo" (*whack-a-mole*) en rondas sucesivas.
* **Fragilidad de `replace_file_content` sobre código escapado:** Editar in-place scripts grandes llenos de barras invertidas (`\\frac`, `\\\\Delta`) y JSON anidado produce fallos frecuentes de coincidencia exacta (`replace_file_content Mismatch`), lo que lleva a los subagentes a crear scripts paralelos en consola (`fix_all.py`, `audit_diversity.py`, `check_primes.py`) para parchar sus propios archivos.

### 5. Serialización y Sobrecarga Estructural en el Análisis Cognitivo (`Stage 1B: Direct CTA`)

* **Barrera secuencial monolítica:** En modo `Direct CTA`, un único subagente (`c2c-cta-direct`) bloquea toda la pipeline durante **11.4 a 20.8 minutos** mientras lee los PDFs originales con `view_file` y sintetiza un árbol curricular masivo.
* **Exceso de campos por distractor en `cta.schema.json`:** Para un curso de 22 a 25 competencias con 6–8 distractores cada una (~150–180 distractores en total), el esquema obliga a redactar **12 propiedades por cada distractor** (`id`, `name`, `wrong_belief`, `correct_belief`, `omitted_step`, `trigger`, `manifestation`, `error_type`, `severity`, `origin`, `evidence`, `remediation_hint`), cuando etapas posteriores (`assemble.py`) solo consumen realmente `id`, `manifestation` y `remediation_hint`. Esto multiplica por 3x el volumen de tokens de salida requeridos en `cta.json`.

### 6. Desequilibrio de Carga y Efecto *Straggler* en Barreras Síncronas

La orquestación usa barreras síncronas estrictas (`Stage 1B` $\to$ `Stage 3` $\to$ `Stage 5`): el Director no puede avanzar a `Stage 4 (build)` hasta que el último autor de shard termine.

* **Particionamiento por conteo plano en lugar de peso cognitivo:** Aunque `plan_shards.py` calcula `calculate_competency_weight(comp)` (donde `Skill = 3.0`, `Concept = 2.0`, `Fact = 1.0 + 0.1 * distractors`), la función `partition_competencies_into_shards` reparte las competencias por **cantidad fija contigua** (`base_size = total_comps // k`) en lugar de equilibrar la suma de pesos. Un shard con mayoría de `Skills` (cuota de 30 ítems y $\ge 6$ distractores con pasos omitidos) requiere mucho más trabajo y validaciones que un shard de `Facts`, convirtiéndose en el *straggler* que retiene toda la barrera.

### 7. Fricción de Entorno y Subprocesos en el Motor de Ejecución

* **Cold-start de librerías pesadas en subprocesos aislados:** Cuando se invoca `execute_sandbox_instance` (usado en `judge.py` para cada reactivo del lote ciego o cuando `C2C_SANDBOX_ISOLATED=1`), levantar un subproceso de Python en Windows e importar módulos científicos (`sympy`, `numpy`, `scipy.stats`) añade entre **300 ms y 1,425 ms por invocación**, además de la latencia de I/O al escribir decenas de archivos intermedios sobre unidades sincronizadas (Google Drive).
* **Discrepancias de entorno en consola:** Los subagentes pierden turnos adicionales en errores de shell (`PowerShell Command / Path Not Found`, `ModuleNotFoundError` por invocar `python` global en vez de `.venv`, y omisión del flag `--cta work/cta.json` al correr `check_templates.py`).

### Palancas Arquitectónicas para Resolver las Causas Raíces de Fondo

1. **Separar el código Python del JSON (Adiós al cuádruple escapado):** Permitir que los autores escriban archivos `.py` nativos por competencia (o un módulo declarativo limpio) en lugar de meter código Python como un string JSON escapado dentro de `"generate_py"`, eliminando de raíz el 80% de los errores `R-20` y `replace_file_content`.
2. **Desacoplar las reglas psicométricas deterministas del LLM:** En lugar de obligar al LLM a adivinar longitudes de texto en `generate_py` para cumplir `R-15` (`0.80x–1.20x`), activar en `engine/assemble.py` (`calibrate_option_lengths`, que hoy es un *no-op* en las líneas 57–81) el balanceo automático de longitud como ya lo hace `RepairLoop._repair_giveaway_lengths` en `repair_loop.py`.
3. **Agrupar errores por plantilla (Deduplicación de semillas en `check_templates.py`):** En vez de imprimir las primeras 15 instancias fallidas (donde 1 sola plantilla con un error en las 50 semillas satura los 15 slots), agrupar el reporte por `(template_id, rule_id)` mostrando 1 ejemplo por plantilla afectada para que el autor vea el 100% de las plantillas con errores en su primera ejecución.
4. **Reducir el tamaño de shard a 2–3 competencias con *Prompt Caching* compartido o Map-Reduce en CTA:** Un shard de 2–3 competencias genera ~40–60 KB de salida, lo que cabe holgadamente en **1 o 2 turnos reales de escritura** sin desbordar `max_output_tokens`, evitando los micro-bucles de 120 turnos y reduciendo el tiempo de pared de `Stage 3` de ~32 minutos a ~4–6 minutos.