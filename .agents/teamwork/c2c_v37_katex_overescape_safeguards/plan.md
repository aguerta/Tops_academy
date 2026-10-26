# Plan Operativo `/flash-triad-orchestrator` (`c2c_v37_katex_overescape_safeguards`)

## Fronteras Exclusivas de Escritura por Etapa (`Exclusive Write Boundaries`)

### Etapa 1 — Gate 1 (4 Streams Paralelos — Intersección de Escritura = ∅)
- **Stream 1A (`stream_1a_{impl,impr,audit}`):**
  - `src/validator/lexical_scanner.py`
  - `src/validator/rules.py`
  - `tests/test_katex_overescape_validator_r23.py`
  - `tests/test_validator.py` (autorizado por resolución BLOCKER Tier A: línea 686)
- **Stream 1B (`stream_1b_{impl,impr,audit}`):**
  - `.agents/skills/content-to-course/engine/assemble.py`
  - `tests/test_assemble_sanitize_katex_r23.py`
- **Stream 1C (`stream_1c_{impl,impr,audit}`):**
  - `.agents/skills/content-to-course/engine/invariants.py`
  - `.agents/skills/content-to-course/compile_shard.py`
  - `tests/test_invariants_and_shard_overescape_r23.py`
- **Stream 1D (`stream_1d_{impl,impr,audit}`):**
  - `run_platform.py`
  - `FUTURE_MILESTONES.md`
  - `docs/future_milestones/FUTURE_MILESTONES.md`
  - `tests/test_platform_katex_admission_guard.py`
