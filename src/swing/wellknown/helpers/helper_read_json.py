# -*- coding: utf-8 -*-

"""
Provides read_json utility function.
"""

import json
from pathlib import Path
from typing import Any, Union

from .helper_read_file import read_file


def read_json(path: Union[str, Path]) -> dict[str, Any]:
    """Read and parse JSON from a file."""
    return json.loads(read_file(path))
