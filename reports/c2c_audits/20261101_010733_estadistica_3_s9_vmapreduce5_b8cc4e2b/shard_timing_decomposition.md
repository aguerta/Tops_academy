### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `25` | **Mediana de Pared:** `314.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_01` (`220.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_13** | `400.0s` | `323.0s` | `100.0s` | `3 (2)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_15** | `389.0s` | `270.0s` | `140.0s` | `4 (3)` | `2` | `[R-15], [TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_20** | `381.0s` | `338.0s` | `60.0s` | `2 (1)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_16** | `359.0s` | `279.0s` | `100.0s` | `3 (2)` | `1` | `SyntaxError en shard_16_data.py (L�nea 192, Columna 5): (unicode error) 'unicodeescape' codec can't decode bytes in position 43-44: truncated \xXX escape, [R-15], [TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_12** | `346.0s` | `301.0s` | `50.0s` | `3 (2)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_17** | `342.0s` | `271.0s` | `91.0s` | `2 (1)` | `0` | `[TPL-DRY], [TPL-VAR], NameError: name 'ver_c18_1' is not defined` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_19** | `332.0s` | `267.0s` | `83.0s` | `3 (2)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_21** | `321.0s` | `244.0s` | `93.0s` | `2 (1)` | `0` | `[R-15]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_14** | `319.0s` | `284.0s` | `57.0s` | `2 (1)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_23** | `319.0s` | `276.0s` | `57.0s` | `2 (1)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_24** | `315.0s` | `235.0s` | `94.0s` | `2 (1)` | `0` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_05** | `315.0s` | `279.0s` | `46.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_18** | `314.0s` | `236.0s` | `97.0s` | `3 (2)` | `1` | `0 errores` | Remediación (2 fallos) |
| **Shard Author shard_11** | `314.0s` | `280.0s` | `40.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_03** | `284.0s` | `256.0s` | `39.0s` | `2 (1)` | `2` | `[TPL-DRY]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_09** | `280.0s` | `223.0s` | `64.0s` | `2 (1)` | `2` | `[R-19]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `273.0s` | `247.0s` | `35.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_08** | `273.0s` | `240.0s` | `41.0s` | `3 (2)` | `2` | `0 errores` | Remediación (2 fallos) |
| **Shard Author shard_10** | `262.0s` | `235.0s` | `33.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_02** | `258.0s` | `119.0s` | `151.0s` | `3 (2)` | `2` | `[TPL-VAR]` | Remediación (2 fallos) |
| **Shard Author shard_22** | `253.0s` | `172.0s` | `96.0s` | `3 (2)` | `1` | `0 errores` | Remediación (2 fallos) |
| **Shard Author shard_25** | `239.0s` | `152.0s` | `92.0s` | `2 (1)` | `0` | `[TPL-DRY], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `230.0s` | `188.0s` | `50.0s` | `2 (1)` | `1` | `[R-19]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `223.0s` | `162.0s` | `72.0s` | `2 (1)` | `2` | `[R-19]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `220.0s` | `31.0s` | `202.0s` | `3 (1)` | `2` | `[R-19]` | Remediación (1 fallos) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `43` | **Mediana de Pared:** `298.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer (C20)** | `429.0s` | `51.0s` | `401.0s` | `7 (3)` | `1` | `0 errores` | Re-intento tras fallo (3 fallos) |
| **Repair Engineer (HAB08)** | `424.0s` | `135.0s` | `300.0s` | `4 (2)` | `4` | `0 errores` | Re-intento tras fallo (2 fallos) |
| **Repair Engineer (C14)** | `406.0s` | `150.0s` | `284.0s` | `5 (2)` | `0` | `0 errores` | Re-intento tras fallo (2 fallos) |
| **Repair Engineer (H02)** | `371.0s` | `37.0s` | `357.0s` | `7 (4)` | `3` | `[R-20], [TPL-VAR]` | Re-intento tras fallo (4 fallos) |
| **Repair Engineer (C16)** | `368.0s` | `137.0s` | `257.0s` | `5 (3)` | `1` | `0 errores` | Re-intento tras fallo (3 fallos) |
| **Repair Engineer (H06)** | `368.0s` | `51.0s` | `336.0s` | `6 (3)` | `1` | `0 errores` | Re-intento tras fallo (3 fallos) |
| **Repair Engineer (C04)** | `357.0s` | `47.0s` | `347.0s` | `7 (4)` | `3` | `[R-20], [TPL-VAR]` | Re-intento tras fallo (4 fallos) |
| **Repair Engineer (C11)** | `349.0s` | `45.0s` | `334.0s` | `6 (2)` | `0` | `0 errores` | Re-intento tras fallo (2 fallos) |
| **Repair Engineer (HAB03)** | `343.0s` | `26.0s` | `332.0s` | `9 (7)` | `7` | `[R-20]` | Re-intento tras fallo (7 fallos) |
| **Repair Engineer (HAB04)** | `328.0s` | `23.0s` | `320.0s` | `6 (3)` | `1` | `0 errores` | Re-intento tras fallo (3 fallos) |
| **Repair Engineer (C08)** | `327.0s` | `44.0s` | `315.0s` | `6 (2)` | `0` | `0 errores` | Re-intento tras fallo (2 fallos) |
| **Repair Engineer (H04)** | `322.0s` | `28.0s` | `315.0s` | `5 (1)` | `1` | `0 errores` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer (C10)** | `316.0s` | `39.0s` | `307.0s` | `6 (2)` | `0` | `0 errores` | Re-intento tras fallo (2 fallos) |
| **Repair Engineer (HAB11)** | `312.0s` | `17.0s` | `304.0s` | `8 (3)` | `2` | `0 errores` | Re-intento tras fallo (3 fallos) |
| **Repair Engineer (HAB09)** | `308.0s` | `18.0s` | `300.0s` | `10 (7)` | `4` | `[R-20]` | Re-intento tras fallo (7 fallos) |
| **Repair Engineer (HAB05)** | `306.0s` | `23.0s` | `297.0s` | `8 (5)` | `3` | `0 errores` | Re-intento tras fallo (5 fallos) |
| **Repair Engineer (H09)** | `305.0s` | `29.0s` | `292.0s` | `9 (6)` | `3` | `0 errores` | Re-intento tras fallo (6 fallos) |
| **Repair Engineer (C15)** | `304.0s` | `43.0s` | `288.0s` | `5 (3)` | `1` | `0 errores` | Re-intento tras fallo (3 fallos) |
| **Repair Engineer (C06)** | `303.0s` | `44.0s` | `294.0s` | `7 (4)` | `4` | `0 errores` | Re-intento tras fallo (4 fallos) |
| **Repair Engineer (H07)** | `302.0s` | `103.0s` | `217.0s` | `7 (5)` | `1` | `0 errores` | Re-intento tras fallo (5 fallos) |
| **Repair Engineer (C03)** | `299.0s` | `50.0s` | `288.0s` | `7 (4)` | `1` | `0 errores` | Re-intento tras fallo (4 fallos) |
| **Repair Engineer (C05)** | `298.0s` | `56.0s` | `278.0s` | `6 (3)` | `0` | `0 errores` | Re-intento tras fallo (3 fallos) |
| **Repair Engineer (C09)** | `294.0s` | `41.0s` | `284.0s` | `6 (3)` | `1` | `0 errores` | Re-intento tras fallo (3 fallos) |
| **Repair Engineer (H08)** | `294.0s` | `28.0s` | `284.0s` | `6 (3)` | `1` | `0 errores` | Re-intento tras fallo (3 fallos) |
| **Repair Engineer (C18)** | `291.0s` | `33.0s` | `283.0s` | `7 (4)` | `1` | `0 errores` | Re-intento tras fallo (4 fallos) |
| **Repair Engineer (H03)** | `289.0s` | `41.0s` | `270.0s` | `6 (4)` | `1` | `0 errores` | Re-intento tras fallo (4 fallos) |
| **Repair Engineer (HAB06)** | `287.0s` | `21.0s` | `278.0s` | `7 (4)` | `3` | `0 errores` | Re-intento tras fallo (4 fallos) |
| **Repair Engineer (C07)** | `285.0s` | `43.0s` | `276.0s` | `8 (5)` | `2` | `0 errores` | Re-intento tras fallo (5 fallos) |
| **Repair Engineer (HAB12)** | `285.0s` | `169.0s` | `125.0s` | `7 (5)` | `7` | `0 errores` | Re-intento tras fallo (5 fallos) |
| **Repair Engineer (C19)** | `282.0s` | `32.0s` | `273.0s` | `9 (6)` | `1` | `0 errores` | Re-intento tras fallo (6 fallos) |
| **Repair Engineer (C02)** | `281.0s` | `53.0s` | `267.0s` | `8 (5)` | `0` | `0 errores` | Re-intento tras fallo (5 fallos) |
| **Repair Engineer (HAB07)** | `275.0s` | `135.0s` | `152.0s` | `5 (3)` | `3` | `0 errores` | Re-intento tras fallo (3 fallos) |
| **Repair Engineer (HAB10)** | `264.0s` | `116.0s` | `157.0s` | `5 (3)` | `1` | `0 errores` | Re-intento tras fallo (3 fallos) |
| **Repair Engineer (HAB09)** | `229.0s` | `63.0s` | `166.0s` | `2 (1)` | `1` | `0 errores` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer (HAB10)** | `196.0s` | `8.0s` | `189.0s` | `2 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (HAB06)** | `184.0s` | `173.0s` | `12.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (H01)** | `130.0s` | `119.0s` | `12.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (HAB10)** | `119.0s` | `109.0s` | `10.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (HAB09)** | `101.0s` | `10.0s` | `91.0s` | `2 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (HAB01)** | `78.0s` | `70.0s` | `9.0s` | `1 (0)` | `3` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (C01)** | `72.0s` | `8.0s` | `64.0s` | `2 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-06** | `68.0s` | `47.6s` | `20.4s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-06** | `59.0s` | `41.3s` | `17.7s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |