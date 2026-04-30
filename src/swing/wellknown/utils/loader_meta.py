# -*- coding: utf-8 -*-

"""
Provides load_meta_data function.
"""

import json
from pathlib import Path
from typing import Any

from .read_json import read_json

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_meta_data() -> dict[str, Any]:
    """Load metadata from JSON file.

    Returns:
        A dictionary containing site metadata including:
        - meta: Standards, components, software, language
        - tags: Analytics and advertising IDs
        - form: Form configurations

    Returns an empty dict if the file is not found or invalid.
    """
    try:
        return read_json(DATA_DIR / "_meta.json")
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
