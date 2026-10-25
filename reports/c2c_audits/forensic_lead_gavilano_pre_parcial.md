# Auditoría Forense de Rendimiento y Arquitectura Multi-Agente
## Pipeline Content-to-Course (C2C v3.21) — Curso: `gavilano_pre_parcial`
### ID de Conversación Orquestadora: [`aad42579-ddbc-49fa-963f-3a9347391b05`](conversation://aad42579-ddbc-49fa-963f-3a9347391b05)

**Fecha de Ejecución y Auditoría:** `2026-10-25 06:50:26 UTC`  
**Autor del Informe:** Run Lead Auditor & Multi-Agent Performance Architect (Top's Academy & Google Antigravity SDK)  
**Directorio de Telemetría Validado:** [`reports/c2c_audits/20261025_015026_gavilano_pre_parcial_aad42579`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/20261025_015026_gavilano_pre_parcial_aad42579)  
**Artefacto Final Publicado:** [`courses/gavilano_pre_parcial.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/gavilano_pre_parcial.json) (2,950 reactivos interactivos)

---

## 1. Resumen Ejecutivo y Metrología de Rendimiento Global (Unit Economics)

La ejecución `gavilano_pre_parcial` representa el despliegue multi-agente concurrente de mayor escala registrado en la plataforma Top's Academy sobre el Google Antigravity SDK: **115 subagentes concurrentes**, **83 shards de autoría**, **10 arquitectos cognitivos en MapReduce** y **22 jueces ciegos**, procesando una carga académica de **10 documentos PDF** (10.05 MB, 246 diapositivas) y generando **2,950 preguntas paramétricas validadas** correspondientes a **127 competencias pedagógicas**.

### 1.1. Comparativa de Tiempo de Pared vs. Tiempo de Cómputo Activo

```
====================================================================================================
METROLOGÍA DE CONCURRENCIA Y FACTOR DE ACELERACIÓN PARALELA
====================================================================================================
Tiempo de Pared Global (Wall-Clock Time)     : 2,844.0 s  (47.4 min)
Tiempo de Cómputo Agregado (Active Compute) : 32,439.0 s (540.65 minutos-agente / 9.01 horas)
Factor de Aceleración Paralela (Speedup)    : 11.41x
Eficiencia de Concurrencia Teórica (83 Shards): 13.7% de eficiencia de empaquetamiento sobre barrera
Intervenciones Manuales del Supervisor      : 0 operaciones (100% Autónomo / Zero-Touch Repair)
====================================================================================================
```

### 1.2. Tokenomics y Eficiencia de Caché de Contexto

El consumo de cuota de API estuvo fuertemente optimizado por el mecanismo de caché de prefijo de Google Antigravity SDK:
- **Tokens de Entrada Brutos (sin caché):** `11,329,722 tokens`
- **Tokens de Caché Reutilizados (Cache Read):** `44,838,076 tokens`
- **Ratio de Acierto de Caché (Cache Hit Rate):** **`74.3%`** de los tokens de entrada fueron servidos desde memoria caché ultra-rápida.
- **Tokens de Salida Generados:** `4,157,991 tokens`
- **Tokens Activos Facturables (Entrada Neta + Salida):** `15,487,713 tokens`
- **Gran Total de Cuota Procesada:** `60,325,789 tokens`
- **Tokens de Razonamiento Profundo (Thinking Tokens):** `744,262 tokens` generados en `646 turnos cognitivos` (2,978,033 caracteres de cadena de pensamiento).

### 1.3. Ratios Unitarios Normalizados (Unit Economics)

| Dimensión de Eficiencia | Métrica Registrada | Interpretación de Ingeniería |
| :--- | :---: | :--- |
| **Tokens Activos por Pregunta** | **`5,250.1 tokens/preg`** | Esfuerzo neto de razonamiento, código de plantilla y validación por reactivo |
| **Tokens Totales por Pregunta** | **`20,449.4 tokens/preg`** | Consumo total de API por reactivo jugable |
| **Segundos de Pared por Pregunta** | **`0.96 s/preg`** | Ritmo de producción percibido de extremo a extremo |
| **Rendimiento de Generación (QPM)** | **`62.24 preg/min`** | Tasa de producción industrial de reactivos pedagógicos |
| **Tokens Activos por Diapositiva** | **`62,958.2 tokens/pág`** | Costo computacional de desestructuración pedagógica por slide |
| **Tokens Activos por Competencia** | **`121,950.5 tokens/comp`** | Densidad de diseño instruccional y derivación paramétrica |
| **Tokens de Autor por Competencia** | **`92,629.7 tokens/comp`** | Esfuerzo directo de síntesis de plantillas en Stage 3 |

---

## 2. Stage 1B: Análisis Map-Reduce de los 10 CTA Architects

En Stage 1B, la descomposición cognitiva de las 127 competencias se orquestó mediante un patrón MapReduce: **10 subagentes Mapper concurrentes** (`part_01` a `part_10`), cada uno con la asignación de un documento PDF específico, seguidos de una sincronización determinista de reducción.

### 2.1. Descomposición Granular de Mappers CTA

| Subagente Mapper | Documento Fuente Asignado | Páginas | Tamaño | Tokens In | Tokens Out | Cache Leído | Errores | Duración |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`part_06`** (Fastest) | `8. Sweezy.Rigidez de precio.pdf` | 21 págs | 482 KB | 100,812 | 33,529 | 286,290 | 1 | **231.0 s** (3.85m) |
| **`part_03`** | `5. Bertrand.Producto diferenciado.pdf`| 21 págs | 570 KB | 94,782 | 27,326 | 272,099 | 1 | **233.0 s** (3.88m) |
| **`part_02`** | `4. Bertrand Producto homogéneo.pdf` | 24 págs | 503 KB | 98,322 | 29,163 | 285,650 | 2 | **247.0 s** (4.12m) |
| **`part_01`** | `3. Cournot.pdf` | 21 págs | 497 KB | 96,185 | 35,546 | 214,804 | 0 | **253.0 s** (4.22m) |
| **`part_09`** | `Micro II. Ejercicios1 (1).pdf` | 12 págs | 257 KB | 97,013 | 38,979 | 265,699 | 2 | **267.0 s** (4.45m) |
| **`part_05`** | `7. Cartel_o_colusión.pdf` | 30 págs | 677 KB | 202,976 | 46,035 | 325,997 | 1 | **315.0 s** (5.25m) |
| **`part_04`** | `6. Stackelberg.pdf` | 21 págs | 540 KB | 116,082 | 48,626 | 300,982 | 0 | **332.0 s** (5.53m) |
| **`part_07`** | `9. Hotelling. Diferenciación horiz.pdf`| 26 págs | 508 KB | 127,380 | 55,033 | 385,956 | 2 | **393.0 s** (6.55m) |
| **`part_08`** | `Competencia_monopolística2.pdf` | 21 págs | 4.17 MB | 119,737 | 54,742 | 372,216 | 2 | **477.0 s** (7.95m) |
| **`part_10` 🛑 (Bottleneck)**| `Monopolio. (1).pdf` | **49 págs** | **2.32 MB** | **147,696** | **70,716** | **550,883** | **4** | **565.0 s** (9.42m) |

### 2.2. Diagnóstico del Cuello de Botella y Retraso de Sincronización en Stage 1B

El tiempo total de pared de la etapa 1B fue fijado por el straggler `part_10` en **565.0 s** (9.42 min), mientras que el mapper más rápido (`part_06`) terminó en **231.0 s** (3.85 min).
- **Penalización por Asimetría de Barrera:** El pipeline permaneció **334.0 segundos (5.57 minutos)** en espera pasiva aguardando a que `part_10` concluyera.
- **Causa Raíz 1 (Carga Desbalanceada):** `Monopolio. (1).pdf` contenía 49 páginas (el 20% de todo el material del curso asignado a un solo mapper). Su salida (`part_10_data.py`) requirió 70,716 tokens de generación frente a los 27,326 tokens de `part_03`.
- **Causa Raíz 2 (Fricción de Herramientas y Violación de Límites):** La inspección forense de los pasos de `part_10` en la base de datos de conversación (`64b75417`) reveló 4 intentos fallidos de herramientas antes de escribir el archivo:
  1. *Paso 08:* Intento de leer `work/cta_parts/part_01_data.py` (búsqueda de ejemplos en un archivo aún inexistente -> `FileNotFoundError`).
  2. *Paso 10:* Intento de leer `work/delta_manifest.json` (archivo inexistente -> `FileNotFoundError`).
  3. *Paso 12:* Ejecución innecesaria de `compile_cta.py --help` en la consola.
  4. *Paso 14:* Intento de inspección del código fuente del compilador (`.agents/skills/content-to-course/compile_cta.py`), bloqueado de inmediato por el hook de seguridad: `tool call denied by pre-tool hook: C2C Worker Boundary: Access denied to internal compiler/validator source code`.

---

## 3. Stage 3: Análisis de Máxima Concurrencia de 83 Shard Authors

Stage 3 constituye el núcleo de carga pesada del pipeline: **83 Shard Authors desplegados concurrentemente** para sintetizar plantillas de código paramétrico en Python (`shard_XX_data.py`), compilar reactivos mediante `compile_shard.py` y validar el cumplimiento estricto de las reglas psicométricas (R-01 a R-20, TPL-D1..D4, TPL-VAR).

```
====================================================================================================
DISTRIBUCIÓN ESTADÍSTICA DE LATENCIA DE LOS 83 SHARDS (STAGE 3)
====================================================================================================
Duración Mínima (Gold Standard): 170.0 s (2.83 min)  [Shard Author shard_03]
Mediana de Pared               : 288.0 s (4.80 min)
Promedio de Pared              : 295.8 s (4.93 min)
Desviación Estándar            :  68.5 s
Duración Máxima (Straggler)    : 609.0 s (10.15 min) [Shard Author shard_56]
Retraso de Barrera (Straggler) : +321.0 s frente a la mediana (+439.0 s frente al Gold Standard)
Total Compilaciones Ejecutadas : 101 compilaciones (83 limpias en pase final)
Total Ediciones Quirúrgicas    : 17 operaciones edit_file en caliente
====================================================================================================
```

### 3.1. Caso de Estudio: Gold Standard Clean-Room (`shard_03`)

El agente `Shard Author shard_03` ejemplifica la ejecución ideal y limpia bajo la arquitectura C2C:
- **Duración Total de Pared:** `170.0 s` (2.83 min).
- **Métricas Operativas:** 8 turnos de conversación, 1 sola llamada a `write_file`, 1 sola compilación ejecutada (`compile_shard.py`), **0 errores**, **0 ediciones post-escritura**.
- **Latencia Pre-1st-Compile:** `172.0 s` (dedicado exclusivamente a leer su work order `author_03.json`, razonar sobre la competencia `Hab-03` y generar la plantilla paramétrica).
- **Latencia Post-1st-Compile:** `10.0 s` (ejecución del script en sandbox y reporte de finalización).
- **Comportamiento Cognitivo:** Cumplimiento estricto del *Turn-0 Autosufficiency Contract*: no navegó carpetas, no buscó ejemplos en otros shards ni ejecutó comandos exploratorios.

---

### 3.2. Top Stragglers: Diagnóstico Forense y Descomposición Pre vs. Post Compile

```
====================================================================================================
TOP 5 STRAGGLERS: DESCOMPOSICIÓN TEMPORAL PRE-1ST-COMPILE vs POST-1ST-COMPILE
====================================================================================================
Shard ID   | Wall Time | Pre-Compile | Post-Compile | Compiles (Fails) | Edits | Tokens Activos
----------------------------------------------------------------------------------------------------
shard_56   |  609.0 s  |   355.0 s   |   259.0 s    |      3 (2)       |   6   |    238,879
shard_82   |  459.0 s  |   447.0 s   |    26.0 s    |      1 (0)       |   0   |    200,427
shard_51   |  450.0 s  |   411.0 s   |    47.0 s    |      2 (1)       |   1   |    202,230
shard_52   |  437.0 s  |   328.0 s   |   118.0 s    |      2 (1)       |   1   |    192,220
shard_59   |  420.0 s  |   406.0 s   |    17.0 s    |      1 (0)       |   0   |    183,261
====================================================================================================
```

#### A. Shard 56 (`609.0 s` — Straggler Absoluto del Pipeline)
1. **Fase Pre-Compile (355.0 s):**
   - El agente recibió las competencias `C-38` y `C-39`.
   - En el *Paso 06*, intentó leer `work/templates/C-38.json` (las plantillas JSON no existen previamente, se generan al compilar el shard).
   - En el *Paso 08*, intentó leer `work/shards/shard_50_data.py` (intento de copiar la sintaxis de un shard hermano -> `FileNotFoundError`).
   - Tras este retraso exploratorio, escribió `shard_56_data.py` (Paso 12).
2. **Fase Post-Compile (254.0 s — Micro-Bucle de Reparación Quirúrgica):**
   - **Compilación 1 (Paso 16):** Falló con **6 errores detectados** (5 consolidados):
     - `[R-20: SINTAXIS / LLAVES]`: Faltaban llaves de escape en fórmulas LaTeX en `C-38` (L245) y `C-39` (L5, L245).
     - `[R-18: DISTRACTORES BOILERPLATE SINTÉTICOS]`: Presencia de distractores sintéticos no anclados en conceptos reales.
     - `[TPL-VAR]`: Violación de diversidad: `Failed to instantiate diversity quota (20 items)`.
   - **Bucle de Edición Quirúrgica (Pasos 17 a 45):** El agente ejecutó **6 llamadas a `edit_file`** consecutivas, intercaladas con lecturas de verificación de líneas mediante `view_file`.
   - **Compilación 2 (Paso 46):** Falló con **1 error consolidado**:
     - `[TPL-D4: OPCIONES DUPLICADAS]` en `C-39.json:L5`: El generador aleatorio generó distractores con contenido idéntico (`$CMg = 78$, $\lim_{E \to \infty} CMg = 40$`).
   - **Compilación 3 (Paso 54):** Éxito limpio tras corregir el generador paramétrico en los pasos 47 a 53.

#### B. Shard 82 (`459.0 s` — Patrón de Vagabundeo Exploratorio Puro)
A diferencia de `shard_56`, `shard_82` tuvo **0 fallos de compilación** y **0 ediciones quirúrgicas**. La totalidad de su retraso ocurrió en la fase previa a la primera compilación (**`447.0 s` Pre-Compile** frente a solo `26.0 s` Post-Compile en 24 turnos).
- **Paso 05-09:** Comenzó listando el directorio `work/shards/` y buscando archivos `shard_data.py` ajenos para tomarlos como referencia.
- **Paso 10:** Intentó listar rutas fuera de su espacio de trabajo, siendo bloqueado por el hook de seguridad: `tool call denied by pre-tool hook: C2C Cross-Course Isolation: Listing sibling courses`.
- **Paso 14-17:** Inspeccionó el archivo compilado ajeno `shard_01.json` para observar la estructura de las preguntas.
- **Paso 20-41 (15 pasos en bucle de búsqueda manual):** Al no encontrar las definiciones completas de sus competencias asignadas (`H-20` y `H-21`) en su archivo de asignación directa, procedió a abrir `cta.json` (un archivo de varios megabytes), haciendo búsquedas por texto y leyendo rangos de 200 líneas sucesivamente (Pasos 24, 26, 28, 30, 32, 34, 36, 38, 40).
- **Paso 42:** Redactó finalmente `shard_82_data.py`.
- **Paso 44:** Compiló en un solo intento con 100% de éxito.

#### C. Shards 51 (`450.0 s`), 52 (`437.0 s`) y 59 (`420.0 s`)
- `shard_51`: Acumuló 411.0 s en pre-compilación debido a fricciones con comillas y variables en PowerShell al intentar buscar archivos, además de reintentos por validaciones de paridad psicométrica (R-14..R-19).
- `shard_52`: Presentó un patrón mixto. Dedicó 328.0 s a inspeccionar `shard_01_data.py` y `shard_52.json` antes de escribir. Su primera compilación falló por `TPL-VAR` y `R-18` en `_gen_c27`, requiriendo un ciclo de edición quirúrgica (+118.0 s post-compile).
- `shard_59`: Pasó 406.0 s pre-compilación realizando búsquedas exhaustivas a lo largo de 10 pasos en el archivo `pre_shard_manifest.json` (líneas 10700 a 11500) para ubicar los distractores de las competencias `C-44` y `C-45`.

---

### 3.3. Análisis de Clústeres de Concurrencia y Disparidad de Carga

Al particionar los 83 shards en 4 rangos de ejecución consecutiva, se observa un fenómeno arquitectónico crítico de **amplificación de varianza**:

| Clúster de Shards | Rango | Shards | Media (s) | Mediana (s) | Min (s) | Max (s) | Desv. Est. (s) | Pre Media (s) | Post Media (s) | Ediciones |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Clúster 1** | Shards 01–20 | 20 | **261.8** | 260.0 | 170.0 | 309.0 | **34.1** | 224.7 | 46.0 | 2 |
| **Clúster 2** | Shards 21–40 | 20 | **268.9** | 265.0 | 190.0 | 323.0 | **36.7** | 245.7 | 33.8 | 4 |
| **Clúster 3** | Shards 41–60 | 20 | **323.8** | 303.5 | 194.0 | **609.0** | **99.2** | 293.0 | 39.5 | **10** |
| **Clúster 4** | Shards 61–83 | 23 | **324.4** | 319.0 | 241.0 | 459.0 | **59.5** | 282.9 | 50.6 | 1 |

```
====================================================================================================
HALLAZGO FORENSE: IMPACTO DE LA DENSIDAD DE COMPETENCIAS POR SHARD
====================================================================================================
Clústeres 1 y 2 (Shards 01-41) : 1 sola competencia por shard (Hab-01 a Hab-41)
  - Tiempo promedio: ~265 s | Desviación estándar baja: ~35 s | Ediciones totales: 6
  - Tokens activos por shard: ~110,000 tokens

Clústeres 3 y 4 (Shards 42-83) : 2 a 3 competencias por shard (C-01..C-54, H-01..H-32)
  - Tiempo promedio: ~324 s (+22% de latencia) | Desviación estándar alta: hasta 99.2 s
  - Ediciones totales: 11 (concentradas en Shards 51, 52, 56)
  - Tokens activos por shard: ~190,000 a 240,000 tokens (+100% de longitud de código)
====================================================================================================
```
**Conclusión de Arquitectura:** Asignar más de 1 competencia por shard duplica la longitud del código generado (8 plantillas paramétricas en un solo archivo en lugar de 4), incrementando drásticamente el espacio de error para llaves no escapadas (`R-20`), colisión de opciones en generadores (`TPL-D4`) e insuficiencia de cuotas de diversidad (`TPL-VAR`).

---

## 4. Stage 5: Arbitraje Psicométrico Ciego (22 Blind Judges)

En Stage 5, la verificación de integridad semántica de los reactivos se confió a un panel colegiado de **22 Blind Judges desplegados en paralelo estricto**.

### 4.1. Concurrencia, Latencia y Aislamiento Epistémico

- **Tamaño de Muestra Evaluada:** `254 reactivos estratificados` (2 reactivos representativos por cada una de las 127 competencias).
- **Distribución de Latencias:**
  - Mínima: `53.0 s` (Judges 11, 12, 20).
  - Mediana: `76.5 s`.
  - Promedio: `78.7 s`.
  - Máxima: `134.0 s` (Blind Judge 02).
- **Consumo de Tokens:** 1,256,972 entrada | 252,637 salida | 1,831,773 caché | 46,245 thinking.
- **Aislamiento Epistémico:** ✅ **100% Hermético**. Se registraron **0 llamadas a `search_web`** y **0 peticiones HTTP externas**. Los 22 jueces operaron en modo de razonamiento puro aislado.

### 4.2. Dictamen Psicométrico y Tasa de Acuerdo

- **Tasa de Acuerdo al Primer Intento:** **`100.0%`** (254 de 254 reactivos con validación psicométrica unánime frente al ground truth).
- **Discrepancias Detectadas:** **`0 discrepancias`**. No se requirió ninguna ronda de arbitraje secundario ni desempate por modelo juez superior.
- **Micro-reparaciones Previas:** La etapa determinista previa (`--stage verify`) corrigió 2 anomalías de escape antes de que el lote fuera sometido a arbitraje ciego.

---

## 5. Taxonomía Exhaustiva de Errores (333 Incidencias Forenses)

Ningún error en la ejecución quedó como caja negra. Los 333 fallos registrados durante la interacción de herramientas y compilación se clasifican formalmente en la siguiente taxonomía:

```
====================================================================================================
TAXONOMÍA CONSOLIDADA DE ERRORES Y FRICCIONES DE HERRAMIENTAS
====================================================================================================
[1] Missing File / Relative Path / FileNotFoundError           : 198 (59.5%)
    - Causa: Agentes intentando leer rutas relativas o archivos que aún no existían
      (ej. templates/*.json antes de compilar, o shard_data.py de shards hermanos).
[2] Token Limit Cutoff / Truncamiento en Respuestas            :  87 (26.1%)
    - Causa: Salidas extensas de comandos CLI truncadas en el buffer de consola.
[3] Anti-Giveaway & Psychometric Parity Violations (R-14..R-19):  23  (6.9%)
    - Causa: Opciones distractoras con disparidad de longitud o pistas léxicas obvias.
[4] PowerShell Command / Quoting / $ Expansion Friction        :  11  (3.3%)
    - Causa: Fallos de sintaxis en comandos Powershell por caracteres reservados ($).
[5] Non-Zero CLI Exit / Subprocess Probes                      :   7  (2.1%)
    - Causa: Prospección exploratoria de binarios con flags erróneos.
[6] CTA Compilation & Schema Errors (CTA-SCHEMA / DAG Cycle)   :   3  (0.9%)
    - Causa: Esquema temporal de prerrequisitos cíclicos en mappers.
[7] Parameter Diversity & Option Collapse (TPL-VAR / TPL-D4)   :   3  (0.9%)
    - Causa: Generadores aleatorios produciendo distractores duplicados o sin variedad.
[8] Shard Compilation Failure (Syntax / Key Errors R-20)       :   1  (0.3%)
    - Causa: Llaves no escapadas en cadenas format f"{...}" con código LaTeX.
----------------------------------------------------------------------------------------------------
TOTAL ERRORES CAPTURADOS Y CATALOGADOS                         : 333 (100.0%)
====================================================================================================
```

---

## 6. Recomendaciones Arquitectónicas Accionables (Soluciones de Ingeniería)

Para evitar la latencia de cola (tail latency) y la aparición de stragglers en futuras ejecuciones a escala masiva (80+ shards), se formulan las siguientes 5 intervenciones técnicas concretas:

### Recomendación 1: Enclosure de Autosuficiencia en Turno 0 (Turn-0 Strict Enclosure)
- **Problema Observado:** Shards como `shard_82` y `shard_59` perdieron más de 400 segundos cada uno deambulando por el sistema de archivos, abriendo `cta.json` de 10 MB o buscando en `pre_shard_manifest.json` porque creían que les faltaban datos.
- **Acción Arquitectónica:** 
  1. Inyectar en el archivo de despacho (`author_XX.json`) el 100% de los metadatos necesarios (fórmulas, definiciones pedagógicas y catálogo de distractores pre-aprobados).
  2. Implementar un **Scope-Lock Hook** estricto que devuelva un error inmediato e instructivo si un Shard Author intenta llamar a `view_file` o `run_command` sobre cualquier archivo fuera de su propio `author_XX.json` o su propio `shard_XX_data.py`.

### Recomendación 2: Particionamiento Isomórfico Estricto a 1 Competencia por Shard
- **Problema Observado:** Los Clústeres 1 y 2 (1 comp/shard) promediaron 265 s y casi 0 ediciones. Los Clústeres 3 y 4 (2 a 3 comps/shard) promediaron 324 s con un pico de 609 s y 11 ediciones quirúrgicas por colapso de opciones.
- **Acción Arquitectónica:**
  - Modificar el algoritmo de sharding (`c2c_shard.py`) para fijar la granularidad en **estrictamente 1 competencia por shard**. Si hay 127 competencias, deben instanciarse 127 shards individuales. El incremento en concurrencia es despreciable gracias a la paralelización del SDK, mientras que la tasa de error por shard se reduce a casi cero.

### Recomendación 3: Pre-Flight Linter en Cabeceras de Plantilla para R-20 y TPL-D4
- **Problema Observado:** `shard_56` requirió 6 ediciones y 254 segundos adicionales de depuración porque sus cadenas LaTeX tenían llaves sin duplicar (`{` en lugar de `{{`) y su bucle aleatorio generó opciones duplicadas.
- **Acción Arquitectónica:**
  - Incluir en el encabezado de cada plantilla generada una función utilitaria determinista:
    ```python
    def sanitize_math_template(raw_str: str) -> str:
        # Pre-escapa llaves de LaTeX que no pertenezcan a variables del generador
        ...
    def ensure_unique_options(generator_fn, min_options=4, max_retries=100):
        # Garantiza conjuntos disjuntos antes de emitir la tupla
        ...
    ```
  - Proporcionar un linter sintáctico en memoria que alerte al agente en consola antes de ejecutar la compilación pesada del validador.

### Recomendación 4: Balanceo Dinámico de Carga en Mappers CTA por Número de Páginas
- **Problema Observado:** La etapa 1B sufrió un retraso de barrera de 334.0 s (5.5 min) porque `part_10` tuvo que procesar un PDF de 49 páginas mientras los demás mappers procesaban archivos de 12 a 21 páginas.
- **Acción Arquitectónica:**
  - Implementar en `c2c_cta.py` una política de partición basada en páginas (Page-Weighted Splitting): cualquier PDF que supere las 25 páginas debe ser dividido en fragmentos de 20 páginas (ej. `Monopolio_p1..25` y `Monopolio_p26..49`), asignando cada fragmento a un mapper distinto. Esto reduce el tiempo crítico de Stage 1B de 565 s a ~260 s.

### Recomendación 5: Mensaje de Barrera Defensiva para Evitar Ingeniería Inversa
- **Problema Observado:** Varios agentes (`part_10`, `shard_42`, `shard_82`) perdieron turnos intentando inspeccionar los scripts internos del pipeline (`compile_cta.py`, `compile_shard.py`, `check_templates.py`) buscando entender las reglas de validación.
- **Acción Arquitectónica:**
  - Incluir en el prompt de sistema una directiva explícita de "Caja Negra Determinista":
    > *"El compilador `compile_shard.py` es un validador de caja negra inviolable. No intentes leer su código ni ejecutar `--help`. Si la compilación falla, el mensaje de error en STDOUT incluye la tupla exacta y la línea a corregir; realiza la edición quirúrgica únicamente en tu archivo de datos."*

---

## 7. Conclusión del Lead Auditor

La ejecución de `gavilano_pre_parcial` valida de forma contundente la solidez arquitectónica del pipeline C2C v3.21 bajo el Google Antigravity SDK:
1. **Escalabilidad Horizontal Comprobada:** Capacidad de orquestar 115 subagentes y 83 shards concurrentes de manera 100% autónoma, logrando un speedup paralelo de **`11.41x`** sin intervención humana.
2. **Eficiencia de Coste y Caché:** Un **`74.3%` de acierto de caché de contexto**, manteniendo los unit economics en **`0.96 s`** y **`5,250 tokens activos`** por pregunta jugable.
3. **Calidad Psicométrica Absoluta:** Un acuerdo del **`100.0%` en arbitraje ciego** (254/254 reactivos limpios).
4. **Ruta Clara de Optimización:** Implementando el *Turn-0 Strict Enclosure* y la partición estricta de *1 competencia por shard*, el tiempo total del pipeline (47.4 min) puede reducirse en un **`35-40%`**, situando la generación masiva de 3,000 preguntas en menos de **`30 minutos`**.

---
*Informe de Auditoría Lead generado y firmado digitalmente por `c2c-run-auditor` (Antigravity SDK).*
