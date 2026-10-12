# Esquema del Contrato de Telemetría: `telemetry.json`

Este documento describe la estructura y semántica del archivo `telemetry.json` generado en cada auditoría de ejecución por el motor `c2c-run-auditor`.

---

## Estructura Jerárquica del JSON

```json
{
  "meta": {
    "audit_timestamp": "2026-10-12T21:43:47.123456+00:00",
    "orchestrator_conversation_id": "1e88b133-6b0d-40d1-b42e-4417b999d118",
    "course_id": "solow_model",
    "course_title": "Modelo de Crecimiento de Solow"
  },
  "summary": {
    "wall_clock_seconds": 8383.0,
    "wall_clock_minutes": 139.72,
    "agent_compute_seconds": 11250.0,
    "parallel_speedup_factor": 1.34,
    "total_tokens": 48452643,
    "total_input_tokens": 2626047,
    "total_output_tokens": 309440,
    "total_cache_read_tokens": 40116240,
    "total_turns": 405,
    "total_subagents_spawned": 6,
    "tool_calls_total": 312,
    "tool_errors_total": 19
  },
  "workload": {
    "source_files": [
      {
        "name": "05_15_07_El_modelo_de_crecimiento_de_Solow.pdf",
        "size_bytes": 1284900,
        "pages": 36,
        "ext": ".pdf"
      }
    ],
    "total_input_bytes": 1284900,
    "total_input_mb": 1.23,
    "total_pages_or_slides": 36,
    "pages_needing_vision": 36,
    "total_handouts": 10,
    "corpus_chars": 85787,
    "corpus_words": 14082,
    "competencies_count": 44,
    "shards_count": 22,
    "questions_count": 1040,
    "cta_mode": "mapreduce",
    "course_id": "solow_model",
    "course_title": "Modelo de Crecimiento de Solow"
  },
  "unit_economics": {
    "tokens_per_page": 1345906.8,
    "tokens_per_input_kb": 38621.5,
    "tokens_per_competency": 1101196.4,
    "tokens_per_question": 46589.1,
    "seconds_per_page": 232.86,
    "seconds_per_question": 8.06,
    "questions_per_minute": 7.44,
    "agent_seconds_per_question": 10.82,
    "output_tokens_per_question": 297.5
  },
  "stages": [
    {
      "stage": "Stage 1A: Vision Handouts",
      "subagents_count": 1,
      "wall_clock_seconds": 587.0,
      "agent_compute_seconds": 587.0,
      "concurrency_speedup": 1.0,
      "input_tokens": 121138,
      "output_tokens": 32558,
      "total_tokens": 153696,
      "subagent_labels": ["Handout Vision Analyzer Shard 1"]
    }
  ],
  "bottlenecks": [
    {
      "severity": "HIGH",
      "type": "TOOL_FRICTION",
      "stage": "CTA Section Mapper 01",
      "title": "Excessive tool errors in CTA Section Mapper 01 (5 errors)",
      "description": "El subagente acumuló 5 errores durante la ejecución de comandos.",
      "subagent_id": "6c6c7e47-e015-4edf-81eb-fac68eeede5c"
    }
  ],
  "orchestrator": {
    "conversation_id": "1e88b133-6b0d-40d1-b42e-4417b999d118",
    "label": "Director (Orchestrator)",
    "duration_seconds": 8383.0,
    "turns_count": 299,
    "input_tokens": 2018577,
    "output_tokens": 160047,
    "cache_read_tokens": 35808715,
    "total_tokens": 37987339,
    "tool_calls_count": 280,
    "tool_calls_by_name": {
      "run_command": 142,
      "view_file": 86,
      "invoke_subagent": 4
    }
  },
  "subagents": [
    {
      "conversation_id": "6afac527-ff0e-4799-a7c6-0b9550d1e5be",
      "label": "Shard Author shard_01",
      "type_name": "self",
      "model": "inherit",
      "duration_seconds": 650.0,
      "turns_count": 62,
      "input_tokens": 266739,
      "output_tokens": 53726,
      "cache_read_tokens": 3087381,
      "total_tokens": 3407846,
      "tool_calls_count": 61,
      "tool_calls_by_name": {
        "write_to_file": 32,
        "replace_file_content": 14,
        "run_command": 10,
        "view_file": 5
      },
      "tool_errors_count": 5
    }
  ]
}
```
