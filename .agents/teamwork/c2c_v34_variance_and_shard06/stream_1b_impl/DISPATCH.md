# DISPATCH — Stream 1B (Fase 1: Implementador `impl_1b`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Implementador del Stream 1B** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1b_impl/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/compile_shard.py`
  2. `.agents/skills/content-to-course/check_templates.py`
  3. `tests/test_shard06_and_dry_archetypes.py` *(nuevo archivo de tests unitarios)*
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1b_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1b_impl/handoff.md`
- **PROHIBIDO** editar cualquier otro archivo del repositorio.

## 2. Paso 0 Obligatorio (*Pre-Flight Sanity Check*)
Antes de realizar cualquier edición:
1. Lee `.agents/skills/content-to-course/compile_shard.py` (especialmente `auto_heal_template_data` L310–L435, `build_adapted_mc7_generator` L540–L660, `compile_shard` L710–L1275 y `main` L1280–L1405) y `.agents/skills/content-to-course/check_templates.py` (`render_compact_aggregated_errors` L1045–L1085 y `format_invariant_error_diagnostic` L1295–L1355).
2. Escribe `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1b_impl/BRIEFING.md` confirmando las líneas y firmas reales. Si detectas un bloqueo fuera de tu frontera, detén ediciones y envía `BLOCKER:: <archivo:línea> | <causa> | <opciones>` al Orquestador (`526cfac0-d37b-49c9-bf09-00b5c520add2`).

## 3. Especificación Técnica de Implementación (100% Agnóstica + Milestone 3)

### A. Herencia DRY de Distractores en `compile_shard.py` (Preservando 4 Arquetipos Milestone 3 sin 4x Boilerplate)
1. **Problema:** Para escribir los 4 arquetipos por competencia del Milestone 3 (`Directo`, `Inverso`, `Perturbación`, `Frontera`), los autores tenían que repetir manualmente 24 a 48 diccionarios largos con `error_rationale` dentro de cada función `gen_*`, a pesar de que `compile_shard.py` ya carga `cta_distractors` desde `cta.json`.
2. **Solución en `build_adapted_mc7_generator` (L540–L660) y `auto_heal_template_data` (L310–L435):**
   - En el código adaptado `_adapted_gen(rng)` generado por `build_adapted_mc7_generator`, cuando la función del autor retorna `dists` (como tercer elemento de la tupla `(vars_d, ans_s, dists)` o en un dict `{"distractors": dists}`):
     - Soportar que cada elemento `d` de `dists` sea:
       1. Un `dict` completo `{"value": ..., "distractor_id": ..., "error_rationale": ...}` (formato actual).
       2. Un `dict` compacto sin `error_rationale` (o con `error_rationale` vacío): `{"value": ..., "distractor_id": "D-XX-01"}` o `{"id": "D-XX-01", "value": ...}`.
       3. Una tupla/lista de 2 elementos `("D-XX-01", value_str)` o `(value_str, "D-XX-01")` (detectando cuál de los 2 elementos coincide con un `distractor_id` tipo `^D-` o presente en `cta_distractors`; si el primero empieza con `D-`, es `(did, val)`, si el segundo empieza con `D-`, es `(val, did)`), o de 3 elementos `("D-XX-01", value_str, error_rationale_str)`.
       4. Un string simple `value_str` (asignando el `distractor_id` por posición desde `cta_distractors`).
     - Cuando `error_rationale` no haya sido provisto explícitamente por el autor (o sea vacío/placeholder), poblarlo automáticamente en `_adapted_gen` (y en `auto_heal_template_data`) usando el mapa `cta_distractors` de esa competencia: construir un rationale limpio y seguro a partir de `remediation_hint` o `wrong_belief` + `omitted_step` de `cta.json` (garantizando que toda expresión LaTeX huérfana pase por `_wrap_bare_latex_in_rationale`).
     - Si el autor **sí** proveyó un `error_rationale` explícito en `d`, preservarlo intacto (pasándolo por `_wrap_bare_latex_in_rationale`).

### B. Inferencia Automática de `work_dir` vía Lockfile, Soporte CLI (`--cta`, `--manifest`, `--output`) y Marcador `pass_<shard_id>.json` en `compile_shard.py`
1. **Inferencia de `work_dir` cuando se omiten `--work` y `--input`:**
   - En `compile_shard` / `main()` (L715–L745 y L1375–L1405): si `work_dir` es `"work"` (el default) y `Path("work/shards/pre_shard_manifest.json")` no existe en el CWD, buscar si existe algún `courses/*/.c2c_subagent_lock.json` o `courses/*/work/.c2c_subagent_lock.json` con `"active": true` (o el directorio `courses/*/work` más reciente que contenga `shards/{shard_id}_data.py`) y usar automáticamente ese `courses/<course_id>/work` como `work_p`.
2. **Soporte completo de flags CLI `--cta`, `--manifest` y `--output` (L1378–L1405):**
   - Si se pasa `--cta <path>`, usarlo como ruta prioritaria a `cta.json` dentro de `compile_shard`.
   - Si se pasa `--output <path>` y `<path>` termina en `.json` (ej. `--output courses/<id>/work/shards/shard_06.json`), además de guardar los templates compilados en `work/templates/<cid>.json`, escribir/actualizar en `<path>` un JSON de recibo de compilación (preservando las claves existentes de `shard_XX.json` si ya existía en disco y añadiendo `"compiled_status": "PASS" | "FAIL"`, `"compiled_templates": written_files`, `"compiled_at": ...`) para que el archivo destino anunciado en `dispatch.py` (`DONE: <output_json>`) exista y esté actualizado en disco.
3. **Marcador Post-PASS `.check_attempts/pass_<shard_id>.json` (L1190–L1265):**
   - Cuando `compile_shard` finalice con **0 errores** (`len(validation_errors) == 0` y todas las competencias del shard compiladas exitosamente), escribir en `work_p / ".check_attempts" / f"pass_{shard_id}.json"` un JSON `{"shard_id": shard_id, "status": "PASS", "source_sha256": current_source_sha256, "template_counts": {cid: len(tpls) ...}, "timestamp": time.time()}`.
   - Si la compilación falla, asegurarse de eliminar `pass_{shard_id}.json` si existía.

### C. Rutas Reales y Diagnóstico Exacto de Campo `R-20` en `check_templates.py`
1. **Priorizar `targets` reales en `render_compact_aggregated_errors` (`check_templates.py` L1049–L1068):**
   - Actualmente el código busca `cand = Path("work/templates") / f"{cid}.json"` **antes** de revisar `targets`, y usa `f"work/templates/{cid}.json"` como fallback por defecto, confundiendo a los agentes sobre dónde vive el archivo.
   - Invertir la prioridad: buscar primero en `targets` cualquier ruta cuyo `.stem == cid` (o directorio en `targets` que contenga `f"{cid}.json"`), devolviendo su ruta relativa al CWD en formato POSIX (`courses/<id>/work/templates/<cid>.json`), y solo usar `Path("work/templates") / f"{cid}.json"` si no hubo match en `targets`.
2. **Claridad en el diagnóstico de `R-20` (`format_invariant_error_diagnostic`, `check_templates.py` L1305–L1318):**
   - Cuando un error `R-20` provenga de una opción o rationale (ej. `"LaTeX math expression in option 2 error_rationale has unbalanced braces: $H = ...$"`), extraer e indicar explícitamente en `por_que` y `accion`:
     - El campo exacto afectado (ej. `options[2].error_rationale (distractor D-...)` o `stem` o `solution`).
     - El fragmento exacto donde ocurre el desbalance (por ejemplo, detectando patrones como `_}{` o `^}{` o mostrando el conteo `open={N} vs close={M}` de llaves).

## 4. Verificación y Entrega
1. Crea `tests/test_shard06_and_dry_archetypes.py` verificando:
   - Compilación de un shard con **4 arquetipos disjuntos** usando formato DRY compacto de distractores (`("D-Hab06-01", r"$@d1@$")` y `{"distractor_id": "D-Hab06-02", "value": r"$@d2@$"}` sin `error_rationale`), comprobando que `compile_shard` inyecta automáticamente los `error_rationale` desde `cta.json` y pasa `check_templates.py --strict` con 0 errores (`R-17`, `R-20`, `R-22`, `TPL-VAR`).
   - Que al pasar `--output <tmp>/shard_06.json --cta <tmp>/cta.json`, el archivo `--output` se actualiza con `"compiled_status": "PASS"` y se crea `.check_attempts/pass_shard_06.json`.
   - Que `render_compact_aggregated_errors` en `check_templates.py` muestra la ruta real `courses/<id>/work/templates/<cid>.json` pasada en `targets` y no `work/templates/<cid>.json`.
2. Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_shard06_and_dry_archetypes.py tests/test_compile_shard.py tests/test_shard_compiler_hardening.py`.
3. Escribe `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1b_impl/handoff.md` y envía `DONE:: Stream 1B Implementer completado` a `526cfac0-d37b-49c9-bf09-00b5c520add2`.
