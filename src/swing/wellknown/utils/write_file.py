# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides write_file utility function.
"""

from __future__ import annotations

from pathlib import Path


def write_file(path: str | Path, data: str) -> str:
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
