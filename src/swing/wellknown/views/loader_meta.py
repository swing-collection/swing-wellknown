# -*- coding: utf-8 -*-

"""
Provides load_meta_data function.
"""

import json
from pathlib import Path
from typing import Any

from ..helpers.helper_read_json import read_json

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_meta_data() -> dict[str, Any]:
    """Load metadata from JSON file."""
    try:
        return read_json(DATA_DIR / "_meta.json")
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
