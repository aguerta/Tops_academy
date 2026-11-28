### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `22` | **Mediana de Pared:** `112.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_09` (`77.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_03** | `196.0s` | `107.0s` | `89.0s` | `3 (2)` | `10` | `[TPL-DYNAMIC-RATIONALE], [TPL-UNLABELED-PARAM], [TPL-STEM-EQUATION-PARITY]` | Remediación (2 fallos) |
| **Shard Author shard_18** | `169.0s` | `73.0s` | `96.0s` | `2 (1)` | `8` | `[INVARIANT], [TPL-DEGENERATE-LITERAL-COND]` | Remediación (1 fallos) |
| **Shard Author shard_05** | `167.0s` | `103.0s` | `64.0s` | `3 (2)` | `2` | `[TPL-ORPHAN-VARS], [TPL-STEM-EQUATION-PARITY]` | Remediación (2 fallos) |
| **Shard Author shard_04** | `165.0s` | `116.0s` | `49.0s` | `2 (1)` | `9` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_02** | `142.0s` | `101.0s` | `41.0s` | `2 (1)` | `4` | `SyntaxError en shard_02_data.py (Línea 210, Columna 76): unexpected character after line continuation character` | Remediación (1 fallos) |
| **Shard Author shard_11** | `135.0s` | `73.0s` | `62.0s` | `2 (1)` | `6` | `[TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `130.0s` | `96.0s` | `34.0s` | `2 (1)` | `3` | `[TPL-STEM-SYMBOL-PARITY], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `129.0s` | `97.0s` | `32.0s` | `2 (1)` | `4` | `[R-19], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_22** | `128.0s` | `67.0s` | `61.0s` | `2 (1)` | `10` | `[TPL-EXEC-ERROR], [TPL-DRY], NameError: name 'X_t' is not defined \| Acción: Corregir el archivo infractor.` | Remediación (1 fallos) |
| **Shard Author shard_12** | `121.0s` | `95.0s` | `26.0s` | `2 (1)` | `1` | `[TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `112.0s` | `99.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_10** | `111.0s` | `83.0s` | `28.0s` | `2 (1)` | `1` | `[TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `107.0s` | `95.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_15** | `104.0s` | `91.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_19** | `104.0s` | `78.0s` | `26.0s` | `2 (1)` | `1` | `[INVARIANT], [TPL-DEGENERATE-LITERAL-COND]` | Remediación (1 fallos) |
| **Shard Author shard_20** | `104.0s` | `89.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_14** | `100.0s` | `70.0s` | `30.0s` | `2 (1)` | `2` | `[TPL-MS-CONDITIONAL-DISTRACTOR], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_13** | `99.0s` | `87.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_21** | `85.0s` | `64.0s` | `21.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_17** | `81.0s` | `69.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_16** | `80.0s` | `67.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_09** | `77.0s` | `65.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `4` | **Mediana de Pared:** `50.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer C-11** | `51.0s` | `36.0s` | `15.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-02** | `50.0s` | `35.0s` | `15.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-07** | `48.0s` | `35.0s` | `13.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-08** | `48.0s` | `34.0s` | `14.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |