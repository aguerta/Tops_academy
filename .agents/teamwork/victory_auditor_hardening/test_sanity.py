import sys
sys.path.insert(0, ".agents/skills/content-to-course")
from prepare import compute_next_ids, sanitize_cli_arg

baseline_comps = (
    [{'id': f'C-{i:02d}'} for i in range(1, 11)] +
    [{'id': f'Hab-{i:02d}'} for i in range(1, 7)] +
    [{'id': f'H-{i:02d}'} for i in range(1, 6)]
)
next_ids = compute_next_ids(baseline_comps)
print("Next IDs from 21 baseline:", next_ids["next_ids_by_prefix"])
assert next_ids["next_ids_by_prefix"]["C-"] == "C-11"
assert next_ids["next_ids_by_prefix"]["Hab-"] == "Hab-07"
assert next_ids["next_ids_by_prefix"]["H-"] == "H-06"
print("Continuous ID generation verified!")

assert sanitize_cli_arg('"hello"') == "hello"
assert sanitize_cli_arg('"""nested"""') == "nested"
assert sanitize_cli_arg(r'"C:\courses\test\\"') == r"C:\courses\test"
print("CLI argument sanitization verified!")
