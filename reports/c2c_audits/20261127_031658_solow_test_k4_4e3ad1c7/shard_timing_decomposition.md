### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `19` | **Mediana de Pared:** `119.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_15` (`86.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_06** | `201.0s` | `109.0s` | `92.0s` | `2 (1)` | `0` | `[VERIFIER-TAUTOLOGY-DETECTED], [TPL-STEM-EQUATION-PARITY], [TPL-DIAG-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_05** | `184.0s` | `113.0s` | `71.0s` | `2 (1)` | `0` | `[TPL-DYNAMIC-RATIONALE], [TPL-ORPHAN-VARS], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `173.0s` | `109.0s` | `64.0s` | `3 (2)` | `8` | `[TPL-ORPHAN-VARS], [TPL-DIGIT-PLACEHOLDER-CONCAT], [TPL-STEM-EQUATION-PARITY]` | Remediación (2 fallos) |
| **Shard Author shard_03** | `153.0s` | `124.0s` | `29.0s` | `2 (1)` | `1` | `[TPL-ORPHAN-VARS], [TPL-DIAG-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `151.0s` | `107.0s` | `44.0s` | `2 (1)` | `5` | `[TPL-ORPHAN-VARS], [TPL-STATIC-OPT], [TPL-DIAG-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `147.0s` | `94.0s` | `53.0s` | `2 (1)` | `8` | `[TPL-ORPHAN-VARS], [TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_19** | `146.0s` | `110.0s` | `36.0s` | `2 (1)` | `1` | `[TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `129.0s` | `115.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_10** | `120.0s` | `106.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_09** | `119.0s` | `77.0s` | `42.0s` | `2 (1)` | `3` | `[TPL-M20-PROOF-DAG], [TPL-STEM-VARIANT-PARITY], [TPL-ASM]` | Remediación (1 fallos) |
| **Shard Author shard_13** | `113.0s` | `83.0s` | `30.0s` | `2 (1)` | `1` | `[TPL-ASM]` | Remediación (1 fallos) |
| **Shard Author shard_11** | `111.0s` | `97.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_12** | `109.0s` | `95.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_02** | `108.0s` | `95.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_18** | `108.0s` | `94.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_16** | `101.0s` | `83.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_17** | `97.0s` | `84.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_14** | `93.0s` | `80.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_15** | `86.0s` | `73.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `8` | **Mediana de Pared:** `50.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer C-09** | `149.0s` | `134.0s` | `15.0s` | `1 (0)` | `15` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-01** | `95.0s` | `83.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-04** | `54.0s` | `40.0s` | `14.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-10** | `50.0s` | `38.0s` | `12.0s` | `1 (0)` | `3` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-01** | `43.0s` | `30.0s` | `13.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-03** | `34.0s` | `22.0s` | `12.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-03** | `33.0s` | `21.0s` | `12.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-01** | `28.0s` | `15.0s` | `13.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |