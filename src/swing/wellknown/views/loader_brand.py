# -*- coding: utf-8 -*-

"""
Provides load_brand_data function.
"""

import json
from pathlib import Path
from typing import Any

from ..helpers.helper_read_json import read_json

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_brand_data() -> dict[str, Any]:
    """Load brand data from JSON file."""
    try:
        return read_json(DATA_DIR / "_brand.json")
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
