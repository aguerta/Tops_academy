import re

with open('system_prompts/output_example_exercises.json', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect each question block
# We can find questions by "id": "Q-...
q_blocks = re.split(r'(?=\{\s*"id":\s*"Q-)', text)
print(f"Total blocks found: {len(q_blocks)-1}")

for b_idx, block in enumerate(q_blocks[1:], 1):
    q_id = re.search(r'"id":\s*"([^"]+)"', block).group(1)
    itype = re.search(r'"interaction_type":\s*"([^"]+)"', block).group(1)
    print(f"\n================ Question {b_idx}: {q_id} ({itype}) ================")
    
    if itype == "multiple_choice_7_options":
        # Extract options
        opts = re.findall(r'\{\s*"option_id":\s*"([A-G])",\s*"content":\s*"(.*?)(?<!\\)",\s*"is_correct":\s*(true|false)', block, re.DOTALL)
        if not opts:
            # try looser regex
            opts = re.findall(r'"option_id":\s*"([A-G])",\s*"content":\s*"(.*?)",\s*"is_correct":\s*(true|false)', block, re.DOTALL)
        print(f"Options found: {len(opts)}")
        opt_data = []
        for opt_id, content, is_corr in opts:
            # clean escapes
            clean_content = content.replace('\\n', ' ').strip()
            length = len(clean_content)
            is_correct_bool = (is_corr == 'true')
            opt_data.append((opt_id, length, is_correct_bool, clean_content))
            print(f"  {opt_id} (correct={is_corr}, len={length}): {clean_content[:60]}...")
        
        if opt_data:
            correct_opts = [o for o in opt_data if o[2]]
            distractors = [o for o in opt_data if not o[2]]
            if correct_opts and distractors:
                c_len = correct_opts[0][1]
                min_d = min(o[1] for o in distractors)
                max_d = max(o[1] for o in distractors)
                
                # Check R2 rule:
                # per item: correct option > 20% longer than longest distractor
                # or > 20% shorter than shortest distractor
                # Let's check exact formula from R2:
                # "a correct option more than 20% longer than the longest distractor,
                # or more than 20% shorter than the shortest distractor"
                longer_ratio = (c_len - max_d) / max_d if c_len > max_d else 0
                shorter_ratio = (min_d - c_len) / min_d if c_len < min_d else 0
                print(f"  Correct len: {c_len}, Distractor min: {min_d}, max: {max_d}")
                print(f"  Exceeds max distractor by: {longer_ratio*100:.1f}%")
                print(f"  Shorter than min distractor by: {shorter_ratio*100:.1f}%")
                is_longest = (c_len >= max_d)
                is_shortest = (c_len <= min_d)
                print(f"  Is longest? {is_longest}, Is shortest? {is_shortest}")

