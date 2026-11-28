### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `21` | **Mediana de Pared:** `108.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_15` (`69.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_06** | `324.0s` | `114.0s` | `210.0s` | `4 (3)` | `5` | `[TPL-D4], [TPL-DIGIT-PLACEHOLDER-CONCAT], [INVARIANT]` | Remediación (3 fallos) |
| **Shard Author shard_07** | `200.0s` | `98.0s` | `102.0s` | `3 (2)` | `9` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (2 fallos) |
| **Shard Author shard_12** | `171.0s` | `85.0s` | `86.0s` | `2 (1)` | `0` | `[TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `148.0s` | `102.0s` | `46.0s` | `2 (1)` | `3` | `[TPL-MS-CONDITIONAL-DISTRACTOR], [TPL-STEM-EQUATION-PARITY], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `147.0s` | `105.0s` | `42.0s` | `2 (1)` | `2` | `[TPL-STEM-EQUATION-PARITY], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_05** | `147.0s` | `89.0s` | `58.0s` | `2 (1)` | `11` | `[TPL-DIGIT-PLACEHOLDER-CONCAT], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_02** | `135.0s` | `99.0s` | `36.0s` | `2 (1)` | `3` | `[TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_03** | `127.0s` | `97.0s` | `30.0s` | `2 (1)` | `2` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `122.0s` | `99.0s` | `23.0s` | `2 (1)` | `1` | `SyntaxError en shard_01_data.py (Línea 313, Columna 17): closing parenthesis '}' does not match opening parenthesis '[' on line 302` | Remediación (1 fallos) |
| **Shard Author shard_16** | `119.0s` | `104.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_14** | `108.0s` | `94.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_19** | `103.0s` | `89.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_21** | `102.0s` | `87.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_20** | `99.0s` | `85.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_09** | `87.0s` | `74.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_13** | `86.0s` | `75.0s` | `11.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_18** | `85.0s` | `74.0s` | `11.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_10** | `82.0s` | `68.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_11** | `79.0s` | `67.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_17** | `76.0s` | `63.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_15** | `69.0s` | `58.0s` | `11.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `6` | **Mediana de Pared:** `54.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-08** | `124.0s` | `102.0s` | `22.0s` | `1 (0)` | `7` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-03** | `57.0s` | `46.0s` | `11.0s` | `1 (0)` | `4` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-03** | `54.0s` | `43.0s` | `11.0s` | `1 (0)` | `3` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-10** | `51.0s` | `38.0s` | `13.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-11** | `46.0s` | `31.0s` | `15.0s` | `1 (0)` | `3` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-09** | `41.0s` | `27.0s` | `14.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |