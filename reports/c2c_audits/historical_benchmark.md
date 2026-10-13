# Content-to-Course: Registro Histórico y Evolución de Rendimiento

> [!NOTE]
> Este documento se actualiza automáticamente con cada auditoría ejecutada. Última actualización: `2026-10-13 08:56:29`. Total de ejecuciones auditadas: **2**.

## 1. Matriz de Evolución Temporal (Normalizada por Carga de Contenido)

| Fecha | Run / Curso | Input (Pág / MB) | Output (Comp / Preg) | Tiempo de Pared | Speedup | Tokens Totales | Tok / Preg | Seg / Preg | Blind Judges (1st) | Intervenciones | Bottlenecks |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `2026-10-13 13:56` | **solow_growth_model** | 36 pág (3.25 MB) | 22 comp / 0 preg | 17.3 min (1038.0s) | **6.69x** | 42,298,536 | **0.0** | **0.0s** | ✅ Limpio | 🛠️ 0 | ⚠️ 2 |
| `2026-10-10 12:00` | **estadistica3_regresion_v3** | 50 pág (1.2 MB) | 16 comp / 480 preg | 60.0 min (3600.0s) | **2.0x** | 8,645,000 | **18,010.4** | **7.5s** | ✅ Limpio | 🛠️ 0 | ✅ 0 |

---

## 2. Métricas Promedio del Sistema (Baselines Globales)

- **Factor de Aceleración Paralela Promedio**: `4.35x`
- **Densidad de Tokens Promedio por Pregunta**: `18,010.4 tokens/pregunta`
- **Latencia Promedio por Pregunta Validada**: `7.5 s/pregunta`
- **Rendimiento Promedio de Generación**: `8.0 preguntas/minuto`

---
*Generado por el motor forense `c2c-run-auditor`.*