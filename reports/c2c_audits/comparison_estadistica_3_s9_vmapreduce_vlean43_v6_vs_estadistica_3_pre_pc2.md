# Comparativa Arquitectónica Forense de Telemetría
### `estadistica_3_s9_vmapreduce_vlean43_v6` vs `estadistica_3_pre_pc2`

**Fecha:** `2026-11-18 18:29:00 UTC`

---

## 1. Tabla Comparativa de Telemetría Real

| Métrica | Estadistica 3 S9 Vmapreduce Vlean43 V6 (`estadistica_3_s9_vmapreduce_vlean43_v6`) | Estadistica 3 Pre Pc2 (`estadistica_3_pre_pc2`) | Factor de Crecimiento / Cambio |
| :--- | :--- | :--- | :--- |
| **Material de Entrada** | 2 archivos (80 págs) | 4 archivos (129 págs) | +61.3% (1.6x) |
| **Competencias Extraídas** | 29 competencias | 57 competencias | +96.6% (2.0x) |
| **Subagentes Desplegados** | 31 subagentes | 103 subagentes | **+232.3% (3.3x)** |
| **Reactivos Validados** | 680 reactivos | 1390 reactivos | +104.4% (2.0x) |
| **Tokens Entrada (Subagentes)** | 1,444,599 | 9,031,361 | **+525.2% (6.3x)** |
| **Tokens Salida (Subagentes)** | 506,882 | 2,080,550 | **+310.5% (4.1x)** |
| **Tokens Caché (Leídos)** | 12,314,632 | 75,427,901 | **+512.5% (6.1x)** |
| **Gran Total Tokens Activos** | 2,231,284 | 12,977,604 | **+481.6% (5.8x)** |
| **Gran Total Facturable** | 14,545,916 | 88,405,505 | **+507.8% (6.1x)** |
| **Tiempo de Pared (Wall Clock)** | 13.2 min (789.0s) | 125.8 min (7545.0s) | **+856.3% (9.6x)** |
| **Factor de Aceleración Paralela** | 4.5x | 9.23x | +4.73x |
| **Tokens / Pregunta** | 21,391.1 | 63,601.1 | **+197.3% (3.0x)** |
| **Segundos / Pregunta** | 1.16s | 5.43s | **+368.1% (4.7x)** |
| **Blind Judges (1er Intento)** | ✅ Pasó (100% limpio) | ❌ Falló (0 fixes) | Cambio de estado |
| **Intervenciones Manuales (Orch)** | 0 fixes | 0 fixes | +0 intervenciones |

---

## 2. Variación Determinista de Ratios

- **Intensidad de Tokens por Pregunta**: `21,391.1` -> `63,601.1` (**+197.3% (3.0x)**).
- **Multiplicador de Tokens Activos**: `**+481.6% (5.8x)**`.
- **Ritmo de Entrega (Seg/Pregunta)**: `1.16s` -> `5.43s`.
- **Arbitraje de Blind Judges (1er Intento)**: `Estadistica 3 S9 Vmapreduce Vlean43 V6 (`estadistica_3_s9_vmapreduce_vlean43_v6`)` = `True`, `Estadistica 3 Pre Pc2 (`estadistica_3_pre_pc2`)` = `False`.
- **Intervenciones del Supervisor**: `0` vs `0`.

---
*Generado por el motor forense `c2c-run-auditor`.*