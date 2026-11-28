# Auditoría Técnica, Psicométrica y Pedagógica (Re-Auditoría Exhaustiva) — `solow_test_k3`

> [!WARNING]
> **CURSO RETIRADO DE LA PLATAFORMA**: Este curso fue eliminado de la plataforma interactiva el **2026-11-28 05:27:42**. Este informe de auditoría se conserva exclusivamente como registro histórico y pedagógico ('legacy').

**Estado en Plataforma:** ELIMINADO  
**Fecha de Eliminación:** 2026-11-28 05:27:42  
**Curso:** Solow Test K3 (`solow_test_k3`)  
**Archivo fuente:** `courses/solow_test_k3.json`  
**Estándar:** Quality Matters (QM) · OSCQR · Bloom's 2-Sigma Mastery Learning · ZPD · Path-to-Mastery v2.0  
**Fecha de auditoría:** 2026-11-27  
**Archivo histórico previo:** `reports/audits_archive/solow_test_k3/solow_test_k3_qa_report_20261127_032118.md`

---

## 1. Resumen Ejecutivo

| Métrica Global | Valor | Estado / Tier |
| :--- | :---: | :--- |
| **Calificación Final QM-OSCQR** | **16.9 / 20.0** | **ACEPTABLE (14.0 - 16.9 pts)** — Requiere pulido antes de certificación Platinum |
| **Mastery Path Readiness Index (MPRI)** | **86.0 / 100.0** | **GOLD MASTERY PATH (85-100)** (en límite inferior; brechas de andamiaje y ergonomía) |
| **Penalizaciones Duras (Hard Deductions)** | **0.0** | Ninguna regla dura automática activada |
| **Competencias / Reactivos** | **21 / 648** | 2 Hechos (`H`), 10 Conceptos (`C`), 9 Habilidades (`Hab`) |
| **Stage-5 Blind Judge Audit** | **100.0%** | 145/145 ítems acordados (`0` desacuerdos sin reparar) |
| **Índice Bloom Ponderado vs. Piso Adaptativo** | **4.01 / 3.83** | Reportado `ÉLITE` por linter, pero **inflado por Goodharting** en 92 ítems (`FIB`/`MS`) |

> [!WARNING]
> **Discrepancia entre Linter Determinista (`risk_score = 0.0`, `20.0/20.0`) y Auditoría Semántica Directa:**  
> La inspección directa de los 648 reactivos en `courses/solow_test_k3.json` reveló **5 familias de defectos reales** invisibles al linter determinista: (1) errores matemáticos de signo en pistas de `Hab-04` (`Q-Hab04-306`..`309`), (2) Goodharting/inflación de Bloom en `92` ítems (`30` `fill_in_the_blank` en `Analyze` y `62` `multiple_select` en `Evaluate`) más descalibración `hard` en `C-05`, (3) `6` tautologías `$n=n$` en distractores de `C-04`, (4) enunciados con números desnudos sin variable (`C-11`, `C-05`) e identificador crudo `$s_{pct}$` (`C-11`), y (5) `109` ítems con doble punto `..` en `error_rationale`.

---

## 2. Evaluación por Dimensiones (Rúbrica QM-OSCQR — 20.0 pts)

| Dimensión | Puntaje | Máximo | Diagnóstico Determinista + Hallazgos Semánticos Verbatim |
| :--- | :---: | :---: | :--- |
| **D1. Arquitectura Curricular, Topología DAG y ZPD** | **3.8** | 4.0 | DAG acíclico y conexo de 21 competencias (`has_cycle=false`, `max_dag_depth=5`, `connected_components=1`). Sin embargo, la banda `hard` de `C-05` (`Q-C05-259`, `Q-C05-260`, `Q-C05-261`) presenta ejercicios triviales de división algebraica (`-0.2 pts`). |
| **D2. Calidad Psicométrica, Modalidad y Anti-Gaming** | **4.3** | 5.0 | Cobertura 100.0% de evocación activa/discriminación (`MC7=0.0%`, `FIB=13.89%`, `MS=20.37%`, `BloomSup=65.74%`), pero se detectan: **6 tautologías `$x=x$`** en distractores de `C-04` (`-0.3 pts`), **sesgo de longitud MS** en `C-03` (`Q-C03-202`..`204`, `2.27%`, `-0.2 pts`) y **109 ítems** con residuo tipográfico `..` en `error_rationale` de `unstructured_model` (`-0.2 pts`). |
| **D3. Andamiaje Socrático y Remediación Diagnóstica** | **4.2** | 5.0 | Aunque el linter reporta `100.0%` de pistas genuinas, la auditoría directa halló **4 ítems `hard` de `Hab-04` (`Q-Hab04-306` a `Q-Hab04-309`) con una fórmula de derivación matemáticamente falsa** en la Pista 1 (signo invertido en el exponente y `?` final), saboteando al estudiante en el flujo *3-Strikes* (`-0.8 pts`). |
| **D4. Alineación Instruccional, Bloom y ZPD** | **3.0** | 4.0 | `bloom_weighted_index` = `4.01 / 5.0` vs. `adaptive_bloom_floor` = `3.83 / 5.0` (`skill_higher_bloom_pct = 100.0%`). No obstante, existe **Goodharting de Bloom en 92 ítems (`14.20%`)**: 30 `fill_in_the_blank` etiquetados como `Analyze`, 62 `multiple_select` como `Evaluate`, y álgebra elemental en `C-05` etiquetada como `Evaluate` (`-0.6 pts`). Además, hay **enunciados confusos** con números desnudos en `C-11` (`6` ítems) y `C-05` (`2` ítems) (`-0.4 pts`). |
| **D5. Ergonomía Cognitiva en UI y Sintaxis KaTeX** | **1.6** | 2.0 | Sintaxis KaTeX estructuralmente válida (`0` llaves abiertas, `0` `$$$`), pero se detectan **identificadores crudos de código `$s_{pct}$` / `s_pct`** en `Q-C11-637`..`639` (`-0.25 pts`) y **fracciones no simplificadas `/1`** en formas canónicas de `Hab-06` y `Hab-07` (`-0.15 pts`). |
| **Subtotal Bruto / Penalizaciones / Nota Final** | **16.9** | **20.0** | Subtotal: **16.9** · Penalizaciones Duras: **0.0** · Nota Final: **16.9 / 20.0** |

---

## 3. Mastery Path Readiness Index (`MPRI`: 86.0 / 100.0)

| Pilar Cognitivo y de Plataforma | Puntaje | Máximo | Diagnóstico Riguroso |
| :--- | :---: | :---: | :--- |
| **1. Progresión Adaptativa ZPD y Bloom (`zpd_adaptive_progression`)** | **16.0** | 20.0 | `bloom_weighted_index` = `4.01` vs. `adaptive_bloom_floor` = `3.83`, pero inflado por **92 ítems `FIB`/`MS`** sobre-etiquetados (`Analyze`/`Evaluate`) y banda `hard` trivial en `C-05`. |
| **2. Modalidad de Evocación y Anti-Gaming (`retrieval_modality_and_anti_gaming`)** | **17.5** | 20.0 | 100.0% evocación activa/discriminación (`MC7=0.0%`), descontado por **6 tautologías `$x=x$`** en `C-04` y sesgo de longitud MS (`2.27%`) en `C-03`. |
| **3. Línea de Vida Socrática (`socratic_scaffolding_lifeline`)** | **21.5** | 25.0 | Pistas generalmente específicas, pero **4 ítems de `Hab-04` (`306`–`309`) contienen error matemático de cálculo** en `hints[0]` que induce a error en *3-Strikes*. |
| **4. Alineación Diagnóstica (`diagnostic_remediation_alignment`)** | **13.5** | 15.0 | 100.0% cobertura de `error_rationale` (528/528), pero **109 ítems** presentan residuo `..` y concordancia gramatical rota en rationales autogenerados de `unstructured_model`. |
| **5. Topología DAG e Interleaving (`dag_and_interleaving_topology`)** | **10.0** | 10.0 | DAG acíclico (`has_cycle=false`), 1 componente conexo, profundidad 5, 0 aristas invertidas. |
| **6. Ergonomía Cognitiva y Framing (`cognitive_ergonomics_and_framing`)** | **7.5** | 10.0 | Penalizado por variable cruda `$s_{pct}$` (`Q-C11-637`..`639`), números desnudos sin etiqueta (`C-11`, `C-05`) y coeficientes `/1` (`Hab-06`, `Hab-07`). |

---

## 4. Hallazgos Verbatim de la Auditoría Semántica Directa (`courses/solow_test_k3.json`)

### 4.1 Error Matemático en Pistas Socráticas (`Hab-04` — Severidad Alta)
En **4 ítems `hard` (`Q-Hab04-306`, `Q-Hab04-307`, `Q-Hab04-308`, `Q-Hab04-309`)**, la `detailed_solution` y la `correct_answer` son correctas, pero la **Pista 1 (`hints[0]`) tiene un error de signo en la derivada de la potencia** más un signo `?` suelto:
- `Q-Hab04-306` / `Q-Hab04-307`:
  > `"Aplique el cambio de variable $z=K^{0.5}$ con $\\dot{z}=0.5K^{0.5}\\dot{K}$?"`  
  *(Error: si $z=K^{0.5}$, entonces $\dot{z}=0.5K^{-0.5}\dot{K}$, no $0.5K^{0.5}\dot{K}$.)*
- `Q-Hab04-308` / `Q-Hab04-309`:
  > `"Aplique el cambio de variable $z=K^{0.3333}$ con $\\dot{z}=0.3333K^{0.6667}\\dot{K}$?"`  
  *(Error: si $z=K^{0.3333}$, entonces $\dot{z}=0.3333K^{-0.6667}\dot{K}$, no $0.3333K^{0.6667}\dot{K}$.)*

### 4.2 Goodharting / Inflación de Taxonomía de Bloom y Descalibración ZPD (`95` ítems)
- **`30/90` `fill_in_the_blank` etiquetados como `Analyze`**:
  - `Q-H02-007` (`hard`, `Analyze`): *"Si la fuerza laboral inicial es $L_0=190$ y crece exponencialmente a una tasa relativa constante $n=0.04$, calcule $L(20)$ en $t=20$ (redondee a 4 decimales):"* $\to$ Sustitución directa en $L_0 e^{nt}$ (`Apply`, no `Analyze`).
  - `Q-H01-034` (`hard`, `Analyze`): *"Evalúe la variación absoluta $\dot{L}$ tras un aumento $\Delta\lambda=0.03$ sobre la tasa base $\lambda_0=0.02$ cuando $L=65$."* $\to$ Producto aritmético $(0.02+0.03)\cdot 65 = 3.25$ (`Apply`, no `Analyze`).
- **`62/132` `multiple_select` etiquetados como `Evaluate`**: Ej. `Q-H02-016`, `Q-H02-017`, `Q-H02-018`, `Q-H01-043`, `Q-H01-044` evalúan reconocimiento/discriminación de ecuaciones (`Understand`/`Analyze`), no juicio crítico de nivel `Evaluate`.
- **Descalibración `hard` + `Evaluate` en `C-05` (`Q-C05-259`, `Q-C05-260`, `Q-C05-261`)**:
  - `Q-C05-259` (`hard`, `Evaluate`): *"Si $sF(r,1)=4r+5$ y $nr=2r$, exprese en función de $r$ la tasa de crecimiento del capital $\dot{K}/K=sF(r,1)/r$:"* $\to$ Clave: `4+5/r`. Es álgebra elemental de 1 paso (`Apply` / `easy`).

### 4.3 Tautologías Numéricas en Distractores (`C-04` — `6` ítems)
En `Q-C04-208` a `Q-C04-213` (`adversarial_break`), la interpolación de plantilla reemplazó `n=n` por `$valor=valor$`:
- `Q-C04-208` (`R2`): *"El equilibrio $5$ es inestable porque `$0.05=0.05$` supera al ahorro $0.25$ en todo el dominio."*
- `Q-C04-209` (`R3`): *"El equilibrio $4$ es inestable porque `$0.06=0.06$` supera al ahorro $0.3$ en todo el dominio."*
- También presente en `Q-C04-210` (`$0.04=0.04$`), `Q-C04-211` (`$0.11=0.11$`), `Q-C04-212` (`$0.09=0.09$`) y `Q-C04-213` (`$0.05=0.05$`).

### 4.4 Enunciados Confusos, Números Desnudos e Identificadores Crudos (`C-11`, `C-05`)
- **Números desnudos sin variable en `C-11` (`6` ítems: `Q-C11-627`, `628`, `630`, `635`, `638`, etc.)**:
  - `Q-C11-628`: *"Analice cómo cambia el empleo al pasar el ahorro de $10\%$ a $15\%$ ($\Delta s=5\%$) con $\bar{r}=10$, $F(\bar{r},1)=3$, $n=4\%$ y $4$:"* (el `$4$` final corresponde al nivel de precios $p=4$, pero no se nombra).
- **Identificador crudo de código `$s_{pct}$` (`3` ítems: `Q-C11-637`, `Q-C11-638`, `Q-C11-639`)**:
  - `Q-C11-638`: *"Construya un contraejemplo numérico de `$s_{pct}$` para refutar la tesis de desempleo universal bajo $\bar{r}=4$, $F(\bar{r},1)=3$, $n=3\%$ y $2$:"* (`sample_witness: {'s_pct': 6}`).
- **Frases de plantilla artificiales y tasas irreales en `C-05`**:
  - `Q-C05-235`: *"Dada la dinámica con $sF(r,1)=3r<5r$ y constante auxiliar $5$, señale el paso que introduce la falacia:"* (tasa poblacional $n=5$, i.e. 500%, y mención opaca a "constante auxiliar $5$").
  - `Q-C05-236`: *"...cuando $sF(r,1)=1r$, $nr=8r$ ($1<8$) y $2$ es positivo..."* (tasa $n=8$ y constante `$2$` sin rol explícito).

### 4.5 Residuos Tipográficos y Sesgo MS (`109` + `3` ítems)
- **`109` ítems con doble punto `..` en `error_rationale`** (ej. `Q-C08-397`: *"Verifica la validez analítica del supuesto Homogeneidad de grado uno en $F(\lambda K, \lambda L) = \lambda F(K, L)$ e isocuantas convexas.. "*).
- **`3` ítems `multiple_select` en `C-03` con sesgo de longitud (`2.27%`)**: `Q-C03-202`, `Q-C03-203`, `Q-C03-204`.
- **Fracciones `/1` sin simplificar en `Hab-06`/`Hab-07`**: `(1/9)*(s/n)**(8/1)` en `Q-Hab06-424` y `n+(6/1)*g` en `Q-Hab07-460`.

---

## 5. Acciones Prioritarias de Remediación

1. **[CRÍTICO — D3] Corregir la regla de la cadena en `hints[0]` de `Q-Hab04-306` a `Q-Hab04-309`**: Cambiar `K^{0.5}` por `K^{-0.5}` (y `K^{0.6667}` por `K^{-0.6667}`) y eliminar el `?` final.
2. **[ALTO — D4/D1] Re-calibrar etiquetas de Bloom y dificultad `hard`**: Degradar los `30` `FIB` en `Analyze` a `Apply`, revisar los `62` `MS` en `Evaluate` y reemplazar `Q-C05-259..261` por problemas genuinamente `hard`/`Evaluate`.
3. **[MEDIO — D4/D5] Corregir enunciados de `C-11` y `C-05`**: Explicitar `"nivel de precios $p=..."` en los 6 ítems con número desnudo de `C-11`, reemplazar `$s_{pct}$` por `$s$` (en `%`) en `Q-C11-637..639` y limpiar las constantes auxiliares opacas en `C-05`.
4. **[MEDIO — D2] Corregir las `6` tautologías `$n=n$` en `C-04` (`Q-C04-208`..`213`)** y balancear longitudes en `Q-C03-202`..`204`.
5. **[BAJO — D2/D5] Limpiar los `109` residuos `..` en `error_rationale`** de `unstructured_model` y simplificar `/1` en `Hab-06`/`Hab-07`.

---

<details>
<summary>Metadatos Estructurados (JSON)</summary>

```json
{
  "course_metadata": {
    "course_id": "solow_test_k3",
    "unit_title": "Solow Test K3",
    "detected_objective": "Dominio y aplicación analítica integral del modelo de crecimiento neoclásico de Solow, sus extensiones y rigideces nominales.",
    "total_competencies": 21,
    "total_questions": 648,
    "bloom_index": {
      "weighted_index": 4.01,
      "adaptive_floor": 3.83,
      "gap": 0.0,
      "apply_plus_pct": 91.2,
      "superior_pct": 72.22,
      "tier": "ÉLITE (inflado por Goodharting en 92 ítems FIB/MS)",
      "coherence_violations_count": 0
    }
  },
  "dimension_scores": {
    "architecture_granularity": {
      "score": 3.8,
      "max": 4.0,
      "feedback": "DAG acíclico y conexo de 21 competencias con 3 bandas ZPD; descontado -0.2 por banda 'hard' trivial en C-05 (Q-C05-259..261)."
    },
    "assessment_quality": {
      "score": 4.3,
      "max": 5.0,
      "feedback": "100.0% evocación activa/discriminación; descontado -0.3 por 6 tautologías '$x=x$' en C-04 (Q-C04-208..213), -0.2 por sesgo MS en C-03 (2.27%) y -0.2 por 109 residuos '..' en error_rationale."
    },
    "scaffolding_hints": {
      "score": 4.2,
      "max": 5.0,
      "feedback": "Pistas generalmente específicas, pero 4 ítems hard de Hab-04 (Q-Hab04-306..309) contienen una derivada falsa en hints[0] (signo invertido en exponente y '?' final), saboteando el flujo 3-Strikes (-0.8 pts)."
    },
    "instructional_alignment": {
      "score": 3.0,
      "max": 4.0,
      "feedback": "bloom_weighted_index=4.01 vs adaptive_bloom_floor=3.83, pero con Goodharting en 92 ítems (30 FIB en Analyze, 62 MS en Evaluate) y álgebra trivial en C-05 como Evaluate (-0.6 pts), más 8 enunciados confusos con números desnudos en C-11/C-05 (-0.4 pts)."
    },
    "technical_ergonomics": {
      "score": 1.6,
      "max": 2.0,
      "feedback": "KaTeX estructuralmente válido, descontado -0.25 por variable cruda $s_{pct}$ en Q-C11-637..639 y -0.15 por fracciones '/1' sin simplificar en Hab-06 y Hab-07."
    }
  },
  "penalties_applied": [],
  "raw_subtotal": 16.9,
  "final_score": 16.9,
  "quality_tier": "ACEPTABLE (14-16.9)",
  "mastery_path_readiness": {
    "mpri_score": 86.0,
    "mpri_max": 100.0,
    "mpri_tier": "GOLD MASTERY PATH (85-100): Certificado con reservas; requiere pulido",
    "pillars": {
      "zpd_adaptive_progression": { "score": 16.0, "max": 20.0 },
      "retrieval_modality_and_anti_gaming": { "score": 17.5, "max": 20.0 },
      "socratic_scaffolding_lifeline": { "score": 21.5, "max": 25.0 },
      "diagnostic_remediation_alignment": { "score": 13.5, "max": 15.0 },
      "dag_and_interleaving_topology": { "score": 10.0, "max": 10.0 },
      "cognitive_ergonomics_and_framing": { "score": 7.5, "max": 10.0 }
    },
    "student_journey_verdict": "Base matemática sólida pero con brechas de calibración adaptativa, Goodharting de Bloom en FIB/MS, 4 pistas con cálculo erróneo en Hab-04 y fricción ergonómica en C-11/C-04 que requieren corrección antes de certificación Platinum."
  },
  "discovered_lint_rules": [
    {
      "rule_id": "HINT_CHAIN_RULE_POSITIVE_EXPONENT_BUG",
      "severity": "critical",
      "regex_pattern": "\\\\dot\\{z\\}=0\\.\\d+K\\^\\{0\\.\\d+\\}\\\\dot\\{K\\}",
      "description": "Error de signo en la regla de la cadena dentro de pistas de linealización (ej. z=K^{0.5} -> dz/dt=0.5 K^{0.5} dK/dt en vez de K^{-0.5}).",
      "evidence_items": ["Q-Hab04-306", "Q-Hab04-307", "Q-Hab04-308", "Q-Hab04-309"]
    },
    {
      "rule_id": "BLOOM_MODALITY_GOODHARTING",
      "severity": "warning",
      "regex_pattern": "(fill_in_the_blank.*Analyze|multiple_select.*Evaluate)",
      "description": "Sobre-etiquetado de taxonomía de Bloom (FIB de cálculo directo en Analyze y MS de discriminación en Evaluate) para inflar bloom_weighted_index.",
      "evidence_items": ["Q-H02-007", "Q-H01-034", "Q-H02-016", "Q-C05-259"]
    },
    {
      "rule_id": "NUMERIC_SELF_EQUALITY_TAUTOLOGY",
      "severity": "warning",
      "regex_pattern": "\\$(\\d+(?:\\.\\d+)?)=\\1\\$",
      "description": "Igualdad numérica tautológica en distractor generada al interpolar el mismo parámetro a ambos lados del '=' (ej. '$0.05=0.05$').",
      "evidence_items": ["Q-C04-208", "Q-C04-209", "Q-C04-210", "Q-C04-211", "Q-C04-212", "Q-C04-213"]
    },
    {
      "rule_id": "RAW_CODE_VAR_SUBSCRIPT_PCT",
      "severity": "warning",
      "regex_pattern": "s_\\{?pct\\}?",
      "description": "Exposición de identificador interno de variable Python/JSON ('s_pct' / '$s_{pct}$') en enunciados y soluciones.",
      "evidence_items": ["Q-C11-637", "Q-C11-638", "Q-C11-639"]
    },
    {
      "rule_id": "BARE_UNLABELLED_PRICE_IN_STEM",
      "severity": "warning",
      "regex_pattern": "n=\\d+\\\\%\\s+y\\s+\\$\\d+\\$:",
      "description": "Número desnudo al final del enunciado sin nombrar la variable económica que representa (nivel de precios p).",
      "evidence_items": ["Q-C11-627", "Q-C11-628", "Q-C11-630", "Q-C11-635", "Q-C11-638"]
    },
    {
      "rule_id": "DOUBLE_PERIOD_TEMPLATE_RESIDUE",
      "severity": "info",
      "regex_pattern": "\\.\\.",
      "description": "Doble punto final en 'error_rationale' autogenerado de 'unstructured_model' (109 ítems afectados).",
      "evidence_items": ["Q-C08-397", "Q-C08-398", "Q-C10-595", "Q-C11-622"]
    }
  ],
  "remediation_actions": [
    "Corregir la derivada en hints[0] de Q-Hab04-306..309 (exponente negativo K^{-0.5} / K^{-0.6667} y quitar '?').",
    "Re-calibrar etiquetas Bloom en los 30 FIB (Analyze->Apply) y 62 MS (Evaluate->Understand/Analyze) y elevar dificultad real de Q-C05-259..261.",
    "Explicitar 'nivel de precios p=...' en los 6 ítems de C-11 con número desnudo y reemplazar '$s_{pct}$' por '$s$' en Q-C11-637..639.",
    "Corregir las 6 tautologías '$x=x$' en Q-C04-208..213 y balancear longitud en Q-C03-202..204.",
    "Limpiar los 109 residuos '..' en error_rationale de unstructured_model y simplificar '/1' en Hab-06/Hab-07."
  ]
}
```

</details>
