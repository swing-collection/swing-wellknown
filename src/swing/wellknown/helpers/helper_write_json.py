# -*- coding: utf-8 -*-

"""
Provides write_json utility function.
"""

import json
from pathlib import Path
from typing import Any, Union

from .helper_write_file import write_file


def write_json(path: Union[str, Path], data: dict[str, Any]) -> str:
    """Write data as JSON to a file."""
    return write_file(path, json.dumps(data, indent=2))
