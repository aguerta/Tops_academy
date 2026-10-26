### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `80` | **Mediana de Pared:** `294.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_45` (`189.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_51** | `430.0s` | `420.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_78** | `426.0s` | `320.0s` | `109.0s` | `3 (0)` | `2` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_49** | `414.0s` | `407.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_58** | `409.0s` | `60.0s` | `353.0s` | `4 (0)` | `2` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_50** | `391.0s` | `244.0s` | `156.0s` | `2 (0)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_56** | `386.0s` | `372.0s` | `19.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_47** | `382.0s` | `333.0s` | `61.0s` | `2 (0)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_68** | `369.0s` | `123.0s` | `257.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_43** | `368.0s` | `361.0s` | `21.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_05** | `359.0s` | `355.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_65** | `358.0s` | `40.0s` | `331.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_16** | `354.0s` | `341.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_60** | `349.0s` | `68.0s` | `284.0s` | `4 (0)` | `2` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_06** | `341.0s` | `338.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_66** | `337.0s` | `334.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_79** | `336.0s` | `110.0s` | `228.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_73** | `335.0s` | `327.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_74** | `332.0s` | `322.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_80** | `332.0s` | `320.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_08** | `325.0s` | `318.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_02** | `324.0s` | `323.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_14** | `324.0s` | `311.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_27** | `319.0s` | `317.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_46** | `319.0s` | `314.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_59** | `316.0s` | `303.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_76** | `316.0s` | `304.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_19** | `310.0s` | `81.0s` | `231.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_10** | `309.0s` | `303.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_30** | `306.0s` | `43.0s` | `274.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_53** | `304.0s` | `295.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_33** | `303.0s` | `56.0s` | `255.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_37** | `303.0s` | `182.0s` | `126.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_04** | `302.0s` | `117.0s` | `198.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_40** | `302.0s` | `289.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_26** | `301.0s` | `299.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_64** | `300.0s` | `296.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_77** | `300.0s` | `289.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_44** | `297.0s` | `291.0s` | `19.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_48** | `295.0s` | `291.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_34** | `294.0s` | `103.0s` | `199.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_03** | `293.0s` | `38.0s` | `269.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_62** | `292.0s` | `293.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_13** | `291.0s` | `283.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_39** | `290.0s` | `140.0s` | `153.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_63** | `290.0s` | `291.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_07** | `286.0s` | `282.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_20** | `285.0s` | `272.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_70** | `285.0s` | `277.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_36** | `282.0s` | `259.0s` | `29.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_42** | `282.0s` | `280.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_32** | `281.0s` | `276.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_75** | `280.0s` | `265.0s` | `21.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_41** | `279.0s` | `280.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_67** | `279.0s` | `273.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_71** | `274.0s` | `265.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_52** | `273.0s` | `245.0s` | `36.0s` | `2 (0)` | `1` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_55** | `271.0s` | `260.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_24** | `267.0s` | `267.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_31** | `263.0s` | `260.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_29** | `262.0s` | `256.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_38** | `260.0s` | `61.0s` | `203.0s` | `3 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_15** | `259.0s` | `248.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_57** | `259.0s` | `248.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_01** | `258.0s` | `255.0s` | `19.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_11** | `254.0s` | `250.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_54** | `254.0s` | `35.0s` | `226.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_25** | `250.0s` | `251.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_22** | `247.0s` | `249.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_72** | `246.0s` | `239.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_09** | `238.0s` | `38.0s` | `210.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_12** | `237.0s` | `231.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_21** | `237.0s` | `238.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_18** | `236.0s` | `220.0s` | `19.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_35** | `231.0s` | `223.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_17** | `227.0s` | `74.0s` | `157.0s` | `2 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_61** | `220.0s` | `218.0s` | `19.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_23** | `218.0s` | `211.0s` | `23.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_69** | `203.0s` | `195.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_28** | `192.0s` | `191.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_45** | `189.0s` | `189.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |