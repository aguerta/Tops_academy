### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `20` | **Mediana de Pared:** `133.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_01` (`107.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_02** | `319.0s` | `99.0s` | `220.0s` | `3 (2)` | `5` | `[TPL-ORPHAN-VARS], [TPL-VAR], [INVARIANT]` | Remediación (2 fallos) |
| **Shard Author shard_05** | `167.0s` | `88.0s` | `79.0s` | `2 (1)` | `1` | `[TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `165.0s` | `93.0s` | `72.0s` | `2 (1)` | `5` | `[VERIFIER-TAUTOLOGY-DETECTED], [TPL-STATIC-OPT], [R-19]` | Remediación (1 fallos) |
| **Shard Author shard_18** | `144.0s` | `78.0s` | `66.0s` | `2 (1)` | `8` | `[TPL-ORPHAN-VARS], [TPL-VAR], [TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `143.0s` | `72.0s` | `71.0s` | `2 (1)` | `6` | `[INVARIANT], [TPL-KATEX-SYMPY-LEAK], [TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (1 fallos) |
| **Shard Author shard_17** | `142.0s` | `69.0s` | `73.0s` | `2 (1)` | `6` | `[TPL-STEM-SYMBOL-PARITY], [TPL-STEM-VARIANT-PARITY], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_09** | `142.0s` | `90.0s` | `52.0s` | `2 (1)` | `4` | `[TPL-DYNAMIC-RATIONALE], [R-19], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_15** | `138.0s` | `84.0s` | `54.0s` | `2 (1)` | `3` | `[TPL-ORPHAN-VARS], [TPL-STEM-SYMBOL-PARITY], [TPL-CONST-DISTRACTOR]` | Remediación (1 fallos) |
| **Shard Author shard_13** | `133.0s` | `87.0s` | `46.0s` | `2 (1)` | `5` | `[R-19], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `133.0s` | `86.0s` | `47.0s` | `2 (1)` | `1` | `[TPL-ORPHAN-VARS], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_14** | `132.0s` | `86.0s` | `46.0s` | `2 (1)` | `2` | `[TPL-ORPHAN-VARS], [TPL-CONST-DISTRACTOR]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `125.0s` | `96.0s` | `29.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_11** | `124.0s` | `86.0s` | `38.0s` | `2 (1)` | `2` | `[TPL-ORPHAN-VARS], [TPL-CONST-DISTRACTOR]` | Remediación (1 fallos) |
| **Shard Author shard_10** | `123.0s` | `68.0s` | `55.0s` | `2 (1)` | `8` | `[TPL-STEM-SYMBOL-PARITY], [R-19], [TPL-STEM-DERIV-GIVEAWAY]` | Remediación (1 fallos) |
| **Shard Author shard_20** | `122.0s` | `69.0s` | `53.0s` | `2 (1)` | `4` | `[TPL-DYNAMIC-RATIONALE], [VERIFIER-TAUTOLOGY-DETECTED], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_16** | `117.0s` | `76.0s` | `41.0s` | `2 (1)` | `1` | `[TPL-ASM]` | Remediación (1 fallos) |
| **Shard Author shard_12** | `114.0s` | `72.0s` | `42.0s` | `2 (1)` | `3` | `[TPL-ORPHAN-VARS], [TPL-STEM-SYMBOL-PARITY], [TPL-CONST-DISTRACTOR]` | Remediación (1 fallos) |
| **Shard Author shard_03** | `111.0s` | `86.0s` | `25.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_19** | `110.0s` | `71.0s` | `39.0s` | `2 (1)` | `2` | `[TPL-ORPHAN-VARS], [TPL-CONST-DISTRACTOR]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `107.0s` | `78.0s` | `29.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `7` | **Mediana de Pared:** `40.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-07** | `156.0s` | `110.0s` | `46.0s` | `2 (1)` | `9` | `[TPL-ORPHAN-VARS], [TPL-DYNAMIC-RATIONALE], [TPL-STATIC-OPT]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer C-05** | `50.0s` | `36.0s` | `14.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-03** | `49.0s` | `34.0s` | `15.0s` | `1 (0)` | `3` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-05** | `40.0s` | `26.0s` | `14.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-05** | `36.0s` | `22.0s` | `14.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-01** | `35.0s` | `22.0s` | `13.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-10** | `34.0s` | `22.0s` | `12.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |