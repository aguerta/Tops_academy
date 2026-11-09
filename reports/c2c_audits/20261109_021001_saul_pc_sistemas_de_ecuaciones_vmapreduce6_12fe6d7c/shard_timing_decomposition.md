### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `41` | **Mediana de Pared:** `495.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_31` (`253.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_12** | `1289.0s` | `273.0s` | `1031.0s` | `8 (7)` | `11` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (7 fallos) |
| **Shard Author shard_22** | `1157.0s` | `659.0s` | `543.0s` | `5 (4)` | `10` | `[R-19], [TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (4 fallos) |
| **Shard Author shard_32** | `916.0s` | `281.0s` | `670.0s` | `4 (3)` | `4` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_17** | `873.0s` | `535.0s` | `347.0s` | `2 (1)` | `5` | `[R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_33** | `862.0s` | `337.0s` | `559.0s` | `4 (3)` | `2` | `[TPL-DRY], [TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_26** | `846.0s` | `342.0s` | `545.0s` | `3 (2)` | `3` | `[TPL-CROSS]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_40** | `846.0s` | `431.0s` | `441.0s` | `4 (3)` | `6` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_02** | `833.0s` | `321.0s` | `536.0s` | `3 (2)` | `3` | `[TPL-VAR], [R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_20** | `806.0s` | `233.0s` | `580.0s` | `3 (2)` | `5` | `[R-19]` | Remediación (2 fallos) |
| **Shard Author shard_29** | `801.0s` | `301.0s` | `538.0s` | `3 (2)` | `2` | `[R-19], [R-16], [R-18]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_04** | `782.0s` | `246.0s` | `558.0s` | `2 (1)` | `2` | `[R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_30** | `769.0s` | `314.0s` | `492.0s` | `3 (2)` | `2` | `[TPL-DRY]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_23** | `765.0s` | `342.0s` | `467.0s` | `4 (3)` | `4` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_16** | `745.0s` | `328.0s` | `427.0s` | `2 (1)` | `3` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_06** | `737.0s` | `295.0s` | `462.0s` | `2 (1)` | `2` | `[R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_08** | `724.0s` | `293.0s` | `448.0s` | `2 (1)` | `3` | `[R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_36** | `697.0s` | `355.0s` | `372.0s` | `2 (1)` | `3` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_24** | `637.0s` | `322.0s` | `358.0s` | `3 (2)` | `2` | `[R-16]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_07** | `587.0s` | `294.0s` | `312.0s` | `2 (1)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_14** | `507.0s` | `265.0s` | `255.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_05** | `495.0s` | `255.0s` | `261.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_11** | `493.0s` | `239.0s` | `270.0s` | `2 (1)` | `2` | `[TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_27** | `416.0s` | `365.0s` | `90.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_13** | `389.0s` | `248.0s` | `155.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_34** | `388.0s` | `277.0s` | `143.0s` | `2 (1)` | `1` | `[TPL-KATEX]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_37** | `378.0s` | `295.0s` | `112.0s` | `2 (1)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_38** | `353.0s` | `336.0s` | `45.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_39** | `349.0s` | `263.0s` | `113.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_03** | `346.0s` | `308.0s` | `61.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_25** | `344.0s` | `243.0s` | `143.0s` | `2 (1)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_28** | `342.0s` | `334.0s` | `46.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_35** | `342.0s` | `308.0s` | `65.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_09** | `341.0s` | `321.0s` | `37.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_18** | `340.0s` | `288.0s` | `61.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_19** | `308.0s` | `287.0s` | `29.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_21** | `304.0s` | `241.0s` | `69.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_15** | `273.0s` | `260.0s` | `24.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_41** | `273.0s` | `237.0s` | `42.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_10** | `255.0s` | `195.0s` | `76.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_01** | `254.0s` | `256.0s` | `24.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_31** | `253.0s` | `256.0s` | `33.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers:** `0 subagentes desplegados` (Pase limpio sin remediación).