### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `33` | **Mediana de Pared:** `372.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_25` (`247.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_30** | `688.0s` | `306.0s` | `402.0s` | `6 (5)` | `10` | `ValueError: could not convert string to float: 'P \\le 0.0118', [R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (5 fallos) |
| **Shard Author shard_14** | `580.0s` | `257.0s` | `328.0s` | `4 (3)` | `3` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_32** | `529.0s` | `304.0s` | `243.0s` | `4 (3)` | `6` | `[R-19], [R-16]` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_29** | `511.0s` | `376.0s` | `156.0s` | `3 (2)` | `5` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_33** | `497.0s` | `345.0s` | `168.0s` | `3 (2)` | `6` | `[R-16]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_22** | `478.0s` | `321.0s` | `184.0s` | `4 (3)` | `9` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_18** | `452.0s` | `331.0s` | `152.0s` | `4 (3)` | `5` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_11** | `446.0s` | `337.0s` | `117.0s` | `2 (1)` | `3` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_20** | `423.0s` | `264.0s` | `188.0s` | `3 (2)` | `2` | `[R-16]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_27** | `409.0s` | `313.0s` | `118.0s` | `3 (2)` | `5` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_06** | `405.0s` | `310.0s` | `107.0s` | `4 (2)` | `3` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_21** | `403.0s` | `307.0s` | `124.0s` | `3 (2)` | `3` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_26** | `402.0s` | `329.0s` | `96.0s` | `3 (2)` | `4` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_12** | `401.0s` | `226.0s` | `182.0s` | `5 (4)` | `4` | `ValueError: could not convert string to float: 'P \\le 0.1512', [TPL-DRY], [TPL-VAR]` | Remediación (4 fallos) |
| **Shard Author shard_23** | `395.0s` | `316.0s` | `105.0s` | `3 (2)` | `4` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_28** | `375.0s` | `252.0s` | `145.0s` | `3 (2)` | `2` | `[R-26]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_24** | `372.0s` | `325.0s` | `72.0s` | `4 (3)` | `3` | `ValueError'. Los verificadores deben retornar booleanos sin sentencias 'raise' de depuraci�n.` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_19** | `369.0s` | `338.0s` | `61.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_31** | `360.0s` | `337.0s` | `42.0s` | `2 (1)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_10** | `357.0s` | `301.0s` | `65.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_02** | `327.0s` | `236.0s` | `106.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_15** | `306.0s` | `258.0s` | `52.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_08** | `304.0s` | `260.0s` | `53.0s` | `3 (2)` | `2` | `ValueError'. Los verificadores deben retornar booleanos sin sentencias 'raise' de depuraci�n.` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_03** | `301.0s` | `255.0s` | `60.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_04** | `298.0s` | `263.0s` | `48.0s` | `2 (1)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_17** | `287.0s` | `262.0s` | `56.0s` | `3 (2)` | `3` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_13** | `268.0s` | `211.0s` | `63.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_05** | `267.0s` | `223.0s` | `56.0s` | `3 (2)` | `2` | `0 errores` | Remediación (2 fallos) |
| **Shard Author shard_16** | `260.0s` | `250.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_07** | `259.0s` | `255.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_01** | `256.0s` | `224.0s` | `48.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_25** | `247.0s` | `256.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_09** | `243.0s` | `211.0s` | `42.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `2` | **Mediana de Pared:** `208.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer (C18)** | `208.0s` | `197.0s` | `12.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (HAB05)** | `67.0s` | `56.0s` | `11.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |