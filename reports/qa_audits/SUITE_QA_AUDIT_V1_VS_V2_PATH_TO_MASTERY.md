# Matriz Comparativa Forense de Auditoría QA: Rúbrica v1 vs. Rúbrica Path-to-Mastery v2.0
## Suite Completa de 9 Cursos Activos en Top's Academy (539 Competencias · 12,610 Reactivos)

**Fecha de Consolidación:** `2026-10-31`  
**Conversación Orquestadora:** [`d57ff84d`](conversation://d57ff84d-cdc3-4c8c-90f8-05bd6b65bee4)  
**Topología de Agentes Auditores:**
- **2 Auditores QA en Gemini 4 Argon** (`estadistica_3_s9_vdirect` y `estadistica_3_s9_vmapreduce`)
- **7 Auditores QA Exclusivos de Curso en Gemini Flash (High)** (suite activa histórica completa: `solow_growth_model`, `saul_control_optimo`, `gavilano_pre_parcial`, `saul_pre_parcial`, `asyntotic_estatistics_v7`, `estadistica_3_pre_parcial`, `estadistica_3_pre_parcial_v2`)

**Archivos de Respaldo y Trazabilidad Inmutable:**
- **Línea Base Histórica v1 (Intacta):** [`reports/qa_audits/v1_baseline_archive/`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v1_baseline_archive/)
- **Reportes y Payloads Path-to-Mastery v2.0:** [`reports/qa_audits/v2_path_to_mastery/`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/) y [`reports/qa_audits/`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/)

---

## 1. Hallazgo Central: Ruptura del "Falso Techo" v1 y Validación Discriminante de v2.0

> [!IMPORTANT]
> **¿Es la nueva rúbrica v2 arbitrariamente punitiva o quirúrgicamente discriminante?**  
> La prueba de fuego empírica la aporta **`solow_growth_model`**: bajo el escrutinio implacable de **Path-to-Mastery v2.0**, `solow_growth_model` sostiene **`18.00 / 20.0` (`Δ = -1.80`)** y alcanza **`MPRI = 89.77 / 100.0` (`GOLD MASTERY PATH`)**, obteniendo puntaje perfecto en **4 de los 6 pilares cognitivos** (`20/20` en evocación activa FIB+MS, `25/25` en salvavidas socrático limpio, `10/10` en DAG y `10/10` en ergonomía KaTeX).  
> En contraste, los 6 cursos generados con el molde Form-A de `compile_shard.py` —que bajo **v1** estaban comprimidos artificialmente entre **`16.8` y `18.8 / 20.0`** (*"Excelente / Aceptable"*)— colapsan entre **`-11.50` y `-13.90` puntos** hasta **`4.90 – 6.30 / 20.0`** (`MPRI = 26.58 – 39.71 / 100`), destapando ceguera de parser (`opt["content"]`), parálisis ZPD del 100%, monocultivo pasivo MC7, envenenamiento anti-socrático de pistas y exploits de memorización visual de 1 única respuesta.

### Estadísticos Descriptivos del Cambio Metodológico (7 Cursos con Línea Base v1)

| Estadístico en la Suite con Baseline v1 ($N = 7$) | Rúbrica Histórica **v1** (`/20.0`) | Rúbrica **Path-to-Mastery v2.0** (`/20.0`) | Índice **`MPRI` v2.0** (`/100.0`) |
| :--- | :---: | :---: | :---: |
| **Media Aritmética** | **18.31 / 20.0** | **8.33 / 20.0** (`Δ = -9.99`) | **45.40 / 100.0** |
| **Mediana** | **18.50 / 20.0** | **6.20 / 20.0** (`Δ = -12.30`) | **39.54 / 100.0** |
| **Rango Dinámico (`Max - Min`)** | **3.00 pts** (`16.8` – `19.8`) | **13.10 pts** (`4.9` – `18.0`) | **63.19 pts** (`26.58` – `89.77`) |
| **Cursos en Tier `EXCELENTE` (`>= 17.0`)** | **6 / 7 (`85.7%`)** | **1 / 7 (`14.3%`)** (`solow_growth_model`) | **1 / 7** (`GOLD MASTERY`) |
| **Cursos en Tier `DEFICIENTE` (`11.0 – 13.9`)** | **0 / 7 (`0.0%`)** | **1 / 7 (`14.3%`)** (`saul_control_optimo`) | **1 / 7** (`ILLUSION OF MASTERY`) |
| **Cursos en Tier `CRÍTICO` (`< 11.0`)** | **0 / 7 (`0.0%`)** | **5 / 7 (`71.4%`)** (+ 2 cursos S9 nuevos = **7 / 9**) | **7 / 9** (`MASTERY-HOSTILE`) |

---

## 2. Tabla Maestra v1 vs. v2 de la Suite Activa Completa (9 Cursos · 12,610 Reactivos)

| Curso Activo (`courses/*.json`) | Comps / Pregs | Modelo Auditor v2 | Nota **v1** (`/20`) | Tier **v1** | Subtotal Bruto **v2** | Pen. Duras **v2** | Nota **v2** (`/20`) | Delta **(`v2 - v1`)** | **`MPRI`** (`/100`) | Tier **Path-to-Mastery v2.0** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| [**`solow_growth_model`**](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/solow_growth_model_qa_report_v2.md) | 25 / 580 | Flash High ([`5183d942`](conversation://5183d942-9ad0-4355-91df-3b51450f020a)) | **19.80** | EXCELENTE | 18.00 | 0.00 | **18.00** | **`-1.80`** | **89.77** | 🏆 **EXCELENTE (`GOLD MASTERY`)** |
| [**`saul_control_optimo`**](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/saul_control_optimo_qa_report_v2.md) | 15 / 350 | Flash High ([`8ad53973`](conversation://8ad53973-4de7-447c-99d4-23bf46fd71cb)) | **18.50** | EXCELENTE | 12.00 | 0.00 | **12.00** | **`-6.50`** | **54.23** | ⚠️ **DEFICIENTE (`ILLUSION OF MASTERY`)** |
| [**`gavilano_pre_parcial`**](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/gavilano_pre_parcial_qa_report_v2.md) | 127 / 2,950 | Flash High ([`8985c796`](conversation://8985c796-6b5a-4715-b38d-77aed0cd77d3)) | **18.50** | EXCELENTE | 9.80 | -3.50 | **6.30** | **`-12.20`** | **39.54** | 🛑 **CRÍTICO (`MASTERY-HOSTILE`)** |
| [**`saul_pre_parcial`**](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/saul_pre_parcial_qa_report_v2.md) | 63 / 1,520 | Flash High ([`52c79c70`](conversation://52c79c70-c7db-477e-b5f2-b319b48f579e)) | **18.00** | EXCELENTE | 9.70 | -3.50 | **6.20** | **`-11.80`** | **39.71** | 🛑 **CRÍTICO (`MASTERY-HOSTILE`)** |
| [**`estadistica_3_s9_vdirect`**](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/estadistica_3_s9_vdirect_qa_report.md) | 27 / 620 | **Argon** ([`bba1045d`](conversation://bba1045d-8aa3-4956-b69f-3072644530d3)) | *N/A (Nuevo)*\* | *(Risk v1: 11.3)* | 8.50 | -2.50 | **6.00** | *N/A* | **35.94** | 🛑 **CRÍTICO (`MASTERY-HOSTILE`)** |
| [**`asyntotic_estatistics_v7`**](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/asyntotic_estatistics_v7_qa_report_v2.md) | 32 / 710 | Flash High ([`93c3b4e1`](conversation://93c3b4e1-f68c-4bc7-a948-f7ad563e331b)) | **17.80** | EXCELENTE | 9.10 | -3.50 | **5.60** | **`-12.20`** | **38.62** | 🛑 **CRÍTICO (`MASTERY-HOSTILE`)** |
| [**`estadistica_3_s9_vmapreduce`**](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/estadistica_3_s9_vmapreduce_qa_report.md) | 39 / 920 | **Argon** ([`3ac50f20`](conversation://3ac50f20-8fbb-4814-8820-c157116032d0)) | *N/A (Nuevo)*\* | *(Risk v1: 13.7)* | 7.50 | -2.00 | **5.50** | *N/A* | **39.45** | 🛑 **CRÍTICO (`MASTERY-HOSTILE`)** |
| [**`estadistica_3_pre_parcial`**](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/estadistica_3_pre_parcial_qa_report_v2.md) | 93 / 2,190 | Flash High ([`aa7e4c75`](conversation://aa7e4c75-9df7-4f93-9733-399354b87d24)) | **16.80** | ACEPTABLE | 8.80 | -3.50 | **5.30** | **`-11.50`** | **29.32** | 🛑 **CRÍTICO (`MASTERY-HOSTILE`)** |
| [**`estadistica_3_pre_parcial_v2`**](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/estadistica_3_pre_parcial_v2_qa_report_v2.md) | 118 / 2,770 | Flash High ([`773b7c54`](conversation://773b7c54-076c-4ac1-84c0-83e3c34f11e2)) | **18.80** | EXCELENTE | 8.40 | -3.50 | **4.90** | **`-13.90`** | **26.58** | 🛑 **CRÍTICO (Mayor Inversión v1→v2)** |

*\*Nota: `estadistica_3_s9_vdirect` y `estadistica_3_s9_vmapreduce` fueron creados el 31-Oct-2026; antes de nuestra actualización del motor, los linters v1 les otorgaban un `risk_score` benigno de apenas `11.29` y `13.70` (frente a `100.0` en v2.0).*

---

## 3. Desglose Dimensional Comparativo (`v1 → v2`) y los 6 Pilares Cognitivos `MPRI`

### 3.1. Desplazamiento por Dimensión Normativa QM-OSCQR (`v1` $\to$ `v2`)

| Curso | D1 Arq/ZPD (`4.0`) | D2 Reactivos (`5.0`) | D3 Andamiaje (`5.0`) | D4 Alineación (`4.0`) | D5 KaTeX/UI (`2.0`) | Pen. Duras | Total `v1 → v2` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`solow_growth_model`** | `4.0 → 3.2` | `4.8 → 4.4` | `5.0 → 4.4` | `4.0 → 4.0` | `2.0 → 2.0` | `0.0 → 0.0` | **`19.8 → 18.0`** |
| **`saul_control_optimo`** | `4.0 → 2.7` | `4.7 → 3.0` | `3.8 → 1.8` | `4.0 → 2.8` | `2.0 → 1.7` | `0.0 → 0.0` | **`18.5 → 12.0`** |
| **`gavilano_pre_parcial`** | `4.0 → 2.5` | `4.8 → 2.6` | `3.7 → 1.2` | `4.0 → 2.3` | `2.0 → 1.2` | `0.0 → -3.5` | **`18.5 → 6.3`** |
| **`saul_pre_parcial`** | `3.8 → 2.4` | `4.5 → 2.5` | `4.0 → 1.2` | `4.0 → 2.5` | `1.7 → 1.1` | `0.0 → -3.5` | **`18.0 → 6.2`** |
| **`estadistica_3_s9_vdirect`** | `— → 2.5` | `— → 1.9` | `— → 1.0` | `— → 2.2` | `— → 0.9` | `— → -2.5` | **`— → 6.0`** |
| **`asyntotic_estatistics_v7`** | `4.0 → 2.5` | `4.4 → 2.2` | `3.5 → 1.0` | `4.0 → 2.3` | `1.9 → 1.1` | `0.0 → -3.5` | **`17.8 → 5.6`** |
| **`estadistica_3_s9_vmapreduce`** | `— → 2.0` | `— → 1.5` | `— → 1.1` | `— → 1.5` | `— → 1.4` | `— → -2.0` | **`— → 5.5`** |
| **`estadistica_3_pre_parcial`** | `4.0 → 2.3` | `3.2 → 2.0` | `3.8 → 1.0` | `4.0 → 2.2` | `1.8 → 1.3` | `0.0 → -3.5` | **`16.8 → 5.3`** |
| **`estadistica_3_pre_parcial_v2`** | `3.5 → 2.2` | `4.8 → 1.8` | `4.8 → 1.2` | `3.9 → 2.1` | `1.8 → 1.1` | `0.0 → -3.5` | **`18.8 → 4.9`** |

### 3.2. Matriz de los 6 Pilares Cognitivos `MPRI` (`/100.0`)

| Curso | P1: ZPD & Bloom (`/20`) | P2: Evocación & Anti-Gaming (`/20`) | P3: Salvavidas Socrático (`/25`) | P4: Diagnóstico `FeedbackToast` (`/15`) | P5: Topología DAG (`/10`) | P6: Ergonomía KaTeX/Dominio (`/10`) | **`MPRI` Total (`/100`)** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`solow_growth_model`** | **13.38** | **20.00** | **25.00** | **11.39** | **10.00** | **10.00** | **`89.77`** |
| **`saul_control_optimo`** | 0.00 | **9.77** | **14.13** | 10.33 | **10.00** | **10.00** | **`54.23`** |
| **`saul_pre_parcial`** | 0.00 | 0.00 | 12.59 | 11.29 | **10.00** | 5.83 | **`39.71`** |
| **`gavilano_pre_parcial`** | 0.00 | 0.00 | 11.32 | 10.58 | **10.00** | 7.64 | **`39.54`** |
| **`estadistica_3_s9_vmapreduce`** | 0.00 | 0.00 | 13.65 | 10.89 | 8.50 | 6.41 | **`39.45`** |
| **`asyntotic_estatistics_v7`** | 0.00 | 0.00 | 13.10 | 9.83 | **10.00** | 5.69 | **`38.62`** |
| **`estadistica_3_s9_vdirect`** | 0.00 | 3.55 | 6.23 | 10.61 | **10.00** | 5.55 | **`35.94`** |
| **`estadistica_3_pre_parcial`** | 0.00 | 0.00 | 10.67 | 5.71 | 5.50 | 7.44 | **`29.32`** |
| **`estadistica_3_pre_parcial_v2`** | 0.00 | 0.00 | 11.05 | 10.24 | **0.00** | 5.29 | **`26.58`** |

---

## 4. Las 6 Causas Raíz Exactas de Por Qué `v1` Fallaba y Qué Mide `v2`

1. **Bug Crítico de Esquema en el Motor v1 (`opt.get("text", "")` vs. `opt["content"]`):**
   Todos los cursos C2C v3 almacenan el texto visible de las alternativas en `opt["content"]`. El motor v1 leía `opt.get("text", "")` (cadena vacía `""` en decenas de miles de opciones), quedando **100% ciego** a:
   - 20 distractores auto-delatores visibles incluso en `solow_growth_model` (`"invirtiendo erróneamente..."`, `"...omitiendo elevar al cuadrado"` en `Hab-05`/`Hab-06`).
   - 16 ítems de *Phantom Keying* en `estadistica_3_pre_parcial` (`Hab-11`, donde v1 solo vio 2).
   - Cientos de opciones con oraciones completas en prosa dentro de `$\text{...}$` (`552` ítems en `pre_parcial_v2`, `220` en `gavilano`, `200` en `pre_parcial`, `165` en `v7`, `160` en `vmapreduce`) que rompen el layout móvil por `white-space: nowrap`.
   - Relleno burocrático artificial `[R-15]` (`", para los parámetros bajo análisis"`, incluyendo muletillas tartamudeadas dobles y gaming de 1-vs-2 muletillas).

2. **Acoplamiento con `calibrateByMasteryDifficulty()` (`sessionShuffler.ts` — Pilar 1 ZPD):**
   v1 jamás verificó la distribución intra-competencia de `difficulty` ni `bloom_taxonomy_level`. En **8 de los 9 cursos activos** (`12,030 / 12,610` preguntas = **`95.4%` del banco total de la plataforma**), `compile_shard.py` fijó `difficulty = "medium"` y `bloom = "Understand"` en el 100% de los ítems, dejando **inoperante** la progresión adaptativa ZPD entre `Attempted (25)` $\to$ `Familiar (50)` $\to$ `Proficient (80)` $\to$ `Mastered (100)`. Incluso en `solow_growth_model`, v2 detectó que 7 de sus 25 competencias son mono-banda (`medium`).

3. **Evocación Activa vs. Reconocimiento Pasivo (`mathEquivalence.ts` — Pilar 2 Modalidad):**
   Solo `solow_growth_model` (`86.21%` FIB + MS: `251` FIB y `249` MS) exige producción simbólica/numérica activa. Los otros **8 cursos activos (`12,030` preguntas)** exhiben **100% de monocultivo `multiple_choice_7_options` (`0` FIB, `0` MS)**, permitiendo resolver competencias `[Skill]` por sustitución inversa desde las opciones.

4. **Envenenamiento Anti-Socrático del Salvavidas de 3-Strikes (`PracticeSession.tsx` — Pilar 3):**
   v1 solo comprobaba `len(hints) >= 3` (`4.8/5.0` en `pre_parcial_v2`). v2 inspecciona la semántica de `hints[1..2]` frente al bloqueo de 3 intentos de `PracticeSession.tsx`, destapando que `compile_shard.py` inyecta `"asegurando considerar adecuadamente: [distractor / error conceptual]"` en miles de reactivos (`529` en `pre_parcial_v2`, `513` en `pre_parcial`, `495` en `gavilano`, `280` regex / `620` simbólicos en `vdirect`, `142` en `saul_pre_parcial`, `60` en `v7`), saboteando activamente al estudiante que pide ayuda.

5. **Exploit de Memorización Visual de Clave Invariante (`answer_memorization_exploit` — Pilar 2):**
   Cuando un autor instancia variables dummy (`@n@`) solo en el `stem` dejando las opciones estáticas, las 20–30 preguntas de una competencia comparten exactamente **1 sola respuesta correcta idéntica** (`14` competencias en `pre_parcial_v2`, `9` en `pre_parcial`, `6` en `gavilano`, `4` en `saul_pre_parcial`, `4` en `v7`, `2` en `vdirect`, `1` en `vmapreduce`). Un alumno alcanza `Mastered (100)` en segundos por reconocimiento visual sin leer los enunciados.

6. **Auditoría Topológica de Grafos Multicapa y Puerta Stage-5 (`dag_mastery_topology_linter` & `stage5_judge_audit`):**
   - **El Caso `estadistica_3_pre_parcial_v2` (`18.8 → 4.9`, `Δ = -13.90`):** v1 elogió 34 nodos sin prerrequisitos como *"nodos raíz fundacionales"*; v2 demostró que `11` son islas desconectadas (`in=0, out=0`) producto de concatenar capítulos sin reconciliar aristas (`0.0/10` en topología DAG), rompiendo el *interleaving* 60/40 de Quizzes y 55/45 de Unit Tests.
   - **Auditoría de Discordancias Stage-5 (`judge_report.json`):** Al cruzar desacuerdos no reparados del Juez Ciego (que pasaban porque el umbral macro era `>= 95%`), v2 destapó claves matemáticamente corruptas en producción: cuantificadores universales vacuos en `vmapreduce` (`C-02`, `T-C-02-02_judge_1`), ecuaciones mal despejadas en `gavilano_pre_parcial` (`10 + 47*38 = 1887` falso en `T-Hab-25-02_judge_1`), varianza asintótica vs. finita en `v7` (`T-Hab-04-01_judge_1`), y 2 plantillas discordantes en `pre_parcial_v2`.

---

## 5. Índice Directo de Artefactos Individuales v1 vs. v2

| Curso | Reporte Histórico v1 (Archivado) | Reporte Forense v2 (Path-to-Mastery) | JSON Estructurado v2 |
| :--- | :--- | :--- | :--- |
| **`solow_growth_model`** | [v1 MD](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v1_baseline_archive/solow_growth_model_qa_report.md) | [v2 MD](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/solow_growth_model_qa_report_v2.md) | [v2 JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/solow_growth_model_qa_report_v2.json) |
| **`saul_control_optimo`** | [v1 MD](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v1_baseline_archive/saul_control_optimo_qa_report.md) | [v2 MD](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/saul_control_optimo_qa_report_v2.md) | [v2 JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/saul_control_optimo_qa_report_v2.json) |
| **`gavilano_pre_parcial`** | [v1 MD](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v1_baseline_archive/gavilano_pre_parcial_qa_report.md) | [v2 MD](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/gavilano_pre_parcial_qa_report_v2.md) | [v2 JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/gavilano_pre_parcial_qa_report_v2.json) |
| **`saul_pre_parcial`** | [v1 MD](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v1_baseline_archive/saul_pre_parcial_qa_report.md) | [v2 MD](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/saul_pre_parcial_qa_report_v2.md) | [v2 JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/saul_pre_parcial_qa_report_v2.json) |
| **`asyntotic_estatistics_v7`** | [v1 MD](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v1_baseline_archive/asyntotic_estatistics_v7_qa_report.md) | [v2 MD](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/asyntotic_estatistics_v7_qa_report_v2.md) | [v2 JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/asyntotic_estatistics_v7_qa_report_v2.json) |
| **`estadistica_3_pre_parcial`** | [v1 MD](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v1_baseline_archive/estadistica_3_pre_parcial_qa_report.md) | [v2 MD](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/estadistica_3_pre_parcial_qa_report_v2.md) | [v2 JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/estadistica_3_pre_parcial_qa_report_v2.json) |
| **`estadistica_3_pre_parcial_v2`** | [v1 MD](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v1_baseline_archive/estadistica_3_pre_parcial_v2_qa_report.md) | [v2 MD](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/estadistica_3_pre_parcial_v2_qa_report_v2.md) | [v2 JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/v2_path_to_mastery/estadistica_3_pre_parcial_v2_qa_report_v2.json) |
| **`estadistica_3_s9_vdirect`** | *Curso Nuevo (31-Oct)* | [v2 MD (Argon)](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/estadistica_3_s9_vdirect_qa_report.md) | [v2 JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/estadistica_3_s9_vdirect_qa_report.json) |
| **`estadistica_3_s9_vmapreduce`** | *Curso Nuevo (31-Oct)* | [v2 MD (Argon)](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/estadistica_3_s9_vmapreduce_qa_report.md) | [v2 JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/estadistica_3_s9_vmapreduce_qa_report.json) |
