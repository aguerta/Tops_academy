### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `18` | **Mediana de Pared:** `142.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_15` (`91.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_01** | `226.0s` | `112.0s` | `114.0s` | `2 (1)` | `9` | `[TPL-ORPHAN-VARS], [TPL-STEM-VARIANT-PARITY], [TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `191.0s` | `95.0s` | `96.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-STATIC-OPT], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `175.0s` | `82.0s` | `93.0s` | `2 (1)` | `0` | `[TPL-KATEX-SYMPY-LEAK], [INVARIANT], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `170.0s` | `98.0s` | `72.0s` | `2 (1)` | `2` | `[TPL-ORPHAN-VARS], [TPL-CONST-DISTRACTOR], [TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_18** | `165.0s` | `80.0s` | `85.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-KATEX], [TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_03** | `154.0s` | `102.0s` | `52.0s` | `2 (1)` | `2` | `[TPL-STATIC-OPT], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_13** | `151.0s` | `72.0s` | `79.0s` | `3 (2)` | `6` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-SYMBOL-PARITY], [TPL-ORPHAN-VARS]` | Remediación (2 fallos) |
| **Shard Author shard_05** | `150.0s` | `95.0s` | `55.0s` | `2 (1)` | `3` | `[TPL-STEM-SYMBOL-PARITY], [TPL-STATIC-OPT], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_16** | `142.0s` | `87.0s` | `55.0s` | `2 (1)` | `3` | `[TPL-STEM-SYMBOL-PARITY], [TPL-ORPHAN-VARS], [TPL-CONST-DISTRACTOR]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `140.0s` | `76.0s` | `64.0s` | `2 (1)` | `5` | `[R-19], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_09** | `139.0s` | `83.0s` | `56.0s` | `2 (1)` | `4` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [TPL-ORPHAN-VARS]` | Remediación (1 fallos) |
| **Shard Author shard_02** | `134.0s` | `82.0s` | `52.0s` | `2 (1)` | `4` | `[TPL-ORPHAN-VARS], [INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_17** | `131.0s` | `71.0s` | `60.0s` | `2 (1)` | `5` | `[TPL-STEM-VARIANT-PARITY], [R-19], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_12** | `128.0s` | `70.0s` | `58.0s` | `2 (1)` | `6` | `[TPL-ORPHAN-VARS], [TPL-STATIC-OPT], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_14** | `116.0s` | `75.0s` | `41.0s` | `2 (1)` | `1` | `[TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_10** | `106.0s` | `75.0s` | `31.0s` | `2 (1)` | `1` | `[TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_11** | `105.0s` | `93.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_15** | `91.0s` | `76.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `4` | **Mediana de Pared:** `39.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-08** | `103.0s` | `85.0s` | `18.0s` | `1 (0)` | `7` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-08** | `39.0s` | `22.0s` | `17.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-03** | `36.0s` | `21.0s` | `15.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer H-01** | `34.0s` | `21.0s` | `13.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |