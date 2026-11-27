### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `11` | **Mediana de Pared:** `106.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_06` (`74.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_08** | `170.0s` | `84.0s` | `86.0s` | `2 (1)` | `0` | `[TPL-MS-CONDITIONAL-DISTRACTOR], [TPL-KATEX], [INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_11** | `160.0s` | `85.0s` | `75.0s` | `4 (3)` | `4` | `SyntaxError en shard_11_data.py (Línea 287, Columna 115): f-string: single '}' is not allowed , [TPL-ORPHAN-VARS], [TPL-STEM-EQUATION-PARITY]` | Remediación (3 fallos) |
| **Shard Author shard_04** | `132.0s` | `95.0s` | `37.0s` | `2 (1)` | `2` | `[TPL-STEM-SYMBOL-PARITY], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_10** | `131.0s` | `75.0s` | `56.0s` | `2 (1)` | `10` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-SYMBOL-PARITY], [TPL-MS-CONDITIONAL-DISTRACTOR]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `117.0s` | `82.0s` | `35.0s` | `2 (1)` | `4` | `[TPL-STEM-EQUATION-PARITY], [TPL-TAUTOLOGICAL-IDENTITY], [TPL-DIAG-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `106.0s` | `73.0s` | `33.0s` | `2 (1)` | `1` | `[TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_03** | `105.0s` | `93.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_02** | `103.0s` | `90.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_09** | `102.0s` | `87.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_05** | `86.0s` | `73.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_06** | `74.0s` | `60.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `1` | **Mediana de Pared:** `65.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer C-03** | `65.0s` | `54.0s` | `11.0s` | `1 (0)` | `6` | `0 errores` | Parche aplicado exitosamente |