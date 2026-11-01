### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `31` | **Mediana de Pared:** `281.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_12` (`187.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_22** | `2082.0s` | `265.0s` | `1840.0s` | `5 (6)` | `12` | `[TPL-DRY], [TPL-VAR], NameError: name 'ver_c16_2' is not defined` | Overthinking / Exploración lenta Pre-Compile; Remediación (6 fallos) |
| **Shard Author shard_25** | `593.0s` | `290.0s` | `324.0s` | `4 (4)` | `12` | `[TPL-DRY], [TPL-VAR], NameError: name 'ver_c01_mc' is not defined` | Overthinking / Exploración lenta Pre-Compile; Remediación (4 fallos) |
| **Shard Author shard_29** | `426.0s` | `283.0s` | `161.0s` | `3 (2)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_28** | `409.0s` | `256.0s` | `172.0s` | `4 (3)` | `2` | `[TPL-DRY], [TPL-VAR], NameError: name 'ver_c12_1' is not defined` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_26** | `398.0s` | `291.0s` | `127.0s` | `3 (2)` | `1` | `[R-15], [TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_15** | `356.0s` | `241.0s` | `125.0s` | `4 (3)` | `2` | `[R-20], [TPL-DRY]` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_04** | `354.0s` | `247.0s` | `122.0s` | `2 (1)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_30** | `343.0s` | `236.0s` | `124.0s` | `3 (2)` | `5` | `[R-15], [TPL-VAR]` | Remediación (2 fallos) |
| **Shard Author shard_18** | `332.0s` | `293.0s` | `65.0s` | `2 (1)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_23** | `330.0s` | `242.0s` | `110.0s` | `2 (1)` | `0` | `[TPL-DRY], [TPL-VAR], NameError: name 'ver_c20_1' is not defined` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_06** | `290.0s` | `262.0s` | `42.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_19** | `289.0s` | `253.0s` | `61.0s` | `2 (1)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_20** | `289.0s` | `218.0s` | `95.0s` | `3 (2)` | `1` | `[R-15], [R-18], [TPL-VAR]` | Remediación (2 fallos) |
| **Shard Author shard_24** | `287.0s` | `247.0s` | `62.0s` | `3 (2)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_21** | `283.0s` | `46.0s` | `261.0s` | `3 (1)` | `0` | `[R-20], [R-19]` | Remediación (1 fallos) |
| **Shard Author shard_11** | `281.0s` | `267.0s` | `25.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_27** | `276.0s` | `237.0s` | `58.0s` | `2 (1)` | `0` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_14** | `257.0s` | `30.0s` | `237.0s` | `3 (1)` | `0` | `[R-15], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `255.0s` | `49.0s` | `222.0s` | `4 (2)` | `2` | `0 errores` | Remediación (2 fallos) |
| **Shard Author shard_17** | `243.0s` | `220.0s` | `33.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_09** | `238.0s` | `182.0s` | `68.0s` | `2 (1)` | `3` | `[TPL-DRY]` | Remediación (1 fallos) |
| **Shard Author shard_31** | `230.0s` | `28.0s` | `219.0s` | `3 (1)` | `0` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_02** | `230.0s` | `216.0s` | `29.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_16** | `228.0s` | `200.0s` | `37.0s` | `3 (2)` | `2` | `0 errores` | Remediación (2 fallos) |
| **Shard Author shard_10** | `223.0s` | `200.0s` | `34.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_13** | `223.0s` | `195.0s` | `39.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_07** | `216.0s` | `204.0s` | `25.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_03** | `212.0s` | `198.0s` | `29.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_05** | `209.0s` | `194.0s` | `30.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_08** | `205.0s` | `191.0s` | `26.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_12** | `187.0s` | `171.0s` | `27.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |