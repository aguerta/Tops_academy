# BRIEFING — Stream 1B (Implementador `impl_1b`)

## Pre-Flight Sanity Check

- **Fecha:** 2026-10-24
- **Implementador:** Stream 1B (`impl_1b`)
- **Frontera exclusiva de escritura:**
  - `.agents/skills/content-to-course/compile_shard.py`
  - `.agents/skills/content-to-course/check_templates.py`
  - `tests/test_shard06_and_dry_archetypes.py`
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1b_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1b_impl/handoff.md`

### 1. Confirmación de Firmas y Ubicaciones Reales en Archivos de Producción

1. **`compile_shard.py`**:
   - `build_adapted_mc7_generator(base_gen_code: str, cid: str, cta_distractors: List[Dict[str, Any]]) -> str` (L485–L605):
     - Actualmente envuelve `generate_params(rng)` asumiendo distractores estructurados en `res["distractors"]` o extrayéndolos de `res["options"]`.
     - No procesa tuplas directas `("D-XX-01", value_str)`, `(value_str, "D-XX-01")`, strings solos ni diccionarios compactos `{"value": ..., "distractor_id": "D-..."}` sin `error_rationale`.
     - No hereda `error_rationale` de `cta.json` cuando el autor los omite en `gen_*`.
   - `compile_shard(work_dir_or_path, shard_id, strict, seeds, output_dir, **kwargs)` (L694–L1355):
     - `work_p` se resuelve directamente desde `work_dir_or_path`. Si no existe `pre_shard_manifest.json`, emite `BLOCKER::` y termina con sys.exit(2). No infiere `work_dir` buscando lockfiles activos o carpetas `courses/*/work`.
     - No acepta explícitamente `--cta`, `--manifest`, `--output` ni actualiza el archivo JSON de recibo en `--output` si termina en `.json`.
     - Al pasar con 0 errores (L1343–L1355), elimina el archivo de intentos `.check_attempts/compile_{norm_shard_id}.json`, pero actualmente no escribe el marcador post-PASS `.check_attempts/pass_{shard_id}.json`.
   - `main()` (L1374–L1405):
     - Declara argumentos `--input`, `--output`, `--cta`, `--manifest`, `--work`, `--shard`, `--output-dir`, `--strict`, `--seeds`. Sin embargo, `args.cta` y `args.manifest` no son reenviados a `compile_shard`, y `--output` sólo se mapea a `eff_out_dir` si no termina en `.json`.
     - Si `work` es `"work"` y no existe en CWD, falla sin buscar en `courses/*`.

2. **`check_templates.py`**:
   - `auto_heal_template_data(data: Dict[str, Any], cta_comp: Optional[Dict[str, Any]] = None)` (L490–L745):
     - Poblaba `error_rationale` para `multiple_select`, pero no completaba automáticamente `error_rationale` faltantes en `multiple_choice_7_options` desde el contexto `cta_comp` ni sanitizaba con `_wrap_bare_latex_in_rationale`.
   - `render_compact_aggregated_errors(errors, targets, max_output_lines, shard_py)` (L994–L1170):
     - En L1049–L1068, verifica `cand1 = Path("work/templates") / f"{cid}.json"` antes de inspeccionar `targets`. Si `targets` tiene `courses/<course_id>/work/templates/<cid>.json`, caía en `work/templates/{cid}.json` si existía un stub o por defecto.
   - `format_invariant_error_diagnostic(...)` (L1203–L1455):
     - En L1304–L1316, para `Unbalanced curly braces in LaTeX math expression`, extrae únicamente un snippet genérico sin identificar con precisión si el campo es `options[X].error_rationale` con su distractor asociado o mostrar el conteo de llaves / patrón problemático.

### 2. Plan de Acción de Implementación

1. **Herencia DRY de Distractores en `compile_shard.py`**:
   - Enriquecer `build_adapted_mc7_generator` para normalizar `dists` en `_adapted_gen(rng)`.
   - Aceptar tuplas `("D-XX-01", val)`, `(val, "D-XX-01")`, `(did, val, rat)`, dicts con sólo `{"value": ..., "distractor_id": ...}` o strings directos.
   - Cruzar con `clean_cta_distractors` para rellenar `distractor_id` y `error_rationale` (enriquecido y formateado) garantizando KaTeX válido.
   - Enriquecer `auto_heal_template_data` en `check_templates.py` para sincronizar rationales faltantes o vacíos en MC7 si estuvieran en las opciones.
2. **Inferencia de `work_dir`, Soporte CLI y Marcador Post-PASS en `compile_shard.py`**:
   - Inferir `work_dir` buscando `courses/*/.c2c_subagent_lock.json`, `courses/*/work/.c2c_subagent_lock.json` con `"active": true`, o carpetas `courses/*/work` que contengan `shards/{shard_id}_data.py`.
   - Soportar parámetros `--cta`, `--manifest`, `--output` en `compile_shard` y `main`.
   - Si `--output` es un archivo JSON, generar/actualizar el archivo de recibo (`"compiled_status": "PASS"`, `"compiled_templates"`, `"compiled_at"`, etc.).
   - Crear `.check_attempts/pass_{shard_id}.json` en caso de PASS; si falla, asegurar su eliminación.
3. **Rutas Reales y Diagnóstico R-20 en `check_templates.py`**:
   - Priorizar `targets` en `render_compact_aggregated_errors` para reportar rutas reales relativas al CWD en formato POSIX.
   - Mejorar `format_invariant_error_diagnostic` para R-20 detallando campo exacto, distractor ID asociado si aplica, fragmento y desbalance `open={N} vs close={M}`.
4. **Verificación**:
   - Crear `tests/test_shard06_and_dry_archetypes.py` cubriendo todas las especificaciones.
   - Correr pytest contra tests nuevos y existentes.
