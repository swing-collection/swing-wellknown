# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides write_json utility function.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .write_file import write_file


def write_json(path: str | Path, data: dict[str, Any]) -> str:
    """Write data as JSON to a file.

    Args:
        path: The path to the file to write.
        data: The dictionary to serialize as JSON.

    Returns:
        The JSON string that was written.

    Raises:
        IOError: If the file cannot be written.
        TypeError: If the data cannot be serialized to JSON.
    """
    return write_file(path, json.dumps(data, indent=2))
