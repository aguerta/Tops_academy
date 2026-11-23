### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `12` | **Mediana de Pared:** `163.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_07` (`108.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_11** | `251.0s` | `62.0s` | `189.0s` | `4 (3)` | `8` | `[TPL-DRY], [INVARIANT]` | Remediación (3 fallos) |
| **Shard Author shard_09** | `217.0s` | `62.0s` | `155.0s` | `4 (3)` | `3` | `[TPL-DRY]` | Remediación (3 fallos) |
| **Shard Author shard_06** | `183.0s` | `42.0s` | `141.0s` | `5 (4)` | `5` | `[TPL-DRY], [TPL-D3], [TPL-DYNAMIC-RATIONALE]` | Remediación (4 fallos) |
| **Shard Author shard_10** | `181.0s` | `65.0s` | `116.0s` | `3 (2)` | `8` | `[TPL-ORPHAN-VARS], [TPL-DRY]` | Remediación (2 fallos) |
| **Shard Author shard_08** | `174.0s` | `61.0s` | `113.0s` | `4 (3)` | `5` | `[TPL-ORPHAN-VARS], [TPL-DRY], [TPL-M20-INVARIANT-CANVAS]` | Remediación (3 fallos) |
| **Shard Author shard_04** | `163.0s` | `43.0s` | `120.0s` | `4 (3)` | `4` | `[TPL-ORPHAN-VARS], [TPL-DRY], [TPL-D3]` | Remediación (3 fallos) |
| **Shard Author shard_01** | `142.0s` | `46.0s` | `96.0s` | `3 (2)` | `2` | `[TPL-ORPHAN-VARS], [TPL-M20-UNSTRUCTURED-MODEL], [TPL-DRY]` | Remediación (2 fallos) |
| **Shard Author shard_02** | `141.0s` | `45.0s` | `96.0s` | `3 (3)` | `3` | `[TPL-EPISTEMIC-CLOSURE], [TPL-D3], [TPL-DRY]` | Remediación (3 fallos) |
| **Shard Author shard_03** | `137.0s` | `46.0s` | `91.0s` | `4 (3)` | `5` | `[TPL-M20-UNSTRUCTURED-MODEL], [TPL-DRY], [TPL-D3]` | Remediación (3 fallos) |
| **Shard Author shard_05** | `129.0s` | `43.0s` | `86.0s` | `3 (2)` | `4` | `[TPL-DRY], [TPL-D3]` | Remediación (2 fallos) |
| **Shard Author shard_12** | `118.0s` | `54.0s` | `64.0s` | `2 (1)` | `0` | `[TPL-DRY]` | Remediación (1 fallos) |
| **Shard Author shard_07** | `108.0s` | `45.0s` | `63.0s` | `3 (2)` | `3` | `[TPL-ORPHAN-VARS], [TPL-DRY], [TPL-M20-INVARIANT-CANVAS]` | Remediación (2 fallos) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `1` | **Mediana de Pared:** `41.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer Hab-01** | `41.0s` | `21.0s` | `20.0s` | `1 (1)` | `2` | `[TPL-M20-INVARIANT-CANVAS], [TPL-VERIFIER-UNSOUND], [TPL-D3]` | Re-intento tras fallo (1 fallos) |