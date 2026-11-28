### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `57` | **Mediana de Pared:** `138.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_37` (`77.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_09** | `232.0s` | `110.0s` | `122.0s` | `2 (1)` | `0` | `[TPL-KATEX-SYMPY-LEAK], [INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_31** | `224.0s` | `114.0s` | `110.0s` | `2 (1)` | `0` | `[TPL-STEM-EQUATION-PARITY], [INVARIANT], [TPL-DEGENERATE-LITERAL-COND]` | Remediación (1 fallos) |
| **Shard Author shard_14** | `211.0s` | `106.0s` | `105.0s` | `2 (1)` | `0` | `[TPL-STEM-EQUATION-PARITY], [TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `203.0s` | `103.0s` | `100.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-STEM-SYMBOL-PARITY], [TPL-CLONE-STEM]` | Remediación (1 fallos) |
| **Shard Author shard_50** | `199.0s` | `93.0s` | `106.0s` | `4 (3)` | `9` | `[INVARIANT], [TPL-DEGENERATE-LITERAL-COND], [TPL-CONST-DISTRACTOR]` | Remediación (3 fallos) |
| **Shard Author shard_49** | `197.0s` | `105.0s` | `92.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-MS-ABSOLUTE-WORD-BIAS], [TPL-M20-ADVERSARIAL]` | Remediación (1 fallos) |
| **Shard Author shard_22** | `188.0s` | `93.0s` | `95.0s` | `2 (1)` | `0` | `[R-19], [TPL-STEM-DERIV-GIVEAWAY], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_57** | `182.0s` | `90.0s` | `92.0s` | `4 (3)` | `5` | `[INVARIANT], [TPL-DYNAMIC-RATIONALE], [TPL-STEM-EQUATION-PARITY]` | Remediación (3 fallos) |
| **Shard Author shard_26** | `180.0s` | `111.0s` | `69.0s` | `2 (1)` | `12` | `[TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_18** | `175.0s` | `110.0s` | `65.0s` | `2 (1)` | `7` | `[TPL-DYNAMIC-RATIONALE], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_20** | `173.0s` | `112.0s` | `61.0s` | `3 (2)` | `4` | `[TPL-STEM-EQUATION-PARITY], [TPL-D4], [INVARIANT]` | Remediación (2 fallos) |
| **Shard Author shard_21** | `171.0s` | `108.0s` | `63.0s` | `4 (3)` | `4` | `SyntaxError en shard_21_data.py (Línea 786, Columna 52): unterminated string literal (detected at line 786) , [VERIFIER-TAUTOLOGY-DETECTED], [TPL-D4]` | Remediación (3 fallos) |
| **Shard Author shard_55** | `169.0s` | `124.0s` | `45.0s` | `2 (1)` | `6` | `[TPL-KATEX], [TPL-D4], [INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_23** | `168.0s` | `114.0s` | `54.0s` | `2 (1)` | `3` | `[TPL-STEM-EQUATION-PARITY], [R-03]` | Remediación (1 fallos) |
| **Shard Author shard_03** | `165.0s` | `99.0s` | `66.0s` | `3 (2)` | `5` | `[TPL-STEM-EQUATION-PARITY], [TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (2 fallos) |
| **Shard Author shard_40** | `165.0s` | `101.0s` | `64.0s` | `2 (1)` | `4` | `[TPL-ORPHAN-VARS], [INVARIANT], [TPL-DEGENERATE-LITERAL-COND]` | Remediación (1 fallos) |
| **Shard Author shard_46** | `164.0s` | `80.0s` | `84.0s` | `3 (2)` | `5` | `[TPL-STEM-VARIANT-PARITY]` | Remediación (2 fallos) |
| **Shard Author shard_13** | `162.0s` | `111.0s` | `51.0s` | `2 (1)` | `2` | `[TPL-ORPHAN-VARS], [TPL-STEM-EQUATION-PARITY], [TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (1 fallos) |
| **Shard Author shard_05** | `160.0s` | `118.0s` | `42.0s` | `2 (1)` | `2` | `[TPL-DYNAMIC-RATIONALE], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_11** | `155.0s` | `101.0s` | `54.0s` | `2 (1)` | `7` | `[TPL-DYNAMIC-RATIONALE], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_10** | `154.0s` | `106.0s` | `48.0s` | `2 (1)` | `5` | `[TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_32** | `154.0s` | `113.0s` | `41.0s` | `2 (1)` | `1` | `[TPL-ASM]` | Remediación (1 fallos) |
| **Shard Author shard_15** | `147.0s` | `106.0s` | `41.0s` | `2 (1)` | `4` | `[TPL-ORPHAN-VARS], [TPL-D4], [TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (1 fallos) |
| **Shard Author shard_19** | `147.0s` | `100.0s` | `47.0s` | `2 (1)` | `3` | `[TPL-ORPHAN-VARS], [TPL-STEM-SYMBOL-PARITY], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_42** | `145.0s` | `111.0s` | `34.0s` | `2 (1)` | `1` | `[TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_27** | `140.0s` | `96.0s` | `44.0s` | `2 (1)` | `1` | `[TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_36** | `140.0s` | `98.0s` | `42.0s` | `2 (1)` | `4` | `[TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `139.0s` | `106.0s` | `33.0s` | `2 (1)` | `2` | `[TPL-STEM-VARIANT-PARITY], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `138.0s` | `110.0s` | `28.0s` | `2 (1)` | `1` | `[TPL-ORPHAN-VARS], [TPL-STEM-SYMBOL-PARITY], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_17** | `136.0s` | `104.0s` | `32.0s` | `2 (1)` | `1` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_47** | `135.0s` | `94.0s` | `41.0s` | `2 (1)` | `3` | `[TPL-STEM-SYMBOL-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_29** | `133.0s` | `118.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_54** | `132.0s` | `95.0s` | `37.0s` | `2 (1)` | `1` | `[TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `131.0s` | `99.0s` | `32.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_44** | `131.0s` | `94.0s` | `37.0s` | `2 (1)` | `3` | `[TPL-MS-ABSOLUTE-WORD-BIAS], [TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_02** | `129.0s` | `89.0s` | `40.0s` | `2 (1)` | `3` | `[TPL-STEM-SYMBOL-PARITY], [TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_30** | `129.0s` | `108.0s` | `21.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_12** | `127.0s` | `113.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_52** | `127.0s` | `89.0s` | `38.0s` | `2 (1)` | `1` | `[TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `124.0s` | `96.0s` | `28.0s` | `2 (1)` | `1` | `[TPL-STEM-SYMBOL-PARITY], [TPL-ORPHAN-VARS], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_16** | `124.0s` | `101.0s` | `23.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_24** | `123.0s` | `109.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_48** | `121.0s` | `85.0s` | `36.0s` | `2 (1)` | `2` | `[TPL-MS-CONDITIONAL-DISTRACTOR], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_51** | `120.0s` | `105.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_56** | `120.0s` | `107.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_43** | `117.0s` | `87.0s` | `30.0s` | `2 (1)` | `2` | `[INVARIANT], [TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_28** | `116.0s` | `103.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_35** | `111.0s` | `85.0s` | `26.0s` | `2 (1)` | `1` | `[INVARIANT], [TPL-DEGENERATE-LITERAL-COND]` | Remediación (1 fallos) |
| **Shard Author shard_53** | `110.0s` | `97.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_25** | `108.0s` | `92.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_41** | `108.0s` | `72.0s` | `36.0s` | `2 (1)` | `4` | `[TPL-MS-ABSOLUTE-WORD-BIAS], [INVARIANT], [TPL-DEGENERATE-LITERAL-COND]` | Remediación (1 fallos) |
| **Shard Author shard_34** | `107.0s` | `94.0s` | `13.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_33** | `105.0s` | `90.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_45** | `103.0s` | `92.0s` | `11.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_39** | `102.0s` | `88.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_38** | `97.0s` | `82.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_37** | `77.0s` | `65.0s` | `12.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `11` | **Mediana de Pared:** `64.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-30** | `122.0s` | `63.0s` | `59.0s` | `2 (1)` | `8` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-VARIANT-PARITY]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer Hab-10** | `88.0s` | `54.0s` | `34.0s` | `2 (1)` | `2` | `[TPL-STEM-EQUATION-PARITY]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer Hab-28** | `85.0s` | `71.0s` | `14.0s` | `1 (0)` | `8` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-22** | `72.0s` | `53.0s` | `19.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-19** | `65.0s` | `49.0s` | `16.0s` | `1 (0)` | `6` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-29** | `64.0s` | `49.0s` | `15.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-20** | `63.0s` | `52.0s` | `11.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer H-03** | `61.0s` | `49.0s` | `12.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer H-03** | `57.0s` | `43.0s` | `14.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-02** | `48.0s` | `37.0s` | `11.0s` | `1 (0)` | `8` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer H-03** | `38.0s` | `24.0s` | `14.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |