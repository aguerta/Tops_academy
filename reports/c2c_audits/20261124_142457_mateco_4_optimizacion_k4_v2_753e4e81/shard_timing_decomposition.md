### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `32` | **Mediana de Pared:** `168.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_24` (`107.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_18** | `279.0s` | `162.0s` | `117.0s` | `2 (1)` | `0` | `[INVARIANT], [TPL-STEM-EQUATION-PARITY], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_02** | `241.0s` | `128.0s` | `113.0s` | `2 (1)` | `0` | `[TPL-STEM-SYMBOL-PARITY], [TPL-STEM-EQUATION-PARITY], [TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_09** | `241.0s` | `122.0s` | `119.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-STEM-SYMBOL-PARITY], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_10** | `240.0s` | `122.0s` | `118.0s` | `2 (1)` | `0` | `[VERIFIER-TAUTOLOGY-DETECTED], [TPL-STEM-EQUATION-PARITY], [TPL-D4]` | Remediación (1 fallos) |
| **Shard Author shard_16** | `234.0s` | `116.0s` | `118.0s` | `4 (3)` | `8` | `[TPL-ORPHAN-VARS], [TPL-STEM-VARIANT-PARITY], [TPL-TAUTOLOGICAL-IDENTITY]` | Remediación (3 fallos) |
| **Shard Author shard_05** | `220.0s` | `131.0s` | `89.0s` | `2 (1)` | `3` | `[TPL-ORPHAN-VARS], [TPL-STEM-GRAMMAR], [INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_14** | `210.0s` | `135.0s` | `75.0s` | `2 (1)` | `9` | `[TPL-DYNAMIC-RATIONALE], [TPL-STEM-VARIANT-PARITY], [TPL-DIAG-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_25** | `207.0s` | `116.0s` | `91.0s` | `2 (1)` | `0` | `[TPL-STEM-SYMBOL-PARITY], [TPL-STEM-VARIANT-PARITY], [INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `205.0s` | `143.0s` | `62.0s` | `2 (1)` | `1` | `[TPL-ORPHAN-VARS], [TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_06** | `199.0s` | `104.0s` | `95.0s` | `2 (1)` | `0` | `[TPL-STEM-VARIANT-PARITY], [TPL-STEM-EQUATION-PARITY], [INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `197.0s` | `148.0s` | `49.0s` | `2 (1)` | `1` | `[TPL-DYNAMIC-RATIONALE], [INVARIANT]` | Remediación (1 fallos) |
| **Shard Author shard_03** | `195.0s` | `131.0s` | `64.0s` | `2 (1)` | `5` | `[TPL-KATEX-SYMPY-LEAK], [TPL-STATIC-OPT], [TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_21** | `187.0s` | `103.0s` | `84.0s` | `2 (1)` | `0` | `[TPL-MS-ABSOLUTE-WORD-BIAS], [TPL-STEM-GRAMMAR], [TPL-DYNAMIC-RATIONALE]` | Remediación (1 fallos) |
| **Shard Author shard_17** | `186.0s` | `121.0s` | `65.0s` | `3 (2)` | `3` | `[TPL-STATIC-OPT], [TPL-DYNAMIC-RATIONALE]` | Remediación (2 fallos) |
| **Shard Author shard_19** | `177.0s` | `122.0s` | `55.0s` | `2 (1)` | `5` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [TPL-STEM-SYMBOL-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_13** | `168.0s` | `120.0s` | `48.0s` | `2 (1)` | `3` | `[TPL-STEM-SYMBOL-PARITY], [INVARIANT], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_20** | `166.0s` | `122.0s` | `44.0s` | `2 (1)` | `4` | `[TPL-STEM-SYMBOL-PARITY], [INVARIANT], [TPL-DEGENERATE-LITERAL-COND]` | Remediación (1 fallos) |
| **Shard Author shard_12** | `162.0s` | `110.0s` | `52.0s` | `2 (1)` | `2` | `[TPL-ORPHAN-VARS], [TPL-STEM-SYMBOL-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_08** | `157.0s` | `121.0s` | `36.0s` | `2 (1)` | `1` | `[TPL-ORPHAN-VARS], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_11** | `154.0s` | `100.0s` | `54.0s` | `2 (1)` | `6` | `[TPL-D4], [R-19]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `151.0s` | `107.0s` | `44.0s` | `2 (1)` | `3` | `[TPL-ORPHAN-VARS], [TPL-STEM-SYMBOL-PARITY], [TPL-STEM-VARIANT-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_29** | `151.0s` | `105.0s` | `46.0s` | `2 (1)` | `2` | `[TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_26** | `134.0s` | `93.0s` | `41.0s` | `2 (1)` | `1` | `[TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (1 fallos) |
| **Shard Author shard_31** | `133.0s` | `118.0s` | `15.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_30** | `128.0s` | `80.0s` | `48.0s` | `2 (1)` | `5` | `[TPL-MS-CONDITIONAL-DISTRACTOR], [TPL-DYNAMIC-RATIONALE], [TPL-STATIC-OPT]` | Remediación (1 fallos) |
| **Shard Author shard_22** | `124.0s` | `80.0s` | `44.0s` | `2 (1)` | `4` | `[TPL-ORPHAN-VARS], [TPL-DIGIT-PLACEHOLDER-CONCAT]` | Remediación (1 fallos) |
| **Shard Author shard_32** | `122.0s` | `88.0s` | `34.0s` | `2 (1)` | `1` | `[TPL-STEM-EQUATION-PARITY]` | Remediación (1 fallos) |
| **Shard Author shard_15** | `116.0s` | `98.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_23** | `115.0s` | `97.0s` | `18.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_28** | `114.0s` | `100.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_27** | `109.0s` | `93.0s` | `16.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |
| **Shard Author shard_24** | `107.0s` | `88.0s` | `19.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `6` | **Mediana de Pared:** `69.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-07** | `145.0s` | `60.0s` | `85.0s` | `3 (2)` | `7` | `[TPL-ORPHAN-VARS], [TPL-STEM-EQUATION-PARITY]` | Re-intento tras fallo (2 fallos) |
| **Repair Engineer Hab-13** | `80.0s` | `63.0s` | `17.0s` | `1 (0)` | `11` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-09** | `69.0s` | `50.0s` | `19.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-14** | `67.0s` | `50.0s` | `17.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-20** | `63.0s` | `30.0s` | `33.0s` | `2 (1)` | `3` | `SyntaxError en shard_05_data.py (Línea 578, Columna 190): f-string: expecting a valid expression after '{'` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer C-01** | `48.0s` | `32.0s` | `16.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |