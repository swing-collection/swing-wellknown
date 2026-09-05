# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides read_json utility function.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .read_file import read_file


def read_json(path: str | Path) -> dict[str, Any]:
    """Read and parse JSON from a file.

    Args:
        path: The path to the JSON file to read.

    Returns:
        The parsed JSON data as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    return json.loads(read_file(path))
