# Content-to-Course: Registro Histórico y Evolución de Rendimiento

> [!NOTE]
> Este documento se actualiza automáticamente con cada auditoría ejecutada. Última actualización: `2026-10-13 00:22:34`. Total de ejecuciones auditadas: **2**.

## 1. Matriz de Evolución Temporal (Normalizada por Carga de Contenido)

| Fecha | Run / Curso | Input (Pág / MB) | Output (Comp / Preg) | Tiempo de Pared | Speedup | Tokens Totales | Tok / Preg | Seg / Preg | Blind Judges (1st) | Intervenciones | Bottlenecks |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `2026-10-13 05:22` | **solow_growth_model** | 36 pág (0.0 MB) | 22 comp / 530 preg | 13.9 min (832.0s) | **11.18x** | 60,073,119 | **113,345.5** | **1.57s** | ✅ Limpio | 🛠️ 0 | ⚠️ 2 |
| `2026-10-10 12:00` | **estadistica3_regresion_v3** | 50 pág (1.2 MB) | 16 comp / 480 preg | 60.0 min (3600.0s) | **2.0x** | 8,645,000 | **18,010.4** | **7.5s** | ✅ Limpio | 🛠️ 0 | ✅ 0 |

---

## 2. Métricas Promedio del Sistema (Baselines Globales)

- **Factor de Aceleración Paralela Promedio**: `6.59x`
- **Densidad de Tokens Promedio por Pregunta**: `65,677.9 tokens/pregunta`
- **Latencia Promedio por Pregunta Validada**: `4.54 s/pregunta`
- **Rendimiento Promedio de Generación**: `23.11 preguntas/minuto`

---
*Generado por el motor forense `c2c-run-auditor`.*