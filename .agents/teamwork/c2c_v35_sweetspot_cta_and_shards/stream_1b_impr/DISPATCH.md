# DISPATCH — Stream 1B (Phase 2: Improver `impr_1b`)

## 1. Rol y Misión
Eres el **Mejorador (Phase 2 Improver)** del **Stream 1B (Shard Compiler Sweet-Spot + Milestone 3 4-Archetype Enforcement)** dentro de `/flash-triad-orchestrator`.
Debes leer primero:
1. `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1b_impl/BRIEFING.md`
2. `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1b_impl/handoff.md`

Tu misión es auditar el trabajo de `impl_1b` y cerrar la brecha crítica descubierta en `v5` (`shard_02_data.py`, `shard_09_data.py`, `shard_19_data.py`): **`compile_shard.py` permitía aprobar (`[+] PASS`) shards que emitían solo 1 tupla por competencia en `TEMPLATES` (o 4 `stem_variants` dentro de 1 sola tupla) en lugar de los 4 arquetipos disjuntos obligatorios del Milestone 3.**

## 2. Frontera Exclusiva de Escritura (100% Disjunta)
- **ARCHIVOS DE PRODUCCIÓN PERMITIDOS:**
  - `.agents/skills/content-to-course/compile_shard.py`
  - `.agents/skills/content-to-course/check_templates.py`
- **ARCHIVOS DE TEST PERMITIDOS:**
  - `tests/test_shard06_and_dry_archetypes.py`
- **ARCHIVOS DE GOBERNANZA PERMITIDOS:**
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1b_impr/handoff.md`
- **PROHIBIDO TOCAR:** Cualquier otro archivo fuera de esta lista.

## 3. Requerimientos Técnicos Exactos para Fase 2 (`impr_1b`)

### A. Gate Estricto `[M3-ARCHETYPES]` en `compile_shard.py` y `check_templates.py`
1. **Parámetro `min_archetypes` y Flag CLI `--min-archetypes`:**
   - En `compile_shard(...)`, agrega el parámetro opcional `min_archetypes: Optional[int] = None` (y asegúrate de que `compile_shard_file(...)` lo propague vía `**kwargs`).
   - En `main()` de `compile_shard.py`, agrega el argumento CLI:
     `parser.add_argument("--min-archetypes", dest="min_archetypes", type=int, default=None, help="Minimum disjoint archetypes (tuples) required per competency in TEMPLATES (e.g. 4 for Milestone 3)")`
     y pásalo a `compile_shard(..., min_archetypes=args.min_archetypes)`.
   - Resuelve `eff_min_arch` dentro de `compile_shard`:
     ```python
     eff_min_arch = 1
     if min_archetypes is not None:
         eff_min_arch = int(min_archetypes)
     elif isinstance(shard_entry, dict) and shard_entry.get("min_archetypes"):
         eff_min_arch = int(shard_entry["min_archetypes"])
     elif isinstance(manifest_data, dict) and manifest_data.get("min_archetypes"):
         eff_min_arch = int(manifest_data["min_archetypes"])
     ```
     *(Nota: por defecto es `1` cuando no se pasa `min_archetypes` ni está en `pre_shard_manifest.json`, garantizando 100% de retrocompatibilidad con todos los unit tests legacy de 1 tupla).*
2. **Validación de Cantidad y Disyunción de Arquetipos (`[M3-ARCHETYPES]`):**
   - Cuando `strict` sea `True` y `eff_min_arch > 1`:
     Para cada `cid` en `expected_cids if expected_cids else list(templates_by_cid.keys())`:
     - Sea `tpls = templates_by_cid.get(cid, [])`.
     - **Caso 1 (`len(tpls) < eff_min_arch`):**
       Registra un error en `m3_errors`:
       `f"{cid}.json ({shard_data_path.name}): [M3-ARCHETYPES] La competencia '{cid}' define solo {len(tpls)} tupla(s) en TEMPLATES, pero Milestone 3 exige mínimo {eff_min_arch} arquetipos disjuntos por competencia (1. Directo, 2. Inverso, 3. Perturbación, 4. Frontera). Nota: poner múltiples stem_variants dentro de 1 sola tupla NO cuenta como 4 arquetipos; agrega las {eff_min_arch - len(tpls)} tuplas faltantes para '{cid}' en TEMPLATES usando un helper parametrizado def _gen_{cid.lower().replace('-', '_')}(rng, arch) + 4 wrappers gen_1..4."`
     - **Caso 2 (`len(tpls) >= eff_min_arch`, pero tuplas clonadas idénticas):**
       Verifica que no todas las tuplas de `cid` compartan exactamente el mismo `(tpl.get("stem_es", "").strip(), tpl.get("generator_code", "").strip())`. Si `len({(t.get("stem_es", "").strip(), t.get("generator_code", "").strip()) for t in tpls}) < min(eff_min_arch, 2)` (es decir, clonaron la misma tupla 4 veces con el mismo enunciado y mismo generador), registra en `m3_errors`:
       `f"{cid}.json ({shard_data_path.name}): [M3-ARCHETYPES] Las {len(tpls)} tuplas de '{cid}' en TEMPLATES son clones idénticos (mismo stem y mismo generador). Cada uno de los {eff_min_arch} arquetipos debe tener su propio enunciado y wrapper/generador (ej. gen_1..4)."`
   - Justo después de `is_clean, raw_errors = check_templates_file_or_dir(...)`, si `m3_errors` no está vacío:
     ```python
     if m3_errors:
         is_clean = False
         raw_errors = m3_errors + list(raw_errors)
     ```
   - En `check_templates.py`, asegúrate de que el clasificador de reglas / `build_compact_diagnostic_groups` reconozca `[M3-ARCHETYPES]` como tag `M3-ARCHETYPES` (con acción clara para agregar las tuplas de arquetipos faltantes en `TEMPLATES`), de modo que `count_distinct_shard_error_hunks` cuente cada competencia con `< 4` arquetipos como 1 error estructurado y emita la directiva de umbral correspondiente (`[UMBRAL < 6 ...]` o `[UMBRAL >= 6 ...]`).

### B. Soporte Impecable para Helper Parametrizado `_gen_<cid>(rng, arch)` en `compile_shard.py`
- Verifica que cuando un autor escribe el patrón compacto de 4 arquetipos:
  ```python
  def _gen_c06(rng, arch):
      n = rng.randint(10, 50)
      ...
      return {"vars": {"n": n, "ans": ans, "d1": d1, ...}, "correct": r"$@ans@$", "distractors": [r"$@d1@$", ...]}
  def gen_c06_1(rng): return _gen_c06(rng, 1)
  def gen_c06_2(rng): return _gen_c06(rng, 2)
  def gen_c06_3(rng): return _gen_c06(rng, 3)
  def gen_c06_4(rng): return _gen_c06(rng, 4)
  ```
  `ShardDataLineLocator.get_preamble_code()` incluya `_gen_c06` en el preámbulo en orden de línea ascendente (`sorted(self.helper_functions, key=lambda k: self.functions[k][0])`) y que `build_adapted_mc7_generator` y `check_templates.py` ejecuten las 4 funciones `gen_c06_1..4` sin ningún fallo en las 50 semillas dry-run.

### C. Nuevas Pruebas Unitarias en `tests/test_shard06_and_dry_archetypes.py`
Agrega al menos 3 nuevos tests en `tests/test_shard06_and_dry_archetypes.py`:
1. `test_milestone3_min_archetypes_rejects_single_tuple_even_with_4_stem_variants`: Simula el caso exacto de `shard_09_data.py` y `shard_19_data.py` (1 sola tupla por competencia con 4 `stem_variants` adentro) cuando `min_archetypes=4` (o `"min_archetypes": 4` en `pre_shard_manifest.json`). Verifica que `compile_shard` retorna `False`, el reporte contiene `[M3-ARCHETYPES]`, y `.check_attempts/compile_<shard>.json` registra `error_count >= 1` y `has_syntax_error: False`.
2. `test_milestone3_min_archetypes_rejects_4_cloned_identical_tuples`: Verifica que repetir 4 veces la misma tupla `(stem, gen_fn)` para una competencia con `min_archetypes=4` falla con `[M3-ARCHETYPES]`.
3. `test_milestone3_min_archetypes_passes_with_compact_shared_helper_pattern`: Verifica que el patrón compacto (`def _gen_c01(rng, arch):` + `gen_c01_1..4` + 4 tuplas de 9 elementos con `[]` en posición 7 y sin 10mo elemento `hints`) pasa `[+] PASS` con `min_archetypes=4` y genera las 4 plantillas en `C-01.json` con `target_misconceptions` y `hints` auto-poblados desde `cta.json`.

## 4. Verificación y Handoff
1. Ejecuta:
   `.venv\Scripts\python.exe -m pytest tests/test_shard06_and_dry_archetypes.py tests/test_compile_shard.py tests/test_shard_compiler_hardening.py tests/test_c2c_error_aggregation.py -q`
2. Normaliza CRLF a LF en los 3 archivos de tu frontera.
3. Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1b_impr/handoff.md` y envía `DONE::` al Orquestador (`7d2e6386-9933-4c70-9e50-a3cf214925f6`).
