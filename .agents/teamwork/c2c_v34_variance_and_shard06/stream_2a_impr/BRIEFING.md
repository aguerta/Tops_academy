# BRIEFING — Stream 2A: Hardening del Mejorador (`impr_2a`)

- **Rol:** Mejorador Senior (`impr_2a`) — Fase 2 de la Tríada Secuencial
- **Fecha:** 2026-10-24
- **Orquestador Conversation ID:** `526cfac0-d37b-49c9-bf09-00b5c520add2`
- **Fase Previa:** Implementador Integrador Post-Gate 1 (`impl_2a`)

---

## 1. Pre-Flight Inspection (Paso 0)

Hemos inspeccionado el handoff de `impl_2a` (`stream_2a_impl/handoff.md`), el archivo de dispatch (`stream_2a_impr/DISPATCH.md`) y el estado del árbol de trabajo (`git status --short`).

### Hallazgos del Pre-Flight:
1. **Aserciones permisivas en `tests/test_forensic_shard06_and_variance_v34.py`:**
   - Línea 436: `diag.cause or diag.field_name` — debe requerir simultáneamente `diag.field_name == "options[1].error_rationale (distractor D-Hab06-02)"`, `"options[1].error_rationale (distractor D-Hab06-02)" in diag.cause`, y `"open=" in diag.cause and "close=" in diag.cause`.
   - Línea 455: `patrón invertido in diag.cause or open= in diag.cause or _}{ in diag.cause` — debe exigir conjunción estricta `and` para los 3 elementos.
   - Línea 468: `assert "work/templates/Hab-06.json" not in rendered or "courses/" in rendered` — aserción tautológica débil; debe validar que el archivo normalizado relativo contenga `courses/asyntotic_estatistics_v4/work/templates/Hab-06.json` y que ninguna línea presente la ruta incorrecta descontextualizada.
   - Líneas 563-564: condicionales `or` en el chequeo del prompt Turn-0 — deben exigir tanto la presencia de etiquetas semánticas como el contenido textual y matemático exacto.

2. **Producción de Shard 06 (`Hab-06`):**
   - Actualmente `courses/asyntotic_estatistics_v4/work/shards/shard_06_data.py` posee 1 sola tupla de template legacy.
   - Milestone 3 exige 4 arquetipos disjuntos pedagógicos:
     1. **Directo/Frontal:** Estimación directa del estadístico de Hausman escalar $H = \frac{(b_{IV} - b_{LS})^2}{V_{IV} - V_{LS}}$ a partir de parámetros muestrales de gemelos.
     2. **Inverso/Diagnóstico:** Deducción del contraste de hipótesis y magnitud esperada de la atenuación frente a la endogeneidad.
     3. **Perturbación/Estática Comparativa:** Análisis de sensibilidad ante cambios en la varianza de error de medición o ratio de fiabilidad $q$.
     4. **Frontera/Casos Límite:** Comportamiento del estadístico y del sesgo en límites de fiabilidad perfecta ($q \to 1$) o correlación de errores nula.
   - Estos 4 arquetipos deben usar el formato DRY de distractores, auto-heredando los racionalizadores de `cta.json`.
   - El código original de 1 tupla (que experimentó los 10 fallos en la corrida `0b8b5084`) debe preservarse intacto en un test de regresión dedicado dentro de `tests/test_forensic_shard06_and_variance_v34.py` (`test_legacy_shard06_exact_code_compiles_cleanly`).

3. **Verificación de Invariantes y KaTeX:**
   - Los 4 arquetipos en `shard_06_data.py` deben compilar limpiamente bajo `compile_shard.py --strict` con 50 semillas dry-run.
   - El archivo generado `Hab-06.json` debe contener los 4 templates (`len(tpl_data["templates"]) == 4`) y pasar `check_templates.py --strict` con 0 errores.
   - Se debe actualizar `test_real_hab06_template_instantiation_and_invariants` para verificar los 4 arquetipos.

---

## 2. Plan de Acción y Fronteras de Escritura

Frontera de escritura estricta respetada al 100%:
- `tests/test_forensic_shard06_and_variance_v34.py`
- `courses/asyntotic_estatistics_v4/work/shards/shard_06_data.py`
- `courses/asyntotic_estatistics_v4/work/shards/shard_06.json`
- `courses/asyntotic_estatistics_v4/work/templates/Hab-06.json`
- `courses/asyntotic_estatistics_v4/work/.check_attempts/*`
- `.agents/teamwork/c2c_v34_variance_and_shard06/stream_2a_impr/BRIEFING.md`
- `.agents/teamwork/c2c_v34_variance_and_shard06/stream_2a_impr/handoff.md`

Procederemos de forma metódica y determinista.
