### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `45` | **Mediana de Pared:** `337.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_03` (`230.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_14** | `628.0s` | `439.0s` | `201.0s` | `2 (0)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_15** | `480.0s` | `144.0s` | `348.0s` | `3 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_24** | `478.0s` | `413.0s` | `71.0s` | `2 (0)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_11** | `450.0s` | `277.0s` | `187.0s` | `2 (0)` | `5` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_41** | `442.0s` | `448.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_23** | `397.0s` | `128.0s` | `275.0s` | `3 (0)` | `1` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_33** | `390.0s` | `398.0s` | `20.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_31** | `386.0s` | `88.0s` | `328.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_34** | `381.0s` | `85.0s` | `324.0s` | `3 (0)` | `1` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_44** | `376.0s` | `355.0s` | `42.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_22** | `371.0s` | `361.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_09** | `364.0s` | `356.0s` | `23.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_30** | `360.0s` | `374.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_40** | `358.0s` | `74.0s` | `308.0s` | `3 (0)` | `1` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_08** | `354.0s` | `354.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_37** | `353.0s` | `323.0s` | `55.0s` | `2 (0)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_39** | `350.0s` | `355.0s` | `20.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_21** | `348.0s` | `340.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_43** | `346.0s` | `352.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_18** | `340.0s` | `290.0s` | `60.0s` | `2 (0)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_16** | `338.0s` | `81.0s` | `268.0s` | `3 (0)` | `1` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_38** | `337.0s` | `343.0s` | `20.0s` | `1 (0)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_20** | `337.0s` | `328.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_02** | `336.0s` | `342.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_32** | `333.0s` | `343.0s` | `19.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_29** | `322.0s` | `339.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_27** | `314.0s` | `83.0s` | `264.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_25** | `308.0s` | `296.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_36** | `306.0s` | `318.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_13** | `301.0s` | `63.0s` | `250.0s` | `3 (0)` | `1` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_12** | `300.0s` | `299.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_17** | `297.0s` | `294.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_26** | `296.0s` | `226.0s` | `74.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_06** | `294.0s` | `71.0s` | `240.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_42** | `289.0s` | `62.0s` | `250.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_01** | `289.0s` | `295.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_28** | `285.0s` | `302.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_04** | `281.0s` | `283.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_35** | `275.0s` | `287.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_10** | `264.0s` | `263.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_05** | `254.0s` | `261.0s` | `11.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_45** | `251.0s` | `225.0s` | `30.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_07** | `239.0s` | `242.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_19** | `231.0s` | `226.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_03** | `230.0s` | `238.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |