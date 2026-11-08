### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `30` | **Mediana de Pared:** `488.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_14` (`297.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_01** | `773.0s` | `303.0s` | `485.0s` | `7 (7)` | `12` | `[R-15], [TPL-ASM], [TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (7 fallos) |
| **Shard Author shard_18** | `770.0s` | `453.0s` | `344.0s` | `5 (4)` | `6` | `[TPL-DRY], [TPL-VAR], [R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (4 fallos) |
| **Shard Author shard_24** | `770.0s` | `343.0s` | `448.0s` | `4 (4)` | `4` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (4 fallos) |
| **Shard Author shard_07** | `749.0s` | `287.0s` | `472.0s` | `4 (2)` | `3` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_29** | `718.0s` | `407.0s` | `327.0s` | `4 (3)` | `4` | `[TPL-CROSS], [TPL-VAR], [R-16]` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_16** | `658.0s` | `289.0s` | `398.0s` | `6 (5)` | `3` | `[TPL-VAR], [R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (5 fallos) |
| **Shard Author shard_26** | `650.0s` | `327.0s` | `342.0s` | `5 (4)` | `10` | `[R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (4 fallos) |
| **Shard Author shard_20** | `613.0s` | `373.0s` | `264.0s` | `8 (7)` | `11` | `[R-15], [TPL-VAR], [TPL-KATEX]` | Overthinking / Exploración lenta Pre-Compile; Remediación (7 fallos) |
| **Shard Author shard_21** | `606.0s` | `370.0s` | `260.0s` | `4 (3)` | `4` | `SyntaxError en shard_21_data.py (L�nea 121, Columna 8): (unicode error) 'unicodeescape' codec can't decode bytes in position 84-85: truncated \xXX escape, [TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_23** | `587.0s` | `386.0s` | `223.0s` | `4 (3)` | `8` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_28** | `572.0s` | `312.0s` | `277.0s` | `5 (4)` | `9` | `[R-16]` | Overthinking / Exploración lenta Pre-Compile; Remediación (4 fallos) |
| **Shard Author shard_22** | `563.0s` | `287.0s` | `299.0s` | `3 (2)` | `1` | `[TPL-DRY], [TPL-VAR], [TPL-CROSS]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_27** | `504.0s` | `276.0s` | `246.0s` | `4 (3)` | `8` | `[R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_25** | `503.0s` | `322.0s` | `201.0s` | `6 (5)` | `6` | `ValueError'. Los verificadores deben retornar booleanos sin sentencias 'raise' de depuraci�n., [R-15]` | Overthinking / Exploración lenta Pre-Compile; Remediación (5 fallos) |
| **Shard Author shard_13** | `488.0s` | `270.0s` | `223.0s` | `3 (2)` | `3` | `[R-16]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_05** | `468.0s` | `441.0s` | `39.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_10** | `440.0s` | `334.0s` | `114.0s` | `4 (3)` | `3` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_17** | `428.0s` | `276.0s` | `180.0s` | `3 (2)` | `1` | `[R-26], [R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_08** | `408.0s` | `258.0s` | `160.0s` | `3 (2)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_06** | `388.0s` | `309.0s` | `90.0s` | `3 (2)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_02** | `384.0s` | `261.0s` | `137.0s` | `3 (2)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_04** | `361.0s` | `238.0s` | `136.0s` | `3 (2)` | `3` | `[R-15]` | Remediación (2 fallos) |
| **Shard Author shard_15** | `361.0s` | `261.0s` | `103.0s` | `3 (2)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_19** | `356.0s` | `238.0s` | `143.0s` | `4 (3)` | `5` | `0 errores` | Remediación (3 fallos) |
| **Shard Author shard_30** | `340.0s` | `284.0s` | `59.0s` | `3 (2)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_12** | `323.0s` | `250.0s` | `79.0s` | `2 (1)` | `4` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_09** | `319.0s` | `288.0s` | `40.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_03** | `304.0s` | `305.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_14** | `297.0s` | `288.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_11** | `275.0s` | `249.0s` | `33.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `2` | **Mediana de Pared:** `13.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer (HAB05)** | `13.0s` | `9.1s` | `3.9s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (C04)** | `9.0s` | `6.3s` | `2.7s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |