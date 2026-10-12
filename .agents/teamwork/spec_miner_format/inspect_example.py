import json
import re
from collections import Counter

file_path = 'system_prompts/output_example_exercises.json'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

print(f"Total length: {len(text)} characters")

# 1. Backslash analysis
# Look at all occurrences of backslash
raw_escapes = []
i = 0
n = len(text)
while i < n:
    if text[i] == '\\':
        if i + 1 < n:
            esc = text[i:i+2]
            raw_escapes.append((i, esc, text[max(0, i-15):min(n, i+25)]))
            i += 2
            continue
    i += 1

counts = Counter([esc[1] for esc in raw_escapes])
print("\n--- Backslash sequence counts ---")
for esc, cnt in counts.most_common():
    print(f"{repr(esc)}: {cnt}")

print("\n--- Examples of potentially silent/corrupting escapes ---")
silent_escapes = ['\\t', '\\n', '\\f', '\\b', '\\r', '\\u']
for esc, cnt in counts.most_common():
    if esc in silent_escapes:
        print(f"\nOccurrences of {repr(esc)} ({cnt} total):")
        matches = [e for e in raw_escapes if e[1] == esc]
        for m in matches[:10]:
            print(f"  Pos {m[0]}: {repr(m[2])}")

print("\n--- Examples of invalid JSON escapes (causing syntax error) ---")
valid_json_second = ['"', '\\', '/', 'b', 'f', 'n', 'r', 't', 'u']
invalid_escapes = [e for e in raw_escapes if e[1][1] not in valid_json_second]
print(f"Total invalid JSON escapes: {len(invalid_escapes)}")
invalid_counts = Counter([e[1] for e in invalid_escapes])
for esc, cnt in invalid_counts.most_common():
    print(f"{repr(esc)}: {cnt}")

# 2. Check unescaped quotes inside strings
print("\n--- Checking unescaped quotes ---")
lines = text.splitlines()
for line_no, line in enumerate(lines, 1):
    # check for pattern like ["A", "B"] inside a string without escaping or double quotes
    if '""' in line or '["' in line and line.strip().startswith('"'):
        # let's see lines with suspicious quotes
        pass
    if '["A"' in line:
        print(f"Line {line_no}: {line}")

# 3. Check raw newlines inside JSON strings
print("\n--- Checking multiline raw strings / newlines ---")
# If a line doesn't end with a closing quote/comma/bracket and the string continues
in_string = False
quote_count = 0
for line_no, line in enumerate(lines, 1):
    # rough count of unescaped quotes
    stripped = line.strip()
    if stripped.startswith('$$') or stripped.startswith('\\dot{') or stripped.startswith('\dot{') or stripped.startswith('$'):
        print(f"Line {line_no} seems to be raw math outside proper JSON string boundary: {line}")

