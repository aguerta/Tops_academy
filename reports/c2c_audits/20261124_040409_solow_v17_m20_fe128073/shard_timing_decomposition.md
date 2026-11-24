### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `19` | **Mediana de Pared:** `134.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_15` (`76.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_07** | `206.0s` | `120.0s` | `86.0s` | `2 (1)` | `7` | `[TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `195.0s` | `130.0s` | `65.0s` | `2 (1)` | `4` | `[TPL-ORPHAN-VARS], [TPL-STEM-VARIANT-PARITY], [TPL-DIAG-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_02** | `175.0s` | `96.0s` | `79.0s` | `2 (1)` | `3` | `[TPL-ORPHAN-VARS]` | Remediación (1 fallos) |
| **Shard Author shard_18** | `161.0s` | `93.0s` | `68.0s` | `2 (1)` | `4` | `[R-19]` | Remediación (1 fallos) |
| **Shard Author shard_05** | `160.0s` | `90.0s` | `70.0s` | `2 (1)` | `5` | `[TPL-ORPHAN-VARS], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `159.0s` | `111.0s` | `48.0s` | `2 (1)` | `1` | `[TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_09** | `149.0s` | `102.0s` | `47.0s` | `2 (1)` | `4` | `[TPL-ORPHAN-VARS], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `136.0s` | `86.0s` | `50.0s` | `2 (1)` | `1` | `[TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `134.0s` | `99.0s` | `35.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_11** | `134.0s` | `85.0s` | `49.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_10** | `122.0s` | `100.0s` | `22.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_03** | `115.0s` | `96.0s` | `19.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_12** | `113.0s` | `99.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_13** | `108.0s` | `86.0s` | `22.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_16** | `102.0s` | `90.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_17** | `101.0s` | `81.0s` | `20.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_19** | `93.0s` | `80.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_14** | `92.0s` | `79.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_15** | `76.0s` | `63.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `3` | **Mediana de Pared:** `63.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-05** | `113.0s` | `46.0s` | `67.0s` | `2 (1)` | `7` | `[TPL-STEM-EQUATION-PARITY]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer Hab-03** | `63.0s` | `46.0s` | `17.0s` | `1 (0)` | `5` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-05** | `40.0s` | `27.0s` | `13.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |