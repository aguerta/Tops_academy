### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `20` | **Mediana de Pared:** `316.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_03` (`239.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_14** | `854.0s` | `370.0s` | `496.0s` | `3 (0)` | `3` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_18** | `500.0s` | `491.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_09** | `450.0s` | `308.0s` | `157.0s` | `2 (0)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_13** | `387.0s` | `310.0s` | `90.0s` | `2 (0)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_04** | `350.0s` | `342.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_20** | `342.0s` | `310.0s` | `36.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_12** | `337.0s` | `333.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_05** | `330.0s` | `321.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_17** | `317.0s` | `311.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_10** | `316.0s` | `316.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_19** | `316.0s` | `310.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_08** | `313.0s` | `315.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_07** | `307.0s` | `298.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_15** | `284.0s` | `278.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_02** | `282.0s` | `276.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_06** | `272.0s` | `263.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_01** | `269.0s` | `265.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_16** | `261.0s` | `257.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_11** | `242.0s` | `243.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_03** | `239.0s` | `234.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |