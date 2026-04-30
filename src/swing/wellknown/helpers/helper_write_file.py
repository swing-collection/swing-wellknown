# -*- coding: utf-8 -*-

"""
Provides write_file utility function.
"""

from pathlib import Path
from typing import Union


def write_file(path: Union[str, Path], data: str) -> str:
    """Write content to a file."""
    with open(path, "w", encoding="utf-8") as file:
        file.write(str(data))
    return data
