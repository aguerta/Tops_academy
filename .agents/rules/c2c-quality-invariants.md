# C2C Quality & Pedagogical Invariants (C2C v4.0 Formal Mas con Menos)

Universal invariants enforced across `compile_shard.py`, `compile_cta.py`, `c2c_hook_guard.py`, and `standardized_audit_engine.py`:

1. **Anti-Mechanization, AST Non-Cloning & Explicit Assumptions:**
   - **4 Disjoint Archetypes (`min_archetypes = 4`, `4/4` distinct AST formulas):** Every competency must define exactly 4 disjoint archetypes in compact `Form-C` (Direct/Forward, Inverse, Perturbation, Boundary/Edge-case).
   - In skills (`Hab-*`), symbolic AST normalization validates that the 4 generating functions yield 4 genuinely distinct algebraic target formulas.
   - The 4th archetype (`boundary_or_edge_case`) must explicitly test the breakdown of an explicit theorem assumption (`assumption_id`) declared in `cta.json`.

2. **Triple Verifier Contract & Strict Boolean Semantics:**
   - **Positive Soundness:** `ver_fn(result_with_correct) is True` across all 50 dry-run seeds.
   - **Strict Distractor Refutation:** For each of the 6 distractores $d_i$ in MC7 (or false options in MS), `ver_fn({**result, 'correct': d_i}) is False` (`[VERIFIER-TAUTOLOGY-DETECTED]` flags trivial `return True` or `try/except: return True`).
   - **Zero Debug Bombs:** Prohibit `raise RuntimeError`, `breakpoint()`, `pdb`, or residual `print()` statements in shard data files (`[TPL-DEBUG-ARTIFACT]`).
   - **Strict Boolean Typing:** Evaluators must enforce `is True` / `is False` without falling prey to `np.bool_(False) is False` truthiness traps.

3. **Diagnostic Isolation & Zero Ad-Hoc Perturbations (`_clean_ds`):**
   - Prohibit ad-hoc delta jitter loops (`_clean_ds`, `cand += 0.35`) in author code (`[TPL-AD-HOC-PERTURBATION]`). Use the engine's deterministic rejection sampling instead.
   - Prohibit all visible meta-information in option text: labels like `"Exact trajectory:"`, parenthetical diagnostics like `(confused with...)`, or prefixes like `"Alternate option X:"`. All pedagogical rationale belongs strictly in `error_rationale`.

4. **Socratic Scaffolding in 3-5 Levels, Epistemic Closure & Clean KaTeX:**
   - Progressive hints must range between 3 and 5 levels, each $\ge 25$ characters, with zero answer leaks in hints 1-2.
   - Prohibit naming competency codes (`C-01`, `Hab-02`) inside user-facing stems, hints, or solutions.
   - Prohibit vacuous quantifiers (e.g. `\forall \varepsilon = 0.05`), un-interpolated template variables (`{sigma2}`), and long prose exceeding 45 characters inside `\text{...}`.
   - Ensure epistemic closure: all non-standard variables and functions required to solve the question must be introduced in the stem.
