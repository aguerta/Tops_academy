import json
from pathlib import Path
import jsonschema

_skill_root = Path(r'd:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course')
schema_path = _skill_root / 'schemas' / 'template.schema.json'
schema = json.loads(schema_path.read_text(encoding='utf-8'))

# Sample Hab-03 generated in debug_schema.py
tpl_path = Path(r"d:\Augusto\personal_portfolio\Tops_academy\tests\test_shard_compiler_hardening.py")
# Let's inspect schema required fields
print("Required in schema:", schema.get("required"))
if "properties" in schema:
    for k in schema.get("required", []):
        print(f"Prop {k}:", schema["properties"].get(k))
