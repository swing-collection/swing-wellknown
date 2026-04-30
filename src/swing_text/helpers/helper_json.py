# -*- coding: utf-8 -*-

"""
Provides JSON file I/O utilities.
"""

import json
from pathlib import Path
from typing import Any, Union


def read_file(path: Union[str, Path]) -> str:
    """Read content from a file."""
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def read_json(path: Union[str, Path]) -> dict[str, Any]:
    """Read and parse JSON from a file."""
    return json.loads(read_file(path))


def write_file(path: Union[str, Path], data: str) -> str:
    """Write content to a file."""
    with open(path, "w", encoding="utf-8") as file:
        file.write(str(data))
    return data


def write_json(path: Union[str, Path], data: dict[str, Any]) -> str:
    """Write data as JSON to a file."""
    return write_file(path, json.dumps(data, indent=2))
