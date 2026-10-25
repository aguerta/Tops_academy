### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `10` | **Mediana de Pared:** `312.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_03` (`202.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_06** | `423.0s` | `291.0s` | `140.0s` | `2 (0)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_09** | `369.0s` | `355.0s` | `19.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_10** | `358.0s` | `345.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_07** | `323.0s` | `239.0s` | `91.0s` | `2 (0)` | `1` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_08** | `312.0s` | `299.0s` | `19.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_02** | `306.0s` | `257.0s` | `51.0s` | `2 (0)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_01** | `270.0s` | `260.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_05** | `263.0s` | `242.0s` | `22.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_04** | `222.0s` | `211.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_03** | `202.0s` | `191.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |