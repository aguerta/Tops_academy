# Antigravity Lifecycle Hooks Safety (`hooks.json`)

Whenever creating, editing, or debugging `.agents/hooks.json` or lifecycle hook scripts (`PreToolUse`, `PostToolUse`, `SessionStart`, `PreInvocation`, `PostInvocation`, `Stop`):

1. **Working Directory Invariant (`cwd = .agents/`):** Antigravity executes hook commands with the working directory set to the directory containing `hooks.json` (e.g., `<repo>/.agents/`), NOT the workspace root.
   - Always write relative script paths starting from `.agents/` (e.g., `"command": "python skills/<skill-name>/<script>.py"`), never `"python .agents/skills/..."`.
   - Inside Python hook scripts, always resolve `REPO_ROOT` from `__file__` (e.g., `Path(__file__).resolve().parents[3]`), never from `Path.cwd()`.
2. **Exit Code `0` Invariant (Prevent Self-Lockout):** Non-zero exit codes (especially Python exit status `2` from missing files or `argparse` errors) cause `PreToolUse` to hard-block all matched tools (`read_file`, `write_file`, `edit_file`, `run_command`).
   - Hook scripts must use Python stdlib only, wrap `main()` in `try ... except BaseException:`, communicate decisions exclusively via camelCase JSON on `stdout` (`{"decision": "allow"}` or `{"decision": "deny", "reason": "..."}`), and **always exit with status `0`**.
3. **Staged Template Activation:** Antigravity hot-reloads `.agents/hooks.json` immediately on disk write. During multi-step or multi-agent development, write and test `.agents/hooks.template.json` from `Set-Location .agents` first (`EXIT_CODE=0`), and copy to `.agents/hooks.json` only after all implementation and tests are verified.
