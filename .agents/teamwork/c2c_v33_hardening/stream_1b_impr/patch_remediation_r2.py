import re
from pathlib import Path

# 1. Update check_templates.py line 2134
check_p = Path(r"d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\check_templates.py")
text = check_p.read_text(encoding="utf-8")

old_code = '    has_placeholder = bool(re.search(r"\\{[A-Za-z0-9_]+(?::[^{}]+)?\\}", stem))\n'
new_code = '''    has_placeholder = bool(
        re.search(r"\\{[A-Za-z0-9_]+(?::[^{}]+)?\\}", stem)
        or re.search(r"@[A-Za-z_][A-Za-z0-9_]*(?::[^@\\s{}]+)?@", stem)
    )\n'''

assert old_code in text, "Could not find old_code in check_templates.py"
text = text.replace(old_code, new_code, 1)

# Also update the error message to mention @var@
old_msg = "stem must contain at least one placeholder '{{var}}' or 'stem_variants' must be present."
new_msg = "stem must contain at least one placeholder '{{var}}' or '@var@' or 'stem_variants' must be present."
text = text.replace(old_msg, new_msg)

check_p.write_text(text, encoding="utf-8")
print("check_templates.py successfully patched for Defect 1!")
