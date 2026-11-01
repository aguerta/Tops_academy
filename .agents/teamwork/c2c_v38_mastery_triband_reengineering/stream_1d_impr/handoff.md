# Handoff Report — Stream 1D (Fase 2: Mejorador)
**Subagent:** `c2c38_improver` (Phase 2 Flash Triad)  
**Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`  
**Stream:** Stream 1D — Engine Invariants, Template Safeguards & KaTeX Hardening  
**Target:** `c2c_v38_mastery_triband_reengineering`  
**Status:** COMPLETE (100% Passed)

---

## 1. Executive Summary

La Fase 2 (Mejorador) de Stream 1D ha completado la auditoría exhaustiva, endurecimiento de casos borde y verificación de contratos sobre la implementación de la Fase 1. Todos los objetivos descritos en `stream_1d_impr/DISPATCH.md` han sido implementados, probados y blindados con 202 pruebas pasando limpiamente (0 errores, 0 fallos).

### Endurecimientos Realizados:

1. **`[TPL-STATIC-OPT]` (Unconditional Mono-Key Blocking & Edge Cases):**
   - Verificado y endurecido el caso adversario donde `vars == {}` / `domain == {}` está vacío y `N >= 2` semillas producen `len(unique_correct) == 1`:
     * Bloqueo garantizado con `[TPL-STATIC-OPT]` bajo `strict=True` para los 3 tipos de reactivos: `multiple_choice_7_options`, `fill_in_the_blank` y `multiple_select`.
     * En `multiple_select`, la respuesta correcta se evalúa como `frozenset` de tuplas `(content, is_correct)` para ser matemáticamente inmune al ordenamiento aleatorio de opciones por semilla.
     * Añadidos tests unitarios explícitos en `tests/test_template_variability.py::test_tpl_static_opt_empty_vars_mono_key_fib_and_ms`.

2. **Multimodal `TPL-D3` Distractor Coverage:**
   - Validado exhaustivamente el comportamiento para competencias multimodales:
     * `100% FIB`: Pasa limpiamente sin requerir distractores de `cta.json` y sin falsos bloqueos.
     * `FIB + MS`: Requiere `>= 2` IDs de distractores válidos declarados en `cta.json` referenciados en las plantillas `multiple_select`.
     * Presencia de `>= 1` plantilla `MC7`: Exige cobertura total `6/6` de los distractores de `cta.json`.
     * En `engine/assemble.py`, se implementó fallback automático en `multiple_select` para asignar distractor IDs de `template["distractor_ids"]` a las opciones con `is_correct=False` si el autor omitió `distractor_id` individual en la opción.
     * Cobertura verificada en `tests/test_template_variability.py::test_multimodal_tpl_d3_coverage`.

3. **`[TPL-DYNAMIC-RATIONALE]` Hardening:**
   - En `check_single_template` (`strict=True`, `seeds >= 15`):
     * Bloqueo por slot individual si un distractor en MC7 o MS varía en contenido (`len(u_contents) > 1`) pero su `error_rationale` permanece estático (`len(u_rats) == 1`).
     * Comprobado que distractores puramente conceptuales e invariantes en plantillas conceptuales de rotación (`len(u_contents) == 1`) no generen falsos positivos en la comprobación de slot.
   - En `check_competency_diversity`:
     * Soporte para inyección directa de `questions` en `check_competency_diversity(..., questions=...)` garantizando cálculo inmediato de cuota `target_quota = len(questions)`.
     * Bloqueo a nivel de competencia si `rationale_uniqueness_pct < 35.0%` en bancos con `>= 30` distractores.
     * Tests verificados en `tests/test_template_variability.py::test_tpl_dynamic_rationale_ms_slot_variation_enforced` y `test_tpl_dynamic_rationale_competency_pool_uniqueness_and_conceptual_invariant`.

4. **KaTeX Prose Overflow (`[KATEX-PROSE-OVERFLOW]`) & `[R-18]`:**
   - Frontera exacta verificada: macros de texto (`\text`, `\textrm`, `\mathrm`) con exactamente 45 caracteres pasan sin errores; con 46 caracteres fallan inequívocamente con `[KATEX-PROSE-OVERFLOW]` y NUNCA emiten la regla deprecada `R-23`.
   - Soporte para llaves anidadas (ej. `\text{valor de $x_{i}$ en el sistema}`) en `validate_katex_syntax`.
   - Desenvoltura completa de `\mathrm{...}` añadida en `_unwrap_text_in_math` (`invariants.py`), garantizando que distractores envueltos en math mode no evadan la detección de esqueletos formulaicos `[R-18]`.
   - Tests verificados en `tests/test_assemble_katex_and_rationale.py::test_katex_prose_overflow_exact_45_boundary_and_nested_braces` y `test_r18_unwrapping_with_nested_braces_and_mathrm`.

5. **PrairieLearn Token Interoperability & Single-Letter LaTeX Shielding (`assemble.py`):**
   - Verificada la interpolación simultánea de `@n@`, `@k@`, `@c@` junto con la preservación intacta de `${k}^*$` y `$\mathbb{R}^{n}$` tanto bajo `is_cta=True` como bajo `is_cta=False`.
   - Enriquecida la protección en `format_template_string` para reconocer macrobases de conjuntos matemáticos (`\mathbb{R}^{n}`).
   - Test verificado en `tests/test_katex_prairielearn_tokens.py::test_simultaneous_pl_tokens_and_latex_math_preservation`.

6. **Hardening de Plantillas de Ejemplo (`examples/{edo,edp}/templates/*.json`):**
   - `C-02.json`: Corregido balance de longitud R-15 en `T-C02-01` (~115 chars para igualar la media de distractores); eliminadas llaves dobles residuales `{{A}}` y `{{tr}}` (R-20); agregadas 3 `stem_variants` por plantilla.
   - `Hab-02.json`: Agregadas 3 `stem_variants` por plantilla; eliminadas llaves dobles residuales `\dot{{x}}`, `\dot{{y}}`, `\mathrm{{tr}}`, `\mathbf{{J}}`, `\begin{{bmatrix}}` (R-20).
   - `C-01.json`: Agregadas 3 `stem_variants` a `T-C01-01` y `T-C01-02`.
   - `Hab-01.json`: Agregadas 3 `stem_variants` a todas las plantillas; reemplazado `\frac{{dx}}{{{a}x}}` por `\frac{dx}{@a@ x}` eliminando R-20; ampliado `mult = rng.randint(1, 15)` en `T-Hab01-02` satisfaciendo la cuota de `>= 7` claves únicas en 15 semillas.
   - Verificado con test automatizado `test_examples_templates_strict_validation` en `strict=True` confirmando 0 errores.

7. **Zero-Domain Compliance:**
   - 100% verificado vía `test_engine_zero_domain_logic`. Cero subcadenas prohibidas (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`) en todos los archivos `.py` de producción bajo `.agents/skills/content-to-course/`.

---

## 2. Modificaciones por Archivo

| Archivo | Intervención |
|---|---|
| `.agents/skills/content-to-course/engine/invariants.py` | En `_unwrap_text_in_math`: agregado soporte para `\mathrm{...}` y protección `m.start() < last_idx`. |
| `.agents/skills/content-to-course/engine/assemble.py` | En `format_template_string`: protección de exponentes de macros de símbolos (`\mathbb{R}^{n}`). En `assemble_question` (MS): fallback ordenado a `template["distractor_ids"]` para opciones erróneas sin ID explícito. |
| `.agents/skills/content-to-course/check_templates.py` | En `check_competency_diversity`: soporte para argumento `questions: Optional[List[Dict[str, Any]]] = None`, asignación de `target_quota = len(questions)`. |
| `examples/edo/templates/C-02.json` | Calibración de longitud anti-giveaway R-15; corrección de `{{A}}`, `{{tr}}` a `{A}`, `{tr}`; 3 `stem_variants` en cada plantilla. |
| `examples/edo/templates/Hab-02.json` | Eliminación de llaves dobles residuales R-20 (`\dot{{x}}`, `\dot{{y}}`, `\mathbf{{J}}`, `\begin{{bmatrix}}`); 3 `stem_variants` en cada plantilla. |
| `examples/edp/templates/C-01.json` | 3 `stem_variants` en `T-C01-01` y `T-C01-02`. |
| `examples/edp/templates/Hab-01.json` | Reemplazo de `\frac{{dx}}{{{a}x}}` por `\frac{dx}{@a@ x}` (R-20); ampliado `mult = rng.randint(1, 15)` en `T-Hab01-02`; 3 `stem_variants` por plantilla. |
| `tests/test_assemble_katex_and_rationale.py` | Añadidos tests `test_katex_prose_overflow_exact_45_boundary_and_nested_braces` y `test_r18_unwrapping_with_nested_braces_and_mathrm`. |
| `tests/test_katex_prairielearn_tokens.py` | Añadido test `test_simultaneous_pl_tokens_and_latex_math_preservation`. |
| `tests/test_template_variability.py` | Añadidos tests `test_tpl_static_opt_empty_vars_mono_key_fib_and_ms`, `test_tpl_dynamic_rationale_ms_slot_variation_enforced`, `test_tpl_dynamic_rationale_competency_pool_uniqueness_and_conceptual_invariant`, `test_multimodal_tpl_d3_coverage`, y `test_examples_templates_strict_validation`. |

---

## 3. Resultados de Verificación de Pruebas

Comando ejecutado:
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_engine_invariants_adversarial.py tests/test_assemble_katex_and_rationale.py tests/test_assemble_sanitize_katex_r23.py tests/test_katex_prairielearn_tokens.py tests/test_c2c_error_aggregation.py tests/test_sandbox_adversarial.py tests/test_sandbox_gil_and_circuit_breaker.py tests/test_template_variability.py -q
```

**Resultado:**
```
........................................................................ [ 35%]
........................................................................ [ 71%]
..........................................................               [100%]
202 passed in 31.79s
```

Comando Zero-Domain ejecutado:
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_skill.py -k "test_engine_zero_domain_logic" -q
```

**Resultado:**
```
.                                                                        [100%]
1 passed, 32 deselected in 0.23s
```

- **Total de pruebas en las 8 suites asignadas:** 202 passed (0 failed, 0 errors, 0 warnings).
- **Frontera de escritura exclusiva:** Estrictamente respetada.
- **Zero-domain check:** 100% limpio.
- Listo para Fase 3 (Auditor).
