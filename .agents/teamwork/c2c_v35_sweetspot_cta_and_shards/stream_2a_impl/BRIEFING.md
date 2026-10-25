# BRIEFING — Pre-Flight Sanity Check (Stream 2A: Integrator Implementer `impl_2a`)

**Fecha:** 2026-10-24  
**Agente:** `impl_2a` (Gate 2, Phase 1: Integrator Implementer)  
**Orquestador:** `7d2e6386-9933-4c70-9e50-a3cf214925f6`  
**Stream:** 2A — Integración End-to-End Sweet-Spot CTA, Shards, Hook Guard & Milestone 3  

---

## 1. Frontera Exclusiva de Escritura (Exclusive Write Boundary)
- **Archivos Autorizados para Edición:**
  1. `.agents/skills/content-to-course/subagent_types.json` (Normalización LF y sincronización con catálogo oficial)
  2. `tests/test_sweetspot_v35_cta_and_shards.py` (Nueva suite integral End-to-End de contrato cruzado v3.5)
- **Artefactos de Gobernanza Permitidos:**
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_2a_impl/BRIEFING.md`
  - `.agents/teamwork/c2c_v35_sweetspot_cta_and_shards/stream_2a_impl/handoff.md`
- **Archivos Estrictamente Protegidos (Solo Lectura):**
  - Todos los archivos de producción de Gate 1:
    - `.agents/skills/content-to-course/compile_cta.py` (L1-L700+)
    - `.agents/skills/content-to-course/cta_merge.py` (L1-L250+)
    - `.agents/skills/content-to-course/check_cta.py` (L1-L350+)
    - `.agents/skills/content-to-course/compile_shard.py` (L1-L1000+)
    - `.agents/skills/content-to-course/check_templates.py` (L1-L850+)
    - `.agents/skills/content-to-course/c2c_hook_guard.py` (L1-L1001)
    - `.agents/skills/content-to-course/dispatch.py` (L1-L2151)
    - `.agents/skills/content-to-course/system_prompts/**/*.md`
  - Suites existentes de Gate 1 (`test_cta_sweetspot_and_autoheal.py`, `test_shard06_and_dry_archetypes.py`, `test_hook_post_pass_and_write_isolation.py`, `test_dispatch_turn0_and_milestone3_prompts.py`, `test_prompts_contract_alignment.py`).

---

## 2. Verificación de Handoffs de Gate 1
- **Stream 1A (`audit_1a`):** Tier-0 Auto-Heal en `cta_merge.py` / `check_cta.py`, localizador AST de líneas Python reales en `compile_cta.py`, directiva dinámica del umbral oficial `< 6` (`[UMBRAL OFICIAL < 6 ERRORES ({error_count}/5)]`), y modular splicing en `cta_fixes/<CID>.py`. 10/10 tests PASS, 90/90 regresión PASS.
- **Stream 1B (`audit_1b`):** Persistencia de `error_count` y `has_syntax_error` en `.check_attempts/compile_{norm_shard_id}.json` y `--output`, directiva dinámica de umbral `< 6` en `check_templates.py`, y validación obligatoria de 4 arquetipos `[M3-ARCHETYPES]` en `compile_shard.py`. 71/71 tests PASS.
- **Stream 1C (`audit_1c`):** Reglas en `c2c_hook_guard.py`: Regla A (aislamiento de scripts Python), Regla B (corte post-PASS bloqueando `write_file`/`edit_file` sobre módulos aprobados), y Regla C (bloqueo de `write_file` en archivos de datos cuando `1 <= error_count < 6`, permitiendo `edit_file` y `*_fixes/<CID>.py`). 55/55 tests PASS.
- **Stream 1D (`audit_1d`):** Actualización de prompts (completos y lean en `system_prompts/`) incorporando el umbral oficial `< 6`, erradicación del escape hatch de 1 tupla, patrón compacto de 4 arquetipos con helper compartido, inyección de `--min-archetypes 4` y `"min_archetypes": 4` en `dispatch.py`. 44/44 tests PASS.

---

## 3. Estado de `subagent_types.json` y Catálogo
- `dispatch.get_type_definitions(lean=False)` genera 4 especificaciones completas (`c2c_cta_architect`, `c2c_shard_author`, `c2c_judge`, `c2c_repair`) a partir de `system_prompts/`.
- `tests/test_forensic_shard06_and_variance_v34.py::TestCatalogSynchronization::test_subagent_types_json_matches_get_type_definitions` verifica la paridad exacta entre `subagent_types.json` y `get_type_definitions(lean=False)`.
- Se requiere normalizar los saltos de línea de `subagent_types.json` de CRLF a LF estricto para evitar advertencias de Git y asegurar consistencia multiplataforma.

---

## 4. Plan de Implementación de la Suite End-to-End `tests/test_sweetspot_v35_cta_and_shards.py`
La suite integrará transversalmente los componentes desarrollados en los Streams 1A, 1B, 1C y 1D:
1. **Grupo 1: Integración CTA (`compile_cta.py` + `c2c_hook_guard.py`):**
   - **Test 1.1:** Simulación de datos con expresiones LaTeX descalzas (`\lim_{n\to\infty}`, `\frac{\sigma^2}{n}`, `\sigma` de `v5`), ejecución de `compile_cta.py` con Tier-0 Auto-Heal -> aprobación con `0` errores, emisión de `pass_cta_part_01.json`, seguido de invocación de `c2c_hook_guard.py` que bajo Regla B bloquea cualquier llamada posterior a `write_file` o `edit_file` sobre `part_01_data.py`.
   - **Test 1.2:** Fallo de compilación de CTA con `1 <= error_count < 6` (ej. 3 errores de consistencia) -> verificación de persistencia de `error_count: 3` en `.check_attempts/compile_cta_part_01.json`, presencia de `[UMBRAL OFICIAL < 6 ERRORES (3/5)]`, y verificación de que `c2c_hook_guard.py` bajo Regla C deniega `write_file` sobre `part_01_data.py` mientras autoriza `edit_file` o `write_file` en `cta_fixes/<CID>.py`.
   - **Test 1.3:** Fallo masivo de CTA con `error_count >= 6` -> verificación de que `c2c_hook_guard.py` permite `write_file` para reescritura de rescate.
2. **Grupo 2: Integración Shards (`compile_shard.py` + `c2c_hook_guard.py` + `dispatch.py`):**
   - **Test 2.1:** Invocación de `dispatch_authors` sobre un espacio de trabajo con `cta.json` -> verificación de estampado de `"min_archetypes": 4` en `pre_shard_manifest.json` y presencia de `--min-archetypes 4` en `compile_cmd`.
   - **Test 2.2:** Shard con 1 sola tupla por competencia (caso `shard_09_data.py` en `v5`) bajo `--min-archetypes 4` -> rechazo con `[M3-ARCHETYPES]`, persistencia de `error_count` (< 6) en `.check_attempts/compile_shard_09.json`, y verificación de que `c2c_hook_guard.py` bloquea `write_file` sobre `shard_09_data.py` instruyendo usar `edit_file` para insertar las tuplas faltantes o crear `shard_fixes/<CID>.py`.
   - **Test 2.3:** Shard implementando el patrón compacto de 4 arquetipos con función base compartida (`def _gen_c06(rng, arch):` + `gen_c06_1..4` + 4 tuplas posicionales de 9 elementos con `[]` en posición 7) -> aprobación con `[+] PASS`, creación de `pass_shard_09.json`, y bloqueo preventivo de `c2c_hook_guard.py` (Regla B) ante intentos de edición subsiguientes.

---

## 5. Próximos Pasos Inmediatos
1. Normalizar saltos de línea LF en `.agents/skills/content-to-course/subagent_types.json`.
2. Escribir y validar exhaustivamente `tests/test_sweetspot_v35_cta_and_shards.py`.
3. Ejecutar la batería completa de verificación (86 tests previos + nueva suite).
4. Generar `handoff.md` y notificar al Orquestador con `DONE::`.
