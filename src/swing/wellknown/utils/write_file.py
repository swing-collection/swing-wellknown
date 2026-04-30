# -*- coding: utf-8 -*-

"""
Provides write_file utility function.
"""

from pathlib import Path
from typing import Union


def write_file(path: Union[str, Path], data: str) -> str:
    """Write content to a file.

    Args:
        path: The path to the file to write.
        data: The content to write to the file.

    Returns:
        The data that was written.

    Raises:
        IOError: If the file cannot be written.
    """
    with open(path, "w", encoding="utf-8") as file:
        file.write(str(data))
    return data
