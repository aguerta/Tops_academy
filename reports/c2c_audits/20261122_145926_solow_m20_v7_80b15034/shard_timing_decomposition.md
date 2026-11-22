### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `14` | **Mediana de Pared:** `141.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_08` (`87.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_09** | `267.0s` | `98.0s` | `169.0s` | `3 (2)` | `0` | `[TPL-ORPHAN-VARS], [TPL-CONST-DISTRACTOR], [TPL-VAR]` | Remediación (2 fallos) |
| **Shard Author shard_11** | `213.0s` | `115.0s` | `98.0s` | `2 (1)` | `0` | `[TPL-CONST-DISTRACTOR], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_10** | `194.0s` | `100.0s` | `94.0s` | `2 (1)` | `0` | `[TPL-DYNAMIC-RATIONALE], [TPL-CONST-DISTRACTOR], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_13** | `181.0s` | `108.0s` | `73.0s` | `3 (2)` | `5` | `[TPL-STEM-SYMBOL-PARITY], [TPL-VAR]` | Remediación (2 fallos) |
| **Shard Author shard_06** | `163.0s` | `66.0s` | `97.0s` | `4 (3)` | `6` | `[TPL-STEM-SYMBOL-PARITY], [VERIFIER-TAUTOLOGY-DETECTED], [TPL-D4]` | Remediación (3 fallos) |
| **Shard Author shard_01** | `143.0s` | `77.0s` | `66.0s` | `2 (1)` | `4` | `[TPL-TAUTOLOGICAL-IDENTITY], [TPL-DYNAMIC-RATIONALE], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_14** | `141.0s` | `94.0s` | `47.0s` | `2 (1)` | `3` | `[R-19], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_12** | `138.0s` | `83.0s` | `55.0s` | `2 (1)` | `4` | `[TPL-ORPHAN-VARS], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `129.0s` | `79.0s` | `50.0s` | `2 (1)` | `1` | `[TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `121.0s` | `77.0s` | `44.0s` | `2 (1)` | `1` | `[TPL-ORPHAN-VARS], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_05** | `116.0s` | `80.0s` | `36.0s` | `2 (1)` | `1` | `[INVARIANT], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_03** | `115.0s` | `71.0s` | `44.0s` | `2 (1)` | `1` | `[TPL-ORPHAN-VARS], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_02** | `110.0s` | `66.0s` | `44.0s` | `2 (1)` | `2` | `[R-19], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `87.0s` | `76.0s` | `11.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `3` | **Mediana de Pared:** `48.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-07** | `86.0s` | `73.0s` | `13.0s` | `1 (0)` | `4` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-08** | `48.0s` | `33.0s` | `15.0s` | `1 (0)` | `4` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-09** | `45.0s` | `31.0s` | `14.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |