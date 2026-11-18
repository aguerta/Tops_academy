# Comparativa Arquitectónica Forense de Telemetría
### `estadistica_3_pre_pc2` vs `estadistica_3_pre_pc2_v7`

**Fecha:** `2026-11-18 18:29:00 UTC`

---

## 1. Tabla Comparativa de Telemetría Real

| Métrica | Estadistica 3 Pre Pc2 (`estadistica_3_pre_pc2`) | Estadistica 3 Pre Pc2 V7 (`estadistica_3_pre_pc2_v7`) | Factor de Crecimiento / Cambio |
| :--- | :--- | :--- | :--- |
| **Material de Entrada** | 4 archivos (129 págs) | 4 archivos (129 págs) | +0.0% (1.0x) |
| **Competencias Extraídas** | 57 competencias | 53 competencias | -7.0% (0.93x) |
| **Subagentes Desplegados** | 103 subagentes | 49 subagentes | -52.4% (0.48x) |
| **Reactivos Validados** | 1390 reactivos | 1290 reactivos | -7.2% (0.93x) |
| **Tokens Entrada (Subagentes)** | 9,031,361 | 2,601,669 | -71.2% (0.29x) |
| **Tokens Salida (Subagentes)** | 2,080,550 | 1,031,381 | -50.4% (0.50x) |
| **Tokens Caché (Leídos)** | 75,427,901 | 17,602,703 | -76.7% (0.23x) |
| **Gran Total Tokens Activos** | 12,977,604 | 3,950,909 | -69.6% (0.30x) |
| **Gran Total Facturable** | 88,405,505 | 21,553,612 | -75.6% (0.24x) |
| **Tiempo de Pared (Wall Clock)** | 125.8 min (7545.0s) | 19.2 min (1155.0s) | -84.7% (0.15x) |
| **Factor de Aceleración Paralela** | 9.23x | 6.7x | -2.53x |
| **Tokens / Pregunta** | 63,601.1 | 16,708.2 | -73.7% (0.26x) |
| **Segundos / Pregunta** | 5.43s | 0.9s | -83.4% (0.17x) |
| **Blind Judges (1er Intento)** | ❌ Falló (0 fixes) | ❌ Falló (0 fixes) | Paridad |
| **Intervenciones Manuales (Orch)** | 0 fixes | 0 fixes | +0 intervenciones |

---

## 2. Variación Determinista de Ratios

- **Intensidad de Tokens por Pregunta**: `63,601.1` -> `16,708.2` (-73.7% (0.26x)).
- **Multiplicador de Tokens Activos**: `-69.6% (0.30x)`.
- **Ritmo de Entrega (Seg/Pregunta)**: `5.43s` -> `0.9s`.
- **Arbitraje de Blind Judges (1er Intento)**: `Estadistica 3 Pre Pc2 (`estadistica_3_pre_pc2`)` = `False`, `Estadistica 3 Pre Pc2 V7 (`estadistica_3_pre_pc2_v7`)` = `False`.
- **Intervenciones del Supervisor**: `0` vs `0`.

---
*Generado por el motor forense `c2c-run-auditor`.*