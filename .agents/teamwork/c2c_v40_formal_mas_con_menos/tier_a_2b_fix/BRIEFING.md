# Pre-Flight Briefing: Tier A Hotfix (`tier_a_2b_fix`)

- **Author:** `c2c40_implementer`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\tier_a_2b_fix`
- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Timestamp:** 2026-11-08T04:55:00Z

---

## 1. Scope & Exclusive Write Boundary Verification
Only the following files are permitted for write/creation:
1. `.agents/skills/content-to-course/compile_shard.py`
2. `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
3. `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
4. `.agents/skills/content-to-course/subagent_types.json`
5. `.agents/teamwork/c2c_v40_formal_mas_con_menos/tier_a_2b_fix/BRIEFING.md` [Pre-flight]
6. `.agents/teamwork/c2c_v40_formal_mas_con_menos/tier_a_2b_fix/handoff.md` [Completion]

All other files (e.g. `run.py`, test files, work folders) are read-only to avoid collisions with concurrent Streams 2A and 2C.

---

## 2. Invariants & Target Line Ranges

### A. `compile_shard.py` (~L350-L415, ~L795-L965, ~L2550-L2565)
1. **`ShardDataLineLocator.parse_ast` (~L385-L415):**
   - Add `self.function_segments: Dict[str, str] = {}`.
   - Register top-level `ast.Assign` and `ast.AnnAssign` where `value` is `ast.Lambda` (single Name target) into `self.functions` and record its exact source segment via `ast.get_source_segment(self.source_text, node)`.
2. **`prune_ast_dependencies` (~L795-L815):**
   - Use `ast.get_source_segment(source_text, node)` in `_get_node_text(node)` to avoid line bleeding across semicolon-separated statements.
   - Register lambda assignments in `functions` so dependency graph tracks them as functions.
3. **`prune_ast_preamble` (~L900-L905):**
   - Match both `def {name}\s*\(` and `{name}\s*=` so lambda targets are excluded cleanly from their preambles.
4. **`extract_function_code` (~L920-L965):**
   - If `getattr(fn_or_str, "__name__", "") == "<lambda>"` and `fn_name_hint`: set `orig_name = fn_name_hint`.
   - Retrieve `raw_src` preferring `locator.function_segments[orig_name]` when available.
   - If `raw_src` is a lambda assignment or expression, use `ast` to transform into:
     ```python
     def {target_name}(<args>):
         return <expr>
     ```
     via `ast.unparse(ast.FunctionDef(...))`.
   - Ensure `generate = generate_params` and `cross_check = verify` aliases remain intact.
5. **Zero-Domain Invariant:**
   - English comments only, no forbidden substrings (`edo`, `pde`, `derivadas`, etc.).

---

### B. `system_prompts/lean/prompt_shard_author.md` (Total bytes <= 4,750, 0 bytes `\r`)
1. **Canonical Form-C Quad-Band Example (`Hab-01 Carnot Cycle`):**
   - Remove `import re` completely.
   - Pure-python number parsing in `_pv(c)`:
     `def _pv(c): return float(str(c).split("=")[-1].replace("$", "").strip())`
   - Explicit `def` for all generator and verifier functions:
     `def gen_h01_1(r): return _gen_h01(r, 1)`, etc.
   - Algebraic disjoint distractors for `arch == 1`:
     `tc = rng.randint(200, 280); th = tc + rng.randint(460, 650); eta = round(1.0 - tc/th, 3)`
     `v1 = (th/tc, tc/th, 1-(tc/th)**2, 1-0.6*tc/th, (th-tc)/(th+tc), (tc/th)**2)`
     Guarantees $d_6 < d_2 < d_5 < \eta < d_4 < d_3 < d_1$ with min gap >= 0.047 across all 15,471 combinations and 0 magic multipliers.
   - `RATS` updated with `@tc@`/`@th@`, >= 20 chars, length balanced.
   - `arch == 4` (`MS`): 4 options balanced to exact length 44 chars (`R-16`), clean KaTeX (`R-18`), `distractor_id` + `error_rationale` on falses.
   - `ver_h01_4(res)` non-tautological verifier validating mathematical truth of selected options.
   - Mandatory test strings: `## 0. SCOPE-LOCK`, `DONE:`, `compile_shard.py`, `Física`, `Sistemas Distribuidos`, `línea`, `stem_variants`, `ArtifactMetadata`, `MC7`, `FIB`, `MS`, `RATS`, `assumption_id`.
   - Size budget: strictly <= 4,750 bytes, LF endings.

---

### C. `system_prompts/prompt_shard_author.md` (LF puro `\n`)
- Mirror Section 2 Form-C canonical snippet to eliminate `import re`, use explicit `def`, algebra-guaranteed distractors, and non-tautological verifiers.

---

### D. `subagent_types.json`
- Regenerate byte-for-byte using `dispatch.get_type_definitions(lean=True)` with trailing `\n` and 0 bytes `\r`.

---

## 3. Verification Plan
1. Standalone compilation test on extracted code block from `lean/prompt_shard_author.md` with `compile_shard(tmp, "shard_01", strict=True, min_archetypes=4)` -> expect `(True, [])`.
2. Pytest suite:
   `& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_compile_shard.py tests/test_c2c_v321_comp4_prompts.py tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_skill.py -k "not dummy_nonexistent" -q`
3. Zero-domain validation via `test_engine_zero_domain_logic` and regex scan.
4. Handoff report and completion dispatch.
