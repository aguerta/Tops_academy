### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `9` | **Mediana de Pared:** `326.0s`
- **Gold Standard Clean-Room:** `Shard Author shard_05` (`93.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Shard Author shard_01** | `518.0s` | `200.0s` | `324.0s` | `3 (2)` | `3` | `[R-15]` | Remediación (2 fallos) |
| **Shard Author shard_08** | `434.0s` | `181.0s` | `265.0s` | `3 (2)` | `1` | `0 errores` | Remediación (2 fallos) |
| **Shard Author shard_06** | `418.0s` | `211.0s` | `218.0s` | `3 (2)` | `12` | `0 errores` | Remediación (2 fallos) |
| **Shard Author shard_02** | `394.0s` | `188.0s` | `214.0s` | `2 (1)` | `1` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_07** | `326.0s` | `189.0s` | `148.0s` | `2 (1)` | `2` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_04** | `298.0s` | `183.0s` | `123.0s` | `2 (1)` | `3` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_03** | `226.0s` | `166.0s` | `68.0s` | `2 (1)` | `3` | `0 errores` | Remediación (1 fallos) |
| **Shard Author shard_09** | `221.0s` | `138.0s` | `96.0s` | `2 (1)` | `0` | `[TPL-DRY]` | Remediación (1 fallos) |
| **Shard Author shard_05** | `93.0s` | `93.0s` | `14.0s` | `1 (0)` | `0` | `0 errores` | Ejecución fluida (Pase limpio) |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `2` | **Mediana de Pared:** `62.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer (HAB08)** | `62.0s` | `44.0s` | `22.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer (HAB03)** | `47.0s` | `33.0s` | `17.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |