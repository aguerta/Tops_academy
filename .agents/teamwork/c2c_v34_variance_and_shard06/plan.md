# Plan Operativo `/flash-triad-orchestrator` (`c2c_v34_variance_and_shard06`)

## Fronteras Exclusivas de Escritura por Etapa (`Exclusive Write Boundaries`)

### Etapa 1 (4 Streams Paralelos — Intersección de Escritura = ∅)
- **Stream 1A (`stream_1a_{impl,impr,audit}`):**
  - `.agents/skills/content-to-course/engine/assemble.py`
  - `tests/test_assemble_katex_and_rationale.py`
- **Stream 1B (`stream_1b_{impl,impr,audit}`):**
  - `.agents/skills/content-to-course/compile_shard.py`
  - `.agents/skills/content-to-course/check_templates.py`
  - `tests/test_shard06_and_dry_archetypes.py`
- **Stream 1C (`stream_1c_{impl,impr,audit}`):**
  - `.agents/skills/content-to-course/dispatch.py`
  - `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
  - `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
  - `.agents/skills/content-to-course/system_prompts/lean/prompt_repair.md`
  - `.agents/skills/content-to-course/system_prompts/prompt_repair.md`
  - `tests/test_dispatch_turn0_and_milestone3_prompts.py`
- **Stream 1D (`stream_1d_{impl,impr,audit}`):**
  - `.agents/skills/content-to-course/c2c_hook_guard.py`
  - `tests/test_hook_post_pass_and_write_isolation.py`

### Etapa 2 (1 Stream Integrador Post-Gate 1)
- **Stream 2A (`stream_2a_{impl,impr,audit}`):**
  - `.agents/skills/content-to-course/subagent_types.json`
  - `courses/asyntotic_estatistics_v4/work/templates/Hab-06.json`
  - `courses/asyntotic_estatistics_v4/work/shards/shard_06.json`
  - `tests/test_forensic_shard06_and_variance_v34.py`
