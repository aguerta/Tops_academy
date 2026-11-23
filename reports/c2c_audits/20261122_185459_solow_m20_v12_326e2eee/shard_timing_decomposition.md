### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `13` | **Mediana de Pared:** `132.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_12` (`99.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_09** | `168.0s` | `85.0s` | `83.0s` | `2 (1)` | `9` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-SYMBOL-PARITY], [TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (1 fallos) |
| **Shard Author shard_02** | `165.0s` | `75.0s` | `90.0s` | `3 (2)` | `3` | `[TPL-ORPHAN-VARS], [VERIFIER-TAUTOLOGY-DETECTED], [TPL-D4]` | Remediación (2 fallos) |
| **Shard Author shard_13** | `158.0s` | `92.0s` | `66.0s` | `2 (1)` | `2` | `[TPL-STEM-SYMBOL-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_05** | `144.0s` | `74.0s` | `70.0s` | `2 (1)` | `6` | `[TPL-DYNAMIC-RATIONALE], [INVARIANT], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `144.0s` | `86.0s` | `58.0s` | `2 (1)` | `4` | `[TPL-ORPHAN-VARS], [TPL-D4], [INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_11** | `135.0s` | `102.0s` | `33.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_10** | `132.0s` | `97.0s` | `35.0s` | `1 (0)` | `1` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_08** | `124.0s` | `79.0s` | `45.0s` | `2 (1)` | `2` | `[TPL-STEM-SYMBOL-PARITY], [TPL-KATEX-SYMPY-LEAK]` | Remediación (1 fallos) |
| **Shard Author shard_03** | `124.0s` | `62.0s` | `62.0s` | `2 (1)` | `6` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `121.0s` | `89.0s` | `32.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_04** | `120.0s` | `75.0s` | `45.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_07** | `107.0s` | `64.0s` | `43.0s` | `2 (1)` | `1` | `[TPL-ORPHAN-VARS], [INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_12** | `99.0s` | `73.0s` | `26.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `5` | **Mediana de Pared:** `46.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-08** | `132.0s` | `78.0s` | `54.0s` | `2 (1)` | `16` | `[TPL-ORPHAN-VARS], [TPL-ADJACENT-PLACEHOLDERS], [TPL-DIGIT-PLACEHOLDER-CONCAT]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer Hab-06** | `61.0s` | `34.0s` | `27.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-01** | `46.0s` | `27.0s` | `19.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-04** | `41.0s` | `23.0s` | `18.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-09** | `39.0s` | `23.0s` | `16.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |