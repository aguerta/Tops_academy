# DISPATCH — Stream 1C (Fase 1: Implementador `impl_1c`)

## 1. Rol y Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)
Eres el **Implementador del Stream 1C** bajo `/flash-triad-orchestrator`.
- **Carpeta de Gobernanza:** `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1c_impl/`
- **Archivos de Producción Permitidos (ÚNICOS que puedes modificar):**
  1. `.agents/skills/content-to-course/c2c_hook_guard.py`
  2. `tests/test_hook_post_pass_and_write_isolation.py`
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1c_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1c_impl/handoff.md`
- **PROHIBIDO** editar cualquier otro archivo del repositorio. Nunca pases `ArtifactMetadata` a `write_file` o `edit_file`.

## 2. Paso 0 Obligatorio (*Pre-Flight Sanity Check*)
Antes de realizar cualquier edición:
1. Lee `.agents/skills/content-to-course/c2c_hook_guard.py` completo (L1–L743) y `tests/test_hook_post_pass_and_write_isolation.py` completo (L1–L657).
2. Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1c_impl/BRIEFING.md` confirmando líneas y firmas reales. Si detectas un bloqueo fuera de tu frontera, detén ediciones y envía `BLOCKER:: <archivo:línea> | <causa> | <opciones>` al Orquestador (`7d2e6386-9933-4c70-9e50-a3cf214925f6`).

## 3. Especificación Técnica de Implementación

### A. Regla A: Whitelist de `cta_fixes/*.py` y `cta_parts/*.py` en `WORKER_AUTHORIZED_PYTHON_PATTERNS`
1. En `WORKER_AUTHORIZED_PYTHON_PATTERNS` (`c2c_hook_guard.py` L82–L89), añadir soporte explícito para:
   - `courses/*/work*/cta_fixes/*.py`, `work*/cta_fixes/*.py`, `cta_fixes/*.py`
   - `courses/*/work*/cta_parts/cta_fixes/*.py`, `work*/cta_parts/cta_fixes/*.py`, `cta_parts/cta_fixes/*.py`
   - `courses/*/work*/cta_parts/*.py`, `work*/cta_parts/*.py`, `cta_parts/*.py`
   - Actualizar también el mensaje de denegación de Regla A (L563–L569) para mencionar `work/cta_fixes/<CID>.py` junto a `work/shards/<shard_id>_data.py` y `work/shards/shard_fixes/<CID>.py`.

### B. Bloqueo de Fugas Exploratorias Pre-Compilación (`tests/`, `git log`, `Get-ChildItem ... courses`)
1. **Lectura de `tests/` por workers:**
   - En `WORKER_DENIED_READ_SUBSTRINGS` (L65–L79), añadir `"tests/"` para que ningún worker pueda usar `view_file` / `read_file` sobre `tests/test_validator.py` u otros archivos de pruebas (como hizo `shard_17` en `v5`, perdiendo `225 s`).
   - En el bloque de `grep_search` / `find_by_name` de workers (L495–L525), incluir `"tests/"` entre los directorios internos bloqueados.
2. **Comandos exploratorios en `run_command` de workers (L435–L465):**
   - Bloquear comandos `git` exploratorios ejecutados por workers: `r"\bgit\s+(?:log|diff|show|status|branch|grep)\b"` -> denegar con mensaje claro indicando que el worker tiene prohibido inspeccionar el historial de git.
   - Endurecer la detección de exploración de `courses/` en `run_command`: actualmente el regex `r"\b(?:dir|ls|get-childitem|gci|find|tree)\b[^;|&\n]*\bcourses\b"` funciona cuando `courses` va después, pero asegurarse de que capture cualquier variante de `Get-ChildItem`, `gci`, `dir`, `ls`, `find`, `tree` que apunte a `courses` (con `-Path`, `-LiteralPath`, `-Recurse`, comillas o barras `courses/`, `courses\`) siempre que NO apunte exclusivamente a su propio `<work_dir>` activo del lockfile (o simplemente mantener la denegación de listado general sobre `courses` como ya exigen los tests existentes).
   - Bloquear también si un worker intenta leer `tests/` vía `run_command` (ej. `Get-Content tests/...` o `type tests\...`).

### C. Regla B Extendida a CTA Post-PASS (`pass_cta_<target_id>.json`)
1. Además de detectar `shard_XX_data.py` con `.check_attempts/pass_shard_XX.json`, detectar cuando un worker intenta `write_file`, `edit_file` o `replace_file_content` sobre `cta_data.py` o `cta_parts/<part_id>_data.py` (o `cta/<part_id>_data.py`):
   - Determinar `cta_target_id`: `"cta_data"` si el archivo es `cta_data.py`, o `<part_id>` (ej. `part_01`, `cta_shard_01`) si el archivo es `<part_id>_data.py` o `part_XX.py` dentro de `cta_parts/` o `cta/`.
   - Buscar `.check_attempts/pass_cta_{cta_target_id}.json` (y `pass_{cta_target_id}.json`). Si existe y su JSON tiene `"status": "PASS"`, denegar la edición con un mensaje claro:
     `BLOCKER:: El módulo CTA {cta_target_id} ya aprobó todas las validaciones estrictas ([+] PASS). Detén cualquier edición o reescritura adicional y emite DONE inmediatamente.`

### D. Regla C Unificada con Umbral Oficial `< 6` Errores (`edit_file` vs `write_file`) para Shards y CTA
1. **Objetivo:** Aplicar el criterio oficial del usuario (**umbral `< 6` errores**) tanto a **Shards** (`shard_XX_data.py`) como a **CTA** (`cta_data.py`, `cta_parts/part_XX_data.py`, `cta/cta_shard_XX_data.py`) cuando la herramienta es `write_file` / `write_to_file`:
   - Nota crítica: Las escrituras a `shard_fixes/*.py` y `cta_fixes/*.py` SIEMPRE están permitidas por Regla C.
   - Cuando el archivo objetivo (`target_disk_path`) **ya existe en disco** y existe un archivo previo de intento de compilación en `.check_attempts/` (`compile_{shard_id}.json` para shards, o `compile_cta_{cta_target_id}.json` / `compile_{cta_target_id}.json` para CTA) con fallos previos registrados (`distinct_compiles >= 1` o `attempts >= 1` o `last_err_hash` o `last_errors` o `error_count` presente):
     - Leer del JSON de intento:
       - `has_syntax_error = bool(compile_state.get("has_syntax_error", False))`
       - `error_count = compile_state.get("error_count")` (puede ser `int` o `None` si es un fixture legacy de test).
     - **Caso 1 (`has_syntax_error is True`):** Permitir `write_file` (`allow`) para que el agente pueda recuperar un archivo con sintaxis rota.
     - **Caso 2 (`isinstance(error_count, int)` — nuevo contrato v3.5 con conteo explícito):**
       - Si `1 <= error_count < 6` (y el archivo existente o nuevo tiene `>= 40` líneas): **DENEGAR `write_file`**!
         - Para Shards, el mensaje de denegación debe incluir:
           `BLOCKER:: El archivo {shard_id}_data.py ya fue compilado ({existing_line_count} líneas) y registra {error_count} errores (< 6, umbral oficial). Para menos de 6 errores está prohibido reescribir todo el archivo desde cero con write_file: usa edit_file quirúrgico (replace_file_content) sobre las líneas reportadas, o escribe un parche modular aislado en work/shards/shard_fixes/<CID>.py.`
           *(Observa que si `existing_line_count > 250`, puedes incluir también la frase `"supera las 250 líneas"` para mantener 100% de compatibilidad con aserciones de texto existentes).*
         - Para CTA, el mensaje de denegación debe incluir:
           `BLOCKER:: El archivo {target_disk_path.name} ya fue compilado ({existing_line_count} líneas) y registra {error_count} errores (< 6, umbral oficial). Para menos de 6 errores está prohibido reescribir todo el archivo desde cero con write_file: usa edit_file quirúrgico (replace_file_content) sobre las líneas reportadas, o escribe un parche modular aislado en work/cta_fixes/<CID>.py.`
       - Si `error_count >= 6`: **PERMITIR `write_file` (`allow`)** (el salto oficial del *sweet spot* cuando hay `>= 6` errores permite hacer `write_file(Overwrite=True)` además de `shard_fixes`/`cta_fixes`).
     - **Caso 3 (`error_count is None` — compatibilidad 100% con tests legacy v3.4 que no pasan `"error_count"` en el JSON mock):**
       - Conservar exactamente la condición legacy: si `existing_line_count > 250` o `new_line_count > 250`, denegar con el mensaje exacto esperado por `test_rule_c_blocks_monolithic_write_file_on_compiled_shard_over_250_lines`; si `<= 250` líneas, permitir (`allow`).

## 4. Verificación y Entrega
1. Mantén al 100% todos los tests existentes en `tests/test_hook_post_pass_and_write_isolation.py` y añade nuevos tests unitarios para:
   - Umbral `< 6` (`error_count` = 1, 3, 5) en Shards (incluso con 120 líneas `< 250`) -> `write_file` es `deny`, `edit_file` es `allow`, `shard_fixes/Hab-01.py` es `allow`.
   - Umbral `>= 6` (`error_count` = 6, 10) en Shards -> `write_file` es `allow`.
   - `has_syntax_error=True` con `error_count=1` -> `write_file` es `allow`.
   - Umbral `< 6` (`error_count` = 2, 5) vs `>= 6` (`error_count` = 6) en CTA (`cta_data.py` y `cta_parts/part_01_data.py`) y Regla B Post-PASS con `pass_cta_part_01.json`, más whitelist de `cta_fixes/C-01.py`.
   - Bloqueo de worker leyendo `tests/test_validator.py` (`view_file`) y ejecutando `git log -n 5` o `Get-ChildItem -Path courses/ -Recurse` (`run_command`).
2. Ejecuta `.venv\Scripts\python.exe -m pytest tests/test_hook_post_pass_and_write_isolation.py tests/test_c2c_hook_guard.py -q`.
3. Escribe `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_1c_impl/handoff.md` y envía `DONE:: Stream 1C Implementer completado` a `7d2e6386-9933-4c70-9e50-a3cf214925f6`.
