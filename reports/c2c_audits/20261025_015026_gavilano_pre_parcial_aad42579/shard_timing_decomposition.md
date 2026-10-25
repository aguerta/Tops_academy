### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `83` | **Mediana de Pared:** `288.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_03` (`170.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_56** | `609.0s` | `355.0s` | `259.0s` | `3 (0)` | `6` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_82** | `459.0s` | `447.0s` | `26.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_51** | `450.0s` | `411.0s` | `47.0s` | `2 (0)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_52** | `437.0s` | `328.0s` | `118.0s` | `2 (0)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_59** | `420.0s` | `406.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_73** | `403.0s` | `389.0s` | `21.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_68** | `388.0s` | `385.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_69** | `386.0s` | `383.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_45** | `373.0s` | `312.0s` | `74.0s` | `2 (0)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_80** | `371.0s` | `359.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_70** | `370.0s` | `333.0s` | `47.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_42** | `369.0s` | `368.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_78** | `366.0s` | `355.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_72** | `357.0s` | `104.0s` | `261.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_65** | `349.0s` | `347.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_62** | `348.0s` | `278.0s` | `86.0s` | `2 (0)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_54** | `336.0s` | `329.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_79** | `336.0s` | `76.0s` | `264.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_40** | `323.0s` | `260.0s` | `68.0s` | `2 (0)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_32** | `322.0s` | `319.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_63** | `319.0s` | `320.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_64** | `317.0s` | `316.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_44** | `316.0s` | `313.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_66** | `316.0s` | `311.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_26** | `315.0s` | `314.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_25** | `311.0s` | `200.0s` | `125.0s` | `3 (0)` | `2` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_41** | `310.0s` | `304.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_04** | `309.0s` | `99.0s` | `221.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_36** | `309.0s` | `304.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_60** | `305.0s` | `293.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_46** | `302.0s` | `299.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_58** | `302.0s` | `290.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_77** | `301.0s` | `291.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_17** | `301.0s` | `292.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_11** | `298.0s` | `292.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_06** | `297.0s` | `294.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_01** | `294.0s` | `294.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_37** | `294.0s` | `289.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_67** | `293.0s` | `289.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_61** | `291.0s` | `278.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_43** | `289.0s` | `286.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_19** | `288.0s` | `293.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_16** | `285.0s` | `275.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_50** | `284.0s` | `233.0s` | `60.0s` | `2 (0)` | `1` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_31** | `283.0s` | `70.0s` | `223.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_34** | `283.0s` | `276.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_02** | `275.0s` | `225.0s` | `63.0s` | `2 (0)` | `2` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_05** | `275.0s` | `271.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_48** | `274.0s` | `271.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_35** | `274.0s` | `255.0s` | `28.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_21** | `266.0s` | `269.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_30** | `264.0s` | `262.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_24** | `262.0s` | `261.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_09** | `261.0s` | `256.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_08** | `259.0s` | `73.0s` | `195.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_71** | `258.0s` | `235.0s` | `32.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_23** | `258.0s` | `243.0s` | `29.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_15** | `257.0s` | `247.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_12** | `254.0s` | `248.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_75** | `253.0s` | `245.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_33** | `253.0s` | `244.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_38** | `250.0s` | `243.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_74** | `247.0s` | `52.0s` | `202.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_81** | `247.0s` | `236.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_83** | `246.0s` | `242.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_49** | `245.0s` | `242.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_13** | `245.0s` | `34.0s` | `217.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_55** | `243.0s` | `225.0s` | `24.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_76** | `241.0s` | `235.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_10** | `241.0s` | `218.0s` | `31.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_07** | `240.0s` | `236.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_39** | `238.0s` | `232.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_28** | `237.0s` | `235.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_14** | `236.0s` | `227.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_18** | `233.0s` | `225.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_22** | `225.0s` | `229.0s` | `11.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_29** | `221.0s` | `219.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_47** | `217.0s` | `212.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_20** | `217.0s` | `222.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_57** | `201.0s` | `193.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_53** | `194.0s` | `190.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_27** | `190.0s` | `190.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_03** | `170.0s` | `172.0s` | `10.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |