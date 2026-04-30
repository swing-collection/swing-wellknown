# -*- coding: utf-8 -*-

"""
Provides load_social_data function.
"""

import json
from pathlib import Path
from typing import Any

from ..helpers.helper_read_json import read_json

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_social_data() -> list[dict[str, Any]]:
    """Load social media data from JSON file."""
    try:
        data = read_json(DATA_DIR / "_social.json")
        return data.get("social", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []
