### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `31` | **Mediana de Pared:** `150.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_15` (`114.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_16** | `306.0s` | `129.0s` | `177.0s` | `4 (3)` | `19` | `NameError: name 'S_21' is not defined. Did you mean: 'S_1'? , [TPL-STEM-SYMBOL-PARITY], [TPL-DYNAMIC-RATIONALE]` | Remediación (3 fallos); Exploración cross-course: ['est3_exp_arm_c'] |
| **Shard Author shard_13** | `219.0s` | `123.0s` | `96.0s` | `1 (1)` | `0` | `[TPL-MS-ABSOLUTE-WORD-BIAS], [TPL-KATEX], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_16** | `205.0s` | `95.0s` | `110.0s` | `3 (2)` | `4` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-SYMBOL-PARITY], [TPL-STATIC-OPT]` | Remediación (2 fallos) |
| **Shard Author shard_14** | `200.0s` | `101.0s` | `99.0s` | `1 (1)` | `0` | `[TPL-STEM-SYMBOL-PARITY], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_12** | `185.0s` | `109.0s` | `76.0s` | `3 (2)` | `3` | `[TPL-DYNAMIC-RATIONALE], [R-20], [INVARIANT]` | Remediación (2 fallos) |
| **Shard Author shard_11** | `183.0s` | `119.0s` | `64.0s` | `2 (1)` | `1` | `[TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `181.0s` | `97.0s` | `84.0s` | `1 (1)` | `0` | `[TPL-DIAG-RATIONALE], [VERIFIER-TAUTOLOGY-DETECTED], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_09** | `177.0s` | `109.0s` | `68.0s` | `2 (1)` | `6` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-SYMBOL-PARITY], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `176.0s` | `108.0s` | `68.0s` | `3 (2)` | `3` | `SyntaxError en shard_07_data.py (Línea 213, Columna 108): f-string: expecting a valid expression after '{' , [TPL-ORPHAN-VARS], [VERIFIER-TAUTOLOGY-DETECTED]` | Remediación (2 fallos) |
| **Shard Author shard_08** | `176.0s` | `107.0s` | `69.0s` | `2 (1)` | `2` | `[TPL-STEM-SYMBOL-PARITY], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `173.0s` | `115.0s` | `58.0s` | `2 (1)` | `2` | `[TPL-ORPHAN-VARS], [INVARIANT], [TPL-DEGENERATE-LITERAL-COND]` | Remediación (1 fallos) |
| **Shard Author shard_10** | `162.0s` | `101.0s` | `61.0s` | `2 (1)` | `5` | `[TPL-STEM-SYMBOL-PARITY], [TPL-TAUTOLOGICAL-IDENTITY], [TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_17** | `161.0s` | `81.0s` | `80.0s` | `2 (1)` | `0` | `[TPL-STEM-SYMBOL-PARITY], [TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_14** | `154.0s` | `95.0s` | `59.0s` | `3 (2)` | `2` | `SyntaxError en shard_14_data.py (Línea 336, Columna 73): f-string: single '}' is not allowed , SyntaxError en shard_14_data.py (Línea 340, Columna 79): f-string: single '}' is not allowed` | Remediación (2 fallos) |
| **Shard Author shard_02** | `154.0s` | `97.0s` | `57.0s` | `2 (1)` | `6` | `[TPL-STEM-SYMBOL-PARITY], [INVARIANT], [TPL-DEGENERATE-LITERAL-COND]` | Remediación (1 fallos) |
| **Shard Author shard_15** | `150.0s` | `125.0s` | `25.0s` | `1 (0)` | `0` | `0 errores` | Exploración cross-course: ['est3_exp_arm_c'] |
| **Shard Author shard_13** | `149.0s` | `121.0s` | `28.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_06b** | `149.0s` | `99.0s` | `50.0s` | `2 (1)` | `8` | `[INVARIANT], [TPL-DEGENERATE-LITERAL-COND]` | Remediación (1 fallos); Exploración cross-course: ['est3_exp_arm_c'] |
| **Shard Author shard_03** | `138.0s` | `91.0s` | `47.0s` | `2 (1)` | `3` | `[TPL-STEM-SYMBOL-PARITY], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `136.0s` | `114.0s` | `22.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_04** | `130.0s` | `109.0s` | `21.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_05** | `125.0s` | `102.0s` | `23.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_10b** | `122.0s` | `78.0s` | `44.0s` | `2 (1)` | `2` | `[TPL-TAUTOLOGICAL-IDENTITY]` | Remediación (1 fallos); Exploración cross-course: ['est3_exp_arm_c'] |
| **Shard Author shard_17** | `120.0s` | `84.0s` | `36.0s` | `2 (1)` | `3` | `[TPL-D4]` | Remediación (1 fallos); Exploración cross-course: ['est3_exp_arm_c'] |
| **Shard Author shard_15** | `114.0s` | `89.0s` | `25.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_16** | `113.0s` | `79.1s` | `33.9s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_01** | `112.0s` | `78.4s` | `33.6s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_08** | `107.0s` | `74.9s` | `32.1s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_09** | `103.0s` | `72.1s` | `30.9s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_02a** | `101.0s` | `75.0s` | `26.0s` | `2 (1)` | `1` | `[TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos); Exploración cross-course: ['est3_exp_arm_c'] |
| **Shard Author shard_10** | `0.0s` | `0.0s` | `0.0s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `6` | **Mediana de Pared:** `41.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer C-13** | `66.0s` | `51.0s` | `15.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-09** | `61.0s` | `45.0s` | `16.0s` | `1 (0)` | `5` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-10** | `41.0s` | `25.0s` | `16.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-08** | `40.0s` | `30.0s` | `10.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-10** | `33.0s` | `22.0s` | `11.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-10** | `19.0s` | `13.3s` | `5.7s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |