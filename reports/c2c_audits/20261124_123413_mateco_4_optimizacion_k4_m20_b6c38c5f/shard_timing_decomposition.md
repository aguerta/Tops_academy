### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `57` | **Mediana de Pared:** `137.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_26` (`94.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_06** | `320.0s` | `136.0s` | `184.0s` | `3 (2)` | `1` | `[TPL-ORPHAN-VARS], [TPL-STEM-SYMBOL-PARITY], [VERIFIER-TAUTOLOGY-DETECTED]` | Remediación (2 fallos) |
| **Shard Author shard_15** | `274.0s` | `115.0s` | `159.0s` | `2 (2)` | `1` | `[TPL-STEM-EQUATION-PARITY], [TPL-DRY], [TPL-D4]` | Remediación (2 fallos) |
| **Shard Author shard_04** | `271.0s` | `146.0s` | `125.0s` | `3 (2)` | `6` | `[TPL-DYNAMIC-RATIONALE], [TPL-ORPHAN-VARS], [TPL-STEM-SYMBOL-PARITY]` | Remediación (2 fallos) |
| **Shard Author shard_01** | `265.0s` | `116.0s` | `149.0s` | `3 (2)` | `2` | `[TPL-STEM-SYMBOL-PARITY], [TPL-STEM-VARIANT-PARITY], [TPL-DYNAMIC-RATIONALE]` | Remediación (2 fallos) |
| **Shard Author shard_14** | `250.0s` | `113.0s` | `137.0s` | `3 (2)` | `12` | `[TPL-ORPHAN-VARS], [TPL-STEM-EQUATION-PARITY], [TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (2 fallos) |
| **Shard Author shard_15** | `242.0s` | `124.0s` | `118.0s` | `3 (2)` | `6` | `[VERIFIER-TAUTOLOGY-DETECTED], [TPL-DYNAMIC-RATIONALE], [TPL-DRY]` | Remediación (2 fallos) |
| **Shard Author shard_02** | `234.0s` | `163.0s` | `71.0s` | `2 (1)` | `3` | `[TPL-DRY], [TPL-STEM-VARIANT-PARITY], NameError: name 'r' is not defined` | Remediación (1 fallos) |
| **Shard Author shard_16** | `234.0s` | `123.0s` | `111.0s` | `2 (1)` | `0` | `[TPL-STEM-EQUATION-PARITY], [R-20]` | Remediación (1 fallos) |
| **Shard Author shard_12** | `208.0s` | `117.0s` | `91.0s` | `2 (1)` | `0` | `[TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_24** | `205.0s` | `88.0s` | `117.0s` | `4 (4)` | `10` | `[TPL-MS-ABSOLUTE-WORD-BIAS], [R-19], [INVARIANT]` | Remediación (4 fallos) |
| **Shard Author shard_03** | `199.0s` | `125.0s` | `74.0s` | `2 (1)` | `5` | `[TPL-STEM-SYMBOL-PARITY], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_02** | `198.0s` | `133.0s` | `65.0s` | `2 (1)` | `6` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_05** | `196.0s` | `144.0s` | `52.0s` | `2 (1)` | `1` | `[TPL-ORPHAN-VARS], [TPL-DRY], ZeroDivisionError: float division by zero` | Remediación (1 fallos) |
| **Shard Author shard_16** | `187.0s` | `144.0s` | `43.0s` | `2 (1)` | `1` | `[TPL-ORPHAN-VARS], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `185.0s` | `114.0s` | `71.0s` | `2 (1)` | `2` | `[TPL-STEM-SYMBOL-PARITY], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_03** | `184.0s` | `118.0s` | `66.0s` | `2 (1)` | `3` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-SYMBOL-PARITY], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_14** | `174.0s` | `90.0s` | `84.0s` | `3 (2)` | `6` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-EQUATION-PARITY]` | Remediación (2 fallos) |
| **Shard Author shard_18** | `174.0s` | `122.0s` | `52.0s` | `2 (1)` | `2` | `[TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_20** | `174.0s` | `120.0s` | `54.0s` | `2 (1)` | `3` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [TPL-ORPHAN-VARS]` | Remediación (1 fallos) |
| **Shard Author shard_11** | `171.0s` | `120.0s` | `51.0s` | `2 (1)` | `5` | `[TPL-DYNAMIC-RATIONALE], [VERIFIER-TAUTOLOGY-DETECTED], [TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (1 fallos) |
| **Shard Author shard_17** | `168.0s` | `111.0s` | `57.0s` | `2 (1)` | `3` | `[INVARIANT], [TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `166.0s` | `116.0s` | `50.0s` | `2 (1)` | `1` | `[TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_05** | `154.0s` | `127.0s` | `27.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_28** | `154.0s` | `89.0s` | `65.0s` | `2 (1)` | `8` | `[TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `151.0s` | `129.0s` | `22.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_13** | `150.0s` | `101.0s` | `49.0s` | `2 (1)` | `3` | `[TPL-ORPHAN-VARS], [TPL-STEM-EQUATION-PARITY], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_17** | `144.0s` | `109.0s` | `35.0s` | `2 (1)` | `2` | `[TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_19** | `144.0s` | `118.0s` | `26.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_10** | `137.0s` | `114.0s` | `23.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_25** | `135.0s` | `117.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_13** | `134.0s` | `114.0s` | `20.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_09** | `131.0s` | `112.0s` | `19.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_06** | `130.0s` | `125.0s` | `5.0s` | `1 (1)` | `0` | `[TPL-STEM-EQUATION-PARITY], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_18** | `128.0s` | `128.0s` | `0.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_31** | `128.0s` | `77.0s` | `51.0s` | `2 (1)` | `1` | `[TPL-MS-ABSOLUTE-WORD-BIAS], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `127.0s` | `106.0s` | `21.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_23** | `127.0s` | `90.0s` | `37.0s` | `2 (1)` | `2` | `[TPL-STEM-VARIANT-PARITY], [TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (1 fallos) |
| **Shard Author shard_22** | `126.0s` | `110.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_26** | `122.0s` | `88.0s` | `34.0s` | `2 (1)` | `2` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_27** | `117.0s` | `102.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_29** | `117.0s` | `102.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_25** | `116.0s` | `100.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_21** | `116.0s` | `99.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_30** | `113.0s` | `95.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_30** | `111.0s` | `97.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_28** | `106.0s` | `89.0s` | `17.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_29** | `99.0s` | `80.0s` | `19.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_27** | `95.0s` | `81.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_26** | `94.0s` | `79.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_31** | `3.0s` | `2.1s` | `0.9s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_07** | `3.0s` | `2.1s` | `0.9s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_08** | `3.0s` | `2.1s` | `0.9s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_20** | `3.0s` | `2.1s` | `0.9s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_21** | `3.0s` | `2.1s` | `0.9s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_09** | `3.0s` | `2.1s` | `0.9s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_22** | `3.0s` | `2.1s` | `0.9s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_19** | `2.0s` | `1.4s` | `0.6s` | `0 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `15` | **Mediana de Pared:** `74.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer C-02** | `252.0s` | `81.0s` | `171.0s` | `5 (5)` | `9` | `[R-19]` | Re-intento tras fallo (5 fallos) |
| **Repair Engineer C-02** | `150.0s` | `42.0s` | `108.0s` | `2 (1)` | `5` | `[R-19]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer Hab-19** | `127.0s` | `61.0s` | `66.0s` | `2 (1)` | `7` | `[INVARIANT]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer Hab-09** | `104.0s` | `81.0s` | `23.0s` | `1 (0)` | `11` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-06** | `98.0s` | `50.0s` | `48.0s` | `2 (1)` | `7` | `[TPL-STEM-EQUATION-PARITY], [TPL-STEM-VARIANT-PARITY]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer Hab-15** | `94.0s` | `67.0s` | `27.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-07** | `93.0s` | `44.0s` | `49.0s` | `2 (1)` | `2` | `[TPL-STEM-EQUATION-PARITY]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer Hab-15** | `74.0s` | `41.0s` | `33.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-09** | `71.0s` | `50.0s` | `21.0s` | `1 (0)` | `5` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-21** | `70.0s` | `19.0s` | `51.0s` | `2 (1)` | `9` | `[INVARIANT], [TPL-DIGIT-PLACEHOLDER-CONCAT]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer Hab-08** | `63.0s` | `45.0s` | `18.0s` | `1 (0)` | `6` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-15** | `55.0s` | `29.0s` | `26.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-19** | `50.0s` | `32.0s` | `18.0s` | `1 (0)` | `3` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-13** | `49.0s` | `31.0s` | `18.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-08** | `43.0s` | `27.0s` | `16.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |