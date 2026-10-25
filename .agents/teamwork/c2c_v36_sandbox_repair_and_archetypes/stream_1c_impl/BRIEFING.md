# BRIEFING — Stream 1C: Pre-Flight Sanity Check

**Fecha:** 2026-10-25
**Agente:** `impl_1c` (Implementador Stream 1C)
**Alcance:**
- `.agents/skills/content-to-course/run.py`
- `.agents/skills/content-to-course/dispatch.py`
- `tests/test_run_templates_and_dispatch_repair.py`

---

## 1. Verificación de Firmas y Líneas Reales

### A. `run.py` (Líneas 720–775)
- **Método verificado:** `Pipeline.run_stage_templates(self) -> Dict[str, Any]` (L711-L775).
- **L724-L749:** Detección de shards `shard_data_files = sorted(list(shards_dir.glob("shard_*_data.py")))` y compilación incondicional vía `compile_shard_mod.compile_shard(...)` o subproceso. Se confirma que no existe verificación de timestamp `mtime` ni consulta a `pre_shard_manifest.json` para saltear shards ya compilados.
- **L756-L767:** `check_templates_file_or_dir(templates_dir, cta_path=cta_file)` evalúa validez. Si `not is_valid`, imprime a `sys.stderr` y lanza `ValueError` sin persistir ningún reporte en `work/reports/templates_report.json`. Tampoco se persiste en caso de éxito.
- **Conclusión:** Confirmado 100%. Se procederá a implementar la compilación incremental (omitiendo shards cuyos templates `.json` están al día) y la persistencia de `templates_report.json` con `errors_by_cid` tanto en PASS como en FAIL previo a lanzar la excepción.

### B. `dispatch.py` (Líneas 1556–1855 y 2069–2111)
- **L1556-L1633:** Sección `elif role == "repair":`.
  - Lee `templates_report.json` únicamente buscando `tr.get("results", [])` con `res.get("status") == "fail"`. No parsea `errors_by_cid` ni la lista global `errors`.
- **L1672-L1688:** Filtrado por `ids`:
  - `for raw_id in ids: rid = str(raw_id).strip()` no separa por comas (e.g. `"C-05,C-11"` se busca como una única clave literal en lugar de dividirse).
- **L1812-L1852:** Creación de archivos y punteros:
  - Genera `item_file = items_dir / f"repair_{idx:02d}.json"` y `cid_item_file = items_dir / f"repair_{safe_cid}.json"`.
  - L1834-L1839: `make_pointer_prompt` referencia `item_file.name` (`repair_{idx:02d}.json`) y se agrega `item_file` a `item_files`. Esto genera colisiones al despachar múltiples veces o invocar por separado.
  - Se debe cambiar para referenciar `cid_item_file.name` (`repair_{cid_norm}.json`) asegurando idempotencia sin colisión.
- **L2069-L2074 & L2108-L2110:** Subcomando `dispatch-repair` en CLI acepta `--ids` con `nargs="*"`. Soporte para strings con comas en CLI o código asegurado.
- **Conclusión:** Confirmado 100%.

---

## 2. Detección de Bloqueos Externos
- **Estado:** Ninguno. Todos los cambios necesarios se encuentran estrictamente dentro de los archivos autorizados en la Frontera Exclusiva de Escritura.
- **Plan de Acción:**
  1. Implementar compilación incremental y `templates_report.json` en `run.py`.
  2. Implementar corrección de `--ids` por comas, parseo de `errors_by_cid`/`errors` y puntero `cid_item_file` en `dispatch.py`.
  3. Crear suite de tests completa en `tests/test_run_templates_and_dispatch_repair.py`.
  4. Ejecutar pytest en suites afectadas y certificar 100% verde.
