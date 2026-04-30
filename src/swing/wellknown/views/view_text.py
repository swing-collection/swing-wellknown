# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Text Template View Class.



"""


# =============================================================================
# Import
# =============================================================================

# Import | Standard Library
import json
from datetime import datetime
from pathlib import Path
from typing import Any

# Import | Libraries
from django.views.generic.base import TemplateView

# Import | Local Modules
from ..helpers.helper_json import read_json


# =============================================================================
# Export
# =============================================================================

__all__: list[str] = ["text_view",]


# =============================================================================
# Data Loading
# =============================================================================

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_brand_data() -> dict[str, Any]:
    """Load brand data from JSON file."""
    try:
        return read_json(DATA_DIR / "_brand.json")
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def load_social_data() -> list[dict[str, Any]]:
    """Load social media data from JSON file."""
    try:
        data = read_json(DATA_DIR / "_social.json")
        return data.get("social", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def load_meta_data() -> dict[str, Any]:
    """Load metadata from JSON file."""
    try:
        return read_json(DATA_DIR / "_meta.json")
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# =============================================================================
# Classes
# =============================================================================

class TextView(TemplateView):
    """
    Text Template View Class
    """

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """
        Returns context with data loaded from JSON files.
        """
        context = super().get_context_data(**kwargs)

        # Load data from JSON files
        brand_data = load_brand_data()
        social_data = load_social_data()
        meta_data = load_meta_data()

        # Extract brand information
        brand = brand_data.get("brand", {})
        brand_name = brand.get("name", {})
        brand_contact = brand.get("contact", {})
        brand_info = brand.get("information", {})

        # Build site context
        context["site"] = {
            "name": brand_name.get("short", ""),
            "name_long": brand_name.get("long", ""),
            "name_legal": brand_name.get("legal", ""),
            "abbr": brand_name.get("abbr", ""),
            "summary": brand_info.get("description", ""),
            "keywords": brand_info.get("keywords", []),
        }

        # Build site_contact context
        urls = brand_contact.get("url", {})
        emails = brand_contact.get("email", {})
        context["site_contact"] = {
            "url": urls.get("main", ""),
            "site_url": urls.get("main", ""),
            "site_email": emails.get("main", ""),
            "email": emails.get("main", ""),
            "locations": brand_contact.get("locations", []),
        }

        # Build social context (only active profiles)
        context["social"] = [
            {"service": s["service"], "profile": s["profile"]}
            for s in social_data
            if s.get("active", False)
        ]

        # Additional context
        context["current_year"] = datetime.now().year
        context["developer"] = brand_name.get("long", "")
        context["site_name"] = brand_name.get("long", "")

        # Meta context
        context["meta"] = meta_data

        return context


# =============================================================================
# Variables | Export
# =============================================================================

text_view = TextView.as_view
