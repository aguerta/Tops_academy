# Comparativa Arquitectónica Forense de Telemetría
### `asyntotic_estatistics_v7` vs `gavilano_pre_parcial`

**Fecha:** `2026-10-25 01:24:26 UTC`

---

## 1. Tabla Comparativa de Telemetría Real

| Métrica | Asyntotic Estatistics V7 (`asyntotic_estatistics_v7`) | Gavilano Pre Parcial (`gavilano_pre_parcial`) | Factor de Crecimiento / Cambio |
| :--- | :--- | :--- | :--- |
| **Material de Entrada** | 2 archivos (52 págs) | 10 archivos (246 págs) | +373.1% (4.7x) |
| **Competencias Extraídas** | 32 competencias | 127 competencias | +296.9% (4.0x) |
| **Subagentes Desplegados** | 28 subagentes | 115 subagentes | **+310.7% (4.1x)** |
| **Reactivos Validados** | 710 reactivos | 2950 reactivos | +315.5% (4.2x) |
| **Tokens Entrada (Subagentes)** | 3,222,680 | 10,797,598 | **+235.1% (3.4x)** |
| **Tokens Salida (Subagentes)** | 1,180,298 | 4,116,669 | **+248.8% (3.5x)** |
| **Tokens Caché (Leídos)** | 16,650,083 | 44,838,076 | **+169.3% (2.7x)** |
| **Gran Total Tokens Activos** | 4,975,558 | 15,487,713 | **+211.3% (3.1x)** |
| **Gran Total Facturable** | 21,625,641 | 60,325,789 | **+179.0% (2.8x)** |
| **Tiempo de Pared (Wall Clock)** | 31.6 min (1896.0s) | 47.4 min (2844.0s) | +50.0% (1.5x) |
| **Factor de Aceleración Paralela** | 5.53x | 11.41x | +5.88x |
| **Tokens / Pregunta** | 30,458.6 | 20,449.4 | -32.9% (0.67x) |
| **Segundos / Pregunta** | 2.67s | 0.96s | -64.0% (0.36x) |
| **Blind Judges (1er Intento)** | ✅ Pasó (100% limpio) | ✅ Pasó (100% limpio) | Paridad |
| **Intervenciones Manuales (Orch)** | 0 fixes | 0 fixes | +0 intervenciones |

---

## 2. Variación Determinista de Ratios

- **Intensidad de Tokens por Pregunta**: `30,458.6` -> `20,449.4` (-32.9% (0.67x)).
- **Multiplicador de Tokens Activos**: `**+211.3% (3.1x)**`.
- **Ritmo de Entrega (Seg/Pregunta)**: `2.67s` -> `0.96s`.
- **Arbitraje de Blind Judges (1er Intento)**: `Asyntotic Estatistics V7 (`asyntotic_estatistics_v7`)` = `True`, `Gavilano Pre Parcial (`gavilano_pre_parcial`)` = `True`.
- **Intervenciones del Supervisor**: `0` vs `0`.

---
*Generado por el motor forense `c2c-run-auditor`.*