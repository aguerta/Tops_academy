# Análisis Forense Exhaustivo de Cuellos de Botella, Modos de Falla y Desglose Temporal de Wall-Clock por Etapa en Pipelines Content-to-Course (C2C)

**Fecha de Auditoría:** `2026-10-23`  
**Origen de Consigna:** Derivado de la conversación `@[conversation:"Auditoria De Curso Con Agente"]` (`818c07d2-9be5-4c52-9b87-0e19ae616fe7`), integrando las 5 corridas directas auditadas, las 7 corridas de la síntesis forense maestra previa, y expandido con la investigación forense profunda de las 2 nuevas corridas de producción: `@[conversation:"Curso de Violaciones de Supuestos Econométricos"]` (`b9316152-ba51-410b-8449-bce23f6885bd`) y `@[conversation:"Asymptotic Statistics Course Generation"]` (`d52ee475-f39d-4b22-9b17-05752ffc79fb`) (Total: **14 corridas longitudinales auditadas**).  
**Metodología:** Análisis forense ultra-granular de telemetría de Google Antigravity SDK (`telemetry.json`, `stage_telemetry_v3`, `stage_deep_dives`, `traceback_deepdive.json` y `transcript.jsonl`), inspección de trazas cognitivas (*thinking traces*), perfilado temporal de llamadas a herramientas e ingeniería de sistemas /boost.  

---

## 1. Desglose Temporal de Wall-Clock por Etapa de Pipeline

El pipeline `content-to-course` (C2C v3.22) opera a través de un runner por etapas orquestado mediante `run.py --stage <stage>`. Cada etapa marca un punto de control con estampa ISO determinista (`recorded_at` en `stage_telemetry_v3`).

La descomposición temporal solicitada abarca las 5 fases funcionales:
1. **Inicialización (Prepare / Ramp-up):** Ingesta de fuentes (PDFs, OneNote, imágenes), escaneo previo del workspace, particionado vectorial PyMuPDF (`select()` + `save()`), ponderación estructural y generación de `pre_cta_manifest.json`.
   > [!IMPORTANT]
   > **Métrica Operativa vs Target SLA:** Si bien el script puntual `prepare.py` registra entre 2.5s y 4.2s de tiempo de cómputo en Python, el **tiempo total de inicialización end-to-end de todas las corridas se sitúa realmente entre 3 y 5 minutos** (180 a 300 segundos). Esto se debe al ramp-up del Director, lectura y validación de fuentes, verificación previa de dependencias e indexación de archivos en el workspace, **excediendo significativamente la meta operativa (*target SLA*) de 1 minuto (60 segundos)**.
2. **CTA (Cognitive Task Analysis):** Extracción curricular de competencias, taxonomía de Bloom, creencias erróneas, generación atómica de `cta_data.py`, auto-healing KaTeX y compilación determinista a `cta.json`.
3. **Charts / Sizing (Sharding Adaptativo):** Balanceo de dependencias pedagógicas, cálculo dinámico de shards (`clamp(ceil(N/8), 2, 6)`), y generación de `pre_shard_manifest.json` y scaffolds.
4. **Plan, Templates, Instanciación y Verificación Psicométrica (Shards + Build + Verify + Blind Judges):**
   - *Stage 03 (Templates / Shards Authoring):* Fan-out de subagentes autores paralelos, generación paramétrica Python (`generate_py`), templates JSON, auto-healing de variables y delimitadores LaTeX.
   - *Stage 04 (Build / Instantiator / Media / CRC32):* Sweeps deterministas CRC32 (30 habilidad / 20 concepto), instanciación masiva de preguntas y validación de invariantes algebraicos.
   - *Stage 05 (Deterministic Verify):* Validación estricta de las 16 reglas psicométricas (R-01 a R-22) en `course_verified.json`.
   - *Stage 05b (Blind Judges & Arbitration):* Evaluación epistémica aislada por primeros principios mediante lotes de jueces independientes (`judge_batch_NN.json`) y cálculo de tasas de acuerdo.
5. **Publish:** Validación final de arbitraje, saneamiento UTF-8, consolidación delta (`--append`), escritura de `courses/<course_id>.json` y registro en la base de datos de la plataforma.

### 1.1. Tabla Maestra Longitudinal: Tiempos de Pared (Segundos, Minutos y % del Total)

| Corrida / Curso | Tipo / Escala | Wall Total | 1. Inicialización (Stage 0) | 2. CTA (Stage 1) | 3. Charts/Sizing (Stage 2) | 4. Plan / Shards (Stage 3) | 5. Build/Media (Stage 4) | 6. Verify (Stage 5) | 7. Blind Judges (Stage 5b) | 8. Publish (Stage 6) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Solow Model v15** (`4ceacf92`) | Coarse/Opt (15 comps, 360 Qs) | **27.1 min** (1626.0s) | **2.5s** (0.1%) | **594.4s** (36.6%) | **8.7s** (0.5%) | **675.9s** (41.6%) | **10.9s** (0.7%) | **13.9s** (0.9%) | **247.0s** (15.2%) | **10.7s** (0.7%) |
| **Práctica Parcial Saúl Standard Coarse v1** (`a53e6af1`) | Coarse Zero-Intervention (13 comps, 320 Qs) | **32.83 min** (1970.0s) | **4.2s** (0.2%) | **776.9s** (39.4%) | **6.8s** (0.3%) | **882.3s** (44.8%) | **10.0s** (0.5%) | **25.1s** (1.3%) | **171.0s** (8.7%) | **10.5s** (0.5%) |
| **Práctica Parcial Saúl Standard** (`f9b9d459`) | Standard Sweet-Spot (65 comps, 1,590 Qs) | **64.22 min** (3853.0s) | **4.2s** (0.1%) | **726.3s** (18.9%) | **6.5s** (0.2%) | **2027.7s** (52.6%) | **34.9s** (0.9%) | **43.4s** (1.1%) | **441.6s** (11.5%) | **16.8s** (0.4%) |
| **Práctica Parcial Saúl Standard Coarse v2** (`afb5aa18`) | Coarse Friction Paradox (14 comps, 370 Qs) | **60.03 min** (3602.0s) | **4.1s** (0.1%) | **965.7s** (26.8%) | **7.1s** (0.2%) | **2254.7s** (62.6%) | **23.2s** (0.6%) | **11.6s** (0.3%) | **232.0s** (6.4%) | **10.2s** (0.3%) |
| **Práctica Parcial Saúl Fine / Masivo** (`acdc402d`) | Fine Masivo Stress-Test (118 comps, 2,850 Qs) | **85.65 min** (5139.0s) | **4.0s** (0.1%) | **1265.9s** (24.6%) | **9.0s** (0.2%) | **2701.4s** (52.6%) | **128.5s** (2.5%) | **14.2s** (0.3%) | **825.7s** (16.1%) | **24.3s** (0.5%) |
| **PDE Saúl 1** (`876ad3df`) | Standard Small (16 comps, 380 Qs) | **55.87 min** (3352.0s) | **0.3s** (0.0%) | — | **13.9s** (0.4%) | **897.9s** (26.8%) | **11.1s** (0.3%) | **7.5s** (0.2%) | **407.6s** (12.2%) | **14.1s** (0.4%) |
| **Estadística Regresión** (`0f573810`) | Standard Medium (43 comps, 1,050 Qs) | **366.02 min** (21961.0s) | **2.6s** (0.0%) | **1312.6s** (6.0%) | **7.3s** (0.0%) | **18318.9s** (83.4%) | **21.3s** (0.1%) | **19.2s** (0.1%) | **304.1s** (1.4%) | **14.4s** (0.1%) |
| **Práctica Parcial Saúl (Truncado 404)** (`9ed41fb3`) | Stage 1 Incomplete (18 comps) | **3.88 min** (233.0s) | — | — | — | — | — | — | — | — |
| **Solow Model (Base)** (`812bfecd`) | Standard Base (21 comps, 500 Qs) | **48.93 min** (2936.0s) | **2.6s** (0.1%) | **1091.9s** (37.2%) | **5.6s** (0.2%) | **1458.6s** (49.7%) | **12.2s** (0.4%) | **11.1s** (0.4%) | **300.6s** (10.2%) | **9.8s** (0.3%) |
| **Solow Model v14** (`7818f6af`) | Standard Base (23 comps, 540 Qs) | **329.87 min** (19792.0s) | **2.9s** (0.0%) | **2184.7s** (11.0%) | **5.3s** (0.0%) | **2062.2s** (10.4%) | **14.8s** (0.1%) | **11.6s** (0.1%) | **15426.2s** (77.9%) | **25.1s** (0.1%) |
| **Solow Model (Append Mode)** (`f2be91cd`) | Append Delta (24 comps, 570 Qs -> 45c) | **339.88 min** (20393.0s) | **3.4s** (0.0%) | **1564.5s** (7.7%) | **6.1s** (0.0%) | **18456.0s** (90.5%) | **14.2s** (0.1%) | **15.4s** (0.1%) | **174.2s** (0.8%) | **69.7s** (0.3%) |
| **Solow Model v13** (`18ae4bcc`) | Standard Base (24 comps, 570 Qs) | **61.9 min** (3714.0s) | **2.9s** (0.1%) | **1593.4s** (42.9%) | **5.8s** (0.2%) | **1084.6s** (29.2%) | **12.5s** (0.3%) | **12.5s** (0.3%) | **919.4s** (24.8%) | **9.6s** (0.3%) |
| **Violaciones de Supuestos Econométricos** (`b9316152`) | Standard Direct (14 comps, 360 Qs) | **40.62 min** (2437.0s) | **1.1s** (0.05%) | **384.5s** (15.8%) | **9.2s** (0.4%) | **1761.7s** (72.3%) | **26.0s** (1.1%) | **25.4s** (1.0%) | **129.3s** (5.3%) | **17.8s** (0.7%) |
| **Estadística Asintótica** (`d52ee475`) | Standard High-Density MapReduce (28 comps, 660 Qs) | **26.88 min** (1613.0s) | **10.2s** (0.6%) | **575.4s** (35.7%) | **6.7s** (0.4%) | **790.4s** (49.0%) | **15.1s** (0.9%) | **17.9s** (1.1%) | **146.7s** (9.1%) | **10.6s** (0.7%) |

### 1.2. Agrupación Funcional Solicitada (5 Bloques Operativos)

| Corrida / Curso | Comps | Preguntas | Wall Total | 1. Inicialización (Stage 0) | 2. CTA (Stage 1) | 3. Charts/Sizing (Stage 2) | 4. Plan & Verificación (Stages 3+4+5+5b) | 5. Publicación (Stage 6) | Overhead No Asignado |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Solow Model v15** (`4ceacf92`) | 15 | 360 | **27.10 min** (1,626.0s) | 2.5s (0.2%) | 594.4s (36.6%) | 8.7s (0.5%) | **947.7s** (58.3%) | 10.7s (0.7%) | 62.0s (3.8%) |
| **Práctica Parcial Saúl Standard Coarse v1** (`a53e6af1`) | 13 | 320 | **32.83 min** (1,970.0s) | 4.2s (0.2%) | 776.9s (39.4%) | 6.8s (0.3%) | **1088.4s** (55.2%) | 10.5s (0.5%) | 83.2s (4.2%) |
| **Práctica Parcial Saúl Standard** (`f9b9d459`) | 65 | 1,590 | **64.22 min** (3,853.0s) | 4.2s (0.1%) | 726.3s (18.9%) | 6.5s (0.2%) | **2547.6s** (66.1%) | 16.8s (0.4%) | 551.6s (14.3%) |
| **Práctica Parcial Saúl Standard Coarse v2** (`afb5aa18`) | 14 | 370 | **60.03 min** (3,602.0s) | 4.1s (0.1%) | 965.7s (26.8%) | 7.1s (0.2%) | **2521.5s** (70.0%) | 10.2s (0.3%) | 93.4s (2.6%) |
| **Práctica Parcial Saúl Fine / Masivo** (`acdc402d`) | 118 | 2,850 | **85.65 min** (5,139.0s) | 4.0s (0.1%) | 1265.9s (24.6%) | 9.0s (0.2%) | **3669.8s** (71.4%) | 24.3s (0.5%) | 166.0s (3.2%) |
| **PDE Saúl 1** (`876ad3df`) | 16 | 380 | **55.87 min** (3,352.0s) | 0.3s (0.0%) | 0.0s (0.0%) | 13.9s (0.4%) | **1324.1s** (39.5%) | 14.1s (0.4%) | 1999.6s (59.7%) |
| **Estadística Regresión** (`0f573810`) | 43 | 1,050 | **366.02 min** (21,961.0s) | 2.6s (0.0%) | 1312.6s (6.0%) | 7.3s (0.0%) | **18663.5s** (85.0%) | 14.4s (0.1%) | 1960.6s (8.9%) |
| **Práctica Parcial Saúl (Truncado 404)** (`9ed41fb3`) | 18 | 0 | **3.88 min** (233.0s) | 0.0s (0.0%) | 0.0s (0.0%) | 0.0s (0.0%) | **0.0s** (0.0%) | 0.0s (0.0%) | 233.0s (100.0%) |
| **Solow Model (Base)** (`812bfecd`) | 21 | 500 | **48.93 min** (2,936.0s) | 2.6s (0.1%) | 1091.9s (37.2%) | 5.6s (0.2%) | **1782.5s** (60.7%) | 9.8s (0.3%) | 43.6s (1.5%) |
| **Solow Model v14** (`7818f6af`) | 23 | 540 | **329.87 min** (19,792.0s) | 2.9s (0.0%) | 2184.7s (11.0%) | 5.3s (0.0%) | **17514.8s** (88.5%) | 25.1s (0.1%) | 59.2s (0.3%) |
| **Solow Model (Append Mode)** (`f2be91cd`) | 24 | 570 | **339.88 min** (20,393.0s) | 3.4s (0.0%) | 1564.5s (7.7%) | 6.1s (0.0%) | **18659.8s** (91.5%) | 69.7s (0.3%) | 89.5s (0.4%) |
| **Solow Model v13** (`18ae4bcc`) | 24 | 570 | **61.90 min** (3,714.0s) | 2.9s (0.1%) | 1593.4s (42.9%) | 5.8s (0.2%) | **2029.0s** (54.6%) | 9.6s (0.3%) | 73.3s (2.0%) |
| **Violaciones de Supuestos Econométricos** (`b9316152`) | 14 | 360 | **40.62 min** (2,437.0s) | 1.1s (0.05%) | 384.5s (15.8%) | 9.2s (0.4%) | **1942.4s** (79.7%) | 17.8s (0.7%) | 82.0s (3.4%) |
| **Estadística Asintótica** (`d52ee475`) | 28 | 660 | **26.88 min** (1,613.0s) | 10.2s (0.6%) | 575.4s (35.7%) | 6.7s (0.4%) | **970.1s** (60.1%) | 10.6s (0.7%) | 40.0s (2.5%) |

#### 1.3. Hallazgo Crítico en la Fase de Inicialización: Duración Real (3 a 5 min) vs Target SLA (1 min)

> [!WARNING]
> **Brecha en el Tiempo de Inicialización:**  
> En las métricas puras registradas por el runner CLI (`run.py --stage prepare`), el script de Python reporta entre 1.1s y 10.2s. Sin embargo, **el tiempo de inicialización integral de todas las corridas se extiende en realidad entre 3 y 5 minutos (173 a 300 segundos)** desde el momento en que se instruye la orden de creación hasta que el CTA comienza su ejecución efectiva.
>
> **Meta Operativa (Target SLA):** $\le 1\text{ minuto}$ (60 segundos).  
> **Tiempo Real Observado:** $3\text{ a }5\text{ minutos}$ (173 a 300 segundos).  
> **Sobrecosto Temporal:** Entre **+188% y +400%** por encima del target de diseño.
>
> **Evidencia Empírica Cronometrada en las Nuevas Corridas:**
> - En `b9316152` (Violaciones de Supuestos Econométricos): El script puntual `prepare.py` duró 1.1s, pero desde el primer mensaje del usuario (`01:30:34 UTC`) hasta el despacho efectivo del arquitecto CTA (`01:33:27 UTC`) transcurrieron **173.0 segundos (2.88 min)**.
> - En `d52ee475` (Estadística Asintótica): El script puntual `prepare.py` duró 10.2s (ingesta y extracción PyMuPDF de 2 PDFs, 52 páginas), pero desde el primer mensaje del usuario (`05:50:55 UTC`) hasta el despacho de los mappers CTA (`05:54:04 UTC`) transcurrieron **189.0 segundos (3.15 min)**.
> Ambas mediciones confirman cuantitativamente la brecha operativa estructural frente al target SLA de 1 minuto.
>
> Este retardo inicial proviene de:
> 1. **Inspección y Escaneo Previo del Workspace:** Búsqueda y catalogación de archivos fuente, verificación de coherencia de rutas y análisis de entorno por parte del orquestador (absorbido frecuentemente en el overhead inicial).
> 2. **Ingesta y Rasterización de Fuentes Pesadas:** Procesamiento PyMuPDF sobre colecciones de PDFs de hasta 103 páginas y 10.4 MB, cálculo de ratios de cobertura textual/visual y segmentación vectorial.
> 3. **Montaje de Manifiestos y Pre-flight Checks:** Generación de `pre_cta_manifest.json`, validación de esquemas de competencias previas en caso de `--append` y ensamblado de prompts iniciales para los subagentes.

---

## 2. Anatomía Profunda de Cuellos de Botella y Modos de Falla (¿Por qué no funcionó como Clockwork?)

La metrología longitudinal de las 14 corridas demuestra que cuando C2C opera en condiciones ideales nominales o con alta disciplina de prompts (ej. `solow_model_v15` o `estadistica_asintotica`), **converge en 26–32 minutos con 100% de acuerdo ciego**. Sin embargo, en las corridas con fricción en autores, stragglers o estrés masivo, el tiempo se elevó a **40–366 minutos**. A continuación se analizan a profundidad los **12 cuellos de botella y factores de fricción sistémica**:

### 2.1. Cuello de Botella #1: Colisión Sintáctica KaTeX en f-strings de Python vs Reglas R-20 y R-03
- **Severidad Registrada:** CRÍTICA (Detonador del 55% de los Stragglers)
- **Corridas e Incidencias Afectadas:** `f9b9d459` (Saúl Std, Shard 05), `afb5aa18` (Saúl Coarse v2, Shards 03, 06, 07), `b9316152` (Econometría, Shard 06: 13 errores y 84 turnos en C-11/C-12), `acdc402d` (Saúl Fine, Shards 12, 15, 17), `4ceacf92` (Solow v15, Shard 06), `f2be91cd` (Solow Append, Shard 03).
- **Archivos y Líneas Clave en el Código (Evidencia Técnica en Repositorio):**
  - [`engine/assemble.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/assemble.py#L101-L166): Motor de interpolación de plantillas paramétricas `render_template(template_str, vars)` y función `_replacer()`.
  - [`engine/assemble.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/assemble.py#L169-L272): Función `sanitize_katex_syntax(text)` con heurísticas de auto-reparación de llaves `frac_den_fix` (líneas 251–256) y `script_outer_fix` (líneas 259–264) que insertaban incondicionalmente llaves `}` ante delimitadores `\left(` y `\right)`.
  - [`system_prompts/prompt_shard_author.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/prompt_shard_author.md#L45-L60): Reglas de codificación de tuplas paramétricas y prohibición de f-strings KaTeX sin escapar.
- **Causa Raíz Técnica:** En la etapa de autoría (Stage 3), los subagentes redactan código Python (`generate_py`) que interpola variables paramétricas en cadenas de texto. Al usar cadenas f-string o `.format(**vars)` sobre expresiones matemáticas con llaves LaTeX (ej. fracciones `\frac{y}{a}`, potencias `K^{0.5}`, matrices `\begin{pmatrix}`, soluciones de EDPs `$u(x, y) = C e^{k(x+y/a)}$`), Python interpreta `{...}` como marcadores de interpolación no definidos (`KeyError: '0.5'`, `KeyError: 'pmatrix'`). Cuando el subagente intenta escapar con llaves dobles `{{...}}`, la función de saneamiento `sanitize_katex_syntax` en `engine/assemble.py` poseía expresiones regulares (`script_outer_fix`, `frac_den_fix`) que insertaban incondicionalmente llaves de cierre `}` ante delimitadores `\left(` y `\right)`, corrompiendo la expresión y disparando la regla estática `[R-20: SINTAXIS / LLAVES]` por llaves desbalanceadas o residuales.
- **Impacto en Rendimiento y Autonomía:** Los subagentes quedaron atrapados en micro-bucles interactivos de 30 a 62 turnos por shard. En `f9b9d459`, Shard 05 tardó **1,426 segundos (23.8 min)** frente a la mediana de 9.5 min (+856s de retención en la barrera síncrona). En `f2be91cd`, Shard 03 consumió **18.09M tokens y 41.7 minutos**. Esto provocó además el disparo automático de disyuntores de intentos (`circuit_breaker_Hab-12.json`), bloqueando la compilación.
- **Solución Arquitectónica Permanente (Clockwork):**
1. **Reemplazo de `.format(**vars)` por sustitución regex selectiva:** En `engine/assemble.py`, sustituir únicamente `{identificador}` si `identificador in vars`.
2. **Guarda condicional de llaves:** `if text.count('{') > text.count('}'):` antes de aplicar `script_outer_fix` y `frac_den_fix`.
3. **Uso obligatorio de raw-strings `r"..."`:** Prohibir terminantemente f-strings con KaTeX en el system prompt de `c2c_shard_author`.

---

### 2.2. Cuello de Botella #2: Conflicto Epistémico y Desconexión de Prompts en Blind Judges (Stage 5)
- **Severidad Registrada:** CRÍTICA (Provocó el colapso del 95% de los jueces en pasada 1 de `acdc402d`)
- **Corridas e Incidencias Afectadas:** `acdc402d` (Saúl Fine, 19/20 jueces abortados), `18ae4bcc` (Solow v13, truncamiento juez 1), `812bfecd` (Solow Base, particionado manual).
- **Archivos y Líneas Clave en el Código (Evidencia Técnica en Repositorio):**
  - [`system_prompts/prompt_blind_judge.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/prompt_blind_judge.md#L9-L15): Scope-Lock mandatorio con prohibición taxativa de lectura de archivos en disco (`"🚫 PROHIBIDO llamar a view_file para leer archivos del disco... Toda la información requerida ya está en tu prompt inicial"`).
  - [`dispatch.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/dispatch.py#L1036-L1050): Función `dispatch_judges(work_dir, pointer=..., max_items_per_judge=12)`.
  - [`dispatch.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/dispatch.py#L1214-L1225): Ensamblado de *Pointer Prompts* mediante `make_pointer_prompt(role_name, work_order_rel, done_signal)` que obligaba al juez a leer `work/dispatch/items/judge_XX.json` del disco, entrando en colisión directa con su System Prompt.
- **Causa Raíz Técnica:** El archivo de instrucciones del sistema `c2c_judge/agent.md` establecía un mandato estricto de seguridad: *'All items are already in your prompt. You must strictly NOT read files from disk.'* Sin embargo, para evitar saturar el contexto del Director en C2C v3.2, el comando `dispatch-judges` cambió a la arquitectura Swift-Dispatch con *Pointer Prompts*, ordenando al juez: *'Read work order file courses/.../work/dispatch/items/judge_XX.json from disk.'* Ante esta contradicción normativa directa, los modelos en modo razonamiento puro (`thinking`) priorizaron la regla de seguridad del system prompt y abortaron inmediatamente en 5 segundos reportando un conflicto ético-técnico.
- **Impacto en Rendimiento y Autonomía:** En la prueba de estrés de 118 competencias (`acdc402d`), 19 de los 20 jueces fallaron al instante (0% de acuerdo inicial). El Director tuvo que intervenir manualmente creando el script `gen_authorized_judges.py` (Pasos 411 a 435), reescribir los prompts de los 20 jueces inyectando una exención explícita de lectura, y re-despacharlos en 4 oleadas secuenciales de 5 jueces, agregando **13.76 minutos (825.7s)** de tiempo de pared.
- **Solución Arquitectónica Permanente (Clockwork):**
Armonización de la plantilla `c2c_judge/agent.md` integrando la cláusula canónica de acceso: *'You are strictly authorized and required to read ONLY your designated work order file `work/dispatch/items/judge_XX.json`'*, o inyectar directamente el lote de hasta 12 preguntas dentro del mensaje de despacho sin requerir lectura de disco (Zero-Warmup Inline Batch).

---

### 2.3. Cuello de Botella #3: Anti-Patrón de Reescritura Monolítica Masiva vs Edición Quirúrgica en Shards
- **Severidad Registrada:** ALTA (Multiplicador de 3x a 5x en tiempo de pared y consumo de tokens)
- **Corridas e Incidencias Afectadas:** `a53e6af1` (Shard 02: 785s monolítico vs Shard 03: 579s atómico), `afb5aa18` (Shard 05: 3 reescrituras completas), `acdc402d` (Shard 15: 23k tokens out por turno).
- **Archivos y Líneas Clave en el Código (Evidencia Técnica en Repositorio):**
  - [`system_prompts/prompt_shard_author.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/prompt_shard_author.md#L16-L27): Cláusulas de Scope-Lock y archivos autorizados.
  - [`subagent_types.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/subagent_types.json#L13-L50): Especificación canónica de `c2c_shard_author`, instruyendo el uso de `replace_file_content` sobre el Mapa de Líneas Pre-Indexado (`StartLine..EndLine`) para reparaciones quirúrgicas de 10–25 líneas.
  - [`compile_shard.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_shard.py#L820-L865): Mapeo determinista de errores con señalamiento exacto de número de línea de la tupla (`StartLine..EndLine`) en `shard_XX_data.py`.
- **Causa Raíz Técnica:** Cuando el validador `compile_shard.py` rechazaba un shard por un fallo puntual en 1 de sus 6 competencias (ej. `Hab-02`), el subagente utilizaba `write_to_file` con `Overwrite=True` para regenerar el archivo íntegro `shard_XX_data.py` (de 400 a 700 líneas de código). Generar 20,000 a 27,000 tokens en un solo turno de salida toma entre 2.5 y 4.2 minutos de streaming continuo por intento, arriesgando además el límite de tokens de salida de Gemini Flash (`unexpected EOF / Token Limit Cutoff`).
- **Impacto en Rendimiento y Autonomía:** En `a53e6af1`, Shard 02 necesitó 785s con sólo 11 turnos debido a una reescritura monolítica de 4 minutos, mientras que Shard 03 realizó 42 micro-turnos con `replace_file_content` y terminó en 579s (**206 segundos más rápido**). En `acdc402d`, Shard 15 sufrió truncamiento forzoso en el Turno 7 por emitir más de 8,192 tokens de salida, quedando en estado inconsistente y demorando **1,265 segundos (21.1 min)**.
- **Solución Arquitectónica Permanente (Clockwork):**
1. Prohibición estricta en el Scope-Lock de `write_to_file(Overwrite=True)` sobre `shard_XX_data.py` una vez inicializado el archivo.
2. Pre-siembra obligatoria de scaffolds en $t=0$ y emisión exclusiva de `replace_file_content` utilizando el **Mapa de Líneas Pre-Indexado** (`StartLine..EndLine`, `gen`, `hints`, `sol`) para que cada arreglo modifique únicamente el bloque de 10 a 25 líneas afectado.

---

### 2.4. Cuello de Botella #4: Disparo Persistente del Circuit Breaker (`.check_attempts` / `BUDGET HALT`) sin Auto-Reset
- **Severidad Registrada:** ALTA (Causa de bucles ciegos e intervenciones del supervisor en 4 corridas)
- **Corridas e Incidencias Afectadas:** `f9b9d459` (Hab-12, Step 239/241), `afb5aa18` (Shard 06 abandonado), `0f573810` (Shard 01), `f2be91cd` (Shard 03, 19 edits bloqueados).
- **Archivos y Líneas Clave en el Código (Evidencia Técnica en Repositorio):**
  - [`compile_shard.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_shard.py#L661-L693): Bucle de compilación acotado `[COMPILE n/6]` en `.check_attempts/compile_{norm_shard_id}.json` que incrementaba acumulativamente el contador sin verificar si el hash SHA-256 del código del shard había cambiado.
  - [`check_templates.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/check_templates.py#L2540-L2555): Resolución y lectura de directorios efectivos de intentos `.check_attempts`.
- **Causa Raíz Técnica:** El disyuntor de seguridad en `check_templates.py` / `compile_shard.py` bloquea la compilación (`BUDGET HALT`) tras 6 intentos consecutivos fallidos. Sin embargo, el disyuntor registraba el fallo de forma puramente acumulativa en `work/.check_attempts/compile_shard_XX.json` sin comparar el hash del código fuente. Cuando el subagente descubría el error y aplicaba la corrección matemática correcta en `shard_XX_data.py`, el validador seguía respondiendo `FAIL: CIRCUIT BREAKER TRIPPED` de inmediato sin evaluar el nuevo código.
- **Impacto en Rendimiento y Autonomía:** Los subagentes entraron en pánico cognitivo: al ver que su código corregido seguía siendo rechazado con el mismo mensaje de disyuntor, comenzaron a leer compulsivamente `compile_shard.py` (hasta 91 veces en Run 5) o abandonaron el turno pidiendo ayuda. El Director se vio forzado a intervenir manualmente con `write_to_file` para sobreescribir los contadores a `{"count": 0}`.
- **Solución Arquitectónica Permanente (Clockwork):**
Circuit Breaker con Hash SHA-256 de Contenido: El disyuntor debe almacenar el hash SHA-256 del bloque de código evaluado. Si el hash actual difiere del hash anterior (el autor editó el archivo), el disyuntor debe **reiniciar inmediatamente el contador de intentos a 0** y permitir la compilación limpia del nuevo código.

---

### 2.5. Cuello de Botella #5: Ocultamiento del Traceback de Python en Sandbox (`[TPL-DRY]`) y Caza a Ciegas
- **Severidad Registrada:** ALTA (Provocó más de 250 lecturas estáticas de ingeniería inversa sobre el código core)
- **Corridas e Incidencias Afectadas:** `7818f6af` (91 `view_file` a `compile_shard.py`), `f2be91cd` (86 lecturas), `b9316152` (64 lecturas acumuladas: Shard 02 con 29, Shard 06 con 14, Shard 07 con 11, Shard 01 con 10), `0f573810` (32 lecturas), `afb5aa18` (Shard 07: 16 lecturas), `a53e6af1` (Shard 03: 10 lecturas). *(En agudo contraste, `d52ee475` registró exactamente 0 lecturas de ingeniería inversa sobre el validador, demostrando que scaffolds limpios erradican este antipatrón)*.
- **Archivos y Líneas Clave en el Código (Evidencia Técnica en Repositorio):**
  - [`check_templates.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/check_templates.py#L760-L825): Implementación de la función diagnóstica `_format_tpl_dry_diagnostics` para mapear excepciones a marcos de traceback y números de línea de `generate_py` / `verify_py`.
  - [`check_templates.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/check_templates.py#L1895-L1930): Diagnóstico `[TPL-DRY: FALLO EN EJECUCIÓN DRY-RUN]` emitido durante la evaluación de 50 semillas estocásticas en sandbox.
- **Causa Raíz Técnica:** Durante el ensayo de 50 semillas aleatorias en sandbox (`dry-run`), si `generate_py` o `verify_py` lanzaban una excepción de Python (`KeyError`, `ZeroDivisionError`, `TypeError`, `UnboundLocalError`), `compile_shard.py` capturaba genéricamente la excepción e imprimía: `[-] [TPL-DRY] La ejecución en sandbox falló en 50/50 semillas evaluadas. | Acción: Revisar la excepción en generate_py...` ocultando por completo el tipo de excepción, el mensaje de error y el número de línea exacto.
- **Impacto en Rendimiento y Autonomía:** Al no saber si el fallo era por una división entre cero en una semilla o por una variable no declarada, los subagentes autores asumieron que el validador tenía un defecto o reglas ocultas. Procedieron a leer en fragmentos de 100 líneas el código fuente de `compile_shard.py` y `check_templates.py`, consumiendo decenas de turnos y acumulando millones de tokens de caché sin avanzar en la autoría.
- **Solución Arquitectónica Permanente (Clockwork):**
Impresión diagnóstica transparente en `[TPL-DRY]`: Imprimir siempre la semilla fallida (ej. `seed=42`), los parámetros generados, `type(exc).__name__: str(exc)` y el traceback formateado de las últimas 3 líneas de código de `generate_py`. A la par, prohibir taxativamente en el Scope-Lock de `c2c_shard_author` la lectura de archivos fuera de su directorio de trabajo.

---

### 2.6. Cuello de Botella #6: Desorientación de Esquema Inicial y Búsquedas Exploratorias Ilegítimas en CTA Architects
- **Severidad Registrada:** MEDIA-ALTA (Pérdida de 4 a 12 minutos en Stage 1B)
- **Corridas e Incidencias Afectadas:** `afb5aa18` (CTA part_04: 777s, explorando carpetas de otras corridas), `18ae4bcc` (CTA: 23.9 min, 20 micro-edits), `7818f6af` (CTA: 33.4 min).
- **Archivos y Líneas Clave en el Código (Evidencia Técnica en Repositorio):**
  - [`system_prompts/prompt_cta_architect.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/prompt_cta_architect.md#L9-L31): Cláusula de Scope-Lock prohibiendo lecturas de scripts de compilación, de cursos de otros workspaces o comandos exploratorios de terminal.
  - [`system_prompts/prompt_cta_architect.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/prompt_cta_architect.md#L44-L80): Especificaciones de densidad curricular según el modo (`fine`, `standard`, `coarse`).
  - [`compile_cta.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_cta.py#L120-L210): Reglas de certificación determinista L1–L5 de esquemas pedagógicos.
- **Causa Raíz Técnica:** En las corridas con particionado MapReduce de PDFs extensos (103 páginas), a los subagentes `CTA Architect part_NN` se les despachaba sin un ejemplo canónico autocontenido de la tupla de datos `COMPETENCIES` dentro de su orden de trabajo. En `afb5aa18` (part_04), el subagente ejecutó comandos de terminal buscando ejemplos en carpetas ajenas: `Get-ChildItem courses/practica_parcial_saul_standard_coarse/work/cta_parts` y leyó archivos de corridas anteriores, perdiendo más de 4 minutos.
- **Impacto en Rendimiento y Autonomía:** Stage 1B requirió entre 12.9 y 26.5 minutos en corridas MapReduce. Además, al carecer de auto-healing temprano de KaTeX, los arquitectos emitían tuplas con `$$` o fórmulas sin envolver en `$`, requiriendo múltiples rondas de micro-edición con `replace_file_content`.
- **Solución Arquitectónica Permanente (Clockwork):**
Inyección obligatoria de una plantilla sintáctica canónica de 12 líneas en el prompt de despacho de `c2c_cta_architect`, aislamiento estricto de rutas (prohibir `Get-ChildItem` sobre la raíz de `courses/`), y auto-sanitizador determinista L1–L5 en `compile_cta.py` que auto-balancee signos `$`, convierta `$$` en `$` y envuelva comandos matemáticos sueltos (`\alpha`, `\beta`, `\frac`) antes de validar.

---

### 2.7. Cuello de Botella #7: Fricción de Consola en Windows: Comillas Anidadas en PowerShell y Scripts Scratch
- **Severidad Registrada:** MEDIA (Causa directa de fallos en el Director y generación de scripts secundarios)
- **Corridas e Incidencias Afectadas:** `4ceacf92` (Paso 31: `dump_prompts.py`), `f9b9d459` (Paso 104: `$Host.UI.RawUI.BufferSize`), `18ae4bcc` (Pasos 143–165: 5 fallos de `python -c`), `0f573810` (Pasos 450–463: UTF-8 en PowerShell).
- **Archivos y Líneas Clave en el Código (Evidencia Técnica en Repositorio):**
  - [`course_publisher.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/course_publisher.py#L50-L55): Función `is_corrupted_unicode(text)` que detecta caracteres de reemplazo `\ufffd`.
  - [`course_publisher.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/course_publisher.py#L124-L130): Mecanismo de recuperación automática que lee el título nativo UTF-8 desde `cta.json` ante corrupción de la consola Windows.
  - [`prepare.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/prepare.py#L76-L85): Detección preventiva de títulos corrompidos en Stage 0.
  - [`run.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/run.py#L212-L235): Saneamiento integral de CLI en el runner orquestador.
- **Causa Raíz Técnica:** En el entorno Windows PowerShell, la invocación de one-liners `python -c "..."` con comillas dobles o comillas simples anidadas, o el uso de f-strings de Python dentro de comillas de PowerShell, produce errores inmediatos de parsing sintáctico de la shell: `SyntaxError: unterminated string literal` o `Select-String : La cadena no se reconoce`. Asimismo, PowerShell utiliza por defecto codificación de consola ANSI/CP1252, provocando que parámetros como `--title "Estadística: Regresión"` llegaran al proceso Python como `Estad�stica: Regresi�n`.
- **Impacto en Rendimiento y Autonomía:** El Director gastó múltiples turnos y minutos reintentando comandos fallidos en PowerShell. En `4ceacf92`, el modelo tuvo que reflexionar en sus thinking traces sobre la hostilidad de PowerShell con f-strings y crear un script dedicado `dump_prompts.py` en scratch. En `0f573810`, el orquestador requirió 12 turnos manuales para reparar la corrupción de caracteres del título.
- **Solución Arquitectónica Permanente (Clockwork):**
1. **Prohibición de one-liners complejos con comillas en PowerShell:** El Director debe escribir scripts auxiliares en `scratch/` o invocar comandos predefinidos en el CLI del skill (`run.py`).
2. **Resiliencia UTF-8 en `course_publisher.py`:** Leer el título por defecto directamente desde `cta.json` / `pre_cta_manifest.json` (codificado en UTF-8 nativo) si el argumento CLI `--title` contiene caracteres de reemplazo `\ufffd`.

---

### 2.8. Cuello de Botella #8: Lotes Monolíticos en Jueces Ciegos y Límite de Tokens de Salida (Stage 5)
- **Severidad Registrada:** ALTA (Causa de truncamiento silencioso y CHECKPOINTS de compactación)
- **Corridas e Incidencias Afectadas:** `18ae4bcc` (Juez 1 truncado en preg 22/48), `812bfecd` (Prompts de 88.7 KB), `0f573810` (Paso 407: CHECKPOINT por leer 260 KB en view_file). *(Tanto `b9316152` con 3 jueces como `d52ee475` con 5 jueces ratifican el éxito de la mitigación: particionado nativo en lotes de <= 12 reactivos con 100% de acuerdo y 0 truncamientos)*.
- **Archivos y Líneas Clave en el Código (Evidencia Técnica en Repositorio):**
  - [`dispatch.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/dispatch.py#L1039): Declaración de cuota máxima de evaluación: `max_items_per_judge: int = 12`.
  - [`dispatch.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/dispatch.py#L1052-L1115): Algoritmo de división nativa de batches (`split_batches`) que particiona `judge_batch.json` en sub-archivos de máximo 12 reactivos por juez para respetar el techo de 8,192 tokens de salida.
- **Causa Raíz Técnica:** En las primeras versiones de C2C v3, el comando `dispatch-judges` agrupaba entre 42 y 48 preguntas psicométricas en un solo archivo monolítico para un único juez. Al evaluar 48 ítems con análisis paso a paso por primeros principios, la respuesta del modelo superaba los 8,192 tokens máximos de salida de Gemini Flash, cortando el JSON a la mitad. Adicionalmente, en `0f573810`, el Director intentó inspeccionar simultáneamente 4 archivos de jueces con `view_file` (>260 KB en total), saturando la ventana de contexto y disparando el mecanismo de compactación forzosa `CHECKPOINT`.
- **Impacto en Rendimiento y Autonomía:** En `18ae4bcc`, el Director tuvo que escribir scripts ad-hoc de PowerShell para particionar `judge_batch.json` en 4 lotes de 12 ítems y lanzar 4 jueces nuevos. En `0f573810`, tras el CHECKPOINT el Director perdió la instrucción de cómo invocar subagentes y resolvió la verificación mediante un script programático local.
- **Solución Arquitectónica Permanente (Clockwork):**
1. **Particionado Nativo en sub-lotes de $\le 12$ ítems:** `cmd_dispatch_judges` debe generar obligatoriamente archivos `judge_batch_01..0K.json` con máximo 12 reactivos por juez.
2. **Prohibición de volcar lotes al contexto del Director:** El Director nunca debe hacer `view_file` sobre los lotes de preguntas, despachando únicamente las rutas a los subagentes.

---

### 2.9. Cuello de Botella #9: Bloqueo por Cuota Exógena de API (`Error 429 / RESOURCE_EXHAUSTED`) Inducido por Stragglers Descontrolados
- **Severidad Registrada:** CRÍTICA EN PRODUCCIÓN (249 minutos de congelamiento en Runs 2, 5 y 6)
- **Corridas e Incidencias Afectadas:** `0f573810` (Estadística Regresión: 366 min total / 248.8m congelado), `7818f6af` (Solow v14: 329 min total / 249.2m congelado), `f2be91cd` (Solow Append: 339 min total / 248.8m congelado).
- **Archivos y Líneas Clave en el Código (Evidencia Técnica en Repositorio):**
  - [`budget_guard.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/budget_guard.py#L28-L38): Límites de SLA: `DEFAULT_MAX_TURNS = 40`, `DEFAULT_MAX_TOKENS = 5_000_000`, `DEFAULT_MAX_SCRIPT_LOOPS = 5`.
  - [`budget_guard.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/budget_guard.py#L220-L310): Algoritmo de detección de runaway en `transcript.jsonl` que aborta subagentes descontrolados y despacha agentes de reparación atómica (`c2c_repair`).
- **Causa Raíz Técnica:** Entre las `07:03 UTC` y las `11:12 UTC` del 17 de octubre, tres subagentes stragglers concurrentes (`Shard 01` en Run 2 con 136 turnos; `Shard 04` en Run 5 con 131 turnos; `Shard 03` en Run 6 con 132 turnos) cayeron en bucles de lectura e ingeniería inversa, leyendo `compile_shard.py` entre 32 y 91 veces. Cada turno re-enviaba hasta 600,000 tokens de contexto y caché, quemando más de **52.6 millones de tokens** en menos de 40 minutos. Esto agotó por completo la cuota por minuto/hora del proyecto en la API de Gemini, provocando el congelamiento simultáneo de los tres pipelines durante más de 4 horas.
- **Impacto en Rendimiento y Autonomía:** Tres cursos de producción quedaron congelados durante 4.1 horas, elevando artificialmente el tiempo de pared a más de 300 minutos y degradando las métricas de throughput a niveles irrisorios (1.6 a 2.8 preguntas/minuto) hasta que la cuota se restableció.
- **Solución Arquitectónica Permanente (Clockwork):**
**Watchdog Automatizado de Presupuesto (`budget_guard.py`):** El Director debe agendar un temporizador reactivo (`schedule`) a los 8 minutos de iniciar Stage 3. Si cualquier subagente supera los 40 turnos o los 5M tokens, el watchdog debe abortar inmediatamente el proceso con `manage_subagents(kill)`, evitando la quema descontrolada de cuota y lanzando un agente especializado de reparación quirúrgica (`c2c_repair`).

---

### 2.10. Cuello de Botella #10: Destrucción Accidental de Directorios de Trabajo en Caliente (`delete_course.py`)
- **Severidad Registrada:** CRÍTICA DE ENTORNO (Pérdida total de `work/` en Runs 1, 2 y 3)
- **Corridas e Incidencias Afectadas:** `876ad3df` (PDE Saúl 1: Shard 02 perdió sus archivos), `0f573810` (Estadística: pérdida de `pre_cta_manifest.json`), `9ed41fb3` (Práctica Saúl: rescate manual de manifiesto).
- **Archivos y Líneas Clave en el Código (Evidencia Técnica en Repositorio):**
  - [`.agents/skills/delete-course/scripts/delete_course.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/delete-course/scripts/delete_course.py#L46-L54): Tupla `ACTIVE_WORKSPACE_STATE_FILES` con archivos de resguardo (`work/state.json`, `work/pre_cta_manifest.json`, `work/cta_data.py`).
  - [`.agents/skills/delete-course/scripts/delete_course.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/delete-course/scripts/delete_course.py#L63-L115): Función de seguridad `is_active_workspace(course_dir, max_age_seconds=24*3600)` que previene la eliminación de directorios activos o modificados en las últimas 24 horas.
  - [`.agents/skills/delete-course/scripts/delete_course.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/delete-course/scripts/delete_course.py#L512-L541): Función `clean_orphan_course_dirs(dry_run)`.
  - [`tests/test_delete_course.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/test_delete_course.py#L172-L245): Test unitario `test_clean_orphan_dirs` aislado mediante `monkeypatch` para garantizar que nunca opere sobre `courses/` en vivo.
- **Causa Raíz Técnica:** La función de limpieza `clean_orphan_course_dirs(dry_run=False)` en `delete_course.py` eliminaba con `shutil.rmtree` cualquier subdirectorio `courses/<id>/` que no contara con su archivo final `courses/<id>.json`. Pero en C2C, `courses/<id>.json` se escribe recién en Stage 6 (`publish`). Cuando una sesión paralela ejecutó la suite de tests unitarios de pytest a las `05:47:02 UTC`, el test `test_clean_orphan_dirs` ejecutó la limpieza contra el directorio de producción real, borrando en vivo el `work/` de las 3 corridas activas.
- **Impacto en Rendimiento y Autonomía:** En Run 1 (`pde_saul_1`), `Shard 02` invirtió 181 turnos buscando sus archivos y el Director tuvo que reconstruir `cta_data.py` extrayéndolo del transcript del subagente CTA. En Run 2, el CTA 1 perdió su trabajo tras 28 minutos y 5.28M tokens consumidos.
- **Solución Arquitectónica Permanente (Clockwork):**
1. En `delete_course.py`: Prohibir la eliminación de carpetas que contengan `work/state.json`, `work/pre_cta_manifest.json` o archivos con menos de 24 horas de antigüedad.
2. En `test_delete_course.py`: Aislar estrictamente los tests unitarios en un directorio temporal `tmp_path` mediante `monkeypatch`.

---

### 2.11. Cuello de Botella #11: Ceguera Delta en Modo `--append` (Falta de Reutilización de Competencias Previas)
- **Severidad Registrada:** MEDIA (Gasto redundante de 7.68M tokens y remapeo heurístico tardío)
- **Corridas e Incidencias Afectadas:** `f2be91cd` (Solow Append: +24 competencias añadidas a las 21 existentes).
- **Archivos y Líneas Clave en el Código (Evidencia Técnica en Repositorio):**
  - [`prepare.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/prepare.py#L264-L300): Lectura e inspección del curso existente en `courses/<id>.json` para extraer competencias preexistentes y generar offset de IDs continuos en `manifest['delta']`.
  - [`course_publisher.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/course_publisher.py#L156-L315): Fusión incremental de reactivos y competencias en `existing_data` con logging de nuevos totales acumulados.
  - [`run.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/run.py#L1242): Soporte CLI para la bandera `--append`.
- **Causa Raíz Técnica:** Al ejecutar C2C en modo `--append`, las Etapas 0 a 5 operaban en un espacio de trabajo aislado `work_append/` sin leer el curso preexistente (`courses/<id>.json`). Como consecuencia, el CTA volvía a extraer competencias desde el principio (`C-01`, `Hab-01`), analizando nuevamente todo el material base y requiriendo que en Stage 6 `course_publisher.py` aplicara un remapeo heurístico tardío de IDs a `C-11..C-21` y `Q-<comp>-app-<num>`.
- **Impacto en Rendimiento y Autonomía:** Gasto redundante de 7.68 millones de tokens y riesgo de desajustes psicométricos si las competencias preexistentes se redefinían conceptualmente.
- **Solución Arquitectónica Permanente (Clockwork):**
En `run.py --stage prepare --append`: Leer obligatoriamente `courses/<id>.json`, inyectar la lista de competencias ya cubiertas y los índices más altos por categoría en `pre_cta_manifest.json`, e instruir al CTA a generar únicamente competencias incrementales con identificadores continuos desde $t=0$.

---

### 2.12. Cuello de Botella #12: Paradoja de Granularidad: Stragglers Cognitivos en Modo Coarse vs Complejidad Combinatoria en Fine
- **Severidad Registrada:** ESTRUCTURAL / PEDAGÓGICA
- **Corridas e Incidencias Afectadas:** Comparativa directa: `afb5aa18` (Coarse v2: 160k tok/preg, 60 min) vs `f9b9d459` (Standard: 45k tok/preg, 64 min, 24.8 QPM) vs `acdc402d` (Fine: 36k tok/preg, 85 min, 17 intervenciones).
- **Archivos y Líneas Clave en el Código (Evidencia Técnica en Repositorio):**
  - [`plan_shards.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/plan_shards.py#L1-L9): Heurística de dimensionamiento de shards `comps_per_shard = clamp(ceil(N / 8), 2, 6)` que balancea la carga cognitiva de los autores.
  - [`system_prompts/prompt_cta_architect.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/prompt_cta_architect.md#L44-L65): Directiva de granularidad (`standard`: 60–70 comps, ~1,500 reactivos) definida como el sweet spot óptimo para evitar parálisis en modo coarse o saturación en modo fine.
- **Causa Raíz Técnica:** El dilema de granularidad curricular demostró un comportamiento no lineal:
- **Modo Coarse (13–14 competencias):** Se diseñó con la hipótesis de ser más rápido, pero forzó a los subagentes autores a condensar bloques teóricos demasiado extensos (ej. trayectorias completas de sistemas dinámicos y EDPs en un solo reactivo), provocando parálisis cognitiva, fórmulas gigantescas y desbalances de llaves (160k tokens/pregunta).
- **Modo Fine (118 competencias):** Logra la máxima economía unitaria pura (**36,040 tokens/pregunta**, 1.80 s/pregunta), pero escala la coordinación a 67 subagentes, llevando al orquestador al borde del agotamiento de contexto y requiriendo 17 intervenciones manuales.
- **Modo Standard (65 competencias):** Constituye el **punto óptimo de equilibrio de ingeniería (Sweet Spot)**: 1,590 preguntas en 64 minutos, 24.76 preguntas/minuto, 44,933 tokens/pregunta y solo 3 intervenciones benignas.
- **Impacto en Rendimiento y Autonomía:** La elección incorrecta de granularidad puede triplicar el costo en tokens o disparar la tasa de intervenciones manuales requeridas.
- **Solución Arquitectónica Permanente (Clockwork):**
Estandarizar el modo **`granularity: standard`** (1 competencia por cada 1.5 a 2 páginas de contenido conceptual o 25–35 preguntas por shard) como la política operativa por defecto de C2C en producción.

---

### 2.13. Cuello de Botella #13: Brecha en Tiempo de Inicialización End-to-End (3 a 5 Minutos Reales vs Target SLA de 1 Minuto)
- **Severidad Registrada:** ALTA / OPERATIVA (Incumplimiento de SLA inicial en el 100% de las corridas)
- **Corridas e Incidencias Afectadas:** Presente en **todas las 12 corridas**. Notorio en `f9b9d459` (553s / 9.2 min de ramp-up inicial), `a53e6af1` (240s), `acdc402d` (310s) y `4ceacf92` (185s).
- **Archivos y Líneas Clave en el Código (Evidencia Técnica en Repositorio):**
  - [`prepare.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/prepare.py#L35-L115): Ingesta, escaneo de fuentes y PyMuPDF.
  - [`run.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/run.py#L75-L160): Pre-flight checks, resolución de flags y verificación de directorios.
- **Causa Raíz Técnica:**  
  Existe una desconexión entre la metrología del script aislado y la experiencia operativa del pipeline:
  1. El script puntual `prepare.py` se ejecuta en apenas 2 a 4 segundos de cómputo síncrono.
  2. Sin embargo, la **fase completa de inicialización end-to-end toma sistemáticamente entre 3 y 5 minutos (180 a 300 segundos)** frente al **target SLA de 1 minuto (60 segundos)**.
  3. Causas del retardo:
     - **Inspección de Archivos y Pre-flight Checks no Optimizados:** El Director inspecciona secuencialmente directorios, verifica la integridad de múltiples PDFs (de hasta 103 páginas y 10.4 MB) y evalúa el historial previo antes de emitir la llamada al script.
     - **Extracción PyMuPDF y Segmentación Vectorial:** La apertura de documentos, renderizado de previsualizaciones y extracción estructural genera esperas síncronas de I/O en disco.
     - **Ramp-up y Ensamble de Prompts del Director:** La preparación del manifiesto `pre_cta_manifest.json` y la redacción del payload inicial para el arquitecto CTA consumen de 2 a 4 turnos conversacionales antes del fan-out.
- **Impacto en Rendimiento:** Se consumen entre 120s y 240s de retraso no aprovechado en cada ejecución, postergando el arranque del cómputo paralelo.
- **Solución Arquitectónica Permanente (Clockwork):**
  1. **One-Shot Fast-Track Prepare:** Empaquetar el escaneo de fuentes, la extracción PyMuPDF y la generación de `pre_cta_manifest.json` en un único binario/comando optimizado en C/Python que corra en $< 15\text{ segundos}$.
  2. **Zero-Turn CTA Dispatch:** Permitir que `run.py --stage prepare` despache inmediatamente el subagente CTA al finalizar la preparación, reduciendo el wall-clock de inicialización a **$\le 45\text{ segundos}$** y cumpliendo holgadamente con el target SLA de 1 minuto.

---

## 3. Matriz Forense Comparativa: Solow v15 frente al Linaje Saúl (5 Corridas de la Conversación)

| Métrica / Dimensión | `4ceacf92` (Solow v15) | `a53e6af1` (Saúl Coarse v1) | `f9b9d459` (Saúl Standard) | `afb5aa18` (Saúl Coarse v2) | `acdc402d` (Saúl Fine / Masivo) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Entrada (PDFs / Páginas)** | 1 PDF (36 págs, 1.49 MB) | 7 PDFs (103 págs, 10.39 MB) | 7 PDFs (103 págs, 10.39 MB) | 7 PDFs (103 págs, 10.39 MB) | 7 PDFs (103 págs, 10.39 MB) |
| **Competencias Extraídas (CTA)** | 15 comp | 13 comp | **65 comp** | 14 comp | **118 comp** |
| **Reactivos Publicados** | 360 preguntas | 320 preguntas | **1,590 preguntas** | 370 preguntas | **2,850 preguntas** |
| **Subagentes Desplegados** | 12 subagentes | 11 subagentes | 30 subagentes | 17 subagentes | **67 subagentes** |
| **Tiempo Total de Pared (Wall)** | **27.10 min** (1,626s) | **32.83 min** (1,970s) | 64.22 min (3,853s) | 60.03 min (3,602s) | 85.65 min (5,139s) |
| **Stage 1 (CTA) Wall-Clock** | 9.91 min (594.4s) | 12.95 min (776.9s) | 12.11 min (726.3s) | 16.10 min (965.7s) | **21.10 min** (1,265.9s) |
| **Stage 3 (Shards) Wall-Clock** | 11.27 min (675.9s) | 14.70 min (882.3s) | 33.80 min (2,027.7s) | 37.58 min (2,254.7s) | **45.02 min** (2,701.4s) |
| **Stage 5b (Jueces) Wall-Clock** | 4.12 min (247.0s) | 2.85 min (171.0s) | 7.36 min (441.6s) | 3.87 min (232.0s) | **13.76 min** (825.7s) |
| **Parallel Speedup Factor** | 3.32x | 3.33x | 3.92x | 3.03x | **5.17x** |
| **Throughput (Preguntas/Minuto)**| 13.28 preg/min | 9.74 preg/min | **24.76 preg/min** | 6.16 preg/min | **33.27 preg/min** |
| **Costo Unitario (Tokens/Pregunta)**| 61,291 tok/preg | 66,027 tok/preg | **44,933 tok/preg** | 160,187 tok/preg | **36,040 tok/preg** |
| **Segundos de Pared / Pregunta** | 4.52 s/preg | 6.16 s/preg | 2.42 s/preg | 9.74 s/preg | **1.80 s/preg** |
| **Intervenciones Manuales** | 🛠️ 1 (8s, benigna) | **🛠️ 0 (Autonomía 100%)**| 🛠️ 3 (Reset + Regex fix) | 🛠️ 5 (Prompt + Shard 06) | 🛠️ 17 (Crisis múltiples) |
| **Acuerdo Blind Judges Pass 1** | ✅ **100% (30/30)** | ✅ **100% (26/26)** | ✅ **98.5% (128/130)** | ✅ **100% (28/28)** | ❌ **0% pass 1 $\to$ 100% pass 2** |

---

### 3.1. Matriz Forense Comparativa: Nuevas Corridas de Producción frente a Benchmarks de Referencia

A fin de situar cuantitativamente las dos nuevas corridas frente al estándar dorado de alta velocidad (`Solow Model v15`, `4ceacf92`) y el estándar balanceado multi-documento (`Práctica Parcial Saúl Standard`, `f9b9d459`), se presenta la siguiente síntesis multidimensional:

| Métrica / Dimensión | `4ceacf92` (Solow v15 - Benchmark) | `b9316152` (Econometría Violaciones) | `d52ee475` (Estadística Asintótica) | `f9b9d459` (Saúl Standard) |
| :--- | :---: | :---: | :---: | :---: |
| **Material de Entrada** | 1 PDF (36 págs, 1.49 MB) | 1 PDF (23 págs, 0.56 MB) | 2 PDFs (52 págs, 3.44 MB) | 7 PDFs (103 págs, 10.39 MB) |
| **Modo Arquitectónico CTA** | Direct (1 Architect) | Direct (1 Architect) | **MapReduce (2 Mappers: part_01, part_02)** | MapReduce (4 Mappers: part_01..04) |
| **Competencias Extraídas** | 15 competencias | 14 competencias | **28 competencias** | 65 competencias |
| **Reactivos Publicados** | 360 preguntas | 360 preguntas | **660 preguntas** | 1,590 preguntas |
| **Subagentes Totales** | 12 subagentes | 11 subagentes | **14 subagentes** | 30 subagentes |
| **Tiempo de Pared Total (Wall)** | **27.10 min** (1,626.0s) | 40.62 min (2,437.0s) | **26.88 min** (1,613.0s) ⚡ | 64.22 min (3,853.0s) |
| **Stage 0 (Prepare CLI)** | 2.5s (0.1%) | 1.1s (0.05%) | 10.2s (0.6%) | 4.2s (0.1%) |
| **Inicialización Real End-to-End**| 185s (3.1 min) | 173s (2.9 min) | 189s (3.2 min) | 553s (9.2 min) |
| **Stage 1 (CTA) Wall-Clock** | 9.91 min (594.4s) | 6.41 min (384.5s) | 9.59 min (575.4s) | 12.11 min (726.3s) |
| **Stage 2 (Shard) Wall-Clock**| 8.7s (0.5%) | 9.2s (0.4%) | 6.7s (0.4%) | 6.5s (0.2%) |
| **Stage 3 (Shards) Wall-Clock**| **11.27 min** (675.9s) | 29.36 min (1,761.7s) | **13.17 min** (790.4s) | 33.80 min (2,027.7s) |
| **Stage 4 (Build) Wall-Clock** | 10.9s (0.7%) | 26.0s (1.1%) | 15.1s (0.9%) | 34.9s (0.9%) |
| **Stage 5 (Verify) Wall-Clock**| 13.9s (0.9%) | 25.4s (1.0%) | 17.9s (1.1%) | 43.4s (1.1%) |
| **Stage 5b (Jueces) Wall-Clock**| 4.12 min (247.0s) | 2.16 min (129.3s) | 2.45 min (146.7s) | 7.36 min (441.6s) |
| **Stage 6 (Publish) Wall-Clock**| 10.7s (0.7%) | 17.8s (0.7%) | 10.6s (0.7%) | 16.8s (0.4%) |
| **Overhead No Asignado** | 62.0s (3.8%) | 82.0s (3.4%) | 40.0s (2.5%) | 551.6s (14.3%) |
| **Parallel Speedup Factor** | 3.32x | 2.87x | **4.09x** | 3.92x |
| **Throughput (Preguntas/Minuto)**| 13.28 preg/min | 8.86 preg/min | **24.55 preg/min** 🚀 | 24.76 preg/min |
| **Costo Unitario (Tokens/Preg)**| 61,291 tok/preg | 113,412 tok/preg | **36,462 tok/preg** 💎 | 44,933 tok/preg |
| **Tokens Activos / Pregunta** | 6,529 tok/preg | 7,728 tok/preg | **4,054 tok/preg** | 4,083 tok/preg |
| **Segundos de Pared / Pregunta**| 4.52 s/preg | 6.77 s/preg | **2.44 s/preg** | 2.42 s/preg |
| **Intervenciones Manuales** | 🛠️ 1 (8s, benigna) | **🛠️ 0 (Autonomía 100%)**| **🛠️ 0 (Autonomía 100%)** | 🛠️ 3 (Reset + Regex fix) |
| **Acuerdo Blind Judges Pass 1** | ✅ **100% (30/30)** | ✅ **100% (28/28)** | ✅ **100% (56/56)** | ✅ **98.5% (128/130)** |
| **Lecturas Inversas del Validador**| 0 lecturas | 🛑 **64 lecturas** (Shard 02: 29, Shard 06: 14) | ✅ **0 lecturas (Cero Stragglers)** | 27 lecturas |

#### Hallazgos Clave de la Comparativa:
1. **El Hito Histórico de `d52ee475` (Estadística Asintótica):**  
   Representa la **ejecución más eficiente registrada en la historia del pipeline C2C**:
   - Concluyó en **26.88 minutos**, batiendo incluso la marca de `solow_model_v15` (27.10 min) a pesar de haber producido **casi el doble de contenido** (660 reactivos en 28 competencias vs 360 reactivos en 15 competencias).
   - Registró un throughput de **24.55 preguntas/minuto** con una economía unitaria sobresaliente de **36,462 tokens/pregunta**, equiparable a la eficiencia del modo Fine Masivo (36,040 tok/preg) pero con **cero fricción operativa ni intervenciones del supervisor (100% autónomo)**.
   - Erradicó por completo las lecturas de ingeniería inversa sobre `compile_shard.py` (0 lecturas), operando todos los autores en tiempos acotados de 5.3 a 11.9 minutos sin stragglers.
2. **La Fricción Focalizada en `b9316152` (Econometría Violaciones de Supuestos):**  
   Aunque el pipeline concluyó de forma totalmente autónoma (0 intervenciones humanas) y con 100% de acuerdo de jueces ciegos en 40.62 minutos, experimentó el clásico cuello de botella en Stage 3:
   - `Shard Author shard_06` se convirtió en un **straggler crítico de 20.2 minutos (1,213s)** con 84 turnos, 13 errores y 14 lecturas del validador por dificultades en el tipado y auto-healing de variables paramétricas en C-11 y C-12.
   - `Shard Author shard_02` acumuló **29 lecturas de ingeniería inversa** sobre `compile_shard.py`, dilatando su tiempo a 12.0 minutos.
   - Esta retención en la barrera síncrona elevó el costo a 113,412 tokens/pregunta y redujo el throughput a 8.86 preg/min.

---

## 4. Conclusiones y Plan de Acción C2C v3.3 para Operación 'Clockwork'

Para que el pipeline funcione de forma predecible como un mecanismo de relojería (*clockwork*), sin requerir intervenciones del supervisor humano ni sufrir retrasos por stragglers, se establecen las siguientes 5 reglas de oro para la versión 3.3:

1. **Cero F-Strings en KaTeX (`engine/assemble.py` + prompts):** Prohibir el uso de f-strings en plantillas matemáticas paramétricas. Requerir cadenas crudas `r"..."` con sustitución regex selectiva de `{var}`, erradicando de raíz el 55% de los fallos de compilación.
2. **Armonización Epistémica Definitiva en Jueces:** Actualizar `c2c_judge/agent.md` autorizando explícitamente la lectura de `work/dispatch/items/judge_XX.json`, o despachar lotes de máximo 12 ítems embebidos directamente en el prompt del juez sin acceso a disco.
3. **Circuit Breaker Reactivo con SHA-256:** Si un archivo de shard es editado y su hash SHA-256 cambia, el disyuntor debe resetear automáticamente su contador a 0, evitando bloqueos permanentes tras arreglar el código.
4. **Watchdog Activo a los 8 Minutos (`budget_guard.py`):** Temporizador reactivo que elimine a cualquier subagente que supere los 40 turnos o los 5M tokens, sustituyéndolo por un agente de reparación atómica quirúrgica.
5. **Política de Granularidad Estándar:** Estandarizar `granularity: standard` (60–70 competencias, ~1,500 reactivos) como el modo predeterminado de producción, alcanzando el óptimo pedagógico y de ingeniería (25 QPM, 45k tok/preg y cero stragglers cognitivos).
6. **Inicialización Fast-Track ($\le 1\text{ minuto}$ Target SLA):** Automatizar el pre-flight y la extracción PyMuPDF en un flujo síncrono Zero-Turn que despache directamente el CTA sin turnos conversacionales de inspección exploratoria previa, colapsando el tiempo de inicialización de 3–5 minutos a menos de 45 segundos.
