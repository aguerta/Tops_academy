### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `16` | **Mediana de Pared:** `311.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_01` (`198.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_14** | `510.0s` | `326.0s` | `193.0s` | `3 (2)` | `1` | `[TPL-DRY], [TPL-VAR], NameError: name 'ver_h01_1' is not defined` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_08** | `380.0s` | `44.0s` | `351.0s` | `4 (2)` | `5` | `0 errores` | Remediación (2 fallos) |
| **Shard Author shard_10** | `345.0s` | `276.0s` | `81.0s` | `2 (1)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_12** | `337.0s` | `256.0s` | `92.0s` | `2 (1)` | `1` | `[R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_13** | `334.0s` | `260.0s` | `84.0s` | `3 (2)` | `3` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_11** | `333.0s` | `264.0s` | `81.0s` | `2 (1)` | `0` | `[TPL-DRY], [TPL-VAR], NameError: name 'ver_c08_1' is not defined` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_09** | `331.0s` | `229.0s` | `116.0s` | `3 (2)` | `2` | `0 errores` | Remediación (2 fallos) |
| **Shard Author shard_16** | `311.0s` | `220.0s` | `94.0s` | `3 (2)` | `5` | `SyntaxError en shard_16_data.py (L�nea 101, Columna 5): (unicode error) 'unicodeescape' codec can't decode bytes in position 50-51: truncated \xXX escape` | Remediación (2 fallos) |
| **Shard Author shard_02** | `268.0s` | `247.0s` | `27.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_06** | `264.0s` | `224.0s` | `43.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_07** | `264.0s` | `224.0s` | `42.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_03** | `255.0s` | `220.0s` | `40.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_15** | `252.0s` | `181.0s` | `79.0s` | `2 (1)` | `0` | `[TPL-DRY], [TPL-VAR], NameError: name 'ver_h03_1' is not defined` | Remediación (1 fallos) |
| **Shard Author shard_04** | `236.0s` | `203.0s` | `38.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_05** | `231.0s` | `190.0s` | `45.0s` | `2 (1)` | `0` | `[TPL-DRY], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `198.0s` | `147.0s` | `58.0s` | `2 (1)` | `2` | `0 errores` | Remediación (1 fallos) |