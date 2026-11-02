### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `29` | **Mediana de Pared:** `311.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_03` (`190.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_25** | `454.0s` | `286.0s` | `186.0s` | `3 (2)` | `1` | `[TPL-DRY], [TPL-VAR], NameError: name 'ver_h08_1' is not defined` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_15** | `445.0s` | `310.0s` | `161.0s` | `3 (2)` | `5` | `[TPL-KATEX], [TPL-ASM], [TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_26** | `423.0s` | `359.0s` | `81.0s` | `3 (2)` | `3` | `[TPL-DRY], [TPL-VAR], NameError: name 'ver_h11_1' is not defined` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_20** | `385.0s` | `314.0s` | `92.0s` | `2 (1)` | `3` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_06** | `382.0s` | `216.0s` | `178.0s` | `3 (2)` | `5` | `[TPL-KATEX], [R-19]` | Remediación (2 fallos) |
| **Shard Author shard_11** | `377.0s` | `274.0s` | `113.0s` | `3 (2)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_18** | `367.0s` | `346.0s` | `44.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_17** | `365.0s` | `351.0s` | `38.0s` | `2 (1)` | `1` | `[TPL-CROSS], [TPL-DRY], [TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_14** | `361.0s` | `334.0s` | `54.0s` | `3 (2)` | `2` | `[TPL-KATEX]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_24** | `354.0s` | `313.0s` | `60.0s` | `2 (1)` | `3` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_22** | `348.0s` | `287.0s` | `82.0s` | `2 (1)` | `4` | `[TPL-DRY], [TPL-VAR], NameError: name 'ver_h02_1' is not defined` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_10** | `344.0s` | `276.0s` | `78.0s` | `3 (2)` | `6` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_19** | `322.0s` | `327.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_21** | `316.0s` | `254.0s` | `83.0s` | `3 (2)` | `3` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_09** | `311.0s` | `232.0s` | `91.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_23** | `310.0s` | `271.0s` | `59.0s` | `3 (2)` | `3` | `[TPL-DRY], [TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_02** | `285.0s` | `282.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_08** | `277.0s` | `276.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_29** | `258.0s` | `253.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_27** | `244.0s` | `245.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_13** | `239.0s` | `235.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_28** | `235.0s` | `236.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_12** | `231.0s` | `228.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_16** | `221.0s` | `231.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_05** | `210.0s` | `211.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_04** | `200.0s` | `200.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_07** | `199.0s` | `195.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_01** | `193.0s` | `197.0s` | `11.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_03** | `190.0s` | `190.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `16` | **Mediana de Pared:** `187.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer (HAB09)** | `304.0s` | `14.0s` | `291.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (HAB05)** | `302.0s` | `12.0s` | `291.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (HAB04)** | `284.0s` | `81.0s` | `205.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (HAB04)** | `262.0s` | `42.0s` | `222.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (HAB05)** | `247.0s` | `35.0s` | `212.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (HAB09)** | `200.0s` | `17.0s` | `183.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (C16)** | `189.0s` | `25.0s` | `168.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (C16)** | `187.0s` | `23.0s` | `168.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (C16)** | `170.0s` | `154.0s` | `16.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (H03)** | `114.0s` | `23.0s` | `94.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (H03)** | `93.0s` | `24.0s` | `72.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (C16)** | `22.0s` | `15.4s` | `6.6s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (HAB05)** | `12.0s` | `8.4s` | `3.6s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (HAB09)** | `12.0s` | `8.4s` | `3.6s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (HAB04)** | `8.0s` | `5.6s` | `2.4s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (H03)** | `7.0s` | `4.9s` | `2.1s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |