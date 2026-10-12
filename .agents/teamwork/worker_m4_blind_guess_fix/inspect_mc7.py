with open(".agents/skills/content-to-course/batch_generator.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

in_mc7 = False
for idx, line in enumerate(lines[464:1115], 465):
    l = line.strip()
    if l.startswith("# H-") or l.startswith("# C-") or l.startswith("# HAB-"):
        print(f"\n{idx}: {l}")
    elif l.startswith("correct ="):
        print(f"  {idx}: {l[:100]}")
    elif l.startswith("distractors ="):
        print(f"  {idx}: {l[:100]}")
