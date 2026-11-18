### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `24` | **Mediana de Pared:** `2739.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_13` (`84.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_14** | `3034.0s` | `99.0s` | `2935.0s` | `11 (10)` | `20` | `[TIMEOUT_INFINITE_LOOP], [TPL-D2], [TPL-D4]` | Remediación (10 fallos) |
| **Shard Author shard_17** | `2835.0s` | `92.0s` | `2743.0s` | `8 (7)` | `14` | `[TIMEOUT_INFINITE_LOOP], [TPL-STEM-GRAMMAR], [TPL-DYNAMIC-RATIONALE]` | Remediación (7 fallos) |
| **Shard Author shard_20** | `2835.0s` | `86.0s` | `2749.0s` | `9 (8)` | `11` | `[TPL-ORPHAN-VARS], [TIMEOUT_INFINITE_LOOP], [TPL-CONST-DISTRACTOR]` | Remediación (8 fallos) |
| **Shard Author shard_01** | `2825.0s` | `73.0s` | `2752.0s` | `10 (9)` | `18` | `[TPL-ORPHAN-VARS], [TIMEOUT_INFINITE_LOOP], [VERIFIER-TAUTOLOGY-DETECTED]` | Remediación (9 fallos) |
| **Shard Author shard_22** | `2818.0s` | `97.0s` | `2721.0s` | `6 (5)` | `9` | `[TIMEOUT_INFINITE_LOOP], [TPL-HINT-LEAK], [TPL-STEM-GRAMMAR]` | Remediación (5 fallos) |
| **Shard Author shard_21** | `2816.0s` | `85.0s` | `2731.0s` | `9 (8)` | `26` | `[TPL-ORPHAN-VARS], [TIMEOUT_INFINITE_LOOP], [TPL-STEM-GRAMMAR]` | Remediación (8 fallos) |
| **Shard Author shard_03** | `2805.0s` | `60.0s` | `2745.0s` | `7 (6)` | `14` | `[TIMEOUT_INFINITE_LOOP], [TPL-STEM-GRAMMAR], [TPL-D4]` | Remediación (6 fallos) |
| **Shard Author shard_16** | `2797.0s` | `82.0s` | `2715.0s` | `9 (8)` | `12` | `[TIMEOUT_INFINITE_LOOP], [VERIFIER-TAUTOLOGY-DETECTED], [TPL-CONST-DISTRACTOR]` | Remediación (8 fallos) |
| **Shard Author shard_23** | `2793.0s` | `96.0s` | `2697.0s` | `9 (8)` | `14` | `[TIMEOUT_INFINITE_LOOP], [TPL-STEM-GRAMMAR], [R-15]` | Remediación (8 fallos) |
| **Shard Author shard_12** | `2779.0s` | `80.0s` | `2699.0s` | `8 (7)` | `11` | `SyntaxError en shard_12_data.py (Línea 391, Columna 59): unexpected character after line continuation character , [TPL-ORPHAN-VARS], [TIMEOUT_INFINITE_LOOP]` | Remediación (7 fallos) |
| **Shard Author shard_15** | `2741.0s` | `80.0s` | `2661.0s` | `8 (7)` | `9` | `[TIMEOUT_INFINITE_LOOP]` | Remediación (7 fallos) |
| **Shard Author shard_09** | `2739.0s` | `68.0s` | `2671.0s` | `7 (6)` | `8` | `[TIMEOUT_INFINITE_LOOP]` | Remediación (6 fallos) |
| **Shard Author shard_19** | `2406.0s` | `86.0s` | `2320.0s` | `10 (10)` | `13` | `[TIMEOUT_INFINITE_LOOP], [TPL-DYNAMIC-RATIONALE], [TPL-CONST-DISTRACTOR]` | Remediación (10 fallos) |
| **Shard Author shard_04** | `2297.0s` | `76.0s` | `2221.0s` | `9 (8)` | `19` | `[TIMEOUT_INFINITE_LOOP], [TPL-CONST-DISTRACTOR], [R-15]` | Remediación (8 fallos) |
| **Shard Author shard_18** | `2292.0s` | `101.0s` | `2191.0s` | `7 (6)` | `7` | `[TIMEOUT_INFINITE_LOOP], [TPL-STEM-GRAMMAR], [R-19]` | Remediación (6 fallos) |
| **Shard Author shard_24** | `2258.0s` | `72.0s` | `2186.0s` | `8 (7)` | `7` | `[TPL-ORPHAN-VARS], [TIMEOUT_INFINITE_LOOP], [TPL-STEM-GRAMMAR]` | Remediación (7 fallos) |
| **Shard Author shard_08** | `2248.0s` | `68.0s` | `2180.0s` | `7 (6)` | `11` | `[TIMEOUT_INFINITE_LOOP], [VERIFIER-TAUTOLOGY-DETECTED], [TPL-CROSS]` | Remediación (6 fallos) |
| **Shard Author shard_11** | `2206.0s` | `70.0s` | `2136.0s` | `6 (5)` | `8` | `[TIMEOUT_INFINITE_LOOP], [TPL-ORPHAN-VARS]` | Remediación (5 fallos) |
| **Shard Author shard_02** | `2108.0s` | `62.0s` | `2046.0s` | `5 (4)` | `5` | `[TIMEOUT_INFINITE_LOOP]` | Remediación (4 fallos) |
| **Shard Author shard_10** | `2098.0s` | `71.0s` | `2027.0s` | `3 (2)` | `4` | `[TIMEOUT_INFINITE_LOOP]` | Remediación (2 fallos) |
| **Shard Author shard_07** | `131.0s` | `84.0s` | `47.0s` | `3 (2)` | `1` | `[TIMEOUT_INFINITE_LOOP], [TPL-CONST-DISTRACTOR]` | Remediación (2 fallos) |
| **Shard Author shard_06** | `98.0s` | `71.0s` | `27.0s` | `2 (1)` | `0` | `[TIMEOUT_INFINITE_LOOP]` | Remediación (1 fallos) |
| **Shard Author shard_05** | `88.0s` | `65.0s` | `23.0s` | `2 (1)` | `0` | `[TIMEOUT_INFINITE_LOOP]` | Remediación (1 fallos) |
| **Shard Author shard_13** | `84.0s` | `53.0s` | `31.0s` | `2 (1)` | `1` | `[TPL-CONST-DISTRACTOR]` | Remediación (1 fallos) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `39` | **Mediana de Pared:** `44.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Batch B** | `2312.0s` | `464.0s` | `1848.0s` | `14 (2)` | `67` | `[TPL-DYNAMIC-RATIONALE], [R-03]` | Diagnóstico profundo previo al primer compile; Re-intento tras fallo (2 fallos) |
| **Repair Engineer Batch C** | `1973.0s` | `406.0s` | `1567.0s` | `21 (9)` | `53` | `[TPL-DYNAMIC-RATIONALE]` | Diagnóstico profundo previo al primer compile; Re-intento tras fallo (9 fallos) |
| **Repair Engineer (HAB04)** | `1765.0s` | `372.0s` | `1393.0s` | `14 (0)` | `69` | `0 errores` | Diagnóstico profundo previo al primer compile |
| **Repair Engineer (C08)** | `529.0s` | `33.0s` | `496.0s` | `7 (6)` | `16` | `[R-19], [TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP]` | Re-intento tras fallo (6 fallos) |
| **Repair Engineer shard_17** | `250.0s` | `30.0s` | `220.0s` | `4 (3)` | `6` | `[R-19]` | Re-intento tras fallo (3 fallos) |
| **Repair Engineer shard_19** | `74.0s` | `51.8s` | `22.2s` | `0 (0)` | `8` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_02** | `71.0s` | `54.0s` | `17.0s` | `1 (1)` | `4` | `[TPL-DYNAMIC-RATIONALE]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer shard_01** | `65.0s` | `62.0s` | `3.0s` | `1 (1)` | `8` | `0 errores` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer shard_17** | `65.0s` | `45.5s` | `19.5s` | `0 (0)` | `8` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_20** | `60.0s` | `43.0s` | `17.0s` | `1 (0)` | `4` | `0 errores` | Parche aplicado exitosamente |
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
| **Repair Engineer shard_04** | `41.0s` | `24.0s` | `17.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_18** | `41.0s` | `28.7s` | `12.3s` | `0 (0)` | `5` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_20** | `39.0s` | `27.3s` | `11.7s` | `0 (0)` | `4` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_24** | `37.0s` | `15.0s` | `22.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_03** | `35.0s` | `21.0s` | `14.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_11** | `34.0s` | `21.0s` | `13.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_12** | `34.0s` | `15.0s` | `19.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (HAB07)** | `34.0s` | `19.0s` | `15.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_16** | `33.0s` | `17.0s` | `16.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_09** | `33.0s` | `20.0s` | `13.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (C33)** | `33.0s` | `17.0s` | `16.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_23** | `33.0s` | `23.1s` | `9.9s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_24** | `31.0s` | `16.0s` | `15.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_10** | `30.0s` | `15.0s` | `15.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **CTA Architect part_02 repair** | `28.0s` | `19.0s` | `9.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_22** | `28.0s` | `19.6s` | `8.4s` | `0 (0)` | `5` | `0 errores` | Parche aplicado exitosamente |
| **CTA Architect part_02 repair** | `23.0s` | `16.1s` | `6.9s` | `0 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer shard_12** | `11.0s` | `7.7s` | `3.3s` | `0 (0)` | `0` | `0 errores` | Parche aplicado exitosamente |