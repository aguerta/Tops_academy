### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `27` | **Mediana de Pared:** `125.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_27` (`72.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_01** | `191.0s` | `138.0s` | `53.0s` | `2 (1)` | `4` | `[TPL-STEM-EQUATION-PARITY], [TPL-STATIC-OPT], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_12** | `184.0s` | `99.0s` | `85.0s` | `2 (1)` | `0` | `[INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_25** | `172.0s` | `91.0s` | `81.0s` | `3 (2)` | `8` | `[TPL-DEGENERATE-LITERAL-COND], [INVARIANT]` | Remediación (2 fallos) |
| **Shard Author shard_03** | `171.0s` | `123.0s` | `48.0s` | `2 (1)` | `3` | `[TPL-STEM-EQUATION-PARITY], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `166.0s` | `129.0s` | `37.0s` | `2 (1)` | `2` | `[R-19], [TPL-STEM-DERIV-GIVEAWAY], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_10** | `156.0s` | `110.0s` | `46.0s` | `2 (1)` | `5` | `[TPL-DYNAMIC-RATIONALE], [TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP]` | Remediación (1 fallos) |
| **Shard Author shard_26** | `156.0s` | `80.0s` | `76.0s` | `2 (1)` | `0` | `[TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (1 fallos) |
| **Shard Author shard_16** | `149.0s` | `103.0s` | `46.0s` | `2 (1)` | `3` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_05** | `148.0s` | `130.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_06** | `144.0s` | `106.0s` | `38.0s` | `2 (1)` | `2` | `[TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_13** | `143.0s` | `71.0s` | `72.0s` | `2 (1)` | `0` | `[TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_23** | `137.0s` | `96.0s` | `41.0s` | `2 (1)` | `4` | `[INVARIANT], [TPL-DEGENERATE-LITERAL-COND]` | Remediación (1 fallos) |
| **Shard Author shard_09** | `126.0s` | `111.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_15** | `125.0s` | `105.0s` | `20.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_19** | `123.0s` | `86.0s` | `37.0s` | `2 (1)` | `3` | `[TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (1 fallos) |
| **Shard Author shard_02** | `119.0s` | `103.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_04** | `119.0s` | `97.0s` | `22.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_17** | `116.0s` | `102.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_18** | `112.0s` | `97.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_24** | `110.0s` | `76.0s` | `34.0s` | `2 (1)` | `2` | `[TPL-STEM-VARIANT-PARITY], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_11** | `108.0s` | `78.0s` | `30.0s` | `2 (1)` | `3` | `[TPL-ORPHAN-VARS], [TPL-STEM-SYMBOL-PARITY], [INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_14** | `102.0s` | `89.0s` | `13.0s` | `1 (0)` | `1` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_08** | `101.0s` | `88.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_20** | `90.0s` | `75.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_21** | `85.0s` | `71.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_22** | `79.0s` | `66.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_27** | `72.0s` | `60.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `2` | **Mediana de Pared:** `69.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-19** | `69.0s` | `57.0s` | `12.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-14** | `55.0s` | `42.0s` | `13.0s` | `1 (0)` | `5` | `0 errores` | Parche aplicado exitosamente |