### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `44` | **Mediana de Pared:** `304.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_27` (`174.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_14** | `796.0s` | `175.0s` | `638.0s` | `6 (5)` | `10` | `[TPL-DRY], [TPL-VAR]` | Remediación (5 fallos) |
| **Shard Author shard_34** | `639.0s` | `326.0s` | `345.0s` | `4 (3)` | `4` | `ValueError: could not convert string to float: '2.708\\'` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_33** | `632.0s` | `244.0s` | `421.0s` | `3 (2)` | `8` | `[R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_39** | `610.0s` | `264.0s` | `374.0s` | `3 (2)` | `4` | `[R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_40** | `592.0s` | `287.0s` | `333.0s` | `2 (1)` | `2` | `[R-16], [R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_44** | `579.0s` | `276.0s` | `327.0s` | `3 (2)` | `5` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_37** | `576.0s` | `257.0s` | `348.0s` | `4 (3)` | `8` | `[R-18], [TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (3 fallos) |
| **Shard Author shard_42** | `480.0s` | `270.0s` | `236.0s` | `3 (2)` | `4` | `[R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_28** | `417.0s` | `287.0s` | `166.0s` | `3 (2)` | `5` | `[R-16]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_06** | `397.0s` | `249.0s` | `168.0s` | `3 (2)` | `3` | `[TPL-DRY], [TPL-VAR], [R-19]` | Overthinking / Exploración lenta Pre-Compile; Remediación (2 fallos) |
| **Shard Author shard_38** | `351.0s` | `316.0s` | `63.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_29** | `347.0s` | `283.0s` | `99.0s` | `2 (1)` | `0` | `[TPL-VAR]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_31** | `347.0s` | `279.0s` | `101.0s` | `1 (1)` | `0` | `[R-16]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_23** | `337.0s` | `273.0s` | `77.0s` | `2 (1)` | `3` | `[TPL-CROSS]` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_08** | `326.0s` | `239.0s` | `106.0s` | `2 (1)` | `2` | `[R-19]` | Remediación (1 fallos) |
| **Shard Author shard_43** | `325.0s` | `254.0s` | `96.0s` | `2 (1)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_32** | `318.0s` | `285.0s` | `66.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_12** | `316.0s` | `228.0s` | `105.0s` | `2 (1)` | `3` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_17** | `316.0s` | `223.0s` | `109.0s` | `3 (2)` | `3` | `[R-19]` | Remediación (2 fallos) |
| **Shard Author shard_01** | `307.0s` | `312.0s` | `19.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_25** | `305.0s` | `302.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_03** | `304.0s` | `237.0s` | `89.0s` | `2 (1)` | `2` | `[R-19]` | Remediación (1 fallos) |
| **Shard Author shard_30** | `295.0s` | `274.0s` | `55.0s` | `2 (1)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile; Remediación (1 fallos) |
| **Shard Author shard_02** | `288.0s` | `158.0s` | `153.0s` | `3 (2)` | `4` | `[R-19]` | Remediación (2 fallos) |
| **Shard Author shard_16** | `286.0s` | `283.0s` | `19.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_26** | `284.0s` | `207.0s` | `89.0s` | `2 (1)` | `2` | `[R-16]` | Remediación (1 fallos) |
| **Shard Author shard_41** | `272.0s` | `222.0s` | `77.0s` | `2 (1)` | `2` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_19** | `260.0s` | `213.0s` | `62.0s` | `2 (1)` | `1` | `[TPL-KATEX]` | Remediación (1 fallos) |
| **Shard Author shard_35** | `259.0s` | `265.0s` | `25.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_20** | `256.0s` | `224.0s` | `46.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_15** | `253.0s` | `253.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_36** | `249.0s` | `252.0s` | `27.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_21** | `244.0s` | `196.0s` | `62.0s` | `2 (1)` | `2` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_07** | `233.0s` | `216.0s` | `37.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_04** | `228.0s` | `203.0s` | `47.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_09** | `218.0s` | `221.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_11** | `213.0s` | `216.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_18** | `210.0s` | `210.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_13** | `209.0s` | `208.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_24** | `198.0s` | `196.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_05** | `196.0s` | `200.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_22** | `181.0s` | `175.0s` | `20.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_10** | `177.0s` | `182.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_27** | `174.0s` | `173.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `13` | **Mediana de Pared:** `259.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer (C01)** | `545.0s` | `537.0s` | `18.0s` | `1 (0)` | `1` | `0 errores` | Diagnóstico profundo previo al primer compile |
| **Repair Engineer (H04)** | `433.0s` | `418.0s` | `18.0s` | `1 (0)` | `3` | `0 errores` | Diagnóstico profundo previo al primer compile |
| **Repair Engineer (C10)** | `314.0s` | `236.0s` | `86.0s` | `2 (1)` | `2` | `[TPL-DRY], [TPL-VAR]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer (H03)** | `286.0s` | `262.0s` | `27.0s` | `1 (0)` | `3` | `0 errores` | Diagnóstico profundo previo al primer compile |
| **Repair Engineer (C18)** | `273.0s` | `262.0s` | `18.0s` | `1 (0)` | `1` | `0 errores` | Diagnóstico profundo previo al primer compile |
| **Repair Engineer (HAB14)** | `269.0s` | `255.0s` | `17.0s` | `1 (0)` | `2` | `0 errores` | Diagnóstico profundo previo al primer compile |
| **Repair Engineer (C16)** | `259.0s` | `249.0s` | `17.0s` | `1 (0)` | `3` | `0 errores` | Diagnóstico profundo previo al primer compile |
| **Repair Engineer (C20)** | `238.0s` | `228.0s` | `15.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (H01)** | `220.0s` | `209.0s` | `15.0s` | `1 (0)` | `4` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (H06)** | `217.0s` | `178.0s` | `42.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (C17)** | `204.0s` | `193.0s` | `18.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (C05)** | `178.0s` | `172.0s` | `15.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (C19)** | `174.0s` | `149.0s` | `31.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |