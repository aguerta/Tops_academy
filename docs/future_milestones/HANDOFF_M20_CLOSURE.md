# HANDOFF — Cierre Real y Certificación Definitiva del Milestone 20 (`milestone_20` vs `main`)

> **Fecha:** 2026-11-19  
> **Rama activa:** `milestone_20` (`HEAD = 17da938`, 29 commits sobre `main`)  
> **Propósito:** Permitir iniciar una **conversación limpia** con contexto forense completo de los bloqueadores reales que impiden certificar el **Milestone 20** tras el `git diff main..HEAD` y tras los 41 fixes de backend (`35d556e..17da938`).

---

## 1. Estado Actual de la Rama y del Repositorio

### Qué YA está sólido (NO rehacer)
* **Compilador C2C y contratos de cuotas/anti-clon:** `compile_cta.py`, `check_cta.py`, `cta_merge.py`, `compile_shard.py`, `check_templates.py`, `stage_contract.py`, `instantiate.py` y los 41 fixes forenses de backend (`L1`–`L4` en commits `35d556e..17da938`).
  * `[M20-MC7-CAP]` (`0 MC7` en `Skill`, `<= 1 MC7` en `Concept`/`Fact`/`PRE-*`), `[M20-ACTIVE-QUOTA]` (`>= 80%` activo), `[CTA-MODALITY-PLAN]` (`2 <= M <= 4`, `K=2` por modalidad activa) y los 4 candados anti-clon (`[TPL-CLONE-AST]`, `[TPL-CLONE-BAND]`, `[TPL-CLONE-STEM]`, `[TPL-CLONE-SYMPY]`) funcionan y pasan pruebas unitarias.
  * `L3-01` (`target_value -> target` en `assemble.py`), `L3-06` (`correct_role in roles` en Stage 0) y la validación topológica de `proof_dag` en `judge.py` ya están corregidos.
* **Arquitectura base de las 6 modalidades M20 en React + `mathjs`:** `SymbolicInput.tsx`, `ProofDAG.tsx`, `StepTile.tsx`, `AdversarialArena.tsx`, `Stage0Modeler.tsx`, `InvariantCanvas.tsx`, `ConceptMatching.tsx`, `TopologyValidator.ts`, `symbolicValidator.ts` y Smart `Blank-First` están implementados y compilan dentro del presupuesto de bundle (`+15.29 KB` gzip).

### Estado sucio actual del working tree (`git status`)
Antes de empezar a editar, inspecciona y limpia/decide qué hacer con los archivos modificados sin commitear actualmente en la rama:
* Modificados:
  * `.agents/skills/content-to-course/subagent_types.json`
  * `reports/c2c_patches/patch_ledger.jsonl`
  * `reports/qa_audits/{cert_course,eco_101,math_base,solow_incremental,solow_model,stats_math}_qa_report.md`
* Untracked (basura de corrida de tests, **eliminar**):
  * `.agents/skills/content-to-course/examples/edp/.check_attempts/C-01.json`
  * `.agents/skills/content-to-course/examples/edp/.check_attempts/circuit_breaker_C-01_Hab-01.json`

---

## 2. Hallazgos Exactos y Tareas Obligatorias para Cerrar el Milestone 20

> **Nota sobre alcance (Decisión explícita con el usuario antes de cerrar):**
> En `main:FUTURE_MILESTONES.md`, el Milestone 20 incluía el **Modo Hierro (`IronExamSession.tsx` + `MetacognitiveModal.tsx`, AC-5)**, que en esta rama fue movido a **Milestone 20-B**. Confirma con el usuario al inicio si el cierre objetivo de esta rama es **Milestone 20 Core** (manteniendo Modo Hierro en M20-B) o **Milestone 20 Completo** (incluyendo `IronExamSession.tsx` + `MetacognitiveModal.tsx`). **Todos los bloqueadores P0 y P1 abajo aplican obligatoriamente incluso para M20 Core.**

---

### BLOQUEADOR P0-1 — Reparar los 2 bugs vivos en `judge.py` (`L4-01`) y el test falso positivo en `test_forensic_41_fixes.py`

1. **`adversarial_break` (`counterexample`) en `.agents/skills/content-to-course/judge.py` (L1528–L1560):**
   * **Causa raíz:** `compile_and_verify_adversarial` en `engine/adversarial_generator.py` (L434–L446) compila cada entrada de `inputs` usando la clave `"id"` (`{"id": iid, "label": ...}`) y descarta `"name"`. Sin embargo, `judge.py` L1531 lee `iname = str(inp.get("name") or "")` sin fallback a `inp.get("id")`. Resultado: en todo ítem compilado real, `iname == ""`, `"" not in u_w` es `True`, `bounds_ok` cae a `False` y **el chequeo de predicados nunca corre**.
   * **Fuga de información en `_sanitize_m20_judge_item` (`judge.py` L329–L335):** Al copiar `adv["predicates"]` al lote ciego (`blind_adv["predicates"] = adv["predicates"]`), se filtran `failure_rationale` y `distractor_id` al Juez Ciego.
   * **Qué cambiar:**
     * En `judge.py` L1531: cambiar a `iname = str(inp.get("id") or inp.get("name") or "")`. Además verificar `inp.get("type") == "integer"` si aplica.
     * En `judge.py` L329–L335: sanitizar `blind_adv["predicates"]` conservando solo `{"id", "expr", "description"}` (sin `failure_rationale` ni `distractor_id`).

2. **`invariant_canvas` (`cartesian`) en `.agents/skills/content-to-course/judge.py` (L1617–L1660):**
   * **Causa raíz:** Si el autor incluyó `target_state` (como hace `prompt_shard_author.md` o `build_canonical_course.py`), `judge.py` L1617–L1620 hace `return False` inmediato si `_values_approx_equal(u_ts, gt_ts)` falla, **sin llegar jamás al evaluador de `invariants` de L1622–L1660**. Además, si el autor escribió `target_state: {"pt_kink": {"x": 5, "y": 10}}` (sin envolver en `"points"`) y el Juez Ciego sigue `prompt_blind_judge.md` (`{"points": {"pt_kink": {"x": 5, "y": 10}}}`), falla siempre.
   * **Qué cambiar:**
     * En `judge.py` L1617–L1620: si `_values_approx_equal(u_ts, gt_ts)` falla **pero** `gt.get("invariants")` está presente y no vacío, **caer (fallthrough)** a la validación contra `gt["invariants"]` en lugar de retornar `False` de inmediato.
     * Normalizar `target_state` en `judge.py` (y/o en `engine/assemble.py`) para aceptar tanto `{"points": {"P1": {"x": ..., "y": ...}}}` como `{"P1": {"x": ..., "y": ...}}`.
     * En L1634–L1639 (`kink_at`): notar que `kink_at` puede declarar solo `x` (sin `y`/`target_y`); evitar exigir `target_y` cuando `ty is None`.

3. **Corregir tests ilusorios en `tests/engine/test_forensic_41_fixes.py`:**
   * En `test_l4_01_03_judge_m20_arbitration` (L335–L344): generar `gt_adv` pasando por `compile_and_verify_adversarial` + `judge._sanitize_m20_judge_item` reales (no dict manual con `"name"`), y verificar que un testigo alternativo válido pasa y un testigo que viola `predicates` o dispara `trap_predicates` falla.
   * En `test_l2_c05_m01_m05_negative_expr_and_adversarial_prompt` (L253–L262): reemplazar `"sympy_verify": "@a@**2 - 9"` (clave inexistente que hace early-return en `proof_compiler.py`) por las claves reales `"sympy_expr": "@a@**2"` y `"expected_sympy_expr": "9"`, y añadir un caso negativo que verifique que una expresión no equivalente lanza `[PROOF-DAG-SYMPY]`.

---

### BLOQUEADOR P0-2 — Reparar y regenerar el Curso Canónico M20 (`build_canonical_course.py` + `m20_canonical_course.json`)

* **Causa raíz:** Ejecutar `python tests/fixtures/m20_canonical_cases/build_canonical_course.py` actualmente **falla con 20 errores** (`[CTA-MODALITY-PLAN]` y `[M20-ACTIVE-QUOTA]`) porque fue creado antes de `K=2` por modalidad activa (`deed8a0`) y nunca fue actualizado. Además, 7 de sus 16 plantillas producen exactamente la misma respuesta correcta en todas las semillas (solo varían un subíndice cosmético).
* **Qué hacer:**
  1. Actualizar `tests/fixtures/m20_canonical_cases/build_canonical_course.py` para cumplir **íntegramente** el contrato vigente sin trampas (`templates_per_modality=2`, `strict=True`):
     * Ajustar `recommended_modalities` (2 a 4 modalidades por competencia) y escribir `>= K=2` plantillas genuinamente distintas por cada modalidad activa (cumpliendo los 4 candados anti-clon `[TPL-CLONE-AST]`, `[TPL-CLONE-BAND]`, `[TPL-CLONE-STEM]`, `[TPL-CLONE-SYMPY]`, `0 MC7` en `Hab-01`/`Hab-02`, `<= 1 MC7` y `>= 80%` activo en `C-01`/`C-02`).
     * Asegurar que `target_state` en `Hab-02` (`invariant_canvas`) use el formato canónico `{"points": {"pt_kink": {"x": x_bar, "y": x2_kink}}}`.
  2. Re-ejecutar `python tests/fixtures/m20_canonical_cases/build_canonical_course.py` y regenerar `tests/fixtures/m20_canonical_cases/m20_canonical_course.json` con `exit code 0`.
  3. Añadir un test en `tests/engine/` que ejecute `build_canonical_course.py` (o su `main()` hacia un `tmp_path`) para garantizar que el curso canónico nunca vuelva a quedar roto por drift del compilador.
  4. Re-ejecutar `pytest tests/e2e/test_m20_bloom_modalities.py -v -n 0` contra el JSON regenerado y verificar 100% PASS.

---

### BLOQUEADOR P1-1 — Corregir bugs de Frontend (`platform/src/`) y paridad con el Backend

Ningún archivo de `platform/src/` fue tocado en los Lotes 1–4. Deben corregirse los siguientes bugs reales:

1. **`AdversarialArena.tsx` + `symbolicValidator.ts` (`adversarial_break`):**
   * **`trap_predicates` ignorados (`platform/src/services/symbolicValidator.ts` L716–L736):** En `validateAdversarialSubmission` (`mode === 'counterexample'`), evaluar `spec.trap_predicates` (antes o al fallar `predicates`) para retornar `matchedDistractorId` y `diagnosticRationale` cuando el alumno cae en una trampa explícita (que `compile_shard.py` sí contabiliza para `TPL-D3`).
   * **`computed_readouts` no renderizados (`platform/src/components/AdversarialArena.tsx` L113–L165):** Renderizar `spec.computed_readouts` en vivo en `mode === 'counterexample'` evaluándolos de forma segura con `mathjs` cuando el alumno completa los inputs (requerido por el Caso Canónico 3: mostrar $M = 0.5A + 0.5B$ y $u(M)$).
   * **`fallacyStep.error_rationale` muerto (`platform/src/services/symbolicValidator.ts` L620–L661):** En `mode === 'find_fallacy'`, si el alumno selecciona un paso que no es la falacia y `picked.valid_explanation` no está presente (o al revelar solución/feedback en `FeedbackToast.tsx`), aprovechar `fallacyStep.error_rationale` en el feedback diagnóstico cuando corresponda (sin revelar la respuesta si aún le quedan intentos, y mostrándolo en `FeedbackToast.tsx` al agotar intentos o acertar).
   * **Paridad de scope en `engine/adversarial_generator.py` (L390–L405):** En `compile_and_verify_adversarial`, **NO** inyectar las variables de `vars_dict` dentro de `witness_scope` al evaluar `predicates`/`trap_predicates`/`computed_readouts` (solo los IDs declarados en `inputs`). Así, si un autor olvida escribir `@k@` y escribe `k` crudo en `expr`, fallará en Shift-Left en Python en lugar de explotar en el navegador.

2. **`ConceptMatching.tsx` + `StepTile.tsx` + `InvariantCanvas.tsx` (fuga de LaTeX crudo y estado fantasma):**
   * **LaTeX crudo en `<select><option>` (`platform/src/components/ConceptMatching.tsx` L74–L89):** Los `<option>` nativos no renderizan KaTeX y muestran literal `$-\frac{\partial v/\partial p}{\partial v/\partial m}$` en `C-02`. Reemplazar el texto del `<option>` por etiqueta corta limpia (p. ej. `Opción A`, `Opción B`, ... o un popover/selector custom que use `<MathText>`) y mostrar la correspondencia asignada con `<MathText>` dentro de la tarjeta de la premisa.
   * **Estado fantasma `activePremiseId` (`platform/src/components/ConceptMatching.tsx` L18–L20 y `QuestionCard.tsx` L798):** Añadir `key={question.id}` en `QuestionCard.tsx` (o `useEffect` en `ConceptMatching.tsx` que reinicie `activePremiseId` cuando cambie `spec.premises`) para que al pasar entre dos preguntas `concept_matching` consecutivas no quede un ID de la pregunta anterior.
   * **`StepTile.tsx` (L113–L127):** Si `justification_bank` contiene LaTeX, o bien limpiar/formatear con selector accesible que soporte `<MathText>`, o bien validar en `proof_compiler.py` que `justification_bank` sea texto plano o renderizarlo fuera de `<option>`.
   * **`InvariantCanvas.tsx` modo `tree` (L187–L241):** Los labels de nodos/aristas con `$...$` en `<text>` SVG no renderizan KaTeX; o usar `<foreignObject>` con `<MathText>` o documentar/sanitizar texto plano en labels de árbol.

3. **`PracticeSession.tsx` (`hasAnswer` en `invariant_canvas`, L377–L378):**
   * Actualmente `case 'invariant_canvas': return structuredAnswer?.kind === 'invariant_canvas';` devuelve `true` antes de que el alumno toque nada (porque `createInitialStructuredAnswer` inicializa el objeto al cargar la pregunta).
   * **Qué cambiar:** Trackear un booleano `canvasInteracted` (se activa en `handleChangeStructuredAnswer` y se resetea al cambiar de pregunta o hacer redo) para que el botón "Comprobar" y `Enter` no envíen un lienzo intacto por accidente.

4. **`TopologyValidator.ts` (L157–L165):**
   * Por defensa en profundidad, en `case 'slider_eq'` aceptar `inv.expr ?? inv.target ?? (inv as any).target_value ?? (inv as any).expected` (y agregar `target_value?: number | string` opcional en `types.ts`), de modo que funcione tanto compilado por `assemble.py` como en fixtures directos.

---

### BLOQUEADOR P1-2 — Prompts M20, Perfiles `lean/`, QA Evaluator y Validación de Rigor

1. **Ejemplos de las 4 modalidades faltantes en prompts (`prompt_shard_author.md` y `prompt_repair.md`):**
   * Actualmente `proof_dag`, `adversarial_break`, `unstructured_model` y `concept_matching` tienen **0 ejemplos de código Python** en `<examples>` de `prompt_shard_author.md` y `prompt_repair.md`.
   * Añadir micro-ejemplos sintácticos completos (y corregir `"target_value"` a `"target"` en `prompt_shard_author.md` L208) para que los subagentes no alucinen claves de esquema.
   * Revisar y sincronizar `system_prompts/lean/*.md` (actualmente `lean/prompt_shard_author.md` fue inflado +209% de `11.9 KB` a `36.8 KB` al copiarle el prompt completo) y regenerar `subagent_types.json`.
   * Verificar si `prompt_cta_direct.md` y `prompt_cta_sectional.md` siguen activos en algún flujo; si están activos, actualizarlos a `recommended_modalities` + `[M20-MC7-CAP]`, o marcarlos explícitamente como legacy/deprecados.

2. **Rigor mínimo en `proof_dag` y `adversarial_break` (`find_fallacy`):**
   * En `engine/proof_compiler.py` (L180–L212): exigir `len(unique_edges) >= 1` (un `proof_dag` con `edges: []` acepta cualquier permutación como correcta). Evaluar elevar el mínimo de pasos de `2` a `>= 3` (actualmente diferido como "Opcional D" en `FUTURE_MILESTONES.md` L223) para eliminar reactivos 50/50 peores que `MC7`.
   * En `engine/adversarial_generator.py` (L226): evaluar elevar `len(raw_steps) >= 3` en `find_fallacy`.

3. **Auditoría real en `course-qa-evaluator` (`standardized_audit_engine.py`):**
   * `docs/specs/sintesis_plantillas_arquetipos.md` (L137) afirma que `course-qa-evaluator` contabiliza y controla `[M20-MC7-CAP]` y `[M20-ACTIVE-QUOTA]`, pero `RetrievalModalityDiversityLinter` en `standardized_audit_engine.py` (L1260–L1335) no emite issues si una competencia `Skill` tiene `MC7` o si una competencia cae por debajo del `80%` activo. Añadir las verificaciones por competencia (respetando retrocompatibilidad para cursos legacy v1) o corregir la afirmación documental.

4. **Piloto empírico mínimo con agentes LLM reales (1 shard real):**
   * Hasta hoy **no se ha corrido ni un solo shard real con subagentes LLM** bajo el contrato M20 (`K=2` por modalidad activa $\implies$ 6–8 plantillas/competencia con modalidades M20 y 4 candados anti-clon). Ejecutar al menos 1 corrida piloto controlada de 1 shard (2–3 competencias) para validar que `prompt_cta_architect` $\to$ `plan_shards` $\to$ `prompt_shard_author` $\to$ `compile_shard` $\to$ `judge` convergen en $\le 12$ turnos sin bloqueos.

---

## 3. Protocolo de Verificación Obligatorio (Gate de Cierre)

Antes de marcar el Milestone 20 como completado y hacer merge a `main`, **todos** estos comandos deben pasar con código `0` y el `git status` debe quedar limpio:

```powershell
# 1. Curso canónico M20 reproducible bajo contrato estricto vigente (K=2, >=80% activo)
python tests/fixtures/m20_canonical_cases/build_canonical_course.py

# 2. Suites de motor, pipeline, fixes forenses y plataforma (Python)
pytest tests/engine tests/pipeline tests/platform tests/test_assemble_and_hook_hardening.py tests/test_qa_evaluator_hardening.py -q

# 3. Validadores TypeScript / Node (Math + M20)
node tests/test_m20_validators.mjs
node tests/platform/test_math_adversarial_suite.mjs

# 4. Build de producción PWA (verificar gzip delta <= 120 KB)
npm --prefix platform run build

# 5. E2E Playwright contra el curso canónico recién compilado
pytest tests/e2e/test_m20_bloom_modalities.py -v -n 0

# 6. Limpieza de git y sincronización de MILESTONES_COMPLETED.md / FUTURE_MILESTONES.md (y espejos en docs/future_milestones/)
git status
```

---

## 4. Prompt Sugerido para Iniciar la Nueva Conversación Limpia

```text
Lee @HANDOFF_M20_CLOSURE.md completo. Vamos a cerrar los bloqueadores pendientes del Milestone 20 en la rama `milestone_20` (HEAD 17da938) en orden de prioridad:
1) Limpieza del working tree y corrección de P0-1 (`judge.py` L4-01 `adversarial_break`/`invariant_canvas` + `test_forensic_41_fixes.py`).
2) Corrección y regeneración de P0-2 (`build_canonical_course.py` + `m20_canonical_course.json` bajo K=2 y >=80% activo + test de regresión).
3) Corrección de P1-1 (bugs de Frontend en `platform/src/`: `AdversarialArena.tsx`, `symbolicValidator.ts`, `ConceptMatching.tsx`, `PracticeSession.tsx`, `TopologyValidator.ts` y paridad de scope en `adversarial_generator.py`).
4) Corrección de P1-2 (ejemplos de modalidades M20 en prompts, `edges >= 1` en `proof_compiler.py` y `standardized_audit_engine.py`).
Antes de empezar, confírmame tu plan y pregúntame si el Modo Hierro (M20-B) queda fuera de esta rama.
```
