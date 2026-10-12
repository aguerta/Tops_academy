# Comparativa Arquitectónica Forense de Telemetría
### `estadistica3_regresion_v3` vs `solow_growth_model`

**Fecha:** `2026-10-12 17:45:54 UTC`

---

## 1. Tabla Comparativa de Telemetría Real

| Métrica | Estadística III (Regresión Lineal y Multivariante) (`estadistica3_regresion_v3`) | El Modelo de Crecimiento Económico de Solow (1956) (`solow_growth_model`) | Factor de Crecimiento / Cambio |
| :--- | :--- | :--- | :--- |
| **Material de Entrada** | 5 archivos (50 págs) | 2 archivos (36 págs) | -28.0% (0.72x) |
| **Competencias Extraídas** | 16 competencias | 44 competencias | +175.0% (2.8x) |
| **Subagentes Desplegados** | 6 subagentes | 20 subagentes | **+233.3% (3.3x)** |
| **Reactivos Validados** | 480 reactivos | 1040 reactivos | +116.7% (2.2x) |
| **Tokens Entrada (Subagentes)** | 600,000 | 4,581,174 | **+663.5% (7.6x)** |
| **Tokens Salida (Subagentes)** | 45,000 | 1,059,019 | **+2253.4% (23.5x)** |
| **Tokens Caché (Leídos)** | 8,000,000 | 82,980,967 | **+937.3% (10.4x)** |
| **Gran Total Tokens Activos** | 699,000 | 7,818,817 | **+1018.6% (11.2x)** |
| **Gran Total Facturable** | 8,645,000 | 90,799,784 | **+950.3% (10.5x)** |
| **Tiempo de Pared (Wall Clock)** | 60.0 min (3600.0s) | 139.7 min (8383.0s) | **+132.9% (2.3x)** |
| **Factor de Aceleración Paralela** | 2.0x | 2.46x | +0.46x |
| **Tokens / Pregunta** | 18,010.4 | 87,307.5 | **+384.8% (4.8x)** |
| **Segundos / Pregunta** | 7.5s | 8.06s | +7.5% (1.1x) |
| **Blind Judges (1er Intento)** | ✅ Pasó perfecto (100% limpio) | ❌ Falló (Req. 17 fixes + auto-repair) | Desviación Crítica: Fallo R-18/R-19 |
| **Intervenciones Manuales (Orch)** | 0 fixes | 17 fixes | +17 intervenciones |

---

## 2. Diagnóstico Comparativo de Eficiencia

- **Intensidad de Tokens por Pregunta**: Pasó de `18,010.4` a `87,307.5` (**+384.8% (4.8x)**).
- **Multiplicador de Tokens Activos**: Las llamadas de subagentes escalaron por un factor de `**+1018.6% (11.2x)**`.
- **Ritmo de Entrega (Seg/Pregunta)**: Se modificó de `7.5s` a `8.06s`.
- **Arbitraje de Blind Judges**: `Estadística III (Regresión Lineal y Multivariante) (`estadistica3_regresion_v3`)` pasó de forma 100% limpia al primer intento, mientras que `El Modelo de Crecimiento Económico de Solow (1956) (`solow_growth_model`)` no pasó al primer intento (colapso por R-18/R-19) y requirió 17 intervenciones manuales del supervisor.
- **Intervenciones del Supervisor**: `0` en la corrida base vs `17` en la corrida analizada.

---
*Generado por el motor forense `c2c-run-auditor`.*