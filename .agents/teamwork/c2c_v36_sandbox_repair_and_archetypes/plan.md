# Plan Operativo `/flash-triad-orchestrator` (`c2c_v36_sandbox_repair_and_archetypes`)

## Fronteras Exclusivas de Escritura por Etapa (`Exclusive Write Boundaries`)

### Etapa 1 — Gate 1 (4 Streams Paralelos — Intersección de Escritura = ∅)
- **Stream 1A (`stream_1a_{impl,impr,audit}`):**
  - `.agents/skills/content-to-course/cta_merge.py`
  - `tests/test_cta_merge_prereq_scoping.py`
- **Stream 1B (`stream_1b_{impl,impr,audit}`):**
  - `.agents/skills/content-to-course/engine/sandbox.py`
  - `.agents/skills/content-to-course/check_templates.py`
  - `tests/test_sandbox_gil_and_circuit_breaker.py`
- **Stream 1C (`stream_1c_{impl,impr,audit}`):**
  - `.agents/skills/content-to-course/run.py`
  - `.agents/skills/content-to-course/dispatch.py`
  - `tests/test_run_templates_and_dispatch_repair.py`
- **Stream 1D (`stream_1d_{impl,impr,audit}`):**
  - `.agents/skills/content-to-course/compile_shard.py`
  - `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
  - `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
  - `tests/test_m3_archetypes_semantic_gate.py`
