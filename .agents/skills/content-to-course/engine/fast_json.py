"""High-speed JSON serialization and deserialization powered by orjson (Rust/C) with stdlib fallback."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Union

try:
    import orjson as _orjson

    HAS_ORJSON = True
except ImportError:
    _orjson = None  # type: ignore[assignment]
    HAS_ORJSON = False


def loads(data: Union[str, bytes, bytearray, memoryview]) -> Any:
    """Parse JSON from str or bytes using orjson when available."""
    if HAS_ORJSON:
        try:
            return _orjson.loads(data)
        except Exception:
            pass
    if isinstance(data, (bytes, bytearray, memoryview)):
        return json.loads(bytes(data).decode("utf-8"))
    return json.loads(data)


def dumps_bytes(obj: Any, indent: bool = False) -> bytes:
    """Serialize an object to UTF-8 JSON bytes using orjson when available."""
    if HAS_ORJSON:
        opts = _orjson.OPT_NON_STR_KEYS | getattr(_orjson, "OPT_SERIALIZE_NUMPY", 0)
        if indent:
            opts |= _orjson.OPT_INDENT_2
        try:
            return _orjson.dumps(obj, option=opts)
        except TypeError:
            pass
    return json.dumps(
        obj,
        ensure_ascii=False,
        indent=2 if indent else None,
    ).encode("utf-8")


def dumps_str(obj: Any, indent: bool = False) -> str:
    """Serialize an object to a UTF-8 JSON string using orjson when available."""
    return dumps_bytes(obj, indent=indent).decode("utf-8")


def read_json(path: Union[str, Path]) -> Any:
    """Read and parse a JSON file directly from raw bytes."""
    p = Path(path)
    return loads(p.read_bytes())


def write_json(path: Union[str, Path], obj: Any, indent: bool = True) -> None:
    """Serialize and write a JSON object directly as UTF-8 bytes."""
    p = Path(path)
    p.write_bytes(dumps_bytes(obj, indent=indent))
