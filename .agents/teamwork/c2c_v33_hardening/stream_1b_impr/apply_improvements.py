import re
from pathlib import Path

check_p = Path(r"d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\check_templates.py")
content = check_p.read_text(encoding="utf-8")

# 1. Add normalize_error_string_for_hash if not present
if "def normalize_error_string_for_hash" not in content:
    norm_fn = """def normalize_error_string_for_hash(text: str) -> str:
    \"\"\"Normalize volatile elements in error messages (hex addresses, module uuids, temp paths, timestamps, CRLF) for deterministic hashing.\"\"\"
    if not isinstance(text, str):
        text = str(text)
    # Normalize CRLF and backslashes
    text = text.replace("\\r\\n", "\\n").replace("\\r", "\\n")
    text = text.replace("\\\\", "/")
    # Strip memory addresses
    text = re.sub(r"at 0x[0-9a-fA-F]+", "at 0xHEX", text)
    # Strip ephemeral module names generated with random UUIDs
    text = re.sub(r"c2c_(?:shard|fix)_mod_[a-zA-Z0-9_-]+_[0-9a-fA-F]{6,8}", "c2c_mod", text)
    # Strip timestamps (ISO, RFC, or common date formats)
    text = re.sub(r"\\b\\d{4}-\\d{2}-\\d{2}[T\\s]\\d{2}:\\d{2}:\\d{2}(?:\\.\\d+)?(?:Z|[+-]\\d{2}:\\d{2})?\\b", "<TIMESTAMP>", text)
    # Strip temp paths and staging paths
    text = re.sub(r"(?:[A-Za-z]:)?/[^\\s:]*?/(?:\\.?tmp|temp|\\.check_attempts/_staged)[^\\s:]*", "<TEMP_PATH>", text, flags=re.IGNORECASE)
    # Strip ephemeral tmp file names
    text = re.sub(r"\\.[a-zA-Z0-9_-]+\\.tmp\\.\\d+_[0-9a-fA-F]+", "<TMP_FILE>", text)
    return text.strip()


"""
    target = "def _extract_template_placeholders(text: str) -> Set[str]:"
    content = content.replace(target, norm_fn + target, 1)

# 2. Update _extract_template_placeholders body to also extract PrairieLearn @var@ and @var:spec@
target_start = "    placeholders: Set[str] = set()\n"
replacement_start = """    placeholders: Set[str] = set()
    if not isinstance(text, str) or not text:
        return placeholders

    # 1. PrairieLearn tokens: @var@ or @var:fmt@
    for m in re.finditer(r"@([a-zA-Z_][a-zA-Z0-9_]*)(?::([^@\\s{}]+))?@", text):
        placeholders.add(m.group(1))

    # 2. Python-style {var} tokens
"""
if "PrairieLearn tokens: @var@" not in content:
    content = content.replace(target_start, replacement_start, 1)

# 3. Update placeholder check in line 2106
old_pattern = r'has_placeholder = bool\(re\.search\(r"\\\{[A-Za-z0-9_]\+\(\?::\[\^\{\}\]\+\)\?\\\}", stem\)\)'
new_pattern_replacement = '''has_placeholder = bool(
        re.search(r"\\{[A-Za-z0-9_]+(?::[^{}]+)?\\}", stem)
        or re.search(r"@[A-Za-z_][A-Za-z0-9_]*(?::[^@\\s{}]+)?@", stem)
    )'''
content = re.sub(old_pattern, lambda m: new_pattern_replacement, content, count=1)

# 4. Update circuit breaker error normalization in check_templates.py
old_cb_norm = 'normalized_errs = sorted([re.sub(r"at 0x[0-9a-fA-F]+", "", e.strip()) for e in errors])'
new_cb_norm = 'normalized_errs = sorted([normalize_error_string_for_hash(e) for e in errors])'
content = content.replace(old_cb_norm, new_cb_norm)

check_p.write_text(content, encoding="utf-8")
print("check_templates.py successfully patched!")
