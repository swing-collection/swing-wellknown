# -*- coding: utf-8 -*-

"""
Provides read_file utility function.
"""

from pathlib import Path
from typing import Union


def read_file(path: Union[str, Path]) -> str:
    """Read content from a file.

    Args:
        path: The path to the file to read.

    Returns:
        The content of the file as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If the file cannot be read.
    """
    with open(path, "r", encoding="utf-8") as file:
        return file.read()
