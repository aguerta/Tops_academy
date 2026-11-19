### Descomposición Temporal y Forense Multi-Shard (`Pre` vs `Post` 1st Compile)
- **Total Shards Auditados:** `0` | **Mediana de Pared:** `0.0s`
- **Gold Standard Clean-Room:** `N/A` (`0.0s`, 0 fallos, 0 ediciones post-escritura)

| Shard | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |

---

### Descomposición Temporal y Forense de Repair Engineers (Stage 3B Remediación)
- **Total Repair Engineers Auditados:** `10` | **Mediana de Pared:** `61.0s`

| Repair Engineer | Duración Total (s) | Pre-1st-Compile (s) | Post-1st-Compile (s) | Compiles (Fails) | Edits | Errores / Códigos | Diagnóstico Causa Raíz |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Repair Engineer shard_11 (C-14, C-15)** | `283.0s` | `148.0s` | `135.0s` | `3 (2)` | `9` | `[R-15], [R-16], [R-19]` | Re-intento tras fallo (2 fallos) |
| **Repair Engineer Hab-03** | `102.0s` | `81.0s` | `21.0s` | `1 (0)` | `5` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-04** | `70.0s` | `48.0s` | `22.0s` | `1 (0)` | `4` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-03** | `63.0s` | `47.0s` | `16.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-07** | `61.0s` | `41.0s` | `20.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-04** | `58.0s` | `41.0s` | `17.0s` | `1 (0)` | `3` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-03** | `58.0s` | `43.0s` | `15.0s` | `1 (1)` | `1` | `0 errores` | Re-intento tras fallo (1 fallos) |
| **Repair Engineer Hab-13** | `45.0s` | `31.0s` | `14.0s` | `1 (0)` | `1` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer Hab-19** | `42.0s` | `31.0s` | `11.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |
| **Repair Engineer C-17** | `37.0s` | `24.0s` | `13.0s` | `1 (0)` | `2` | `0 errores` | Parche aplicado exitosamente |