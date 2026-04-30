# -*- coding: utf-8 -*-

"""
Provides read_file utility function.
"""

from pathlib import Path
from typing import Union


def read_file(path: Union[str, Path]) -> str:
    """Read content from a file."""
    with open(path, "r", encoding="utf-8") as file:
        return file.read()
