### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `23` | **Mediana de Pared:** `120.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_15` (`83.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_13** | `317.0s` | `79.0s` | `238.0s` | `7 (6)` | `12` | `[TPL-ORPHAN-VARS], [TPL-STEM-SYMBOL-PARITY], [TPL-STEM-VARIANT-PARITY]` | Remediación (6 fallos) |
| **Shard Author shard_02** | `221.0s` | `121.0s` | `100.0s` | `3 (2)` | `1` | `[INVARIANT], [TPL-DEGENERATE-LITERAL-COND], [TPL-DYNAMIC-RATIONALE]` | Remediación (2 fallos) |
| **Shard Author shard_09** | `218.0s` | `121.0s` | `97.0s` | `4 (3)` | `8` | `SyntaxError en shard_09_data.py (Línea 399, Columna 85): f-string: single '}' is not allowed , [VERIFIER-TAUTOLOGY-DETECTED], [TPL-D4]` | Remediación (3 fallos) |
| **Shard Author shard_06** | `184.0s` | `123.0s` | `61.0s` | `2 (1)` | `10` | `[INVARIANT], [TPL-DEGENERATE-LITERAL-COND], [TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (1 fallos) |
| **Shard Author shard_10** | `174.0s` | `96.0s` | `78.0s` | `2 (1)` | `12` | `[TPL-STEM-SYMBOL-PARITY], [TPL-DYNAMIC-RATIONALE], [VERIFIER-TAUTOLOGY-DETECTED]` | Remediación (1 fallos) |
| **Shard Author shard_21** | `167.0s` | `101.0s` | `66.0s` | `3 (2)` | `3` | `0 errores` | Remediación (2 fallos) |
| **Shard Author shard_03** | `163.0s` | `120.0s` | `43.0s` | `2 (1)` | `3` | `[TPL-KATEX-SYMPY-LEAK]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `158.0s` | `115.0s` | `43.0s` | `2 (1)` | `4` | `[TPL-STEM-SYMBOL-PARITY], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_16** | `157.0s` | `69.0s` | `88.0s` | `4 (3)` | `8` | `[TPL-STATIC-OPT]` | Remediación (3 fallos) |
| **Shard Author shard_07** | `155.0s` | `118.0s` | `37.0s` | `2 (1)` | `2` | `[INVARIANT], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_22** | `123.0s` | `72.0s` | `51.0s` | `3 (2)` | `3` | `[TPL-STEM-SYMBOL-PARITY], [TPL-STATIC-OPT]` | Remediación (2 fallos) |
| **Shard Author shard_01** | `120.0s` | `108.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_12** | `119.0s` | `80.0s` | `39.0s` | `2 (1)` | `2` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_23** | `118.0s` | `82.0s` | `36.0s` | `2 (1)` | `2` | `[TPL-STEM-SYMBOL-PARITY], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_05** | `115.0s` | `103.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_04** | `108.0s` | `94.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_19** | `107.0s` | `90.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_20** | `96.0s` | `81.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_11** | `95.0s` | `81.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_17** | `94.0s` | `80.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_18** | `87.0s` | `73.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_14** | `84.0s` | `72.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_15** | `83.0s` | `70.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `7` | **Mediana de Pared:** `55.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer C-09** | `61.0s` | `39.0s` | `22.0s` | `1 (0)` | `3` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-05** | `56.0s` | `19.0s` | `37.0s` | `2 (1)` | `2` | `[TPL-M20-PROOF-DAG], [TPL-ASM]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer C-09** | `55.0s` | `42.0s` | `13.0s` | `1 (0)` | `3` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-09** | `55.0s` | `43.0s` | `12.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-13** | `45.0s` | `33.0s` | `12.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-09** | `43.0s` | `31.0s` | `12.0s` | `1 (0)` | `3` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-10** | `41.0s` | `29.0s` | `12.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |