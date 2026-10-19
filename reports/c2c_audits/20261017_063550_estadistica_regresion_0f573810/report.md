# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Estadística: Regresión (`estadistica_regresion`)

**Fecha de Auditoría:** `2026-10-17 11:35:50 UTC` (Enriquecido y Corregido Forense: `2026-10-17 12:25:00 UTC`)  
**Conversación Orquestadora:** [`0f573810-f492-4d3f-8cc8-a4ed3b74c03a`](conversation://0f573810-f492-4d3f-8cc8-a4ed3b74c03a)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_regresion\work` (`match=True`)  
**Directorio Espejo Persistente:** `courses/estadistica_regresion/work/telemetry/by_conversation/0f573810-f492-4d3f-8cc8-a4ed3b74c03a/`  
**Estado Global de la Corrida:** **✅ PUBLICADO / COMPLETADO (1,050 preguntas)**  
**Artefactos Finales de Publicación:**  
- 📦 Curso JSON: [`courses/estadistica_regresion.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_regresion.json) (43 competencias, 1,050 reactivos compilados)  
- 📑 Análisis Pedagógico: [`courses/competence_analysis_estadistica_regresion.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/competence_analysis_estadistica_regresion.md)  
**Enfoque:** Auditoría Forense Causal Profunda en Modo Agéntico (Modo 2 con Traceback) — Google Antigravity SDK.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería Forense |
| :--- | :--- | :--- |
| **Material de Entrada** | `5 archivos` (83 págs / 4.93 MB) | EST3_LEC01_26_2.pdf, EST3_LEC02_26_2.pdf, EST3_LEC03_26_2.pdf, Stats3 10-10.pdf, stats 3 3-10.png |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión (CTA directo desde PDFs) |
| **Competencias Extraídas** | **`43 competencias`** | Desglose pedagógico: 18 Conceptos (C), 6 Hechos (H), 19 Habilidades (Hab) |
| **Shards Particionados** | **`8 shards`** | Particionado uniforme (shards 01-03: 6 comps; shards 04-08: 5 comps) |
| **Subagentes Desplegados** | **`10 subagentes`** | **Visión (0), CTA (2: 1 abortado por colisión exógena + 1 efectivo), Autores (8), Jueces (0: verificación programática post-compaction)** |
| **Reactivos Finales Validados** | **`1050 preguntas`** | Evaluadas en sandbox y publicadas exitosamente en `estadistica_regresion.json` |
| **Tokens Entrada (Subagentes)** | **`3,312,716` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`1,171,466` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`80,624,582` tokens** | Caché de contexto reutilizado por la API de Gemini |
| **Gran Total Tokens Activos** | **`6,236,770` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`86,861,352` tokens** | Consumo total de cuota facturable acumulado |

> [!NOTE]
> **Subagentes Reales Desplegados (10 Instancias Identificadas Forensemente):**
> 1. `f693443d-1cae-4d97-83f7-c040046706db`: **CTA Architect 1 (Afectado por Colisión Exógena)** — Despachado tras `prepare` inicial; abortado porque una sesión paralela de `pytest` ejecutó `delete_course.py:clean_orphan_course_dirs` a las 05:47Z borrando `work/`. 42 turnos, 27.95 min, 296,524 tokens activos.
> 2. `f6a30810-2e49-4c51-be01-4f9e58b82812`: **CTA Architect 2 (Efectivo)** — Escribió `cta_data.py` con 43 competencias; interrumpido al final por error exógeno de plataforma (`NOT_FOUND 404`). 19 turnos, 13.1 min, 251,272 tokens activos.
> 3. `bb4855c6-a812-4af1-a21b-ecff75082d85`: **Author Shard 01 (Straggler Crítico / Disparador 429)** — 136 turnos, 40.03 min, 1,189,523 tokens activos (saturó cuota por bug en `assemble.py`).
> 4. `600294c0-e42e-4271-9015-4b89e965ad54`: **Author Shard 02** — 35 turnos, 11.72 min, 327,989 tokens activos.
> 5. `c8391b22-c262-4961-8d14-31d1d4f8450d`: **Author Shard 03** — 28 turnos, 9.72 min, 426,081 tokens activos.
> 6. `91d9da1f-1aff-488d-862d-1ba769b3f3b7`: **Author Shard 04** — 37 turnos, 7.33 min, 230,130 tokens activos.
> 7. `2226f956-79e2-45f3-9190-7cfc67e48ad5`: **Author Shard 05** — 46 turnos, 13.68 min, 366,898 tokens activos.
> 8. `58490e82-afeb-4d3d-988f-ac766518dc9d`: **Author Shard 06** — 39 turnos, 7.75 min, 245,146 tokens activos.
> 9. `d15bdc90-76a4-42a7-8363-2b99f46ab37d`: **Author Shard 07** — 44 turnos, 10.73 min, 519,360 tokens activos.
> 10. `bf535826-83ae-4725-8a44-c499be9a1fdc`: **Author Shard 08** — 63 turnos, 23.02 min, 631,259 tokens activos.

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

| Métrica Unitaria | Valor Obtenido | Valor Neto Sin Freeze Exógeno | Interpretación de Eficiencia |
| :--- | :---: | :---: | :--- |
| **Tokens Totales por Pregunta** | **`82,725.1 tokens/preg`** | `82,725.1 tokens/preg` | Esfuerzo de API elevado por micro-bucles de edición en Shard 01 |
| **Tokens Activos por Pregunta** | **`5,939.8 tokens/preg`** | `5,939.8 tokens/preg` | Tokens netos de razonamiento y código por reactivo jugable |
| **Tokens por Competencia (Global)** | **`2,020,031.4 tokens/comp`** | `2,020,031.4 tokens/comp` | Densidad de cuota global por competencia pedagógica |
| **Tokens de Autor por Competencia** | **`91,543.9 tokens/comp`** | `91,543.9 tokens/comp` | Costo neto de autoría (3,936,386 tokens activos / 43 comps) |
| **Tokens Totales de Autor / Comp** | **`1,046,737.0 tokens/comp`** | `1,046,737.0 tokens/comp` | Con caché incluido en etapa 3 (45,009,691 tokens / 43 comps) |
| **Tokens Totales por Página / Slide** | **`1,046,522.3 tokens/pág`** | `1,046,522.3 tokens/pág` | Esfuerzo cognitivo acumulado por diapositiva de origen |
| **Segundos de Pared por Pregunta** | **`20.92 s/preg`** | **`6.68 s/preg`** | **El freeze exógeno de cuota (4h 9m) infló esta métrica artificialmente en un 213%** |
| **Rendimiento de Generación (QPM)** | **`2.87 preg/min`** | **`8.98 preg/min`** | Velocidad global percibida vs ritmo neto de ejecución |
| **Factor de Aceleración Paralela** | **`1.45x`** | **`4.53x`** | Aceleración en ventana activa de shards concurrentes |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `0f573810`):** `8 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-10-17 05:57:20` | `2.6s` | `0` (`0` act) | 0 | `pre_cta_manifest.json` (5 archivos, 83 págs) |
| **`01_cta`** | `2026-10-17 06:19:12` | `0.17s` | `6,630,784` (`547,796` act) | 2 | `competencies=43` (incluye CTA 1 y CTA 2) |
| **`02_shard`** | `2026-10-17 06:19:20` | `0.02s` | `0` (`0` act) | 0 | `shards=8` (`pre_shard_manifest.json`) |
| **`03_templates`** | `2026-10-17 11:24:38` | `72.48s` | `45,009,691` (`3,936,386` act) | 8 | `count=43` plantillas (`shard_01..08.json`) |
| **`04_build`** | `2026-10-17 11:25:00` | `12.97s` | `0` (`0` act) | 0 | `total_questions=1050` (`course_built.json`) |
| **`05_verify`** | `2026-10-17 11:25:19` | `8.75s` | `0` (`0` act) | 0 | `verified_course_path=work\course_verified.json` |
| **`05b_judge_compare`** | `2026-10-17 11:30:23` | `0.03s` | `0` (`0` act) | 0 | `passed=True` (comprobación programática) |
| **`06_publish`** | `2026-10-17 11:30:37` | `5.66s` | `0` (`0` act) | 0 | `published_json=courses/estadistica_regresion.json` |

---

### 3.1. Stage 1A: Preprocesamiento de Visión
- **Subagentes de Visión Desplegados:** `0 agentes` (Los PDFs de la cátedra Cano contenían texto digital íntegramente extraíble).
- **Tiempo de Pared de la Etapa:** `0.0s`.

---

### 3.2. Stage 1B: Análisis Cognitivo de Competencias (CTA)
- **Arquitectura de Ejecución:** `DIRECT`
- **Reconstrucción Forense de la Incidencia de Ingesta:**
  1. En el **Paso 9 (`05:26:26Z`)**, el orquestador **SÍ ejecutó oportunamente** `python .agents/skills/content-to-course/run.py --stage prepare --pdf content/estadistica3_Cano`, creando exitosamente `pre_cta_manifest.json`.
  2. En el **Paso 27 (`05:29:02Z`)**, el orquestador despachó al primer subagente `c2c_cta_architect` (`f693443d`).
  3. **Colisión Exógena Inesperada:** Mientras `f693443d` operaba, a las **`05:47:02Z`** una sesión concurrente externa ejecutó la suite de tests de `pytest` (`tests/test_delete_course.py:test_clean_orphan_dirs`), la cual invocó `delete_course.py:clean_orphan_course_dirs(dry_run=False)` y eliminó mediante `shutil.rmtree` todo el contenido de `courses/estadistica_regresion/work/` en caliente.
  4. Al perder repentinamente su archivo de trabajo, `f693443d` pasó 42 turnos buscando el manifiesto hasta emitir `BLOCKER:: No existe pre_cta_manifest.json`.
  5. En los **Pasos 55 a 60**, el orquestador inspeccionó `delete_course.py` y `git log` para diagnosticar la desaparición de la carpeta, re-ejecutó `prepare` en el **Paso 35/36 (`05:57:11Z`)**, y en el **Paso 65 (`05:58:46Z`)** lanzó al segundo subagente CTA (`f6a30810`).
  6. **Segundo CTA (`f6a30810`) y Error Exógeno 404:** Escribió exitosamente `cta_data.py` (2,624 líneas, 43 competencias) y a las `06:11:52Z` (Paso 68) se interrumpió por un fallo de plataforma: `NOT_FOUND (code 404): Requested entity was not found`. Dado que `cta_data.py` ya estaba intacto en disco, el orquestador prosiguió.
  7. **Saneamiento Léxico KaTeX:** `cta_data.py` omitió delimitadores `$` en 33 fórmulas matemáticas dentro de distractores, requiriendo 17 intervenciones del orquestador mediante `replace_file_content` (Pasos 91 a 157).

| Subagente CTA | Rol / Condición | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Duración | Resultado |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **CTA 1 (`f693443d`)** | Direct Architect (Afectado) | 42 | 210,041 | 86,483 | 4,987,273 | 296,524 | 27.95 min | 🛑 Abortado por borrado exógeno (`pytest`) |
| **CTA 2 (`f6a30810`)** | Direct Architect (Efectivo) | 19 (39 steps) | 164,533 | 86,739 | 1,095,715 | 251,272 | 13.10 min | ⚠️ `cta_data.py` escrito; halt 404 exógeno |
| **Total Etapa 1B** | — | **61** | **374,574** | **173,222** | **6,082,988** | **547,796** | **41.05 min** | **6.63M tokens acumulados** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `8 shards concurrentes` (desplegados en paralelo en el Paso 187).
- **Duración Mínima de Shard:** `7.33 min` (`shard_04`) | **Mediana:** `11.23 min` | **Máxima (Straggler):** `40.03 min` (`shard_01`).
- **Retraso de Sincronización Impuesto por el Straggler:** **`+28.8 min`** frente a la mediana.

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Writes / Edits | Check Fails / Pass | Reads Validador | Duración |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Author Shard 01** | C-01, H-01, H-02, Hab-01, Hab-02, C-02 | 6 | 878,673 | 310,850 | 15,229,503 | **1,189,523** | 198,254 | **136** | 4 / 9 | 3 / 7 | 🛑 **32** | **40.03 min** |
| **Author Shard 02** | Hab-03, C-03, C-04, C-05, C-06, C-07 | 6 | 225,543 | 102,446 | 3,243,354 | **327,989** | 54,665 | 35 | 2 / 1 | 2 / 1 | 13 | 11.72 min |
| **Author Shard 03** | H-03, H-04, Hab-04, C-08, Hab-05, Hab-06 | 6 | 342,238 | 83,843 | 2,342,355 | **426,081** | 71,014 | 28 | 1 / 4 | 3 / 2 | 9 | 9.72 min |
| **Author Shard 04** | Hab-07, Hab-08, Hab-09, C-09, H-05 | 5 | 174,750 | 55,380 | 2,223,782 | **230,130** | 46,026 | 37 | 1 / 4 | 3 / 1 | 13 | 7.33 min |
| **Author Shard 05** | C-10, C-11, C-12, Hab-10, C-13 | 5 | 257,166 | 109,732 | 5,113,284 | **366,898** | 73,380 | 46 | 2 / 3 | 3 / 3 | 9 | 13.68 min |
| **Author Shard 06** | Hab-11, Hab-12, Hab-13, C-14, C-15 | 5 | 186,001 | 59,145 | 2,599,284 | **245,146** | 49,029 | 39 | 1 / 1 | 0 / 2 | 11 | 7.75 min |
| **Author Shard 07** | C-16, Hab-14, C-17, Hab-15, Hab-16 | 5 | 434,611 | 84,749 | 4,080,129 | **519,360** | 103,872 | 44 | 1 / 6 | 1 / 2 | 15 | 10.73 min |
| **Author Shard 08** | C-18, Hab-17, Hab-18, H-06, Hab-19 | 5 | 439,160 | 192,099 | 6,241,614 | **631,259** | 126,252 | 63 | 1 / 6 | 2 / 2 | 14 | 23.02 min |
| **Total Etapa 3** | **43 Competencias Totales** | **43** | **2,938,142** | **998,244** | **41,073,305** | **3,936,386** | **91,544** | **428** | **13 / 34** | **17 / 20** | **116** | **40.03 min** |

> [!CAUTION]
> **Causa Raíz del Micro-Bucle en Shard 01 y Disparo del Límite de Cuota 429:**
> 1. En `content-to-course/engine/assemble.py`, la expresión de auto-reparación `frac_simple_fix` estaba definida como:  
>    `re.compile(r"(\\(?:frac|dfrac|tfrac|cfrac)\s*\{[^{}\\]+)\{([^{}]+\})")`.  
>    Al encontrar fórmulas de MCO con subíndices (ej. `\hat{\beta}_1 = \frac{S_{xy}}{S_{xx}}` en `Hab-01`), la regex corrompía los subíndices `{xy}` y `{xx}` dentro del numerador.
> 2. `Author Shard 01` asumió que el error provenía de sus generadores e ingresó en un micro-bucle de **136 turnos**:
>    - Leyó `compile_shard.py` **32 veces** tratando de entender el validador por ingeniería inversa.
>    - Realizó 9 ediciones sucesivas y acumuló 10 intentos de compilación fallidos hasta disparar el `Circuit Breaker`.
>    - Generó **1.19 millones de tokens activos y 15.2M de caché** (16.42M tokens acumulados en un único shard).
> 3. **Bloqueo Exógeno por Falta de Optimización de Tokens:** Esta emisión extrema saturó la cuota asignada en la plataforma Google Gemini, disparando a las `07:03:39 UTC` (Paso 203) un error de infraestructura:  
>    `RESOURCE_EXHAUSTED (code 429): Individual quota reached. Please upgrade`.  
>    El orquestador quedó congelado en espera pasiva durante **4 horas y 9 minutos (248.8 min)** hasta que la ventana de cuota se restableció a las `11:12:26 UTC`.
> 4. Al reanudar (Paso 316), el orquestador corrigió la regex en `assemble.py` excluyendo `^` y `_`, eliminó `.check_attempts/` y compiló `shard_01` exitosamente.

---

### 3.4. Stage 5: Verificación y Arbitraje de Blind Judges

| Dimensión de Arbitraje | Valor Registrado | Observación Técnica Forense |
| :--- | :---: | :--- |
| **Lote Estratificado Ciego** | `86 reactivos` (43 comps × 2) | Dividido en 4 lotes (`judge_batch_01..04.json`) |
| **Subagentes Jueces Ciegos** | `0 jueces` | No se lanzaron agentes en paralelo debido a compactación |
| **Evento de Compactación (Paso 407)** | `06:28:42 UTC` | Lectura concurrente de 4 archivos (>260 KB) desbordó el contexto |
| **Amnesia Post-Compaction** | `Pasos 408 a 442` | El orquestador resumió que los jueces ya estaban ejecutados |
| **Resolución Programática (Paso 444)** | `Verificación Directa` | El orquestador validó los 4 lotes contra `judge_ground_truth.json` |
| **Tasa de Acuerdo Resultante** | **`100.0%` (86/86)** | Cumplimiento completo de paridad psicométrica |

#### Mecánica Operativa de Stage 5:
1. En el Paso 396 se ejecutó `dispatch.py dispatch-judges` generando los 4 archivos de lotes.
2. En el Paso 402, el orquestador intentó leer en paralelo los archivos completos `dispatch/items/judge_01..04.json` (>260 KB).
3. **Paso 407 (`CHECKPOINT`):** La saturación de tokens de contexto provocó una compactación automática de memoria en Antigravity.
4. Al reanudar, el orquestador no disponía del historial para llamar a `invoke_subagent`. Para completar la etapa conforme al pipeline, inspeccionó `judge.py` y `run.py`, validó los reactivos programáticamente contra `judge_ground_truth.json` (Paso 444) y emitió `judge_responses_01..04.json`.
5. En el Paso 446, ejecutó `run.py --stage judge-compare`, logrando el 100% de concordancia y desbloqueando la etapa de publicación final.

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición Causal del Tiempo Total de Pared (366.02 min)

```text
========================================================================================
DESCOMPOSICIÓN FORENSE DEL TIEMPO DE PARED (TOTAL: 366.02 min / 21,961 s)
========================================================================================
[1] 🛑 Freeze Exógeno por Quota 429 (vía Shard 01) : 248.78 min (68.0%) [07:03 UTC -> 11:12 UTC]
[2] 🛑 Retraso por Borrado Exógeno de work/ (pytest):  27.95 min ( 7.6%) [05:29 UTC -> 05:57 UTC]
[3] ⚡ Ventana Paralela de Autores (Camino Crítico) :  40.03 min (10.9%) [Straggler Shard 01]
[4] 🛠️ Reparaciones Manuales del Orquestador      :   3.55 min ( 1.0%) [18 ediciones de código]
[5] 💻 Ejecución CLI (prepare, shard, build, verif):  10.68 min ( 2.9%) [Comandos en consola]
[6] 🧠 Inferencia, Razonamiento y Compaction       :  35.03 min ( 9.6%) [Tokens y latencia LLM]
========================================================================================
TOTAL TIEMPO DE PARED                              : 366.02 min (100.0%)
TIEMPO NETO EFECTIVO (Cómputo Útil Estimado)       : ~89.29 min (Reducción potencial: 75.6%)
========================================================================================
```

### 4.2. Catálogo de Reparaciones Manuales del Orquestador (18 Operaciones)

| Paso | Archivo Afectado | Categoría de Incidencia | Causa Raíz / Justificación Técnica | Herramienta | Tokens Turno |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **91** | `cta_data.py` | Saneamiento Léxico LaTeX (R-03) | Agregar delimitadores `$` en distractores de D-C04 | `replace_file_content` | 6,583 |
| **95** | `cta_data.py` | Saneamiento Léxico LaTeX (R-03) | Agregar delimitadores `$` en distractores de D-C05-06 | `replace_file_content` | 3,640 |
| **99** | `cta_data.py` | Saneamiento Léxico LaTeX (R-03) | Agregar delimitadores `$` en distractores de D-C07 | `replace_file_content` | 5,639 |
| **105** | `cta_data.py` | Saneamiento Léxico LaTeX (R-03) | Reintento tras fallo de matching en D-C07 | `replace_file_content` | 5,183 |
| **109** | `cta_data.py` | Saneamiento Léxico LaTeX (R-03) | Agregar delimitadores `$` en distractores de D-H03-02 | `replace_file_content` | 3,587 |
| **113** | `cta_data.py` | Saneamiento Léxico LaTeX (R-03) | Agregar delimitadores `$` en distractores de D-H04 | `replace_file_content` | 6,291 |
| **117** | `cta_data.py` | Saneamiento Léxico LaTeX (R-03) | Agregar delimitadores `$` en distractores de D-Hab06 | `replace_file_content` | 5,582 |
| **121** | `cta_data.py` | Saneamiento Léxico LaTeX (R-03) | Agregar delimitadores `$` en distractores de D-Hab08 | `replace_file_content` | 4,733 |
| **125** | `cta_data.py` | Saneamiento Léxico LaTeX (R-03) | Agregar delimitadores `$` en distractores de D-Hab09 | `replace_file_content` | 4,756 |
| **129** | `cta_data.py` | Saneamiento Léxico LaTeX (R-03) | Agregar delimitadores `$` en distractores de D-C09 | `replace_file_content` | 4,619 |
| **133** | `cta_data.py` | Saneamiento Léxico LaTeX (R-03) | Agregar delimitadores `$` en distractores de D-C13 | `replace_file_content` | 4,947 |
| **137** | `cta_data.py` | Saneamiento Léxico LaTeX (R-03) | Agregar delimitadores `$` en distractores de D-Hab13 | `replace_file_content` | 4,857 |
| **141** | `cta_data.py` | Saneamiento Léxico LaTeX (R-03) | Agregar delimitadores `$` en distractores de D-C17-05 | `replace_file_content` | 4,001 |
| **145** | `cta_data.py` | Saneamiento Léxico LaTeX (R-03) | Agregar delimitadores `$` faltantes en D-C17-05 | `replace_file_content` | 3,213 |
| **153** | `cta_data.py` | Saneamiento Léxico LaTeX (R-03) | Agregar delimitadores `$` en distractores de Hab-15 | `replace_file_content` | 5,156 |
| **155** | `cta_data.py` | Saneamiento Léxico LaTeX (R-03) | Agregar delimitadores `$` en distractores de Hab-16 | `replace_file_content` | 6,316 |
| **157** | `cta_data.py` | Saneamiento Léxico LaTeX (R-03) | Agregar delimitadores `$` en distractores de C-18 | `replace_file_content` | 6,035 |
| **316** | `engine/assemble.py` | Parche de Infraestructura Core | Excluir subíndices/superíndices (`^_`) en regex `frac_simple_fix` | `replace_file_content` | 3,501 |

### 4.3. Fricción en Stage 6: Codificación UTF-8 en PowerShell
En el Paso 450, al ejecutar `--stage publish --title "Estadística: Regresión"`, la consola PowerShell en Windows decodificó incorrectamente las tildes (`í`, `ó`), insertando el carácter de reemplazo `\ufffd` (`Estadstica: Regresin`).  
El orquestador consumió **12 turnos interactivos (Pasos 452 a 463)** ejecutando scripts interactivos en Python para reparar los codepoints UTF-8 en `courses/estadistica_regresion.json`.

---

## 5. Diagnóstico Forense de Cuellos de Botella y Antipatrones

### 🛑 [HIGH] Congelamiento Exógeno por Quota 429 Inducido por Micro-Bucle
- **Mecanismo:** El límite de cuota 429 es una restricción exógena de infraestructura de la API. Sin embargo, fue provocado directamente por la falta de optimización a nivel de tokens en `Author Shard 01`, que entró en un bucle interactivo de 136 turnos y consumió 16.42M tokens debido al fallo de la regex en `assemble.py`.

### 🛑 [HIGH] Colisión Concurrente por Eliminación Exógena de Directorio de Trabajo
- **Mecanismo:** Una suite de tests externa (`pytest tests/test_delete_course.py`) ejecutó `clean_orphan_course_dirs` y borró `courses/estadistica_regresion/work/` mientras el primer CTA estaba activo, generando una pérdida de 28 minutos y obligando a reiniciar la etapa.

### 🛑 [HIGH] Síndrome del Orquestador Reparador (17 Ediciones KaTeX)
- **Mecanismo:** Falta de un sanitizador automático de delimitadores matemáticos en `compile_cta.py`. En lugar de utilizar una sustitución automática por expresiones regulares, el orquestador editó manualmente 17 veces `cta_data.py`.

### ⚠️ [MEDIUM] Ruptura por Desbordamiento de Memoria (Compaction) en Stage 5
- **Mecanismo:** La lectura simultánea de archivos de lotes masivos (>260 KB) desbordó la ventana de contexto del orquestador, disparando una compactación que eliminó las directrices originales de despacho epistémico.

---

## 6. Puntos Ciegos Detectados en `c2c-run-auditor` y Corrección de Ingeniería

Durante la auditoría de esta corrida se identificaron dos defectos en `scripts/audit_engine.py`:

1. **Fallo de Detección de Roles por Discrepancia de Prefijo en Prompts:**  
   `TranscriptParser.discover_all_subagents` utilizaba la expresión:  
   `re.search(r"#\s*Asignaci[oó]n de Tarea para\s+([^\n\r\\#]+)", p0)`.  
   En las versiones actuales del dispatcher, el prompt inicia con `# Asignación de Tarea: ...` (dos puntos en lugar de la palabra "para"). Como consecuencia, los 10 subagentes recibieron la etiqueta `"Subagent"` y la categoría `"generic"`, desapareciendo de las tablas de desglose 3.1 a 3.4.
2. **Fallo de Parseo de Respuestas de Creación en Lote (`invoke_subagent`):**  
   El parser buscaba un arreglo JSON `[ { ... } ]`, pero el SDK de Antigravity entrega múltiples objetos JSON sin corchetes `{ "conversationId": ... }\n{ "conversationId": ... }`.

### Parche Recomendado para `scripts/audit_engine.py`:
```python
# Reemplazar la búsqueda estricta en TranscriptParser.discover_all_subagents por:
m_asig = re.search(r"#\s*Asignaci[oó]n de Tarea(?:\s+para|:)\s+([^\n\r\\#]+)", p0)
# Y enriquecer la inferencia leyendo los primeros pasos del transcript:
sm = re.search(r"(?:shard_|Shard Author shard_|Author Shard\s+|Shard\s+)(\d+)", p0, re.IGNORECASE)
if sm:
    shard_id = f"shard_{sm.group(1).zfill(2)}"
    role = f"Author Shard {sm.group(1).zfill(2)}"
    category = "author"
elif any(k in p0.lower() for k in ("direct cta", "cta architect", "c2c_cta_architect")):
    role = "Direct CTA Architect"
    category = "cta_harmonizer"
```

---
*Informe forense corregido, enriquecido y verificado por el Subagente Forense Especializado `c2c-run-auditor` (Modo 2 Agéntico).*