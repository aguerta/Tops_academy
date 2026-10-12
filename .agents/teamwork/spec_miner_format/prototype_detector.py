"""
Prototype LaTeX backslash and JSON escape detector.
"""
import re
import json

def detect_raw_text_issues(raw_text: str):
    issues = []
    
    # 1. Check for single backslash before LaTeX commands that silently produce control chars
    # silent commands: \begin, \bar, \beta, \frac, \tau, \theta, \text, \times, \nu, \nabla, \right, etc.
    silent_latex_patterns = [
        (r'(?<!\\)\\begin', r'\begin (turns into backspace + egin)'),
        (r'(?<!\\)\\bar', r'\bar (turns into backspace + ar)'),
        (r'(?<!\\)\\beta', r'\beta (turns into backspace + eta)'),
        (r'(?<!\\)\\frac', r'\frac (turns into form feed + rac)'),
        (r'(?<!\\)\\tau', r'\tau (turns into tab + au)'),
        (r'(?<!\\)\\theta', r'\theta (turns into tab + heta)'),
        (r'(?<!\\)\\text', r'\text (turns into tab + ext)'),
        (r'(?<!\\)\\times', r'\times (turns into tab + imes)'),
        (r'(?<!\\)\\nu', r'\nu (turns into newline + u)'),
        (r'(?<!\\)\\nabla', r'\nabla (turns into newline + abla)'),
        (r'(?<!\\)\\right', r'\right (turns into carriage return + ight)'),
    ]
    
    for pat, desc in silent_latex_patterns:
        for m in re.finditer(pat, raw_text):
            pos = m.start()
            line = raw_text[:pos].count('\n') + 1
            col = pos - raw_text[:pos].rfind('\n')
            issues.append({
                "type": "silent_latex_corruption",
                "line": line,
                "col": col,
                "detail": f"Corrupted LaTeX escape: {desc} at line {line}, col {col}. Must be double-escaped as '\\\\...'"
            })

    # 2. Check for invalid JSON escapes
    # Valid escapes in JSON strings are: \", \\, \/, \b, \f, \n, \r, \t, \uXXXX
    # Any other single backslash is an invalid escape.
    # Note: we need to find backslashes inside JSON strings.
    # A simple robust pattern: (?<!\\)\\(?!["\\/bfnrtu])
    for m in re.finditer(r'(?<!\\)\\(?!["\\/bfnrtu])', raw_text):
        pos = m.start()
        line = raw_text[:pos].count('\n') + 1
        col = pos - raw_text[:pos].rfind('\n')
        # get snippet
        char_after = raw_text[pos+1:pos+10]
        issues.append({
            "type": "invalid_json_escape",
            "line": line,
            "col": col,
            "detail": f"Invalid JSON escape sequence '\\{char_after}' at line {line}, col {col}. Must be escaped as '\\\\'"
        })
        
    return issues

def detect_parsed_control_characters(data, path="root"):
    issues = []
    if isinstance(data, str):
        # check for \x08 (backspace), \x0c (formfeed), \x00 (null), \x0b (vtab)
        if '\x08' in data:
            issues.append(f"{path}: contains ASCII 0x08 (Backspace), indicative of corrupted '\\b...' (e.g. \\begin, \\beta, \\bar)")
        if '\x0c' in data:
            issues.append(f"{path}: contains ASCII 0x0C (Form Feed), indicative of corrupted '\\f...' (e.g. \\frac)")
        if '\x00' in data:
            issues.append(f"{path}: contains ASCII 0x00 (Null character)")
        if '\x0b' in data:
            issues.append(f"{path}: contains ASCII 0x0B (Vertical Tab)")
        # check for \t followed by LaTeX keywords
        if re.search(r'\t(au|heta|ext|imes|ilde|an)', data):
            issues.append(f"{path}: contains Tab character preceding LaTeX token, indicative of corrupted '\\t...' (e.g. \\tau, \\theta, \\text)")
        # check for \r followed by ight
        if '\right' in repr(data) or re.search(r'\r(ight)', data):
            issues.append(f"{path}: contains Carriage Return preceding LaTeX token, indicative of corrupted '\\right'")
    elif isinstance(data, dict):
        for k, v in data.items():
            issues.extend(detect_parsed_control_characters(v, f"{path}.{k}"))
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            issues.extend(detect_parsed_control_characters(item, f"{path}[{idx}]"))
    return issues

# Test on a snippet
test_raw = r'{"stem": "\frac{1}{2} + \tau + \beta + \alpha"}'
print("Testing test_raw:")
issues = detect_raw_text_issues(test_raw)
for iss in issues:
    print(" ", iss["detail"])

