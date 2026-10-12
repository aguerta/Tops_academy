# Investigación Arquitectónica y Diseño Detallado: `content-to-course` v2

**Fecha:** 2026-10-11  
**Autor:** Explorer Survey Skill Agent (`explorer_survey_skill`)  
**Directorio de trabajo:** `g:\Mi unidad\Competence_analyser\.agents\teamwork\explorer_survey_skill`  
**Destinatario:** Orchestrator (`8c6e51b9-04fd-4a8c-a9ab-21b3a1985725`)

---

## 1. Resumen Ejecutivo

La skill actual `content-to-course` presenta un acoplamiento monolítico severo con los dominios de Ecuaciones en Derivadas Parciales (EDP) y Sistemas de Ecuaciones Diferenciales Ordinarias (EDO). Este acoplamiento se manifiesta en:
1. Detección heurística de dominios por palabras clave y llamadas externas a APIs con fallback silencioso a plantillas Markdown hardcodeadas en `cta_analyzer.py`.
2. Más de 3,400 líneas de lógica de síntesis matemática ad-hoc distribuidas entre `batch_generator.py` (2,243 líneas) y `edos_synthesizer.py` (1,164 líneas).
3. Un verificador ciego (`BlindSolver` en `verifier.py`) compuesto por más de 30 reglas de expresiones regulares que sobreajustan preguntas de EDP/EDO.
4. Un extractor de PDFs (`pdf_extractor.py`) limitado a texto plano que ignora imágenes manuscritas vectoriales (OneNote) y no acepta imágenes sueltas (`.png`, `.jpg`).
5. Dependencia estrecha en `tests/test_skill.py` de métodos de dominio (`test_blind_solver_cobb_douglas_degree`, `test_characteristic_roots_*`).

Para transformar `content-to-course` en un motor verdaderamente agnóstico capaz de procesar cualquier tema académico (demostrado con Estadística III) sin modificar una sola línea de código Python por tema, se requiere una reestructuración basada en **JSON como contrato estricto por etapas**:
- **Etapa 0 (Ingesta & Visión):** `ingest.py` con soporte universal de PDFs e imágenes, teselado con 10% de solape para imágenes > 2500 px, caché SHA-256 y `check_pages.py`.
- **Etapa 1 (CTA Estructurado):** `schemas/cta.schema.json` y `check_cta.py` que exigen distractores fusionados (*expert blindness* + misconceptions) con evidencia documental obligatoria.
- **Etapa 2 (Plantillas Paramétricas):** `schemas/template.schema.json` y `check_templates.py` con fragmentos `generate(rng)` y `cross_check(result)`.
- **Etapa 3 (Motor Genérico):** `engine/sandbox.py` (lista blanca AST + subproceso aislado), `engine/instantiate.py` (semillas deterministas y deduplicación), `engine/assemble.py` (balanceo de longitud anti-giveaway e interacción Khan), `engine/render.py` (helpers LaTeX `bmatrix`, `table_array`), `engine/invariants.py` y `engine/diversity.py`.
- **Etapa 4 (Verificación & Staging):** `judge.py` (juez LLM ciego sobre 2 instancias por plantilla) y `run.py` modular (`--stage`, `--from-stage`, `--review-cta`, fail-fast sin fallback silencioso).
- **Ejemplos Few-Shot:** Migración de 2 competencias de EDP y 2 de EDO a `examples/edp/` y `examples/edo/` como datos de referencia y pruebas de regresión.
- **Refactor de Plataforma:** `mathEquivalence.ts` y `types.ts` para respuestas FIB con coma decimal, fracciones (`5/6` vs `0.8333`), tolerancia de 4 decimales (`0.00005`) y soporte uniforme de `canonical_algebraic`, `value` y `expression`.

---

## 2. Inventario de Código de Dominio y Estrategia de Eliminación

Un escaneo exhaustivo sobre los archivos `.py` de la skill reveló las siguientes ocurrencias de términos y lógica de dominio (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `lagrange`, `cauchy`, `lotka`):

| Archivo | Líneas | Coincidencias de Dominio | Naturaleza del Acoplamiento | Acción de Eliminación / Migración |
|---|---|---|---|---|
| `edos_synthesizer.py` | 1,164 | 54 (100% del archivo) | Síntesis hardcodeada de 20 competencias de EDOs, autovalores, Jacobiano, macroeconomía dinámica (IS-LM, Goodwin, Lotka-Volterra). | **ELIMINAR COMPLETAMENTE**. Migrar 2 competencias a `examples/edo/`. |
| `batch_generator.py` | 2,243 | 125 | Generación por ramas `if code == "H-01": ...`, delegación a `EDOSSynthesizer`, diccionario `fallback_misconceptions` con EDP. | **ELIMINAR COMPLETAMENTE**. Extraer la lógica genérica de rebalanceo de longitud anti-giveaway y barajado A–G a `engine/assemble.py`. |
| `verifier.py` | 1,009 | 79 | `BlindSolver` con >30 reglas regex para EDP/EDO; `SymPyVerifier` con `verify_characteristic_roots` y `verify_euler_homogeneity`. | **REFACTORIZAR / ELIMINAR**. Reemplazar `BlindSolver` por `judge.py`. Mover la equivalencia simbólica SymPy genérica a `engine/invariants.py`. |
| `cta_analyzer.py` | 1,001 | 71 | `_analyze_edos_document`, `_analyze_pde_document`, routing por keywords, llamadas a APIs externas vía `urllib.request`. | **REEMPLAZAR** por `check_cta.py`. El análisis cognitivo lo ejecuta el subagente de Antigravity escribiendo directamente `cta.json`. |
| `run.py` | 244 | 5 | Heurísticas `if "sistema" in title ... cid = "sistemas_edos"`, ejecución lineal sin etapas reanudables. | **REESCRIBIR** como orquestador modular v2 (`--stage`, `--from-stage`, `--review-cta`, fail-fast sin fallback). |
| `pdf_extractor.py` | 480 | 4 | No procesa imágenes sueltas (`.png`) ni renderiza páginas a imagen para visión; extrae texto plano con PyMuPDF/pdfplumber. | **REEMPLAZAR** por `ingest.py` (render a PNG, clasificación Beamer vs tinta, teselado > 2500 px, manifiesto SHA-256). |
| `repair_loop.py` | 587 | 0 (directas) | Importa `BatchGenerator` y `CompetencyItem` en `_repair_quota_shortfalls` (líneas 355, 380). | **DESACOPLAR**: Eliminar la dependencia de `BatchGenerator`. La satisfacción de cuota la garantiza `engine/instantiate.py`. Conservar sanitizador de LaTeX (`sanitize_latex_escapes`). |
| `course_publisher.py` | 276 | 0 | Publicación genérica en disco, validación estricta y fusión en modo `--append`. | **CONSERVAR / REFACTORIZAR LEVE**: Reutilizable al 100%. |

---

## 3. Arquitectura de Componentes Nuevos

```
.agents/skills/content-to-course/
├── SKILL.md                          # Documentación del flujo de 5 etapas, subagentes y contratos
├── run.py                            # Orquestador modular CLI (--stage, --from-stage, --review-cta)
├── ingest.py                         # Ingesta universal: PDFs (Beamer vs tinta), imágenes, teselado >2500px, manifiesto SHA-256
├── check_pages.py                    # Validación de manifest.json, cobertura 100% de páginas y verificación cruzada de texto
├── check_cta.py                      # Validación de cta.json contra cta.schema.json, reglas CTA-D1/D2 y evidencia
├── check_templates.py                # Validación de templates/*.json contra template.schema.json, AST, TPL-D1..D4
├── judge.py                          # Lote de juez ciego (2 inst/plantilla sin clave) y arbitraje de discordancias
├── course_publisher.py               # Publicador a courses/<id>.json con soporte --append
├── repair_loop.py                    # Sanitizador léxico de LaTeX y reparador de longitud anti-giveaway desacoplado
├── schemas/
│   ├── pages.schema.json             # Contrato de manifiesto de páginas e imágenes
│   ├── cta.schema.json               # Contrato de análisis cognitivo con distractores fusionados
│   └── template.schema.json          # Contrato de plantillas paramétricas por competencia
├── engine/
│   ├── __init__.py
│   ├── sandbox.py                    # Lista blanca AST + ejecución aislada en subproceso con timeout (2s)
│   ├── instantiate.py                # Reparto de cuotas (30/20), barrido de semillas y deduplicación estricta
│   ├── assemble.py                   # Armado de ítems Khan, barajado A-G, opciones, hints y balanceo anti-giveaway
│   ├── render.py                     # Helpers LaTeX inyectados: bmatrix, table_array, fmt, latex_frac
│   ├── invariants.py                 # Chequeo del 100% de instancias (1 correcta, distractores únicos, cross_check)
│   └── diversity.py                  # Medición de diversidad léxica enmascarada (unique_masked / total >= 0.5)
└── examples/
    ├── edp/
    │   ├── cta.json                  # 2 competencias de EDP (ej. Hab-01 Homogeneidad, Hab-04 Lagrange)
    │   └── templates/                # >=6 plantillas por competencia (MC7, FIB, MS) con generate_py
    │       ├── Hab-01.json
    │       └── Hab-04.json
    └── edo/
        ├── cta.json                  # 2 competencias de EDO (ej. Hab-01 Forma Matricial, Hab-03 Traza-Determinante)
        └── templates/
            ├── Hab-01.json
            └── Hab-03.json
```

---

## 4. Especificación Detallada de Módulos

### 4.1. Contratos y Esquemas (`schemas/`)

#### 1. `schemas/pages.schema.json`
Define el manifiesto `work/pages/manifest.json`:
- `course_id`: Identificador del curso.
- `items`: Arreglo de entradas:
  - `item_id`: Identificador único (ej. `doc1_p03`, `stats_img_tile_0_1`).
  - `doc_name`: Nombre del archivo fuente original.
  - `source_path`: Ruta absoluta o relativa al origen.
  - `kind`: `beamer_text` | `ink_pdf` | `image_standard` | `image_tile` | `image_overview`.
  - `sha256`: Hash criptográfico del archivo o render para caché.
  - `page_num`: Número de página si proviene de un PDF.
  - `render_path`: Ruta al PNG renderizado (`work/pages/renders/...`).
  - `tile_info`: Objeto opcional `{ row, col, total_rows, total_cols, overlap_pct, bbox }`.
  - `has_text_layer`: Booleano indicando si existe texto extraíble.
  - `text_layer_path`: Ruta a `text_layer.txt` si aplica.
  - `transcription_path`: Ruta al archivo Markdown resultante (`work/pages/transcriptions/...md`).

#### 2. `schemas/cta.schema.json`
Define `work/cta.json`:
- `course_id`: Slug del curso.
- `title`: Título formal del curso.
- `macro_competency`: Declaración de desempeño terminal.
- `competencies`: Lista de competencias (`Fact`, `Concept`, `Skill`):
  - `id`: `H-XX`, `C-XX`, `Hab-XX`.
  - `type`: `fact` | `concept` | `skill`.
  - `name`: Nombre formal.
  - `description_latex`: Descripción técnica con notación matemática.
  - `bloom`: Nivel de la taxonomía de Bloom (`Remember`, `Understand`, `Apply`, `Analyze`, `Evaluate`, `Create`).
  - `prerequisites`: Arreglo de IDs de prerrequisitos (debe formar un DAG sin ciclos).
  - `distractors`: Arreglo de modelos de error (mínimo 3, mínimo 6 para `Skill`, ≥2 con `omitted_step` para `Skill`):
    - `id`: Prefijado con la competencia (ej. `D-Hab01-01`).
    - `name`: Nombre descriptivo del error.
    - `wrong_belief`: Creencia errónea (cadena o `null`).
    - `correct_belief`: Creencia correcta (cadena).
    - `omitted_step`: Paso omitido por ceguera del experto (cadena o `null`). Al menos uno de `wrong_belief` u `omitted_step` debe ser no nulo.
    - `trigger`: Detonante de la confusión.
    - `manifestation`: Manifestación observable en la respuesta.
    - `error_type`: Enum (`sign_error`, `overgeneralization`, `procedural_slip`, `conceptual_swap`, `boundary_case`, `unit_or_scale`, `notation`, `skipped_step`, `other`).
    - `severity`: `low` | `medium` | `high`.
    - `origin`: `source` (explícito en el material) | `inferred` (propuesto por el LLM).
    - `evidence`: `{ doc: string, page: integer | string }`.
    - `remediation_hint`: Pista correctiva para el estudiante.
  - `source_examples`: Arreglo de ejemplos numéricos o literales de la fuente.
  - `evidence`: Arreglo de referencias `{ doc: string, page: integer | string }`.

#### 3. `schemas/template.schema.json`
Define `work/templates/<comp_id>.json`:
- `competency_id`: ID de la competencia correspondiente.
- `templates`: Arreglo de ≥6 plantillas (≥2 por tipo: `multiple_choice_7_options`, `fill_in_the_blank`, `multiple_select`):
  - `id`: Identificador de la plantilla (ej. `T-Hab01-01`).
  - `interaction_type`: Tipo de interacción Khan.
  - `difficulty`: `easy` | `medium` | `hard`.
  - `bloom`: Nivel Bloom evaluado.
  - `stem`: Enunciado paramétrico con marcadores `{var}` y KaTeX.
  - `generate_py`: Código Python conteniendo `def generate(rng): ...`.
    - Retorna dict: `{"vars": dict, "correct": any, "distractors": [{"value": any, "distractor_id": str}], "equivalents": list[str], "tolerance": float}`.
  - `cross_check_py`: Código Python conteniendo `def cross_check(result): ...` que valida independientemente el resultado generado retornando `True`/`False`.
  - `hints`: Lista de 3 a 5 pistas progresivas con marcadores `{var}`.
  - `solution`: Solución detallada paso a paso.
  - `distractor_ids`: Lista de IDs de distractores referenciados.
  - `graph`: Especificación gráfica declarativa opcional (`GraphSpec`).

---

### 4.2. Ingesta Multiformato y Visión (`ingest.py`, `check_pages.py`)

#### `ingest.py`
1. **Detección Universal:** Acepta directorios o listas de rutas. Clasifica por extensión y contenido:
   - Archivos PDF: Utiliza PyMuPDF (`fitz`). Inspecciona el número de páginas y extrae caracteres de texto.
     - Si el promedio de caracteres por página < 50 (como `Stats3 10-10.pdf`, que tiene 9 páginas con solo 308 caracteres de metadatos), se clasifica como `ink_pdf` (tinta manuscrita/escaneada) y se renderiza a 150 DPI sin asumir capa de texto.
     - Si contiene texto suficiente (Beamer LaTeX como `EST3_LEC01/02/03`), se clasifica como `beamer_text`, se extrae la capa de texto normalizando diacríticos corruptos (`´`+vocal -> vocal con tilde, `ˆ\beta` -> `\hat{\beta}`) a `text_layer.txt`, y se renderiza a 130 DPI.
   - Archivos de Imagen (`.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tiff`):
     - Inspecciona dimensiones mediante `PIL.Image`.
     - Si `max(width, height) > 2500 px` (ej. `stats 3 3-10.png` de 5941 × 3327 px): activa el **algoritmo de teselado**:
       - Divide la imagen en una grilla de 3 columnas × 2 filas (6 teselas) aplicando un **10% de solape horizontal y vertical** para garantizar que fórmulas o tablas en los bordes de corte no queden truncadas.
       - Genera además una versión de vista general reducida (thumbnail general ≤ 1800 px) para dar contexto espacial global.
     - Si `max(width, height) <= 2500 px`: se registra como `image_standard` completa.
2. **Caché y Manifiesto:**
   - Calcula el hash SHA-256 de cada imagen y render.
   - Si `work/pages/manifest.json` ya contiene una entrada con el mismo hash y su archivo de transcripción `pages/<doc>/<id>.md` existe y no está vacío, no se repite la operación (idempotencia y ahorro de tiempo).
3. **Distribución de Carga:** Genera `work/vision_batches.json` dividiendo el total de imágenes/teselas en lotes balanceados de ~10 elementos por subagente.

#### `check_pages.py`
- Verifica que el 100% de los elementos registrados en `manifest.json` posean un archivo de transcripción `.md` no vacío.
- Realiza verificación cruzada para `beamer_text`: extrae números y comandos clave de `text_layer.txt` y comprueba su presencia en la transcripción. Reporta discrepancias si la cobertura < 85%.

---

### 4.3. Motor Genérico y Sandbox (`engine/`)

#### 1. `engine/sandbox.py`
- **Análisis Estático AST:**
  - Inspecciona el árbol sintáctico de `generate_py` y `cross_check_py`.
  - Whitelist estricta de módulos importables: `math`, `fractions`, `statistics`, `sympy`, `numpy`, `scipy.stats`.
  - El módulo `random` se prohíbe como import directo; el generador pseudoaleatorio se inyecta como argumento `rng`.
  - Blacklist estricta de nodos AST: prohíbe llamadas a `open`, `eval`, `exec`, `compile`, `__import__`, `globals`, `locals`, `getattr`, `setattr`, `delattr`.
  - Prohíbe cualquier acceso a atributos que comiencen con doble guion bajo (`__dunder__`), previniendo introspección o escapes de sandbox (`__class__.__subclasses__`).
  - Prohíbe módulos peligrosos (`os`, `sys`, `subprocess`, `shutil`, `socket`, `urllib`, `pathlib`).
- **Ejecución Aislada:**
  - Ejecuta el código en un subproceso aislado o runner controlado con límite de tiempo estricto de **2.0 segundos** por llamada y límite de memoria de 256 MB.
  - Inyecta helpers matemáticos de renderizado (`bmatrix`, `fmt`, `table_array`, `latex_frac`) y el objeto `rng` con semilla reproducible.

#### 2. `engine/instantiate.py`
- Distribuye la cuota total de la competencia (30 para `Skill`, 20 para `Fact`/`Concept`) equitativamente entre sus ≥6 plantillas.
- Para cada plantilla, itera variando semillas pseudoaleatorias deterministas (`seed = base_seed + i * 1000 + t_idx`).
- **Deduplicación Estricta:**
  - Registra las tuplas de parámetros generadas (`vars`). Si una tupla ya fue utilizada en esa plantilla, se descarta y se avanza la semilla.
  - Registra el texto final del enunciado (`stem`). Si un enunciado resultante es idéntico a uno previo, se descarta.
- Continúa iterando hasta completar la cuota asignada a cada plantilla.

#### 3. `engine/assemble.py`
- Transforma los diccionarios generados por las plantillas en objetos de pregunta conformes al esquema de la plataforma:
  - **MC7:** Toma la respuesta correcta y los 6 distractores (cada uno con su `distractor_id`). Aplica barajado pseudoaleatorio uniforme asignando etiquetas de A a G.
  - **FIB:** Genera la respuesta canónica (`canonical_algebraic` o `value`), la lista `accepted_equivalents` y la tolerancia numérica (`tolerance`, por defecto `0.00005`).
  - **MS:** Evalúa entre 4 y 6 afirmaciones con cardinalidad correcta entre 1 y $n-1$.
  - **Andamiaje:** Asigna 3 a 5 pistas progresivas, la solución paso a paso y el `common_misconception_warning` (tomado del `remediation_hint` del distractor más común).
  - **Rebalanceo de Longitud Anti-Giveaway:** Integra el algoritmo psicométrico de longitud:
    - *Nivel ítem:* $0.80 \cdot \min(D) \le L_{\text{correct}} \le 1.20 \cdot \max(D)$.
    - *Nivel curso:* La opción correcta no puede ser la más larga en más del 25% de los ítems MC, ni la más corta en más del 25%.
  - **Sanitización de Escapes LaTeX:** Garantiza que las barras invertidas de KaTeX no formen caracteres de control silenciosos (`\t`, `\n`, `\f`, `\r`, `\b`) mediante serialización estricta.

#### 4. `engine/render.py`
Librería inyectada disponible dentro de `generate_py`:
- `bmatrix(A)`: convierte arreglos 2D o matrices NumPy/SymPy a `\begin{bmatrix} a & b \\ c & d \end{bmatrix}`.
- `table_array(rows, headers)`: genera tablas matriciales KaTeX `\begin{array}{ccc} ... \end{array}` (útil para salidas tabulares de software econométrico como EViews).
- `fmt(val, nd=4)`: formatea decimales asegurando representación limpia sin problemas de punto flotante.
- `latex_frac(n, d)`: genera `\frac{n}{d}` simplificado.

#### 5. `engine/invariants.py` y `engine/diversity.py`
- **Invariantes (100% de las instancias generadas):**
  - MC7 posee exactamente una opción correcta y 6 distractores.
  - Todos los valores de distractores son mutuamente distintos y distintos de la respuesta correcta.
  - La función `cross_check(result)` retorna `True`.
  - La opción correcta no aparece mencionada textualmente en el enunciado o en las pistas iniciales.
  - Las relaciones de longitud anti-giveaway se cumplen al 100%.
  - Cada distractor referencia un `distractor_id` válido del `cta.json`.
- **Diversidad:**
  - Sustituye números, variables y expresiones matemáticas por marcadores unificados (`<NUM>`, `<MATH>`).
  - Calcula la tasa de diversidad: `len(set(enunciados_enmascarados)) / total_preguntas`.
  - Exige una relación ≥ 0.50 en cada competencia.

---

### 4.4. Arbitraje con Juez Ciego y Orquestador (`judge.py`, `run.py`)

#### `judge.py`
- Muestrea exactamente 2 instancias por plantilla de forma determinista.
- Genera el archivo `work/judge_batch.json` que contiene los enunciados y opciones de las preguntas **omitiendo la clave de respuesta, soluciones y pistas**.
- Un subagente evaluador (o agente independiente) resuelve las preguntas a ciegas y genera sus respuestas.
- `judge.py` compara las respuestas del juez contra las claves generadas por el motor.
- Si existe discrepancia, reporta la plantilla discordante. El subagente autor dispone de hasta 3 iteraciones para corregir la plantilla (`generate_py` o el enunciado).
- Criterio de aceptación: ≥ 95% de coincidencia sobre la muestra auditada.

#### `run.py`
Orquestador modular CLI:
- Opciones principales:
  - `--stage [ingest|cta|templates|build|verify|publish]`: Ejecuta únicamente la etapa solicitada.
  - `--from-stage [ingest|cta|templates|build|verify|publish]`: Inicia desde la etapa especificada y continúa secuencialmente.
  - `--review-cta`: Detiene la ejecución tras la generación de `cta.json` para permitir la revisión pedagógica humana antes de generar plantillas.
  - `--content <ruta>`: Ruta a carpeta de contenidos o archivo PDF.
  - `--course-id <slug>`: Slug del curso (ej. `estadistica3_regresion`).
  - `--title <titulo>`: Título formal del curso.
  - `--work-dir <ruta>`: Directorio de trabajo intermedio (por defecto `courses/<course_id>/work`).
  - `--output-dir <ruta>`: Directorio de publicación final (por defecto `courses/`).
  - `--append`: Activa el modo de anexión a un curso preexistente.
- **Fail-Fast Estricto:**
  - Si falta cualquier artefacto (`manifest.json`, `cta.json`, `templates/*.json`) al iniciar una etapa, termina inmediatamente con código de salida ≠ 0 y un mensaje de error explícito indicando qué archivo falta y cómo generarlo.
  - No contiene lógica de fallback silencioso a plantillas previas ni invoca APIs externas.

---

### 4.5. Ejemplos Few-Shot (`examples/edp/`, `examples/edo/`)

Para evitar que los subagentes generen plantillas o taxonomías desconectadas y para asegurar la regresión continua del motor genérico, se crean dos bancos de referencia completos:

1. `skill/examples/edp/`:
   - `cta.json`: 2 competencias completas de EDP:
     - `Hab-01`: Cálculo de Grado de Homogeneidad e Identidad de Euler.
     - `Hab-04`: Integrales Primeras y Curvas Características en EDP de Lagrange.
     - Incluye lista `distractors` completa con `wrong_belief`, `omitted_step`, severidad, evidencia y pistas.
   - `templates/Hab-01.json`, `templates/Hab-04.json`: ≥6 plantillas paramétricas con `generate_py` y `cross_check_py` que usan `sympy` y `numpy`.
2. `skill/examples/edo/`:
   - `cta.json`: 2 competencias completas de EDO:
     - `Hab-01`: Reducción Matricial Compacta a $\dot{X} = AX + B$.
     - `Hab-03`: Diagnóstico Espectral en el Plano Traza-Determinante.
     - Incluye lista `distractors` completa con evidencias y pasos omitidos.
   - `templates/Hab-01.json`, `templates/Hab-03.json`: ≥6 plantillas paramétricas con `generate_py` y `cross_check_py`.

---

### 4.6. Refactor de la Plataforma para Calificación Numérica (FIB)

#### 1. `platform/src/types.ts`
Actualizar `FillBlankAnswer`:
```typescript
export interface FillBlankAnswer {
  expression?: string;
  canonical_algebraic?: string;
  value?: string | number;
  accepted_equivalents?: string[];
  tolerance?: number;
  min_decimals?: number;
}
```

#### 2. `platform/src/utils/mathEquivalence.ts`
- **Extracción Uniforme de Objetivo:**
  ```typescript
  const targetExpr = typeof targetAnswer === 'string'
    ? targetAnswer
    : (targetAnswer.canonical_algebraic || targetAnswer.value?.toString() || targetAnswer.expression || '');
  ```
- **Normalización de Coma Decimal:**
  Reemplazar comas numéricas por puntos antes del análisis matemático:
  ```typescript
  // Normalizar '0,8333' -> '0.8333', cuidando de no alterar sintaxis de listas separadas por coma
  s = s.replace(/(\d+),(\d+)/g, '$1.$2');
  ```
- **Regla de 4 Decimales y Fracciones:**
  - Tolerancia numérica por defecto: `0.00005` (o el valor de `tolerance` si se provee explícitamente en el objeto).
  - Evaluar numéricamente tanto entradas directas como fracciones (`5/6` vs `0.8333`).
  - Si `|val_estudiante - val_target| <= tolerance`, aceptar como equivalente.
  - Si el estudiante provee mayor precisión (`0.833333`), la comparación con tolerancia la acepta naturalmente.
  - Asegurar que números exactos (`5`, `0.25`) se reconozcan tanto en formato fraccionario como decimal.

#### 3. `tests/test_math_adversarial_suite.ts`
Agregar casos de prueba para:
- Coma decimal europea/latinoamericana: `0,8333` vs `0.8333`.
- Fracción vs decimal con tolerancia: `5/6` vs `0.8333`.
- Estadísticos con 4 decimales: `0.0030` vs `0.003`.
- Respuestas con objetivo declarado bajo `canonical_algebraic` y `value`.

---

## 5. Reescritura de `tests/test_skill.py`

El archivo `tests/test_skill.py` actual contiene 27 pruebas acopladas a la implementación vieja. Se reescribe para cubrir exhaustivamente las garantías de la arquitectura v2:

1. **Rechazo AST de Seguridad:**
   - Rechazo de `import os`, `import sys`, `import subprocess`.
   - Rechazo de llamadas a `open()`, `eval()`, `exec()`, `__import__()`.
   - Rechazo de accesos a atributos dunder (`__class__`, `__bases__`, `__subclasses__`).
2. **Aislamiento y Timeout:**
   - Función con bucle infinito `while True: pass` termina con `TimeoutError` en ≤ 2.0 s.
   - Función que agota memoria termina controladamente.
3. **Determinismo por Semilla:**
   - La misma semilla con la misma plantilla produce exactamente la misma tupla `(vars, correct, distractors)`.
   - Semillas diferentes generan variaciones diferentes.
4. **Deduplicación:**
   - `instantiate.py` rechaza parámetros repetidos y enunciados duplicados.
5. **Contratos Psicometría y Tipologías:**
   - MC7: exactamente 7 opciones, exactamente 1 correcta, 6 distractores con `distractor_id`s distintos.
   - MS: 4 a 6 opciones, entre 1 y $n-1$ correctas.
   - FIB: calificación escalar con tolerancia y equivalencia de fracciones.
6. **Validación de Esquemas:**
   - `check_cta` rechaza un CTA con <3 distractores o una Skill con <6 distractores o sin `omitted_step`.
   - `check_cta` rechaza evidencias que citan páginas inexistentes en `manifest.json`.
   - `check_templates` rechaza plantillas que usan distractores no declarados en el CTA.
7. **Fail-Fast de `run.py`:**
   - `run.py --stage cta` falla con código ≠ 0 si no existe `manifest.json`.
   - `run.py --stage build` falla con código ≠ 0 si no existe `cta.json`.
8. **Ingesta y Teselado:**
   - Imagen de prueba > 2500 px se divide en teselas con 10% de solape y se registra en `manifest.json`.
   - Caché SHA-256 previene re-renderizado de archivos ya procesados.
9. **Regresión con Ejemplos Few-Shot:**
   - El motor genérico instancia válidamente las plantillas de `examples/edp/` y `examples/edo/`.

---

## 6. Plan de Implementación por Fases y Milestones

```
FASE 1: INFRAESTRUCTURA DE CÓDIGO (Skill + Plataforma + Tests + Freeze)
├── Milestone 1: Esquemas y Contratos (pages, cta, template)
├── Milestone 2: Ingesta Universal y Visión (ingest.py, check_pages.py)
├── Milestone 3: Motor Genérico y Sandbox (sandbox, instantiate, assemble, render, invariants, diversity, check_cta, check_templates)
├── Milestone 4: Orquestador y Juez (judge.py, run.py v2, desacoplamiento de repair_loop.py, actualización de SKILL.md)
├── Milestone 5: Limpieza, Migración y Ejemplos Few-Shot (borrado de edos_synthesizer.py/batch_generator.py, examples/edp/, examples/edo/, reescritura de tests/test_skill.py)
├── Milestone 6: Refactor de Plataforma (types.ts, mathEquivalence.ts, test_math_adversarial_suite.ts)
└── Milestone 7: Verificación Integral y Congelación (Code Freeze baseline)

FASE 2: GENERACIÓN DEL CURSO DE ESTADÍSTICA III (Cero cambios en código)
├── Etapa 0: Ingesta y Transcripción de content/estadistica3_Cano (≈84 imágenes/teselas)
├── Etapa 1: Análisis CTA -> cta.json (evidencia de Beamer, OneNote manuscrito y EViews PNG)
├── Etapa 2: Subagentes generan plantillas paramétricas -> templates/<id>.json
├── Etapa 3: Instanciación genérica -> courses/estadistica3_regresion.json
├── Etapa 4: Auditoría del Juez Ciego y Validador Strict
└── Etapa 5: Smoke test en plataforma web
```

---

## 7. Conclusión

La arquitectura propuesta elimina el 100% del código de dominio en `.agents/skills/content-to-course/`. Sustituye la generación heurística acoplada por un pipeline desacoplado guiado por esquemas formales, código paramétrico en sandbox seguro y validación multifactorial independiente. La Fase 1 dejará el motor completamente listo, testeado y congelado, habilitando la Fase 2 para procesar Estadística III (y cualquier curso futuro) como pura operación de datos sin alterar código.
