### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `10` | **Mediana de Pared:** `238.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_10` (`81.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_05** | `258.0s` | `107.0s` | `151.0s` | `3 (2)` | `1` | `[TPL-ORPHAN-VARS], [TPL-DRY], [TPL-VAR]` | Remediación (2 fallos) |
| **Shard Author shard_01** | `250.0s` | `128.0s` | `122.0s` | `2 (1)` | `0` | `[TPL-STEM-GRAMMAR], [INVARIANT], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `249.0s` | `127.0s` | `122.0s` | `2 (1)` | `0` | `[TPL-STEM-GRAMMAR], [TPL-CONST-DISTRACTOR], [VERIFIER-TAUTOLOGY-DETECTED]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `244.0s` | `119.0s` | `125.0s` | `2 (1)` | `0` | `[TPL-DYNAMIC-RATIONALE], [TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `238.0s` | `114.0s` | `124.0s` | `3 (2)` | `12` | `[TPL-ORPHAN-VARS], [R-19], [TPL-VAR]` | Remediación (2 fallos) |
| **Shard Author shard_03** | `228.0s` | `110.0s` | `118.0s` | `2 (1)` | `0` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-VARIANT-PARITY], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_09** | `218.0s` | `99.0s` | `119.0s` | `3 (2)` | `1` | `[INVARIANT], [TPL-STATIC-OPT]` | Remediación (2 fallos) |
| **Shard Author shard_02** | `163.0s` | `111.0s` | `52.0s` | `2 (1)` | `2` | `[TPL-ORPHAN-VARS], [VERIFIER-TAUTOLOGY-DETECTED]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `148.0s` | `97.0s` | `51.0s` | `2 (1)` | `2` | `[VERIFIER-TAUTOLOGY-DETECTED], [TPL-CONST-DISTRACTOR], [TPL-CROSS]` | Remediación (1 fallos) |
| **Shard Author shard_10** | `81.0s` | `70.0s` | `11.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `2` | **Mediana de Pared:** `151.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-05** | `151.0s` | `99.0s` | `52.0s` | `2 (1)` | `11` | `[TPL-ORPHAN-VARS], [INVARIANT], [TPL-D4]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer C-06** | `38.0s` | `25.0s` | `13.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |