### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `12` | **Mediana de Pared:** `149.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_04` (`98.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_12** | `204.0s` | `88.0s` | `116.0s` | `3 (2)` | `1` | `[TPL-DYNAMIC-RATIONALE], [TPL-DIGIT-PLACEHOLDER-CONCAT], [TPL-VAR]` | Remediación (2 fallos) |
| **Shard Author shard_02** | `184.0s` | `88.0s` | `96.0s` | `2 (1)` | `1` | `[TPL-ORPHAN-VARS], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_10** | `176.0s` | `106.0s` | `70.0s` | `2 (1)` | `3` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_05** | `154.0s` | `87.0s` | `67.0s` | `2 (1)` | `5` | `[TPL-ORPHAN-VARS], [R-19], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_09** | `152.0s` | `97.0s` | `55.0s` | `2 (1)` | `2` | `[TPL-ORPHAN-VARS], [TPL-CONST-DISTRACTOR]` | Remediación (1 fallos) |
| **Shard Author shard_11** | `149.0s` | `94.0s` | `55.0s` | `2 (1)` | `3` | `[TPL-STEM-SYMBOL-PARITY], [TPL-ORPHAN-VARS], [TPL-CONST-DISTRACTOR]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `138.0s` | `111.0s` | `27.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_03** | `129.0s` | `70.0s` | `59.0s` | `2 (1)` | `2` | `[TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `112.0s` | `71.0s` | `41.0s` | `2 (1)` | `1` | `[TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `110.0s` | `73.0s` | `37.0s` | `2 (1)` | `2` | `[TPL-M20-ADVERSARIAL], [TPL-ASM], [TPL-D3]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `103.0s` | `69.0s` | `34.0s` | `2 (1)` | `2` | `[TPL-STEM-SYMBOL-PARITY], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `98.0s` | `78.0s` | `20.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `4` | **Mediana de Pared:** `71.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-07** | `131.0s` | `81.0s` | `50.0s` | `2 (1)` | `10` | `[TPL-ORPHAN-VARS], [TPL-KATEX-SYMPY-LEAK], [TPL-D3]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer C-11** | `71.0s` | `56.0s` | `15.0s` | `1 (0)` | `4` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-05** | `53.0s` | `40.0s` | `13.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-05** | `41.0s` | `29.0s` | `12.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |