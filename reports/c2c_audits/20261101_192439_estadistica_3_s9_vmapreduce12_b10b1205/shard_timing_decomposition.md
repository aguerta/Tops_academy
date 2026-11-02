### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `25` | **Mediana de Pared:** `303.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_08` (`210.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_15** | `720.0s` | `259.0s` | `485.0s` | `3 (2)` | `2` | `[TPL-DRY], [TPL-VAR], NameError: name 'ver_c05_1' is not defined` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_18** | `518.0s` | `297.0s` | `242.0s` | `3 (2)` | `1` | `[R-15], [TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_20** | `512.0s` | `38.0s` | `493.0s` | `6 (4)` | `4` | `[TPL-DRY], [TPL-VAR], NameError: name 'gen_c01_1' is not defined` | Remediación (4 fallos) |
| **Shard Author shard_25** | `426.0s` | `297.0s` | `143.0s` | `4 (3)` | `5` | `[R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_12** | `406.0s` | `247.0s` | `166.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_17** | `369.0s` | `320.0s` | `71.0s` | `2 (1)` | `1` | `[R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_16** | `352.0s` | `277.0s` | `98.0s` | `2 (1)` | `2` | `[R-15], [TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_14** | `326.0s` | `337.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_01** | `324.0s` | `35.0s` | `303.0s` | `3 (1)` | `2` | `[R-19]` | Remediación (1 fallos) |
| **Shard Author shard_21** | `321.0s` | `254.0s` | `85.0s` | `2 (1)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_24** | `317.0s` | `318.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_19** | `303.0s` | `281.0s` | `42.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_13** | `303.0s` | `271.0s` | `39.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_05** | `300.0s` | `246.0s` | `64.0s` | `3 (2)` | `2` | `[TPL-DRY]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_22** | `292.0s` | `293.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_23** | `292.0s` | `292.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_10** | `287.0s` | `282.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_07** | `268.0s` | `266.0s` | `11.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_11** | `259.0s` | `254.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_02** | `255.0s` | `240.0s` | `28.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_04** | `249.0s` | `214.0s` | `46.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_06** | `245.0s` | `24.0s` | `231.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_03** | `231.0s` | `230.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_09** | `230.0s` | `204.0s` | `34.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_08** | `210.0s` | `197.0s` | `22.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `3` | **Mediana de Pared:** `287.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer (C06)** | `308.0s` | `11.0s` | `298.0s` | `2 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (HAB12)** | `287.0s` | `12.0s` | `276.0s` | `2 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (HAB06)** | `248.0s` | `33.0s` | `216.0s` | `2 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |