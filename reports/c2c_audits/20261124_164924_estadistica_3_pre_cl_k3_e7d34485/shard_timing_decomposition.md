### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `18` | **Mediana de Pared:** `113.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_17` (`83.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_01** | `151.0s` | `93.0s` | `58.0s` | `2 (1)` | `5` | `[TPL-DYNAMIC-RATIONALE], [TPL-STATIC-OPT], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_05** | `149.0s` | `105.0s` | `44.0s` | `2 (1)` | `6` | `[TPL-DRY], NameError: name 'Var' is not defined` | Remediación (1 fallos) |
| **Shard Author shard_04** | `135.0s` | `96.0s` | `39.0s` | `2 (1)` | `2` | `[TPL-DYNAMIC-RATIONALE], [TPL-ORPHAN-VARS], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_16** | `129.0s` | `73.0s` | `56.0s` | `3 (2)` | `5` | `SyntaxError en shard_16_data.py (Línea 170, Columna 38): unexpected character after line continuation character , [TPL-STEM-VARIANT-PARITY]` | Remediación (2 fallos) |
| **Shard Author shard_08** | `121.0s` | `84.0s` | `37.0s` | `2 (1)` | `3` | `[TPL-STEM-SYMBOL-PARITY], [TPL-ORPHAN-VARS], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_02** | `117.0s` | `78.0s` | `39.0s` | `2 (1)` | `2` | `[TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_18** | `117.0s` | `86.0s` | `31.0s` | `2 (1)` | `2` | `[TPL-ORPHAN-VARS], [TPL-M20-PROOF-DAG], [TPL-ASM]` | Remediación (1 fallos) |
| **Shard Author shard_11** | `116.0s` | `79.0s` | `37.0s` | `2 (1)` | `3` | `[TPL-DYNAMIC-RATIONALE], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `113.0s` | `98.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_14** | `111.0s` | `99.0s` | `12.0s` | `1 (0)` | `3` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_07** | `110.0s` | `92.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_10** | `109.0s` | `72.0s` | `37.0s` | `2 (1)` | `2` | `[TPL-DYNAMIC-RATIONALE], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_03** | `104.0s` | `90.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_13** | `103.0s` | `74.0s` | `29.0s` | `2 (1)` | `1` | `[TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (1 fallos) |
| **Shard Author shard_15** | `103.0s` | `90.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_09** | `95.0s` | `59.0s` | `36.0s` | `2 (1)` | `4` | `[TPL-MS-ABSOLUTE-WORD-BIAS], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_12** | `92.0s` | `80.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_17** | `83.0s` | `68.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `1` | **Mediana de Pared:** `46.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-06** | `46.0s` | `32.0s` | `14.0s` | `1 (0)` | `4` | `0 errores` | Parche aplicado exitosamente |