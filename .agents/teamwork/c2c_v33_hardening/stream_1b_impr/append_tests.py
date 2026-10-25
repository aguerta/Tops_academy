import re
from pathlib import Path

test_file = Path(r"d:\Augusto\personal_portfolio\Tops_academy\tests\test_shard_compiler_hardening.py")
content = test_file.read_text(encoding="utf-8")

additional_zero_disk_test = '''
    def test_zero_disk_mutation_across_all_five_failure_paths_with_crlf(self, tmp_path: Path):
        """Adversarial check: byte-for-byte SHA256 identity across 5 failure paths with CRLF on Windows."""
        import hashlib

        # 5 Failure cases
        cases = {
            "syntax_error": (
                "TEMPLATES = [\n"
                "    ('C-01', 'fill_in_the_blank', 'Broken syntax ((\n"
            ),
            "zero_division": (
                "def gen(rng):\n"
                "    return 10 / 0\n"
                "def ver(r): return True\n"
                "TEMPLATES = [\n"
                "    ('C-01', 'fill_in_the_blank', 'Stem {v}', gen, ver, 'Sol', 'KC', [], ('doc.pdf', 1, ''))\n"
                "]\n"
            ),
            "katex_failure": (
                "import random\n"
                "def gen(rng):\n"
                "    return {'vars': {'a': 1}, 'correct': '1', 'distractors': []}\n"
                "def ver(r): return True\n"
                "TEMPLATES = [\n"
                "    ('C-01', 'fill_in_the_blank', 'Formula $ \\\\frac{a} $ sin cerrar', gen, ver, 'Sol', 'KC', [], ('doc.pdf', 1, ''))\n"
                "]\n"
            ),
            "r16_parity_failure": (
                "import random\n"
                "def gen(rng):\n"
                "    v = rng.randint(10, 50)\n"
                "    return {'vars': {'v': v}, 'correct': 'X', 'distractors': ['Un distractor sumamente largo y detallado que supera por mucho la longitud de la correcta ' * 3 for _ in range(6)]}\n"
                "def ver(r): return True\n"
                "TEMPLATES = [\n"
                "    ('C-01', 'multiple_choice_7_options', 'Stem {v}', gen, ver, 'Sol', 'KC', ['D1','D2','D3','D4','D5','D6'], ('doc.pdf', 1, ''))\n"
                "]\n"
            ),
            "tpl_var_collapse": (
                "def gen(rng):\n"
                "    return {'vars': {'const': 1}, 'correct': '1', 'distractors': ['2','3','4','5','6','7']}\n"
                "def ver(r): return True\n"
                "TEMPLATES = [\n"
                "    ('C-01', 'multiple_choice_7_options', 'Static stem without variations', gen, ver, 'Sol', 'KC', ['D1','D2','D3','D4','D5','D6'], ('doc.pdf', 1, ''))\n"
                "]\n"
            ),
        }

        for case_name, code_lf in cases.items():
            sub_dir = tmp_path / f"zero_disk_{case_name}"
            work_dir, shards_dir = _setup_test_workspace(sub_dir, "shard_01", ["C-01"])
            shard_py = shards_dir / "shard_01_data.py"

            # Force Windows CRLF endings
            code_crlf = code_lf.replace("\\n", "\\r\\n")
            shard_py.write_bytes(code_crlf.encode("utf-8"))

            sha_before = hashlib.sha256(shard_py.read_bytes()).hexdigest()

            success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
            assert not success, f"Expected failure for {case_name}, but compile succeeded!"

            raw_bytes_after = shard_py.read_bytes()
            sha_after = hashlib.sha256(raw_bytes_after).hexdigest()

            # Byte-for-byte SHA256 equality guaranteed
            assert sha_before == sha_after, f"Zero-Disk-Mutation violated for {case_name}!"
            assert b"\\r\\n" in raw_bytes_after, f"CRLF endings corrupted for {case_name}!"
'''

additional_splicing_tests = '''
    def test_100_percent_fix_coverage_rescues_shard_with_broken_syntax_error(self, tmp_path: Path):
        """Adversarial check: 100% shard_fixes coverage rescues shard even if shard_XX_data.py has SyntaxError on L600."""
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_06", ["Hab-03", "Hab-04"])
        shard_py = shards_dir / "shard_06_data.py"

        # Simulate broken code with Python SyntaxError left by aborted author
        broken_code = "# Line 1\n" * 599 + "def broken_syntax_on_line_600(((\n"
        shard_py.write_text(broken_code, encoding="utf-8")

        # c2c_repair writes clean fix files for 100% of competencies in shard_fixes/
        fixes_dir = shards_dir / "shard_fixes"
        fixes_dir.mkdir(parents=True, exist_ok=True)

        fix_hab03 = (
            "import random\\n"
            "def gen_h03(rng):\\n"
            "    a = rng.randint(10, 50)\\n"
            "    return {'vars': {'a': a}, 'correct': str(a), 'distractors': []}\\n"
            "def ver_h03(r): return True\\n"
            "TEMPLATES = [\\n"
            "    ('Hab-03', 'fill_in_the_blank', 'Stem H03 {a}', gen_h03, ver_h03, 'Sol {a}', 'KC', [], ('doc.pdf', 1, ''))\\n"
            "]\\n"
        )
        (fixes_dir / "Hab-03.py").write_text(fix_hab03, encoding="utf-8")

        fix_hab04 = (
            "import random\\n"
            "def gen_h04(rng):\\n"
            "    b = rng.randint(100, 200)\\n"
            "    return {'vars': {'b': b}, 'correct': str(b), 'distractors': []}\\n"
            "def ver_h04(r): return True\\n"
            "TEMPLATES = [\\n"
            "    ('Hab-04', 'fill_in_the_blank', 'Stem H04 {b}', gen_h04, ver_h04, 'Sol {b}', 'KC', [], ('doc.pdf', 2, ''))\\n"
            "]\\n"
        )
        (fixes_dir / "Hab-04.py").write_text(fix_hab04, encoding="utf-8")

        success, errors = compile_shard(work_dir, shard_id="shard_06", strict=False)
        assert success, f"Expected successful rescue via shard_fixes, got errors: {errors}"

        # Both templates compiled cleanly
        assert (work_dir / "templates" / "Hab-03.json").is_file()
        assert (work_dir / "templates" / "Hab-04.json").is_file()

    def test_100_percent_fix_coverage_when_shard_file_is_completely_missing(self, tmp_path: Path):
        """Adversarial check: 100% shard_fixes coverage compiles cleanly even when shard_data.py does not exist."""
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_06", ["Hab-03", "Hab-04"])
        # Ensure shard_06_data.py does NOT exist
        shard_py = shards_dir / "shard_06_data.py"
        if shard_py.is_file():
            shard_py.unlink()

        fixes_dir = shards_dir / "shard_fixes"
        fixes_dir.mkdir(parents=True, exist_ok=True)

        fix_code = (
            "import random\\n"
            "def gen(rng):\\n"
            "    v = rng.randint(1, 100)\\n"
            "    return {'vars': {'v': v}, 'correct': str(v), 'distractors': []}\\n"
            "def ver(r): return True\\n"
            "TEMPLATES = [\\n"
            "    ('{cid}', 'fill_in_the_blank', 'Stem {cid} {{v}}', gen, ver, 'Sol', 'KC', [], ('doc.pdf', 1, ''))\\n"
            "]\\n"
        )
        (fixes_dir / "Hab-03.py").write_text(fix_code.format(cid="Hab-03"), encoding="utf-8")
        (fixes_dir / "Hab-04.py").write_text(fix_code.format(cid="Hab-04"), encoding="utf-8")

        success, errors = compile_shard(work_dir, shard_id="shard_06", strict=False)
        assert success, f"Expected clean compile from fixes only, got errors: {errors}"
        assert (work_dir / "templates" / "Hab-03.json").is_file()
        assert (work_dir / "templates" / "Hab-04.json").is_file()

    def test_fix_filename_normalization_variants(self, tmp_path: Path):
        """Adversarial check: both hab-03.py (lowercase) and Hab_04.py (underscore) map to Hab-03 and Hab-04."""
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_06", ["Hab-03", "Hab-04"])
        fixes_dir = shards_dir / "shard_fixes"
        fixes_dir.mkdir(parents=True, exist_ok=True)

        fix_template = (
            "import random\\n"
            "def gen(rng):\\n"
            "    x = rng.randint(1, 99)\\n"
            "    return {'vars': {'x': x}, 'correct': str(x), 'distractors': []}\\n"
            "def ver(r): return True\\n"
            "TEMPLATES = [\\n"
            "    ('{cid}', 'fill_in_the_blank', 'Stem {cid} {{x}}', gen, ver, 'Sol', 'KC', [], ('doc.pdf', 1, ''))\\n"
            "]\\n"
        )
        # hab-03.py (lowercase)
        (fixes_dir / "hab-03.py").write_text(fix_template.format(cid="Hab-03"), encoding="utf-8")
        # Hab_04.py (underscore)
        (fixes_dir / "Hab_04.py").write_text(fix_template.format(cid="Hab-04"), encoding="utf-8")

        success, errors = compile_shard(work_dir, shard_id="shard_06", strict=False)
        assert success, f"Expected clean normalization match, got: {errors}"
        assert (work_dir / "templates" / "Hab-03.json").is_file()
        assert (work_dir / "templates" / "Hab-04.json").is_file()

    def test_sys_modules_and_linecache_cache_safety_on_repeated_compiles(self, tmp_path: Path):
        """Adversarial check: repeated compile_shard() calls in the same process do not serve stale cached fix files."""
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_01", ["C-01"])
        fixes_dir = shards_dir / "shard_fixes"
        fixes_dir.mkdir(parents=True, exist_ok=True)
        fix_c01 = fixes_dir / "C-01.py"

        # Version 1 of fix file
        fix_v1 = (
            "import random\\n"
            "def gen_c01(rng):\\n"
            "    v = rng.randint(1, 10)\\n"
            "    return {'vars': {'v': v}, 'correct': 'VERSION_ONE', 'distractors': []}\\n"
            "def ver_c01(r): return True\\n"
            "TEMPLATES = [\\n"
            "    ('C-01', 'fill_in_the_blank', 'Stem V1 {v}', gen_c01, ver_c01, 'Sol V1 {v}', 'KC', [], ('doc.pdf', 1, ''))\\n"
            "]\\n"
        )
        fix_c01.write_text(fix_v1, encoding="utf-8")
        s1, e1 = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert s1
        t1 = json.loads((work_dir / "templates" / "C-01.json").read_text(encoding="utf-8"))
        assert "Stem V1" in t1["stem"]

        # Version 2 of fix file: modify code in place
        fix_v2 = (
            "import random\\n"
            "def gen_c01(rng):\\n"
            "    v = rng.randint(20, 30)\\n"
            "    return {'vars': {'v': v}, 'correct': 'VERSION_TWO', 'distractors': []}\\n"
            "def ver_c01(r): return True\\n"
            "TEMPLATES = [\\n"
            "    ('C-01', 'fill_in_the_blank', 'Stem V2 {v}', gen_c01, ver_c01, 'Sol V2 {v}', 'KC', [], ('doc.pdf', 1, ''))\\n"
            "]\\n"
        )
        fix_c01.write_text(fix_v2, encoding="utf-8")
        s2, e2 = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert s2
        t2 = json.loads((work_dir / "templates" / "C-01.json").read_text(encoding="utf-8"))
        assert "Stem V2" in t2["stem"], "Stale cached version served instead of fresh code!"
'''

additional_diagnostics_tests = '''
    def test_pure_prairielearn_at_var_template_accepted_without_braces(self, tmp_path: Path):
        """Adversarial check: pure @var@ PrairieLearn template with zero {...} braces passes check_templates without TPL-VAR false rejection."""
        from check_templates import check_single_template

        # Pure @var@ template with ZERO curly brace placeholders
        template = {
            "id": "T-C01",
            "competency_id": "C-01",
            "type": "fill_in_the_blank",
            "stem": r"Calcule el valor de $\\\\frac{@a@}{@b@}$ aplicando el teorema fundamental.",
            "stem_variants": [],  # Empty stem_variants to strictly exercise stem placeholder detection!
            "solution": r"El valor calculado es @res@.",
            "hints": [r"Recuerde dividir @a@ entre @b@."],
            "generate_py": (
                "import random\\n"
                "def generate(rng):\\n"
                "    a = rng.randint(10, 50)\\n"
                "    b = rng.randint(2, 9)\\n"
                "    res = round(a / b, 2)\\n"
                "    return {'vars': {'a': a, 'b': b, 'res': res}, 'correct': str(res), 'distractors': []}\\n"
            ),
            "cross_check_py": "def cross_check(res): return True\\n",
            "distractor_ids": [],
        }

        errors = check_single_template(template, num_dry_run_seeds=20)
        # Must NOT complain about missing {var} placeholder
        tpl_var_errs = [e for e in errors if "TPL-VAR" in e and "stem must contain at least one placeholder" in e]
        assert len(tpl_var_errs) == 0, f"False positive TPL-VAR rejection on pure @var@ template: {tpl_var_errs}"

    def test_single_letter_vars_alongside_latex_macros_not_flagged(self):
        """Adversarial check: single-letter vars alongside LaTeX macros produce 0 false positives, while real leaks are caught."""
        from check_templates import check_unrendered_placeholders_in_instance
        from engine.invariants import check_unrendered_placeholders

        vars_dict = {"n": 100, "d": 4, "a": 2, "b": 5}

        # Valid mathematical text with LaTeX macros and single-letter arguments
        valid_latex = r"Calcule $\\\\frac{a}{b}$ cuando $X_n \\\\xrightarrow{d} X$ con $x_{n}$ y ${k}^*$."
        errs = check_unrendered_placeholders(valid_latex, "stem", variables=vars_dict)
        assert len(errs) == 0, f"False positives on valid LaTeX: {errs}"

        # Real leaked placeholders: {delta}, @delta@, and bare {n} in prose
        leaked_text = r"El error es tol <= {delta} y @delta@ con resultado {n}."
        leaked_errs = check_unrendered_placeholders(leaked_text, "stem", variables=vars_dict)
        assert len(leaked_errs) == 3, f"Expected 3 errors for leaked tokens, got: {leaked_errs}"
        assert any("{delta}" in e for e in leaked_errs)
        assert any("@delta@" in e for e in leaked_errs)
        assert any("{n}" in e for e in leaked_errs)

    def test_circuit_breaker_hash_stability_across_volatile_elements(self):
        """Adversarial check: circuit breaker err_hash is invariant to random module UUIDs, timestamps, temp paths, and CRLF."""
        from check_templates import normalize_error_string_for_hash
        import hashlib

        err_run1 = (
            "[-] Error en c2c_shard_mod_shard_01_a1b2c3\\r\\n"
            "    File \"C:\\\\Users\\\\test\\\\AppData\\\\Local\\\\Temp\\\\tmp123\\\\shard_01_data.py\", line 15\\n"
            "    Timestamp: 2026-10-24T10:15:30.123456Z at 0x7f8b9c0d1e2f\\n"
            "    TypeError: unsupported operand type(s) for +: 'int' and 'str'\\n"
        )

        err_run2 = (
            "[-] Error en c2c_shard_mod_shard_01_f9e8d7\\n"
            "    File \"/home/user/.check_attempts/_staged/shard_01_data.py\", line 15\\n"
            "    Timestamp: 2026-10-24 12:45:00 at 0x1a2b3c4d5e6f\\n"
            "    TypeError: unsupported operand type(s) for +: 'int' and 'str'\\n"
        )

        norm1 = normalize_error_string_for_hash(err_run1)
        norm2 = normalize_error_string_for_hash(err_run2)

        hash1 = hashlib.sha256(norm1.encode("utf-8")).hexdigest()
        hash2 = hashlib.sha256(norm2.encode("utf-8")).hexdigest()

        assert hash1 == hash2, f"Error hashes diverged across volatile elements!\\nNorm1: {norm1}\\nNorm2: {norm2}"
'''

# Insert additional_zero_disk_test into TestZeroDiskMutation
content = content.replace(
    "        assert disk_content == original_code\n",
    "        assert disk_content == original_code\n" + additional_zero_disk_test,
    1
)

# Insert additional_splicing_tests into TestModularCompetencySplicing
content = content.replace(
    "        assert state2[\"distinct_compiles\"] == 2\n",
    "        assert state2[\"distinct_compiles\"] == 2\n" + additional_splicing_tests,
    1
)

# Append additional_diagnostics_tests into TestSurgicalDiagnostics
content = content.rstrip() + additional_diagnostics_tests + "\n"

test_file.write_text(content, encoding="utf-8")
print("tests/test_shard_compiler_hardening.py successfully expanded!")
