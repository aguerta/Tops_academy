import re
from pathlib import Path

shard_p = Path(r"d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\compile_shard.py")
content = shard_p.read_text(encoding="utf-8")

# 1. Add discover_fix_files function before compile_shard
if "def discover_fix_files" not in content:
    discover_fn = '''def discover_fix_files(fixes_dir: Optional[Path], expected_cids: List[str]) -> Tuple[Dict[str, Path], List[Path]]:
    """Discovers and maps shard fix files to competency IDs with case-insensitive and delimiter-agnostic normalization.
    
    Matches Hab-03, Hab_03, hab-03, hab_03, T-Hab-03, and hab03 to Hab-03.
    Returns (fix_files_by_cid, all_relevant_fix_files).
    """
    fix_files_by_cid: Dict[str, Path] = {}
    relevant_files: List[Path] = []
    if not fixes_dir or not fixes_dir.is_dir():
        return fix_files_by_cid, relevant_files

    all_fix_files = sorted(fixes_dir.glob("*.py"))
    for fix_p in all_fix_files:
        stem = fix_p.stem
        norm_stem = re.sub(r"[^a-zA-Z0-9]", "", stem).lower()
        matched = False
        for ecid in expected_cids:
            norm_ecid = re.sub(r"[^a-zA-Z0-9]", "", ecid).lower()
            if (
                stem == ecid
                or stem == ecid.replace("-", "_")
                or stem.lower() == ecid.lower()
                or stem.replace("_", "-").lower() == ecid.lower()
                or norm_stem == norm_ecid
                or norm_stem == f"t{norm_ecid}"
            ):
                fix_files_by_cid[ecid] = fix_p
                if fix_p not in relevant_files:
                    relevant_files.append(fix_p)
                matched = True
                break
        if not matched:
            norm_stem_cid = stem.replace("_", "-")
            fix_files_by_cid[norm_stem_cid] = fix_p
            if fix_p not in relevant_files:
                relevant_files.append(fix_p)

    return fix_files_by_cid, relevant_files


'''
    content = content.replace("def compile_shard(\n", discover_fn + "def compile_shard(\n", 1)

# 2. In compile_shard, clear linecache and sys.modules at the beginning of compile_shard
cache_clear = '''    # Guarantee sys.modules and linecache safety across multiple compiles in same process
    import linecache
    linecache.clearcache()
    for k in list(sys.modules.keys()):
        if k.startswith("c2c_fix_mod_") or k.startswith("c2c_shard_mod_"):
            sys.modules.pop(k, None)
'''
if "linecache.clearcache()" not in content:
    target_start = '    target_p = Path(work_dir_or_path).resolve()\n'
    content = content.replace(target_start, target_start + cache_clear, 1)

# 3. Replace fix files discovery and shard data path check
old_fix_and_path = '''    # Locate shard data path if not provided
    if not shard_data_path or not shard_data_path.is_file():
        shard_data_path_str = shard_entry.get("shard_data_path")
        if shard_data_path_str and Path(shard_data_path_str).is_file():
            shard_data_path = Path(shard_data_path_str).resolve()
        else:
            candidate = shards_dir / f"{norm_shard_id}_data.py"
            if candidate.is_file():
                shard_data_path = candidate
            else:
                has_all_fixes = bool(
                    expected_cids and fixes_dir.is_dir() and all(
                        any((fixes_dir / f"{cand}.py").is_file() for cand in (cid, cid.replace("-", "_"), cid.replace("_", "-")))
                        for cid in expected_cids
                    )
                )
                if not has_all_fixes:
                    err_msg = f"ERROR: No existe el archivo de datos del shard: {candidate}"
                    print(err_msg, file=sys.stderr)
                    return False, [err_msg]
                shard_data_path = candidate

    # Discover relevant fix files for hashing and modular splicing
    relevant_fix_files = []
    if fixes_dir and fixes_dir.is_dir():
        for f in sorted(fixes_dir.glob("*.py")):
            stem = f.stem
            for ecid in expected_cids:
                if stem == ecid or stem == ecid.replace("-", "_") or stem.lower() == ecid.lower() or stem.replace("_", "-").lower() == ecid.lower():
                    if f not in relevant_fix_files:
                        relevant_fix_files.append(f)'''

new_fix_and_path = '''    # Discover relevant fix files for hashing and modular splicing
    fix_files_by_cid, relevant_fix_files = discover_fix_files(fixes_dir, expected_cids)
    has_all_fixes = bool(expected_cids and all(ecid in fix_files_by_cid for ecid in expected_cids))

    # Locate shard data path if not provided
    if not shard_data_path or not shard_data_path.is_file():
        shard_data_path_str = shard_entry.get("shard_data_path")
        if shard_data_path_str and Path(shard_data_path_str).is_file():
            shard_data_path = Path(shard_data_path_str).resolve()
        else:
            candidate = shards_dir / f"{norm_shard_id}_data.py"
            if candidate.is_file():
                shard_data_path = candidate
            else:
                if not has_all_fixes:
                    err_msg = f"ERROR: No existe el archivo de datos del shard: {candidate}"
                    print(err_msg, file=sys.stderr)
                    return False, [err_msg]
                shard_data_path = candidate'''

assert old_fix_and_path in content, "Could not find old_fix_and_path"
content = content.replace(old_fix_and_path, new_fix_and_path, 1)

# 4. Update _fail and post-check_templates error hashing with normalize_error_string_for_hash
old_fail_hash = '''        normalized_errs = sorted([re.sub(r"at 0x[0-9a-fA-F]+", "", msg.strip())])'''
new_fail_hash = '''        from check_templates import normalize_error_string_for_hash
        normalized_errs = sorted([normalize_error_string_for_hash(msg)])'''
assert old_fail_hash in content, "Could not find old_fail_hash"
content = content.replace(old_fail_hash, new_fail_hash, 1)

old_post_hash = '''        normalized_errs = sorted([re.sub(r"at 0x[0-9a-fA-F]+", "", str(e).strip()) for e in raw_errors])'''
new_post_hash = '''        from check_templates import normalize_error_string_for_hash
        normalized_errs = sorted([normalize_error_string_for_hash(str(e)) for e in raw_errors])'''
assert old_post_hash in content, "Could not find old_post_hash"
content = content.replace(old_post_hash, new_post_hash, 1)

# 5. Handle shard_XX_data.py SyntaxError / exec exception when has_all_fixes is True
old_syntax_and_load = '''    # 2. AST Line Locator & Syntax Verification (evaluated on in-memory healed source)
    locator = ShardDataLineLocator(shard_data_path, source_text=healed_source)
    if raw_source and locator.syntax_error:
        print(f"FAIL: Error sintáctico en {shard_data_path.name}:", file=sys.stderr)
        return _fail(locator.syntax_error)

    # 3. Load shard module dynamically from in-memory string
    mod_name = f"c2c_shard_mod_{norm_shard_id}_{uuid.uuid4().hex[:6]}"
    mod = types.ModuleType(mod_name)
    mod.__file__ = str(shard_data_path)
    if healed_source:
        try:
            code_obj = compile(healed_source, str(shard_data_path), "exec")
            exec(code_obj, mod.__dict__)
        except Exception as e:
            tb = traceback.format_exc()
            err_msg = f"FAIL: Excepción al ejecutar {shard_data_path.name}:\\n{tb}"
            return _fail(err_msg)

    base_templates = getattr(mod, "TEMPLATES", None) or []'''

new_syntax_and_load = '''    # 2. AST Line Locator & Syntax Verification (evaluated on in-memory healed source)
    locator = ShardDataLineLocator(shard_data_path, source_text=healed_source)
    skip_base_module = False
    if raw_source and locator.syntax_error:
        if has_all_fixes:
            print(
                f"[!] Warning: {shard_data_path.name} contiene error sintáctico, pero el 100% de las competencias "
                f"({expected_cids}) están cubiertas por fijaciones en shard_fixes/. Omitiendo {shard_data_path.name}.",
                file=sys.stderr,
            )
            skip_base_module = True
        else:
            print(f"FAIL: Error sintáctico en {shard_data_path.name}:", file=sys.stderr)
            return _fail(locator.syntax_error)

    # 3. Load shard module dynamically from in-memory string
    mod_name = f"c2c_shard_mod_{norm_shard_id}_{uuid.uuid4().hex[:6]}"
    mod = types.ModuleType(mod_name)
    mod.__file__ = str(shard_data_path)
    if healed_source and not skip_base_module:
        try:
            code_obj = compile(healed_source, str(shard_data_path), "exec")
            sys.modules[mod_name] = mod
            exec(code_obj, mod.__dict__)
        except Exception as e:
            if has_all_fixes:
                print(
                    f"[!] Warning: Excepción al ejecutar {shard_data_path.name}, pero el 100% de las competencias "
                    f"están cubiertas por shard_fixes/. Omitiendo {shard_data_path.name}.",
                    file=sys.stderr,
                )
                skip_base_module = True
            else:
                tb = traceback.format_exc()
                err_msg = f"FAIL: Excepción al ejecutar {shard_data_path.name}:\\n{tb}"
                return _fail(err_msg)

    base_templates = [] if skip_base_module else (getattr(mod, "TEMPLATES", None) or [])'''

assert old_syntax_and_load in content, "Could not find old_syntax_and_load"
content = content.replace(old_syntax_and_load, new_syntax_and_load, 1)

# 6. Simplify the fix_files_by_cid lookup in step 3 since it's already discovered
old_fix_lookup = '''    # Discover and splice fix files from shards/shard_fixes/<CID>.py
    known_types = {"multiple_choice", "multiple_choice_7_options", "fill_in_the_blank", "multiple_select", "open_ended"}
    fix_files_by_cid: Dict[str, Path] = {}
    if fixes_dir and fixes_dir.is_dir():
        for fix_p in fixes_dir.glob("*.py"):
            stem = fix_p.stem
            for ecid in expected_cids:
                if stem == ecid or stem == ecid.replace("-", "_") or stem.lower() == ecid.lower() or stem.replace("_", "-").lower() == ecid.lower():
                    fix_files_by_cid[ecid] = fix_p
            norm_stem_cid = stem.replace("_", "-")
            if norm_stem_cid not in fix_files_by_cid:
                fix_files_by_cid[norm_stem_cid] = fix_p'''

new_fix_lookup = '''    # Splice fix files from shards/shard_fixes/<CID>.py
    known_types = {"multiple_choice", "multiple_choice_7_options", "fill_in_the_blank", "multiple_select", "open_ended"}'''

assert old_fix_lookup in content, "Could not find old_fix_lookup"
content = content.replace(old_fix_lookup, new_fix_lookup, 1)

# 7. Register fix_mod into sys.modules
old_exec_fix = '''            fix_code_obj = compile(healed_fix_text, str(fix_path), "exec")
            exec(fix_code_obj, fix_mod.__dict__)'''
new_exec_fix = '''            fix_code_obj = compile(healed_fix_text, str(fix_path), "exec")
            sys.modules[fix_mod_name] = fix_mod
            exec(fix_code_obj, fix_mod.__dict__)'''
assert old_exec_fix in content, "Could not find old_exec_fix"
content = content.replace(old_exec_fix, new_exec_fix, 1)

shard_p.write_text(content, encoding="utf-8")
print("compile_shard.py successfully patched!")
