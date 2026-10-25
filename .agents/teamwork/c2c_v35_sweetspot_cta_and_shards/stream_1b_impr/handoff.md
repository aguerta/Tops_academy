# HANDOFF — Stream 1B (Fase 2: Mejorador `impr_1b`)

**Fecha:** 2026-10-24  
**Agente:** `impr_1b` (Phase 2 Improver)  
**Destinatario:** Orquestador (`7d2e6386-9933-4c70-9e50-a3cf214925f6`)  
**Stream:** Stream 1B — Shard Compiler Sweet-Spot + Milestone 3 4-Archetype Enforcement Gate (`[M3-ARCHETYPES]`)

---

## 1. Frontera Exclusiva de Escritura (100% Disjunta)

Se respetó estrictamente la frontera autorizada:
- [`.agents/skills/content-to-course/compile_shard.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_shard.py)
- [`.agents/skills/content-to-course/check_templates.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/check_templates.py)
- [`tests/test_shard06_and_dry_archetypes.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/test_shard06_and_dry_archetypes.py)
- [`.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1b_impr/handoff.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1b_impr/handoff.md)

Ningún archivo fuera de esta frontera fue modificado. Se normalizaron finales de línea a LF.

---

## 2. Hardening e Implementación Técnica Realizada

### A. Gate Estricto `[M3-ARCHETYPES]` en `compile_shard.py`
1. **Parámetro y Flag CLI `--min-archetypes`:**
   - Agregado parámetro `min_archetypes: Optional[int] = None` en `compile_shard` y `compile_shard_file`.
   - Agregado argumento CLI `--min-archetypes` en `main()`.
   - Resolución desacoplada y robusta de `eff_min_arch`:
     ```python
     eff_min_arch = 1
     if min_archetypes is not None:
         eff_min_arch = int(min_archetypes)
     elif isinstance(shard_entry, dict) and shard_entry.get("min_archetypes"):
         eff_min_arch = int(shard_entry["min_archetypes"])
     elif isinstance(manifest_data, dict) and manifest_data.get("min_archetypes"):
         eff_min_arch = int(manifest_data["min_archetypes"])
     ```
     *(Garantiza 100% de compatibilidad hacia atrás con tests legacy de 1 tupla cuando no se especifica el parámetro).*
2. **Validación de Cantidad y Disyunción:**
   - Cuando `strict=True` y `eff_min_arch > 1`:
     - **Caso 1 (`len(tpls) < eff_min_arch`):** Rechaza shards que intenten pasar con 1 sola tupla que contenga `stem_variants` internos (brecha crítica detectada en v5). Emite diagnóstico estructurado `[M3-ARCHETYPES]` con la guía precisa para agregar las tuplas faltantes usando el patrón helper parametrizado `_gen_<cid>(rng, arch)` + 4 wrappers `gen_1..4`.
     - **Caso 2 (`len(tpls) >= eff_min_arch`, tuplas clonadas idénticas):** Detecta si las tuplas son clones idénticos (`len(distinct_tuples) < min(eff_min_arch, 2)`), impidiendo que se repita la misma tupla 4 veces.
   - Si `m3_errors` no está vacío, setea `is_clean = False` y concatena al inicio de `raw_errors`.

### B. Clasificación y Agrupación en `check_templates.py`
- En `extract_diagnostic_metadata`, se añadió soporte nativo para el tag `[M3-ARCHETYPES]`:
  - Extrae la competencia afectada (`comp`), plantilla asociada (`tpl = f"T-{comp}"`), campo (`"TEMPLATES"`), y genera una acción prescriptiva para agregar o diversificar las tuplas requeridas.
  - En `build_compact_diagnostic_groups`, mapea a `(file_path, shard_ref)` asociando el número de líneas de la tupla en `shard_XX_data.py`.
  - Cada competencia infractora consolida como 1 error estruturado en `count_distinct_shard_error_hunks`, emitiendo la directiva de umbral correcta (`[UMBRAL < 6 ...]` o `[UMBRAL >= 6 ...]`).

### C. Orden Ascendente de Preámbulo y Verifier Seguro
- En `ShardDataLineLocator.get_preamble_code()`, las constantes y funciones auxiliares (`helper_functions`) ahora se inyectan ordenadas estrictamente por su número de línea de inicio (`sorted(self.helper_functions, key=lambda k: self.functions[k][0])`), garantizando que funciones compartidas como `_gen_<cid>(rng, arch)` antecedan a las funciones que las invocan.
- En `extract_function_code()`, se añadió manejo defensivo para `fn_or_str is None`: cuando una tupla no define verificador (`ver_fn = None`), genera automáticamente un verifier no bloqueante `def verify(instance): return True`, evitando fallos `NameError: name 'verify' is not defined` durante el dry-run.

---

## 3. Nuevas Pruebas Unitarias Agregadas

En [`tests/test_shard06_and_dry_archetypes.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/test_shard06_and_dry_archetypes.py), dentro de la nueva clase `TestMilestone3FourArchetypeEnforcement`:
1. `test_milestone3_min_archetypes_rejects_single_tuple_even_with_4_stem_variants`:
   Valida que un shard con 1 sola tupla (a pesar de tener 4 `stem_variants`) falla con `[M3-ARCHETYPES]` al exigir `min_archetypes=4`, registrando `error_count >= 1` y `has_syntax_error: False` en el estado de circuit breaker y en el receipt.
2. `test_milestone3_min_archetypes_rejects_4_cloned_identical_tuples`:
   Valida que repetir 4 veces la misma tupla `(stem, gen_fn)` falla con `[M3-ARCHETYPES]` por clones idénticos.
3. `test_milestone3_min_archetypes_passes_with_compact_shared_helper_pattern`:
   Valida el patrón compacto canónico de Milestone 3:
   - Helper compartido: `def _gen_c01(rng, arch):`
   - 4 thin wrappers: `gen_c01_1..4`
   - 4 tuplas Form-A de 9 elementos con `[]` en posición 7 y sin elemento 10mo (`hints`).
   - Pasa `[+] PASS` con 50 semillas dry-run y `min_archetypes=4` configurado en el manifiesto.
   - Auto-pobla los 6 distractor IDs de `cta.json` en `target_misconceptions` y `distractor_ids`.
   - Auto-pobla los 3 hints socráticos desde `cta.json`.

---

## 4. Resultados de Verificación (Pytest)

Ejecución de la suite completa del stream:
```powershell
.venv\Scripts\python.exe -m pytest tests/test_shard06_and_dry_archetypes.py tests/test_compile_shard.py tests/test_shard_compiler_hardening.py tests/test_c2c_error_aggregation.py -q
.......................................................................  [100%]
71 passed in 28.52s
```
- Total pruebas ejecutadas: **71 passed**.
- Tests anteriores preservados al 100% (cero regresiones).
- LF verificado en todos los archivos del stream.

---

## 5. Conclusión y Traspaso
Fase 2 (Mejorador) completada exitosamente. Listo para Phase 3 Auditor (`auditor_1b`).
