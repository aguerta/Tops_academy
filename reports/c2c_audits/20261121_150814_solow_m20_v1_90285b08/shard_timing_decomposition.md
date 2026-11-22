### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `9` | **Mediana de Pared:** `218.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_05` (`154.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_02** | `319.0s` | `109.0s` | `210.0s` | `3 (2)` | `2` | `[TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP], [INVARIANT]` | Remediación (2 fallos) |
| **Shard Author shard_06** | `245.0s` | `109.0s` | `136.0s` | `2 (2)` | `0` | `[TPL-ASM], [TPL-D1], [TPL-DRY]` | Remediación (2 fallos) |
| **Shard Author shard_08** | `236.0s` | `119.0s` | `117.0s` | `2 (1)` | `0` | `[TPL-DYNAMIC-RATIONALE], [TPL-ORPHAN-VARS], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_04** | `223.0s` | `100.0s` | `123.0s` | `2 (1)` | `0` | `[TPL-DRY], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_03** | `218.0s` | `103.0s` | `115.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-STATIC-OPT], [TPL-VAR]` | Remediación (1 fallos) |
| **Shard Author shard_01** | `215.0s` | `88.0s` | `127.0s` | `2 (1)` | `0` | `[TPL-ORPHAN-VARS], [TPL-DRY]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `212.0s` | `126.0s` | `86.0s` | `2 (2)` | `5` | `[TPL-ORPHAN-VARS], [TPL-D2], [R-15]` | Remediación (2 fallos) |
| **Shard Author shard_09** | `201.0s` | `93.0s` | `108.0s` | `2 (2)` | `0` | `[TPL-ORPHAN-VARS], [TPL-D2], [INVARIANT]` | Remediación (2 fallos) |
| **Shard Author shard_05** | `154.0s` | `89.0s` | `65.0s` | `2 (1)` | `2` | `[TPL-VERIFIER-UNSOUND], [TPL-STATIC-OPT], [TPL-DRY]` | Remediación (1 fallos) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `15` | **Mediana de Pared:** `78.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer C-01** | `134.0s` | `23.0s` | `111.0s` | `3 (3)` | `4` | `[TPL-ORPHAN-VARS], [TPL-D1], [TPL-DRY]` | Re-intento tras fallo (3 fallos) |
| **Repair Engineer C-01** | `110.0s` | `63.0s` | `47.0s` | `2 (2)` | `2` | `[TPL-ORPHAN-VARS], [TPL-D2], [TPL-D1]` | Re-intento tras fallo (2 fallos) |
| **Repair Engineer shard_09 (C-04, H-01)** | `105.0s` | `58.0s` | `47.0s` | `2 (2)` | `8` | `[TPL-D2], [TPL-VAR], ValueError: Distractor ID 'D-H01-04' no esta declarado en cta.json (H-01).` | Re-intento tras fallo (2 fallos) |
| **Repair Engineer shard_09 (C-04, C-05, H-01)** | `92.0s` | `25.0s` | `67.0s` | `2 (2)` | `7` | `[TPL-D2], [TPL-AD-HOC-PERTURBATION], [TPL-UNBOUNDED-LOOP]` | Re-intento tras fallo (2 fallos) |
| **Repair Engineer shard_09 (C-04, H-01)** | `90.0s` | `33.0s` | `57.0s` | `2 (2)` | `7` | `[CTA-MODALITY-PLAN], [TPL-D2], [TPL-DRY]` | Re-intento tras fallo (2 fallos) |
| **Repair Engineer shard_09 (C-04, H-01)** | `90.0s` | `31.0s` | `59.0s` | `2 (1)` | `8` | `[TPL-DYNAMIC-RATIONALE], [CTA-MODALITY-PLAN], [TPL-D2]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer shard_07 (C-06, C-07, C-08)** | `84.0s` | `20.0s` | `64.0s` | `2 (2)` | `7` | `[TPL-D2], [CTA-MODALITY-PLAN]` | Re-intento tras fallo (2 fallos) |
| **Repair Engineer shard_06 (C-01, C-02, C-03)** | `78.0s` | `18.0s` | `60.0s` | `2 (2)` | `4` | `[TPL-D2], [TPL-ORPHAN-VARS], [CTA-MODALITY-PLAN]` | Re-intento tras fallo (2 fallos) |
| **Repair Engineer C-06** | `71.0s` | `49.0s` | `22.0s` | `1 (1)` | `5` | `[TPL-D2]` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer C-06** | `69.0s` | `21.0s` | `48.0s` | `2 (2)` | `4` | `[CTA-MODALITY-PLAN], [TPL-D1], [TPL-DRY]` | Re-intento tras fallo (2 fallos) |
| **Repair Engineer Hab-04** | `56.0s` | `30.0s` | `26.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-01** | `45.0s` | `32.0s` | `13.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-03** | `41.0s` | `26.0s` | `15.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-06** | `38.0s` | `24.0s` | `14.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-09** | `34.0s` | `19.0s` | `15.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |