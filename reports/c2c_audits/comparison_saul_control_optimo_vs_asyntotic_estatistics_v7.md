# Comparativa Arquitectónica Forense de Telemetría
### `saul_control_optimo` vs `asyntotic_estatistics_v7`

**Fecha:** `2026-10-25 01:24:30 UTC`

---

## 1. Tabla Comparativa de Telemetría Real

| Métrica | Saul Control Optimo (`saul_control_optimo`) | Asyntotic Estatistics V7 (`asyntotic_estatistics_v7`) | Factor de Crecimiento / Cambio |
| :--- | :--- | :--- | :--- |
| **Material de Entrada** | 1 archivos (32 págs) | 2 archivos (52 págs) | +62.5% (1.6x) |
| **Competencias Extraídas** | 15 competencias | 32 competencias | +113.3% (2.1x) |
| **Subagentes Desplegados** | 14 subagentes | 28 subagentes | **+100.0% (2.0x)** |
| **Reactivos Validados** | 350 reactivos | 710 reactivos | +102.9% (2.0x) |
| **Tokens Entrada (Subagentes)** | 1,426,821 | 3,222,680 | **+125.9% (2.3x)** |
| **Tokens Salida (Subagentes)** | 555,194 | 1,180,298 | **+112.6% (2.1x)** |
| **Tokens Caché (Leídos)** | 7,059,374 | 16,650,083 | **+135.9% (2.4x)** |
| **Gran Total Tokens Activos** | 2,208,012 | 4,975,558 | **+125.3% (2.3x)** |
| **Gran Total Facturable** | 9,267,386 | 21,625,641 | **+133.4% (2.3x)** |
| **Tiempo de Pared (Wall Clock)** | 22.3 min (1340.0s) | 31.6 min (1896.0s) | +41.5% (1.4x) |
| **Factor de Aceleración Paralela** | 3.9x | 5.53x | +1.63x |
| **Tokens / Pregunta** | 26,478.2 | 30,458.6 | +15.0% (1.2x) |
| **Segundos / Pregunta** | 3.83s | 2.67s | -30.3% (0.70x) |
| **Blind Judges (1er Intento)** | ✅ Pasó (100% limpio) | ✅ Pasó (100% limpio) | Paridad |
| **Intervenciones Manuales (Orch)** | 0 fixes | 0 fixes | +0 intervenciones |

---

## 2. Variación Determinista de Ratios

- **Intensidad de Tokens por Pregunta**: `26,478.2` -> `30,458.6` (+15.0% (1.2x)).
- **Multiplicador de Tokens Activos**: `**+125.3% (2.3x)**`.
- **Ritmo de Entrega (Seg/Pregunta)**: `3.83s` -> `2.67s`.
- **Arbitraje de Blind Judges (1er Intento)**: `Saul Control Optimo (`saul_control_optimo`)` = `True`, `Asyntotic Estatistics V7 (`asyntotic_estatistics_v7`)` = `True`.
- **Intervenciones del Supervisor**: `0` vs `0`.

---
*Generado por el motor forense `c2c-run-auditor`.*