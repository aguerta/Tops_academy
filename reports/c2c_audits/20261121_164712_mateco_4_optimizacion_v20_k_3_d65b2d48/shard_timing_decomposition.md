### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `21` | **Mediana de Pared:** `194.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_09` (`85.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_05** | `368.0s` | `105.0s` | `263.0s` | `4 (3)` | `3` | `[TPL-VERIFIER-UNSOUND], [TPL-STEM-VARIANT-PARITY], [TPL-DRY]` | Remediación (3 fallos) |
| **Shard Author shard_16** | `327.0s` | `120.0s` | `207.0s` | `4 (4)` | `7` | `[TPL-DYNAMIC-RATIONALE], [TPL-ORPHAN-VARS], [TPL-DRY]` | Remediación (4 fallos) |
| **Shard Author shard_18** | `312.0s` | `127.0s` | `185.0s` | `3 (2)` | `5` | `[TPL-ORPHAN-VARS], [TPL-STEM-VARIANT-PARITY], [TPL-KATEX]` | Remediación (2 fallos) |
| **Shard Author shard_19** | `286.0s` | `115.0s` | `171.0s` | `3 (2)` | `3` | `[TPL-ORPHAN-VARS], [TPL-STEM-VARIANT-PARITY], [TPL-DRY]` | Remediación (2 fallos) |
| **Shard Author shard_02** | `278.0s` | `94.0s` | `184.0s` | `3 (2)` | `1` | `[TPL-ORPHAN-VARS], [TPL-VERIFIER-UNSOUND], [TPL-STEM-VARIANT-PARITY]` | Remediación (2 fallos) |
| **Shard Author shard_15** | `276.0s` | `125.0s` | `151.0s` | `3 (2)` | `9` | `[TPL-ORPHAN-VARS], [TPL-STEM-VARIANT-PARITY], [TPL-STEM-GRAMMAR]` | Remediación (2 fallos) |
| **Shard Author shard_17** | `246.0s` | `119.0s` | `127.0s` | `2 (1)` | `0` | `[TPL-KATEX], [TPL-DYNAMIC-RATIONALE], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_10** | `229.0s` | `97.0s` | `132.0s` | `3 (3)` | `6` | `[TPL-ORPHAN-VARS], [TPL-DRY], [TPL-VAR]` | Remediación (3 fallos) |
| **Shard Author shard_01** | `214.0s` | `108.0s` | `106.0s` | `2 (1)` | `2` | `[TPL-ORPHAN-VARS], [INVARIANT], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `209.0s` | `101.0s` | `108.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-STATIC-OPT], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `194.0s` | `94.0s` | `100.0s` | `3 (2)` | `9` | `[TPL-DRY], [R-19], [TPL-VAR]` | Remediación (2 fallos) |
| **Shard Author shard_20** | `190.0s` | `110.0s` | `80.0s` | `2 (1)` | `4` | `[TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_14** | `186.0s` | `84.0s` | `102.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `183.0s` | `75.0s` | `108.0s` | `3 (2)` | `4` | `[TPL-ORPHAN-VARS], [TPL-D4], [TPL-STATIC-OPT]` | Remediación (2 fallos) |
| **Shard Author shard_12** | `181.0s` | `92.0s` | `89.0s` | `2 (1)` | `0` | `[TPL-DYNAMIC-RATIONALE], [TPL-ORPHAN-VARS], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_13** | `178.0s` | `86.0s` | `92.0s` | `2 (1)` | `0` | `[TPL-STATIC-OPT], [INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `172.0s` | `88.0s` | `84.0s` | `3 (2)` | `6` | `[TPL-ORPHAN-VARS], [TPL-STATIC-OPT], [TPL-STEM-VARIANT-PARITY]` | Remediación (2 fallos) |
| **Shard Author shard_11** | `158.0s` | `69.0s` | `89.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-STATIC-OPT], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_21** | `149.0s` | `74.0s` | `75.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-STEM-VARIANT-PARITY], [TPL-STEM-GRAMMAR]` | Remediación (1 fallos) |
| **Shard Author shard_03** | `127.0s` | `105.0s` | `22.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_09** | `85.0s` | `70.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `7` | **Mediana de Pared:** `41.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer C-15** | `78.0s` | `42.0s` | `36.0s` | `2 (1)` | `4` | `[TPL-CONST-DISTRACTOR]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer C-02** | `47.0s` | `30.0s` | `17.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-20** | `42.0s` | `26.0s` | `16.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-10** | `41.0s` | `26.0s` | `15.0s` | `1 (0)` | `3` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-06** | `40.0s` | `21.0s` | `19.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-02** | `39.0s` | `20.0s` | `19.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-02** | `36.0s` | `20.0s` | `16.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |