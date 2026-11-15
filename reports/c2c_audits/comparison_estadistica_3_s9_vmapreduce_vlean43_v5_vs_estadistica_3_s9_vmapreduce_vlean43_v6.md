# Comparativa Arquitectónica Forense de Telemetría
### `estadistica_3_s9_vmapreduce_vlean43_v5` vs `estadistica_3_s9_vmapreduce_vlean43_v6`

**Fecha:** `2026-11-14 21:47:54 UTC`

---

## 1. Tabla Comparativa de Telemetría Real

| Métrica | Estadistica 3 S9 vMapReduce vlean4.3 v5 (`estadistica_3_s9_vmapreduce_vlean43_v5`) | Estadistica 3 S9 Vmapreduce Vlean43 V6 (`estadistica_3_s9_vmapreduce_vlean43_v6`) | Factor de Crecimiento / Cambio |
| :--- | :--- | :--- | :--- |
| **Material de Entrada** | 2 archivos (80 págs) | 2 archivos (80 págs) | +0.0% (1.0x) |
| **Competencias Extraídas** | 20 competencias | 29 competencias | +45.0% (1.4x) |
| **Subagentes Desplegados** | 26 subagentes | 31 subagentes | +19.2% (1.2x) |
| **Reactivos Validados** | 490 reactivos | 680 reactivos | +38.8% (1.4x) |
| **Tokens Entrada (Subagentes)** | 1,705,433 | 1,444,599 | -15.3% (0.85x) |
| **Tokens Salida (Subagentes)** | 828,888 | 506,882 | -38.8% (0.61x) |
| **Tokens Caché (Leídos)** | 13,024,547 | 12,069,089 | -7.3% (0.93x) |
| **Gran Total Tokens Activos** | 2,775,941 | 2,222,391 | -19.9% (0.80x) |
| **Gran Total Facturable** | 15,800,488 | 14,291,480 | -9.6% (0.90x) |
| **Tiempo de Pared (Wall Clock)** | 20.7 min (1242.0s) | 12.9 min (773.0s) | -37.8% (0.62x) |
| **Factor de Aceleración Paralela** | 4.28x | 4.57x | +0.29x |
| **Tokens / Pregunta** | 32,245.9 | 21,016.9 | -34.8% (0.65x) |
| **Segundos / Pregunta** | 2.53s | 1.14s | -54.9% (0.45x) |
| **Blind Judges (1er Intento)** | ✅ Pasó (100% limpio) | ✅ Pasó (100% limpio) | Paridad |
| **Intervenciones Manuales (Orch)** | 0 fixes | 0 fixes | +0 intervenciones |

---

## 2. Variación Determinista de Ratios

- **Intensidad de Tokens por Pregunta**: `32,245.9` -> `21,016.9` (-34.8% (0.65x)).
- **Multiplicador de Tokens Activos**: `-19.9% (0.80x)`.
- **Ritmo de Entrega (Seg/Pregunta)**: `2.53s` -> `1.14s`.
- **Arbitraje de Blind Judges (1er Intento)**: `Estadistica 3 S9 vMapReduce vlean4.3 v5 (`estadistica_3_s9_vmapreduce_vlean43_v5`)` = `True`, `Estadistica 3 S9 Vmapreduce Vlean43 V6 (`estadistica_3_s9_vmapreduce_vlean43_v6`)` = `True`.
- **Intervenciones del Supervisor**: `0` vs `0`.

---
*Generado por el motor forense `c2c-run-auditor`.*