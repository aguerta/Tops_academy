import json
import os
from datetime import datetime

CONVERSATIONS = [
    {
        "role": "Shard Author shard_28",
        "id": "148b3b07-e351-44ae-b244-3cb08982dca0",
        "title": "1. Shard Author shard_28 (c2c_shard_author)"
    },
    {
        "role": "Repair Engineer H-05 (Intento 1)",
        "id": "a55d920d-0537-444c-9283-187b51b14199",
        "title": "2. Repair Engineer H-05 - Primer Intento (c2c_repair)"
    },
    {
        "role": "Repair Engineer H-05 (Intento 2)",
        "id": "93a1618d-aa57-41ba-8e09-64d8b76616ed",
        "title": "3. Repair Engineer H-05 - Segundo Intento (c2c_repair)"
    }
]

BRAIN_DIR = r"C:\Users\augus\.gemini\antigravity\brain"
OUTPUT_MD = r"D:\Augusto\personal_portfolio\Tops_academy\transcripts_shard_28_and_repair_h05.md"

def format_step(step):
    idx = step.get("step_index", "?")
    source = step.get("source", "")
    stype = step.get("type", "")
    created_at = step.get("created_at", "")
    content = step.get("content", "")
    thinking = step.get("thinking", "")
    tool_calls = step.get("tool_calls", [])

    lines = []
    lines.append(f"### Paso {idx} `[{source} | {stype}]` - *{created_at}*\n")

    if thinking:
        lines.append("<details><summary><b>💭 Pensamiento Interno (Thinking)</b></summary>\n")
        lines.append(f"```text\n{thinking.strip()}\n```\n</details>\n")

    if content:
        lines.append(f"**Contenido / Mensaje:**\n\n{content.strip()}\n")

    if tool_calls:
        lines.append(f"**Llamadas a Herramientas ({len(tool_calls)}):**\n")
        for tc in tool_calls:
            tname = tc.get("name", "tool")
            targs = tc.get("args", {})
            lines.append(f"- **Herramienta:** `{tname}`\n")
            if isinstance(targs, str):
                try:
                    targs = json.loads(targs)
                except Exception:
                    pass
            args_str = json.dumps(targs, indent=2, ensure_ascii=False) if isinstance(targs, (dict, list)) else str(targs)
            lines.append(f"```json\n{args_str}\n```\n")

    lines.append("---\n")
    return "\n".join(lines)

def main():
    md_out = []
    md_out.append("# Transcripciones de Shard Author shard_28 y Repair Engineer H-05\n")
    md_out.append(f"> Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    md_out.append("> Recopilación forense completa de interacciones, razonamientos (`thinking`), tool calls y outputs de los subagentes involucrados en `shard_28` y competencia `H-05`.\n\n")

    md_out.append("## Tabla de Contenidos\n")
    for item in CONVERSATIONS:
        anchor = item["title"].lower().replace(" ", "-").replace(".", "").replace("(", "").replace(")", "")
        md_out.append(f"- [{item['title']}](#{anchor}) (`ID: {item['id']}`)\n")
    md_out.append("\n---\n\n")

    for item in CONVERSATIONS:
        cid = item["id"]
        cpath_full = os.path.join(BRAIN_DIR, cid, ".system_generated", "logs", "transcript_full.jsonl")
        cpath_compact = os.path.join(BRAIN_DIR, cid, ".system_generated", "logs", "transcript.jsonl")
        
        path_to_read = cpath_full if os.path.exists(cpath_full) else cpath_compact

        md_out.append(f"## {item['title']}\n")
        md_out.append(f"- **Conversation ID:** `{cid}`\n")
        md_out.append(f"- **Archivo Origen:** `{path_to_read}`\n\n")

        if not os.path.exists(path_to_read):
            md_out.append(f"*Archivo de transcript no encontrado en `{path_to_read}`.*\n\n")
            continue

        step_count = 0
        with open(path_to_read, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    step_data = json.loads(line)
                    md_out.append(format_step(step_data))
                    step_count += 1
                except Exception as e:
                    md_out.append(f"> Error parseando línea: {e}\n\n")

        md_out.append(f"*Fin del transcript de {item['role']} ({step_count} pasos procesados).*\n\n---\n\n")

    with open(OUTPUT_MD, "w", encoding="utf-8") as f_out:
        f_out.write("".join(md_out))

    print(f"Dump completado exitosamente: {OUTPUT_MD} ({os.path.getsize(OUTPUT_MD)} bytes)")

if __name__ == "__main__":
    main()
