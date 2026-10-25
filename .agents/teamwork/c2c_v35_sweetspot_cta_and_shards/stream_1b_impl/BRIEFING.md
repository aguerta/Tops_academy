# BRIEFING — Pre-Flight Sanity Check (Stream 1B: Implementador `impl_1b`)

**Fecha y Hora:** 2026-10-24  
**Agente:** `impl_1b` (Phase 1 Implementer)  
**Orquestador:** `7d2e6386-9933-4c70-9e50-a3cf214925f6`  

---

## 1. Verificación de Fronteras de Escritura Exclusiva (`Exclusive Write Boundary`)

| Archivo | Tipo | Estado de Inspección |
|---|---|---|
| `.agents/skills/content-to-course/compile_shard.py` | Producción | Leído (L1040–L1690 inspeccionado en detalle) |
| `.agents/skills/content-to-course/check_templates.py` | Producción | Leído (L1207–L1425 inspeccionado en detalle) |
| `tests/test_shard06_and_dry_archetypes.py` | Test suite | Leído (L1–L651 inspeccionado en detalle) |
| `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1b_impl/BRIEFING.md` | Gobernanza | Creación actual |
| `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1b_impl/handoff.md` | Gobernanza | Pendiente tras ejecución de tests |

**Confirmación:** Ningún archivo fuera de esta frontera será modificado ni creado. No se pasará `ArtifactMetadata` en llamadas a herramientas de archivos.

---

## 2. Inspección de Líneas y Firmas Reales

### A. `.agents/skills/content-to-course/compile_shard.py`
- **L1046–L1052:** Inicialización de `state` en `.check_attempts/compile_{norm_shard_id}.json`:
  ```python
  state: Dict[str, Any] = {
      "distinct_compiles": 0,
      "same_error_streak": 0,
      "last_source_sha256": "",
      "last_err_hash": "",
      "last_errors": [],
  }
  ```
  *Modificación confirmada:* Agregar `"error_count": 0` y `"has_syntax_error": False`.
- **L1087:** Función interna `_fail(msg: str) -> Tuple[bool, List[str]]:`
  *Modificación confirmada:* Ampliar firma a `def _fail(msg: str, has_syntax_error: bool = False, error_count: int = 1) -> Tuple[bool, List[str]]:`.
  Persistir `state["error_count"] = error_count` y `state["has_syntax_error"] = bool(has_syntax_error)`, así como en `receipt_p` (`r_data`).
- **L1163–L1174:** Invocación ante `locator.syntax_error`:
  *Modificación confirmada:* Pasar `has_syntax_error=True, error_count=1`.
- **L1180–L1196:** Excepción durante `compile(healed_source, ...)`:
  *Modificación confirmada:* Detectar `isinstance(e, SyntaxError)` y propagar `has_syntax_error=True, error_count=1`.
- **L1224–L1226:** `fix_loc.syntax_error` en `shard_fixes/`:
  *Modificación confirmada:* Pasar `has_syntax_error=True, error_count=1`.
- **L1230–L1275:** Excepción en `compile(healed_fix_text, ...)`:
  *Modificación confirmada:* Detectar `isinstance(e_fix, SyntaxError)` y propagar `has_syntax_error=True, error_count=1`.
- **L1604–L1650 (`if not is_clean:`):**
  *Modificación confirmada:* Invocar `count_distinct_shard_error_hunks(raw_errors, targets=compiled_paths, shard_py=shard_data_path)`, asignar a `state["error_count"]` y `state["has_syntax_error"] = False`, persistir en `compile_att_file` y `receipt_p`.
  En L1647, reportar en `stderr`: `{len(raw_errors)} errores detectados ({error_count} errores consolidados) al compilar {shard_id}`.

### B. `.agents/skills/content-to-course/check_templates.py`
- **L1207–L1415 (`render_compact_aggregated_errors`):**
  - Factorizar la extracción y agrupación en función reutilizable `build_compact_diagnostic_groups(errors, targets=None, shard_py=None) -> Tuple[Dict[...], int]`.
  - Crear helper exportado `count_distinct_shard_error_hunks(raw_errors, targets=None, shard_py=None) -> int` que retorne `max(1, total_items)` si `raw_errors` no está vacío.
  - En `render_compact_aggregated_errors`:
    - Evaluar `hunk_count = max(1, total_items)`.
    - Generar la directiva dinámica:
      - Si `1 <= hunk_count < 6`: `[UMBRAL < 6 ({hunk_count}/5 errores)]: Usa edit_file (replace_file_content) quirúrgico en las líneas indicadas; PROHIBIDO write_file completo.`
      - Si `hunk_count >= 6`: `[UMBRAL >= 6 ({hunk_count} errores)]: Usa write_file modular en shard_fixes/<CID>.py (1-2 comps) o write_file(Overwrite=True) completo.`
    - Garantizar que la directiva figure al final y que el número de líneas nunca exceda `max_output_lines` (`<= 28` por defecto).

### C. `tests/test_shard06_and_dry_archetypes.py`
- Agregar clase de tests `TestStructuredErrorCountAndThresholdDirectives` cubriendo:
  1. `test_state_and_receipt_persist_error_count_and_syntax_flag_under_threshold` (1 a 5 errores consolidados, `[UMBRAL < 6 ...]`).
  2. `test_state_and_receipt_persist_error_count_over_threshold` (>= 6 errores consolidados, `[UMBRAL >= 6 ...]`).
  3. `test_state_records_syntax_error_flag_on_python_syntax_error` (`has_syntax_error: True`, `error_count: 1`).
  4. `test_render_compact_aggregated_errors_never_exceeds_max_output_lines_and_includes_directive` (<= 28 líneas y directiva presente).

---

## 3. Evaluación de Bloqueos (`BLOCKER::` Assessment)
- **Bloqueos externos detectados:** NINGUNO.
- Todos los cambios se encuentran contenidos estrictamente dentro de los 3 archivos permitidos.
- Las suites existentes pasan al 100% (48 tests en `test_shard06_and_dry_archetypes.py`, `test_compile_shard.py`, `test_shard_compiler_hardening.py` y 16 tests en `test_c2c_error_aggregation.py`).

**Conclusión:** Procediendo a implementación fase 1.
