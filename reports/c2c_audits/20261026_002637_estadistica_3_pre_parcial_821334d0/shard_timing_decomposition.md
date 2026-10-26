### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `63` | **Mediana de Pared:** `310.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_20` (`221.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_54** | `599.0s` | `358.0s` | `280.0s` | `1 (0)` | `3` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_31** | `574.0s` | `559.0s` | `26.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_61** | `477.0s` | `406.0s` | `104.0s` | `2 (0)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_18** | `465.0s` | `165.0s` | `320.0s` | `3 (0)` | `3` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_42** | `464.0s` | `125.0s` | `387.0s` | `3 (0)` | `1` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_56** | `433.0s` | `390.0s` | `80.0s` | `2 (0)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_46** | `417.0s` | `334.0s` | `127.0s` | `2 (0)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_53** | `391.0s` | `148.0s` | `282.0s` | `3 (0)` | `1` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_36** | `385.0s` | `420.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_55** | `373.0s` | `389.0s` | `22.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_32** | `373.0s` | `369.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_60** | `371.0s` | `366.0s` | `39.0s` | `2 (0)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_50** | `369.0s` | `197.0s` | `213.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_52** | `366.0s` | `307.0s` | `99.0s` | `2 (0)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_57** | `364.0s` | `383.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_48** | `362.0s` | `388.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_30** | `362.0s` | `360.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_28** | `358.0s` | `133.0s` | `238.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_19** | `356.0s` | `362.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_14** | `355.0s` | `362.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_35** | `351.0s` | `140.0s` | `264.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_38** | `351.0s` | `152.0s` | `249.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_40** | `348.0s` | `379.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_06** | `348.0s` | `353.0s` | `22.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_08** | `347.0s` | `360.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_05** | `345.0s` | `359.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_17** | `344.0s` | `349.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_45** | `326.0s` | `114.0s` | `257.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_59** | `321.0s` | `341.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_51** | `319.0s` | `340.0s` | `19.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_49** | `310.0s` | `337.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_02** | `310.0s` | `325.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_12** | `297.0s` | `307.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_22** | `296.0s` | `298.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_62** | `292.0s` | `308.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_21** | `292.0s` | `294.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_34** | `291.0s` | `113.0s` | `232.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_09** | `288.0s` | `125.0s` | `188.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_16** | `287.0s` | `95.0s` | `213.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_23** | `287.0s` | `290.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_63** | `286.0s` | `161.0s` | `157.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_44** | `285.0s` | `314.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_43** | `284.0s` | `316.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_26** | `282.0s` | `282.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_39** | `274.0s` | `308.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_07** | `273.0s` | `283.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_41** | `269.0s` | `303.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_01** | `269.0s` | `115.0s` | `185.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_10** | `267.0s` | `211.0s` | `80.0s` | `2 (0)` | `1` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_25** | `265.0s` | `267.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_11** | `263.0s` | `273.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_47** | `260.0s` | `288.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_29** | `259.0s` | `252.0s` | `19.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_15** | `256.0s` | `261.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_37** | `254.0s` | `287.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_27** | `254.0s` | `46.0s` | `221.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_03** | `252.0s` | `267.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_04** | `252.0s` | `269.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_58** | `248.0s` | `267.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_13** | `246.0s` | `255.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_33** | `242.0s` | `72.0s` | `180.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_24** | `227.0s` | `229.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_20** | `221.0s` | `225.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |