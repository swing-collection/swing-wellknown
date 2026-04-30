# -*- coding: utf-8 -*-

"""
Provides write_json utility function.
"""

import json
from pathlib import Path
from typing import Any, Union

from .write_file import write_file


def write_json(path: Union[str, Path], data: dict[str, Any]) -> str:
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
