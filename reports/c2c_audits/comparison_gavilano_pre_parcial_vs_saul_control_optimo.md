# Comparativa Arquitectónica Forense de Telemetría
### `gavilano_pre_parcial` vs `saul_control_optimo`

**Fecha:** `2026-10-25 01:24:22 UTC`

---

## 1. Tabla Comparativa de Telemetría Real

| Métrica | Gavilano Pre Parcial (`gavilano_pre_parcial`) | Saul Control Optimo (`saul_control_optimo`) | Factor de Crecimiento / Cambio |
| :--- | :--- | :--- | :--- |
| **Material de Entrada** | 10 archivos (246 págs) | 1 archivos (32 págs) | -87.0% (0.13x) |
| **Competencias Extraídas** | 127 competencias | 15 competencias | -88.2% (0.12x) |
| **Subagentes Desplegados** | 115 subagentes | 14 subagentes | -87.8% (0.12x) |
| **Reactivos Validados** | 2950 reactivos | 350 reactivos | -88.1% (0.12x) |
| **Tokens Entrada (Subagentes)** | 10,797,598 | 1,426,821 | -86.8% (0.13x) |
| **Tokens Salida (Subagentes)** | 4,116,669 | 555,194 | -86.5% (0.13x) |
| **Tokens Caché (Leídos)** | 44,838,076 | 7,059,374 | -84.3% (0.16x) |
| **Gran Total Tokens Activos** | 15,487,713 | 2,208,012 | -85.7% (0.14x) |
| **Gran Total Facturable** | 60,325,789 | 9,267,386 | -84.6% (0.15x) |
| **Tiempo de Pared (Wall Clock)** | 47.4 min (2844.0s) | 22.3 min (1340.0s) | -52.9% (0.47x) |
| **Factor de Aceleración Paralela** | 11.41x | 3.9x | -7.51x |
| **Tokens / Pregunta** | 20,449.4 | 26,478.2 | +29.5% (1.3x) |
| **Segundos / Pregunta** | 0.96s | 3.83s | **+299.0% (4.0x)** |
| **Blind Judges (1er Intento)** | ✅ Pasó (100% limpio) | ✅ Pasó (100% limpio) | Paridad |
| **Intervenciones Manuales (Orch)** | 0 fixes | 0 fixes | +0 intervenciones |

---

## 2. Variación Determinista de Ratios

- **Intensidad de Tokens por Pregunta**: `20,449.4` -> `26,478.2` (+29.5% (1.3x)).
- **Multiplicador de Tokens Activos**: `-85.7% (0.14x)`.
- **Ritmo de Entrega (Seg/Pregunta)**: `0.96s` -> `3.83s`.
- **Arbitraje de Blind Judges (1er Intento)**: `Gavilano Pre Parcial (`gavilano_pre_parcial`)` = `True`, `Saul Control Optimo (`saul_control_optimo`)` = `True`.
- **Intervenciones del Supervisor**: `0` vs `0`.

---
*Generado por el motor forense `c2c-run-auditor`.*