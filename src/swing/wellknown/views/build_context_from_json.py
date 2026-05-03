# -*- coding: utf-8 -*-

"""Build context data from JSON files."""

from datetime import datetime
from typing import Any

from ..utils import load_brand_data, load_meta_data, load_social_data


def _build_context_from_json() -> dict[str, Any]:
    """Build template context from JSON files (fallback)."""
    brand_data = load_brand_data()
    social_data = load_social_data()
    meta_data = load_meta_data()

    # Extract brand information
    brand = brand_data.get("brand", {})
    brand_name = brand.get("name", {})
    brand_contact = brand.get("contact", {})
    brand_info = brand.get("information", {})

    # Build site context
    site = {
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
    site_contact = {
        "url": urls.get("main", ""),
        "site_url": urls.get("main", ""),
        "site_email": emails.get("main", ""),
        "email": emails.get("main", ""),
        "locations": brand_contact.get("locations", []),
    }

    # Build social context (only active profiles)
    social = [
        {"service": s["service"], "profile": s["profile"]}
        for s in social_data
        if s.get("active", False)
    ]

    return {
        "site": site,
        "site_contact": site_contact,
        "social": social,
        "meta": meta_data,
        "current_year": datetime.now().year,
        "developer": brand_name.get("long", ""),
        "site_name": brand_name.get("long", ""),
    }
