### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `27` | **Mediana de Pared:** `130.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_21` (`87.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_11** | `196.0s` | `101.0s` | `95.0s` | `3 (3)` | `6` | `[TPL-DYNAMIC-RATIONALE], [TPL-D4], [TPL-ORPHAN-VARS]` | Remediación (3 fallos) |
| **Shard Author shard_18** | `187.0s` | `112.0s` | `75.0s` | `2 (1)` | `0` | `[TPL-STEM-VARIANT-PARITY], [TPL-MS-CONDITIONAL-DISTRACTOR]` | Remediación (1 fallos) |
| **Shard Author shard_03** | `181.0s` | `131.0s` | `50.0s` | `2 (1)` | `4` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-SYMBOL-PARITY], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `169.0s` | `111.0s` | `58.0s` | `2 (1)` | `3` | `[TPL-STEM-EQUATION-PARITY], [TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `157.0s` | `104.0s` | `53.0s` | `2 (1)` | `8` | `[TPL-STEM-GRAMMAR]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `154.0s` | `93.0s` | `61.0s` | `2 (1)` | `4` | `[VERIFIER-TAUTOLOGY-DETECTED], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_26** | `152.0s` | `86.0s` | `66.0s` | `3 (2)` | `3` | `[TPL-ORPHAN-VARS], [TPL-STEM-SYMBOL-PARITY], [TPL-DYNAMIC-RATIONALE]` | Remediación (2 fallos) |
| **Shard Author shard_12** | `148.0s` | `96.0s` | `52.0s` | `2 (1)` | `3` | `[TPL-ORPHAN-VARS], [VERIFIER-TAUTOLOGY-DETECTED]` | Remediación (1 fallos) |
| **Shard Author shard_02** | `143.0s` | `104.0s` | `39.0s` | `2 (1)` | `2` | `[TPL-TAUTOLOGICAL-IDENTITY], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_23** | `137.0s` | `91.0s` | `46.0s` | `2 (1)` | `4` | `[TPL-MS-CONDITIONAL-DISTRACTOR], [INVARIANT], [TPL-DEGENERATE-LITERAL-COND]` | Remediación (1 fallos) |
| **Shard Author shard_17** | `135.0s` | `91.0s` | `44.0s` | `2 (1)` | `1` | `[TPL-ORPHAN-VARS]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `132.0s` | `115.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_22** | `131.0s` | `98.0s` | `33.0s` | `2 (1)` | `2` | `[TPL-ORPHAN-VARS], [TPL-STEM-SYMBOL-PARITY], [TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_13** | `130.0s` | `95.0s` | `35.0s` | `2 (1)` | `3` | `[INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_27** | `120.0s` | `79.0s` | `41.0s` | `2 (1)` | `4` | `[INVARIANT], [TPL-DEGENERATE-LITERAL-COND]` | Remediación (1 fallos) |
| **Shard Author shard_10** | `119.0s` | `104.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_05** | `118.0s` | `104.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_09** | `118.0s` | `106.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_20** | `111.0s` | `98.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_19** | `109.0s` | `96.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_07** | `106.0s` | `89.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_25** | `98.0s` | `66.0s` | `32.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_16** | `96.0s` | `79.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_15** | `95.0s` | `78.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_14** | `95.0s` | `81.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_24** | `91.0s` | `77.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_21** | `87.0s` | `72.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `4` | **Mediana de Pared:** `72.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-12** | `97.0s` | `47.0s` | `50.0s` | `2 (1)` | `2` | `[TPL-ORPHAN-VARS], [TPL-STEM-EQUATION-PARITY]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer Hab-07** | `72.0s` | `31.0s` | `41.0s` | `2 (1)` | `2` | `[TPL-STEM-EQUATION-PARITY]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer Hab-11** | `54.0s` | `41.0s` | `13.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-07** | `53.0s` | `38.0s` | `15.0s` | `1 (0)` | `6` | `0 errores` | Parche aplicado exitosamente |