# File Encoding

All file operations (creation, opening, reading, writing, and editing) must strictly use UTF-8 encoding.
- Never use ASCII or system-default legacy encodings (such as Windows-1252/CP-1252).
- The project strictly works with Spanish text, which requires full support for accented characters (á, é, í, ó, ú), ñ, diéresis (ü), and inverted punctuation (¿, ¡).
- When writing Python code or scripts, always explicitly specify `encoding='utf-8'` when reading or writing files (e.g., `open(file, 'r', encoding='utf-8')`).
- When writing text files in Python on Windows (`open(...)`) or hashing source text (`sha256`), normalize to LF (`newline='\n'` / `.replace('\r\n', '\n')`) to avoid CRLF drift.
- Shell and command-line operations must preserve and emit UTF-8 encoding.
