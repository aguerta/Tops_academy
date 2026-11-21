### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `24` | **Mediana de Pared:** `2739.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_13` (`84.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_14** | `3034.0s` | `2123.8s` | `910.2s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_17** | `2835.0s` | `1984.5s` | `850.5s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_20** | `2835.0s` | `1984.5s` | `850.5s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_01** | `2825.0s` | `1977.5s` | `847.5s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_22** | `2818.0s` | `1972.6s` | `845.4s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_21** | `2816.0s` | `1971.2s` | `844.8s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_03** | `2805.0s` | `1963.5s` | `841.5s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_16** | `2797.0s` | `1957.9s` | `839.1s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_23** | `2793.0s` | `1955.1s` | `837.9s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_12** | `2779.0s` | `1945.3s` | `833.7s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_15** | `2741.0s` | `1918.7s` | `822.3s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_09** | `2739.0s` | `1917.3s` | `821.7s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_19** | `2406.0s` | `1684.2s` | `721.8s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_04** | `2297.0s` | `1607.9s` | `689.1s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_18** | `2292.0s` | `1604.4s` | `687.6s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_24** | `2258.0s` | `1580.6s` | `677.4s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_08** | `2248.0s` | `1573.6s` | `674.4s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_11** | `2206.0s` | `1544.2s` | `661.8s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_02** | `2108.0s` | `1475.6s` | `632.4s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_10** | `2098.0s` | `1468.6s` | `629.4s` | `0 (0)` | `0` | `0 errores` | Overthinking / Exploración lenta Pre-Compile |
| **Shard Author shard_07** | `131.0s` | `91.7s` | `39.3s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_06** | `98.0s` | `68.6s` | `29.4s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_05** | `88.0s` | `61.6s` | `26.4s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_13** | `84.0s` | `58.8s` | `25.2s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `39` | **Mediana de Pared:** `44.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Batch B** | `2312.0s` | `464.0s` | `1848.0s` | `14 (2)` | `67` | `[TPL-DYNAMIC-RATIONALE], [R-03]` | Diagnóstico profundo previo al primer compile; Re-intento tras fallo (2 fallos) |
| **Repair Engineer Batch C** | `1973.0s` | `406.0s` | `1567.0s` | `21 (9)` | `53` | `[TPL-DYNAMIC-RATIONALE]` | Diagnóstico profundo previo al primer compile; Re-intento tras fallo (9 fallos) |
| **Repair Engineer (HAB04)** | `1765.0s` | `372.0s` | `1393.0s` | `14 (0)` | `69` | `0 errores` | Diagnóstico profundo previo al primer compile |
| **Repair Engineer C-08** | `529.0s` | `370.3s` | `158.7s` | `0 (0)` | `0` | `0 errores` | Diagnóstico profundo previo al primer compile |
| **Repair Engineer shard_17** | `250.0s` | `175.0s` | `75.0s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_19** | `74.0s` | `51.8s` | `22.2s` | `0 (0)` | `8` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_02** | `71.0s` | `54.0s` | `17.0s` | `1 (1)` | `4` | `[TPL-DYNAMIC-RATIONALE]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer shard_01** | `65.0s` | `62.0s` | `3.0s` | `1 (1)` | `8` | `0 errores` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer shard_17** | `65.0s` | `45.5s` | `19.5s` | `0 (0)` | `8` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_20** | `60.0s` | `42.0s` | `18.0s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_06** | `59.0s` | `55.0s` | `4.0s` | `1 (0)` | `4` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_05** | `58.0s` | `40.6s` | `17.4s` | `0 (0)` | `4` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_03** | `57.0s` | `55.0s` | `2.0s` | `1 (0)` | `8` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_07** | `55.0s` | `37.0s` | `18.0s` | `1 (0)` | `5` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_10** | `52.0s` | `35.0s` | `17.0s` | `1 (0)` | `4` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_12** | `52.0s` | `49.0s` | `3.0s` | `1 (0)` | `5` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_16** | `51.0s` | `35.7s` | `15.3s` | `0 (0)` | `6` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_15** | `47.0s` | `32.9s` | `14.1s` | `0 (0)` | `8` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_13** | `44.0s` | `42.0s` | `2.0s` | `1 (0)` | `4` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_14** | `44.0s` | `30.8s` | `13.2s` | `0 (0)` | `9` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_21** | `42.0s` | `23.0s` | `19.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_04** | `41.0s` | `28.7s` | `12.3s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_18** | `41.0s` | `28.7s` | `12.3s` | `0 (0)` | `5` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_20** | `39.0s` | `27.3s` | `11.7s` | `0 (0)` | `4` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_24** | `37.0s` | `25.9s` | `11.1s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_03** | `35.0s` | `24.5s` | `10.5s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_11** | `34.0s` | `23.8s` | `10.2s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_12** | `34.0s` | `23.8s` | `10.2s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-07** | `34.0s` | `23.8s` | `10.2s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_16** | `33.0s` | `23.1s` | `9.9s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_09** | `33.0s` | `23.1s` | `9.9s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-33** | `33.0s` | `23.1s` | `9.9s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_23** | `33.0s` | `23.1s` | `9.9s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_24** | `31.0s` | `16.0s` | `15.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_10** | `30.0s` | `21.0s` | `9.0s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **CTA Architect part_02 repair** | `28.0s` | `19.6s` | `8.4s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_22** | `28.0s` | `19.6s` | `8.4s` | `0 (0)` | `5` | `0 errores` | Parche aplicado exitosamente |
| **CTA Architect part_02 repair** | `23.0s` | `16.1s` | `6.9s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_12** | `11.0s` | `7.7s` | `3.3s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |