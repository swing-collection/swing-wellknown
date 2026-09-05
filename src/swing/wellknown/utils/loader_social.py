# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides load_social_data function.
"""

import json
from pathlib import Path
from typing import Any

from .read_json import read_json

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_social_data() -> list[dict[str, Any]]:
    """Load social media data from JSON file.

    Returns:
        A list of social media account dictionaries, each containing:
        - service: The social media platform name
        - profile: The profile URL
        - active: Whether the account is active

    Returns an empty list if the file is not found or invalid.
    """
    try:
        data = read_json(DATA_DIR / "_social.json")
        return data.get("social", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []
