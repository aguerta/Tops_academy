### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `25` | **Mediana de Pared:** `155.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_05` (`111.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_16** | `219.0s` | `132.0s` | `87.0s` | `2 (1)` | `8` | `[INVARIANT], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_14** | `210.0s` | `135.0s` | `75.0s` | `2 (1)` | `3` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-SYMBOL-PARITY], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_12** | `203.0s` | `144.0s` | `59.0s` | `2 (1)` | `1` | `[TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_10** | `202.0s` | `108.0s` | `94.0s` | `2 (1)` | `0` | `[TPL-DYNAMIC-RATIONALE], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_11** | `196.0s` | `124.0s` | `72.0s` | `2 (1)` | `2` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_08** | `189.0s` | `108.0s` | `81.0s` | `1 (1)` | `0` | `[TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_09** | `176.0s` | `100.0s` | `76.0s` | `2 (1)` | `8` | `[TPL-STEM-SYMBOL-PARITY], [VERIFIER-TAUTOLOGY-DETECTED], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_02** | `168.0s` | `84.0s` | `84.0s` | `2 (1)` | `0` | `[INVARIANT], [TPL-DEGENERATE-LITERAL-COND], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_03** | `168.0s` | `126.0s` | `42.0s` | `2 (1)` | `2` | `[VERIFIER-TAUTOLOGY-DETECTED], [TPL-D4], [TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `164.0s` | `91.0s` | `73.0s` | `2 (1)` | `1` | `[TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_12** | `156.0s` | `129.0s` | `27.0s` | `1 (1)` | `0` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_14** | `156.0s` | `128.0s` | `28.0s` | `1 (1)` | `0` | `[R-20]` | Remediación (1 fallos) |
| **Shard Author shard_13** | `155.0s` | `126.0s` | `29.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_13** | `153.0s` | `129.0s` | `24.0s` | `1 (1)` | `0` | `[TPL-MS-CONDITIONAL-DISTRACTOR], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `153.0s` | `112.0s` | `41.0s` | `2 (1)` | `2` | `[TPL-DRY], NameError: name 'Var' is not defined` | Remediación (1 fallos) |
| **Shard Author shard_11** | `150.0s` | `105.0s` | `45.0s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_01** | `147.0s` | `103.0s` | `44.0s` | `2 (1)` | `6` | `[INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `143.0s` | `140.0s` | `3.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_15** | `141.0s` | `117.0s` | `24.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_07** | `140.0s` | `106.0s` | `34.0s` | `2 (1)` | `4` | `[TPL-D4], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_17** | `127.0s` | `90.0s` | `37.0s` | `2 (1)` | `3` | `[TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_15** | `126.0s` | `88.2s` | `37.8s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_04** | `116.0s` | `98.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_05** | `111.0s` | `97.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_09** | `109.0s` | `76.3s` | `32.7s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `4` | **Mediana de Pared:** `58.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-01** | `68.0s` | `42.0s` | `26.0s` | `2 (0)` | `9` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-01** | `58.0s` | `32.0s` | `26.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-07** | `52.0s` | `28.0s` | `24.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-02** | `46.0s` | `28.0s` | `18.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |