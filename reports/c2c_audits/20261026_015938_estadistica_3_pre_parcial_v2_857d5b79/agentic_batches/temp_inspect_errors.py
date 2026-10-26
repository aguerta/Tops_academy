import json

with open("reports/c2c_audits/20261026_015938_estadistica_3_pre_parcial_v2_857d5b79/agentic_batches/shards_batch_08.json", "r", encoding="utf-8") as f:
    batch = json.load(f)

for s in batch["subagents"]:
    sid = s.get("shard_id")
    print(f"\n==================== {sid} ({s.get('label')}) ====================")
    steps = s.get("steps", [])
    errors_found = 0
    for idx, st in enumerate(steps):
        # Look for tool call and result
        t_call = st.get("tool_call") or {}
        t_res = st.get("tool_step_result") or {}
        t_name = st.get("tool_name") or t_call.get("name")
        t_args = st.get("tool_args") or t_call.get("args") or {}
        
        # Check if error
        is_err = False
        err_msg = ""
        if isinstance(t_res, dict):
            if t_res.get("error"):
                is_err = True
                err_msg = str(t_res.get("error"))
            elif t_res.get("exit_code", 0) != 0:
                is_err = True
                err_msg = f"Exit code {t_res.get('exit_code')}: {t_res.get('output', '')[:200]}"
            elif "Error" in str(t_res.get("output", "")):
                # Could be a compile error or tool error
                is_err = True
                err_msg = str(t_res.get("output", ""))[:200]
        elif isinstance(t_res, str) and ("Error" in t_res or "fail" in t_res.lower()):
            is_err = True
            err_msg = t_res[:200]
            
        if is_err:
            errors_found += 1
            print(f"  Turn/Step {idx} [{t_name}]:")
            print(f"    Args: {t_args}")
            print(f"    Error/Output: {err_msg}")
            th = st.get("thought", "")
            if th:
                print(f"    Thought: {th[:250]}...")
    if errors_found == 0:
        print("  No tool errors detected in steps!")
