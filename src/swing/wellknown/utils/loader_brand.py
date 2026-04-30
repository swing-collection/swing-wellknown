# -*- coding: utf-8 -*-

"""
Provides load_brand_data function.
"""

import json
from pathlib import Path
from typing import Any

from .read_json import read_json

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_brand_data() -> dict[str, Any]:
    """Load brand data from JSON file.

    Returns:
        A dictionary containing brand information including:
        - name: Brand names (short, long, legal, abbr)
        - contact: Contact information (url, email, phone, locations)
        - information: Additional brand info (description, keywords)

    Returns an empty dict if the file is not found or invalid.
    """
    try:
        return read_json(DATA_DIR / "_brand.json")
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
