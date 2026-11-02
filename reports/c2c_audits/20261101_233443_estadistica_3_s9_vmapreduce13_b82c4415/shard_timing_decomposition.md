### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `33` | **Mediana de Pared:** `314.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_06` (`180.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_30** | `519.0s` | `383.0s` | `156.0s` | `4 (3)` | `5` | `[R-15], [TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_22** | `461.0s` | `282.0s` | `206.0s` | `3 (2)` | `5` | `[TPL-DRY], [TPL-VAR], [R-15]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_20** | `459.0s` | `325.0s` | `163.0s` | `3 (2)` | `5` | `[R-15], [TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_23** | `453.0s` | `302.0s` | `177.0s` | `3 (2)` | `4` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_16** | `426.0s` | `251.0s` | `208.0s` | `4 (3)` | `10` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_27** | `416.0s` | `322.0s` | `116.0s` | `3 (2)` | `5` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_18** | `413.0s` | `347.0s` | `97.0s` | `3 (2)` | `7` | `[TPL-KATEX]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_24** | `408.0s` | `294.0s` | `139.0s` | `5 (4)` | `5` | `[TPL-DRY]` | Overthinking / Exploración lenta Pre-Compile; Remediación (4 fallos) |
| **Shard Author shard_17** | `405.0s` | `312.0s` | `125.0s` | `3 (2)` | `5` | `[R-15], [TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_05** | `405.0s` | `348.0s` | `69.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_25** | `400.0s` | `279.0s` | `145.0s` | `4 (3)` | `4` | `[TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_28** | `388.0s` | `329.0s` | `81.0s` | `3 (2)` | `3` | `[TPL-DRY], [TPL-VAR], NameError: name 'ver_c14_1' is not defined` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_02** | `363.0s` | `277.0s` | `100.0s` | `2 (1)` | `1` | `[R-15], [TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_32** | `347.0s` | `222.0s` | `143.0s` | `4 (3)` | `4` | `[TPL-KATEX], [R-15], [TPL-VAR]` | Remediación (3 fallos) |
| **Shard Author shard_29** | `323.0s` | `218.0s` | `126.0s` | `2 (1)` | `1` | `[R-15], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_33** | `323.0s` | `234.0s` | `105.0s` | `3 (2)` | `2` | `0 errores` | Remediación (2 fallos) |
| **Shard Author shard_15** | `314.0s` | `282.0s` | `36.0s` | `2 (1)` | `1` | `[TPL-DRY]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_12** | `313.0s` | `303.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_31** | `312.0s` | `315.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_19** | `310.0s` | `325.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_21** | `302.0s` | `306.0s` | `24.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_14** | `287.0s` | `278.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_04** | `285.0s` | `283.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_03** | `274.0s` | `252.0s` | `35.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_09** | `250.0s` | `246.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_26** | `242.0s` | `214.0s` | `51.0s` | `2 (1)` | `1` | `[R-15]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `241.0s` | `242.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_08** | `237.0s` | `234.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_10** | `235.0s` | `230.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_13** | `216.0s` | `186.0s` | `34.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_11** | `215.0s` | `208.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_07** | `214.0s` | `213.0s` | `11.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_06** | `180.0s` | `179.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `2` | **Mediana de Pared:** `382.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer (C23)** | `382.0s` | `263.0s` | `119.0s` | `2 (1)` | `3` | `0 errores` | Diagnóstico profundo previo al primer compile; Re-intento tras fallo (1 fallos) |
| **Repair Engineer (HAB03)** | `170.0s` | `155.0s` | `15.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |