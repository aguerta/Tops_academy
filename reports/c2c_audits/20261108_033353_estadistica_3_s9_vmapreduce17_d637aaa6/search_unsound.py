from pathlib import Path

target_file = Path(".agents") / "skills" / "content-to-course" / "compile_shard.py"
text = target_file.read_text(encoding="utf-8")

lines = text.splitlines()
for idx, line in enumerate(lines):
    if "def run_ver" in line or "run_ver =" in line:
        print(f"Line {idx+1}: {line}")
        for j in range(max(0, idx - 5), min(len(lines), idx + 35)):
            print(f"  {j+1:4d}: {lines[j]}")


