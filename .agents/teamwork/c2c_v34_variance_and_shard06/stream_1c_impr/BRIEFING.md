# Pre-Flight Briefing — Stream 1C (Fase 2: Mejorador `impr_1c`)

- **Subagente:** Mejorador Stream 1C (`impr_1c`)
- **Fase:** Fase 2 (Mejorador)
- **Fecha:** 2026-10-24
- **Orquestador Conversation ID:** `526cfac0-d37b-49c9-bf09-00b5c520add2`

---

## 1. Inspección de Cambios del Implementador (`impl_1c`)

Se inspeccionaron detalladamente los cambios realizados en Fase 1:
1. `dispatch.py`: Inyección Turn-0 de `correct_belief`, `manifestation`, `remediation_hint`, directriz anti-lectura y limpieza de `.check_attempts/pass_<shard_id>.json`.
2. `system_prompts/lean/prompt_shard_author.md`: 4 arquetipos Milestone 3, distractores DRY, Turn-0 y Post-PASS; peso 4,718 bytes (`<= 4,750`).
3. `system_prompts/prompt_shard_author.md`: Actualización exhaustiva con Milestone 3, DRY y corte Post-PASS.
4. `system_prompts/lean/prompt_repair.md`: Especificación lean para `c2c_repair` con `[R-20]` y parches modulares; peso 2,492 bytes (`<= 5,000`).
5. `system_prompts/prompt_repair.md`: Versión completa creada formalmente.
6. `tests/test_dispatch_turn0_and_milestone3_prompts.py`: Suite con 4 tests pasando al 100%.

Todos los tests actuales (41 en total) pasan sin regresiones.

---

## 2. Frontera Exclusiva de Escritura (`Exclusive Write Boundaries`)

- `.agents/skills/content-to-course/dispatch.py`
- `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
- `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
- `.agents/skills/content-to-course/system_prompts/lean/prompt_repair.md`
- `.agents/skills/content-to-course/system_prompts/prompt_repair.md`
- `tests/test_dispatch_turn0_and_milestone3_prompts.py`
- `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1c_impr/BRIEFING.md`
- `.agents/teamwork/c2c_v34_variance_and_shard06/stream_1c_impr/handoff.md`

---

## 3. Plan de Endurecimiento (Hardening)

1. **Sanitización de campos vacíos/None en `dispatch.py`:**
   - Crear helper `_clean_str` para garantizar que valores `None`, `"None"`, `"null"`, `"undefined"`, o vacíos nunca generen cadenas literales `"None"` o `"null"` en `author_XX.json`.
   - Omitir cabecera de `correct_belief` si el campo está ausente o es nulo.
   - Preservar notación KaTeX con subíndices y superíndices anidados sin alteración.
2. **Normalización de rutas Windows/POSIX:**
   - Reemplazar separadores `\` por `/` en rutas de documentos resueltas en `dispatch_authors`.
3. **Resiliencia en limpieza de `.check_attempts/` en `dispatch_repair`:**
   - Limpiar `pass_{shard_id}.json`, `pass_{norm_s_id}.json`, `pass_{cid}.json`, `pass_{norm_cid}.json` y variantes de competencia.
   - Envolver el acceso en bloque `try...except` para garantizar que si el directorio no existe, está bloqueado por otro proceso en Windows o carece de permisos, nunca lance una excepción no controlada.
4. **Validación sintáctica Python (AST) en System Prompts:**
   - Comprobar que el 100% de los bloques de código Python en `prompt_shard_author.md` y `prompt_repair.md` (Full y Lean) sean sintácticamente válidos.
   - Mantener `lean/prompt_shard_author.md` con margen seguro (`<= 4,750 bytes`).
5. **Ampliación de Tests Unitarios:**
   - Agregar tests con casos adversarios: valores `None`/corruptos en distractor, fórmulas KaTeX con subíndices anidados, rutas Windows, limpieza de `.check_attempts` bloqueado/inexistente, y validación AST completa de snippets.
