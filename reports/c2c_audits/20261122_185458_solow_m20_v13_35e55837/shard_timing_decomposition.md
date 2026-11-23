### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `20` | **Mediana de Pared:** `126.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_19` (`76.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_05** | `196.0s` | `98.0s` | `98.0s` | `2 (1)` | `5` | `[TPL-ORPHAN-VARS], [VERIFIER-TAUTOLOGY-DETECTED], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `172.0s` | `97.0s` | `75.0s` | `2 (1)` | `2` | `[TPL-ORPHAN-VARS], [VERIFIER-TAUTOLOGY-DETECTED], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_09** | `156.0s` | `70.0s` | `86.0s` | `3 (2)` | `5` | `[TPL-ORPHAN-VARS], [TPL-STEM-SYMBOL-PARITY], [INVARIANT]` | Remediación (2 fallos) |
| **Shard Author shard_01** | `150.0s` | `81.0s` | `69.0s` | `2 (1)` | `2` | `[INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_18** | `147.0s` | `86.0s` | `61.0s` | `2 (1)` | `3` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-SYMBOL-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_02** | `146.0s` | `78.0s` | `68.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_03** | `139.0s` | `84.0s` | `55.0s` | `2 (1)` | `1` | `[TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_12** | `137.0s` | `73.0s` | `64.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [INVARIANT], [TPL-ASM]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `131.0s` | `77.0s` | `54.0s` | `2 (1)` | `3` | `[TPL-ORPHAN-VARS], [INVARIANT], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `126.0s` | `70.0s` | `56.0s` | `2 (1)` | `1` | `[TPL-ORPHAN-VARS], [VERIFIER-TAUTOLOGY-DETECTED], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `121.0s` | `86.0s` | `35.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_11** | `117.0s` | `71.0s` | `46.0s` | `2 (1)` | `4` | `[TPL-ORPHAN-VARS]` | Remediación (1 fallos) |
| **Shard Author shard_10** | `113.0s` | `72.0s` | `41.0s` | `2 (1)` | `2` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [TPL-ASM]` | Remediación (1 fallos) |
| **Shard Author shard_13** | `112.0s` | `85.0s` | `27.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_16** | `109.0s` | `66.0s` | `43.0s` | `2 (1)` | `2` | `[TPL-ORPHAN-VARS]` | Remediación (1 fallos) |
| **Shard Author shard_20** | `97.0s` | `63.0s` | `34.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_17** | `95.0s` | `76.0s` | `19.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_14** | `81.0s` | `65.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_15** | `80.0s` | `64.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_19** | `76.0s` | `60.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `6` | **Mediana de Pared:** `45.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-08** | `101.0s` | `98.0s` | `3.0s` | `1 (1)` | `9` | `[TPL-DYNAMIC-RATIONALE], [TPL-ORPHAN-VARS], [TPL-TAUTOLOGICAL-IDENTITY]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer Hab-09** | `48.0s` | `24.0s` | `24.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-04** | `45.0s` | `22.0s` | `23.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-08** | `0.0s` | `0.0s` | `0.0s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-08** | `0.0s` | `0.0s` | `0.0s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-08** | `0.0s` | `0.0s` | `0.0s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |