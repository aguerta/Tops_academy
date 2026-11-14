"""Common test fixtures, path constants, and helper utilities."""

from __future__ import annotations

from pathlib import Path
import socket

# Repository Path Constants
REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"
PLATFORM_DIR = REPO_ROOT / "platform"
PLATFORM_SRC = PLATFORM_DIR / "src"
COURSES_DIR = REPO_ROOT / "courses"


def find_free_port() -> int:
    """Bind to an ephemeral port on 127.0.0.1 and return the allocated port number."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def strip_code_comments(src: str) -> str:
    """Robust comment stripper supporting JS/TS/JSX and CSS.

    Removes // line comments and /* ... */ block comments (including JSX {/* ... */}),
    while strictly preserving string literals ('...', "...", `...`).
    Maintains approximate newline structure for clean diagnostics across Windows (CRLF) and POSIX (LF).
    """
    out: list[str] = []
    i = 0
    n = len(src)
    state = "NORMAL"

    while i < n:
        c = src[i]
        next_c = src[i + 1] if i + 1 < n else ""

        if state == "NORMAL":
            if c == "/" and next_c == "/":
                state = "LINE_COMMENT"
                i += 2
                continue
            elif c == "/" and next_c == "*":
                state = "BLOCK_COMMENT"
                i += 2
                continue
            elif c == "'":
                state = "SINGLE_QUOTE"
                out.append(c)
                i += 1
                continue
            elif c == '"':
                state = "DOUBLE_QUOTE"
                out.append(c)
                i += 1
                continue
            elif c == "`":
                state = "BACKTICK"
                out.append(c)
                i += 1
                continue
            else:
                out.append(c)
                i += 1
                continue

        elif state == "SINGLE_QUOTE":
            out.append(c)
            if c == "\\":
                if i + 1 < n:
                    out.append(src[i + 1])
                    i += 2
                    continue
            elif c == "'":
                state = "NORMAL"
            i += 1

        elif state == "DOUBLE_QUOTE":
            out.append(c)
            if c == "\\":
                if i + 1 < n:
                    out.append(src[i + 1])
                    i += 2
                    continue
            elif c == '"':
                state = "NORMAL"
            i += 1

        elif state == "BACKTICK":
            out.append(c)
            if c == "\\":
                if i + 1 < n:
                    out.append(src[i + 1])
                    i += 2
                    continue
            elif c == "`":
                state = "NORMAL"
            i += 1

        elif state == "LINE_COMMENT":
            if c == "\n":
                state = "NORMAL"
                out.append("\n")
            i += 1

        elif state == "BLOCK_COMMENT":
            if c == "*" and next_c == "/":
                state = "NORMAL"
                i += 2
                continue
            elif c == "\n":
                out.append("\n")
            i += 1

    return "".join(out)
