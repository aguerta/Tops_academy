"""
Probe how raw file text vs json.loads interacts with backslashes and control characters.
"""
import json

# Case A: User wrote in raw file: "\tau" (single backslash t)
# In JSON RFC 8259, \t is parsed as ASCII 0x09 (Tab).
raw_json_tab = '{"stem": "\\tau"}' # in Python literal, "\\tau" is \ followed by t
parsed_tab = json.loads(raw_json_tab)
print("Case \\tau parsed string repr:", repr(parsed_tab["stem"]))
print("Contains ASCII 9 (tab)?", '\t' in parsed_tab["stem"])

# Case B: User wrote in raw file: "\frac" (single backslash f)
raw_json_ff = '{"stem": "\\frac"}' # in Python literal, \ followed by f
parsed_ff = json.loads(raw_json_ff)
print("Case \\frac parsed string repr:", repr(parsed_ff["stem"]))
print("Contains ASCII 12 (formfeed)?", '\f' in parsed_ff["stem"])

# Case C: User wrote in raw file: "\nu" (single backslash n)
raw_json_nl = '{"stem": "\\nu"}'
parsed_nl = json.loads(raw_json_nl)
print("Case \\nu parsed string repr:", repr(parsed_nl["stem"]))
print("Contains ASCII 10 (newline)?", '\n' in parsed_nl["stem"])

# Case D: User wrote in raw file: "\beta" (single backslash b)
raw_json_bs = '{"stem": "\\beta"}'
parsed_bs = json.loads(raw_json_bs)
print("Case \\beta parsed string repr:", repr(parsed_bs["stem"]))
print("Contains ASCII 8 (backspace)?", '\b' in parsed_bs["stem"])

# Case E: Properly escaped: "\\\\tau" in raw file (double backslash in raw file)
# In Python string literal for raw file containing "\\tau":
raw_json_escaped = '{"stem": "\\\\tau"}'
parsed_escaped = json.loads(raw_json_escaped)
print("Case \\\\tau parsed string repr:", repr(parsed_escaped["stem"]))
print("Is it literal \\tau?", parsed_escaped["stem"] == "\\tau")

