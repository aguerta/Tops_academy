### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `12` | **Mediana de Pared:** `326.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_07` (`253.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_08** | `431.0s` | `294.0s` | `146.0s` | `2 (1)` | `2` | `[R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_03** | `416.0s` | `227.0s` | `192.0s` | `2 (1)` | `3` | `[R-19]` | Remediación (1 fallos) |
| **Shard Author shard_11** | `397.0s` | `324.0s` | `80.0s` | `2 (1)` | `2` | `[TPL-DRY], [TPL-VAR], NameError: name 'ver_c07_1' is not defined` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_01** | `394.0s` | `223.0s` | `176.0s` | `4 (3)` | `5` | `[R-19], [TPL-DRY], [TPL-VAR]` | Remediación (3 fallos) |
| **Shard Author shard_12** | `371.0s` | `311.0s` | `66.0s` | `2 (1)` | `1` | `[TPL-DRY], [TPL-VAR], NameError: name 'ver_h03_1' is not defined` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_10** | `326.0s` | `228.0s` | `106.0s` | `3 (2)` | `3` | `[R-15], [TPL-VAR]` | Remediación (2 fallos) |
| **Shard Author shard_06** | `324.0s` | `243.0s` | `82.0s` | `2 (1)` | `2` | `[R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_04** | `313.0s` | `34.0s` | `281.0s` | `5 (3)` | `2` | `[TPL-VAR]` | Remediación (3 fallos) |
| **Shard Author shard_02** | `269.0s` | `200.0s` | `72.0s` | `3 (2)` | `2` | `[R-18]` | Remediación (2 fallos) |
| **Shard Author shard_05** | `264.0s` | `247.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_07** | `253.0s` | `249.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_09** | `231.0s` | `28.0s` | `211.0s` | `2 (1)` | `0` | `0 errores` | Remediación (1 fallos) |