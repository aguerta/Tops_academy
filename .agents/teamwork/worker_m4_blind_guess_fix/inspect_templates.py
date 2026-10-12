import re

with open(".agents/skills/content-to-course/batch_generator.py", "r", encoding="utf-8") as f:
    text = f.read()

pattern = r"# -+\s+# ((?:H|C|HAB)-\d+):[^\n]*\s+# -+\s+elif? code == \"[^\"]+\"[^:]*:(.*?)(?=\n\s+# -+\s+# (?:H|C|HAB-)|\n\s+def _synthesize_fib_content)"
matches = re.findall(pattern, text, re.DOTALL)
print(f"Found {len(matches)} competencies")

for cid, body in matches:
    print(f"\n==================== {cid} ====================")
    lines = body.strip().split("\n")
    for line in lines:
        if any(line.strip().startswith(prefix) for prefix in ["stem =", "correct =", "distractors =", "sol =", "warn ="]):
            print(f"  {line.strip()[:100]}")
