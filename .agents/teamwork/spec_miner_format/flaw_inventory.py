"""
Generate exact inventory of flaws in output_example_exercises.json
"""
import re

with open('system_prompts/output_example_exercises.json', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    raw_text = "".join(lines)

flaws = {
    "syntax_invalid_escapes": [],
    "silent_control_char_escapes": [],
    "unescaped_raw_newlines": [],
    "unescaped_quotes": [],
    "structural_schema_defects": [],
    "giveaway_defects": []
}

# 1. Check raw line by line for invalid escapes and silent escapes
for line_idx, line in enumerate(lines, 1):
    # Unescaped quotes like "["A", "B", "E"]"
    if '""' in line or '["A"' in line:
        flaws["unescaped_quotes"].append({
            "line": line_idx,
            "snippet": line.strip()
        })
    
    # Check invalid escapes in line
    for m in re.finditer(r'(?<!\\)\\(?!["\\/bfnrtu])([a-zA-Z]+)', line):
        cmd = m.group(1)
        flaws["syntax_invalid_escapes"].append({
            "line": line_idx,
            "cmd": cmd,
            "snippet": line.strip()[:80]
        })
        
    # Check silent escapes
    for m in re.finditer(r'(?<!\\)\\(begin|end|frac|tau|theta|text|times|nu|beta|nabla|right|bar)', line):
        cmd = m.group(1)
        flaws["silent_control_char_escapes"].append({
            "line": line_idx,
            "cmd": cmd,
            "snippet": line.strip()[:80]
        })

print(f"Total invalid JSON escapes: {len(flaws['syntax_invalid_escapes'])}")
print(f"Total silent control char escapes: {len(flaws['silent_control_char_escapes'])}")
print(f"Total unescaped quote occurrences: {len(flaws['unescaped_quotes'])}")

# Check raw newlines inside strings
# A raw newline occurs when a string opened with " has not closed before \n
in_string = False
multiline_strings = []
current_start = None
for line_idx, line in enumerate(lines, 1):
    # Count quotes not preceded by backslash
    quotes = [m.start() for m in re.finditer(r'(?<!\\)"', line)]
    if len(quotes) % 2 != 0:
        if not in_string:
            in_string = True
            current_start = line_idx
        else:
            in_string = False
            multiline_strings.append((current_start, line_idx))

print(f"Total multiline unescaped string blocks: {len(multiline_strings)}")
for start, end in multiline_strings:
    print(f"  String spans lines {start} to {end}")

