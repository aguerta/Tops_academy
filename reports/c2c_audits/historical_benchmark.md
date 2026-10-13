# Content-to-Course: Registro Histórico y Evolución de Rendimiento

> [!NOTE]
> Este documento se actualiza automáticamente con cada auditoría ejecutada. Última actualización: `2026-10-13 14:54:30`. Total de ejecuciones auditadas: **2**.

## 1. Matriz de Evolución Temporal (Normalizada por Carga de Contenido)

| Fecha | Run / Curso | Input (Pág / MB) | Output (Comp / Preg) | Tiempo de Pared | Speedup | Tokens Totales | Tok / Preg | Seg / Preg | Blind Judges (1st) | Intervenciones | Bottlenecks |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `2026-10-13 19:54` | **solow_growth_model** | 36 pág (0.0 MB) | 25 comp / 580 preg | 143.2 min (8595.0s) | **1.74x** | 48,667,362 | **83,909.2** | **14.82s** | ❌ Falló | 🛠️ 4 | ⚠️ 3 |
| `2026-10-10 12:00` | **estadistica3_regresion_v3** | 50 pág (1.2 MB) | 16 comp / 480 preg | 60.0 min (3600.0s) | **2.0x** | 8,645,000 | **18,010.4** | **7.5s** | ✅ Limpio | 🛠️ 0 | ✅ 0 |

---

## 2. Métricas Promedio del Sistema (Baselines Globales)

- **Factor de Aceleración Paralela Promedio**: `1.87x`
- **Densidad de Tokens Promedio por Pregunta**: `50,959.8 tokens/pregunta`
- **Latencia Promedio por Pregunta Validada**: `11.16 s/pregunta`
- **Rendimiento Promedio de Generación**: `6.03 preguntas/minuto`

---
*Generado por el motor forense `c2c-run-auditor`.*