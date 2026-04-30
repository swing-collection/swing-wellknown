# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Text Template View Class.

Loads configuration from database when available, with fallback to JSON files.
"""


# =============================================================================
# Import
# =============================================================================

# Import | Standard Library
from datetime import datetime
from typing import Any
import logging

# Import | Libraries
from django.views.generic.base import TemplateView

# Import | Local Modules
from ..utils import load_brand_data, load_meta_data, load_social_data


logger = logging.getLogger(__name__)


# =============================================================================
# Helper Functions
# =============================================================================

def _load_from_database():
    """
    Try to load configuration from database models.
    Returns None if models don't exist or database not configured.
    """
    try:
        from ..models import (
            SiteConfiguration,
            Location,
            SocialAccount,
            SiteMeta,
            SecurityPolicy,
        )

        # Check if any configuration exists
        if not SiteConfiguration.objects.exists():
            return None

        config = SiteConfiguration.load()
        site_meta = SiteMeta.load()
        locations = list(Location.objects.filter().order_by("order", "name"))
        social_accounts = list(
            SocialAccount.objects.filter(is_active=True).order_by("order", "service")
        )

        # Try to load security policy
        try:
            security = SecurityPolicy.load()
        except Exception:  # noqa: BLE001
            security = None

        return {
            "config": config,
            "locations": locations,
            "social_accounts": social_accounts,
            "site_meta": site_meta,
            "security": security,
        }

    except Exception:  # noqa: BLE001
        logger.debug("Database not available, falling back to JSON")
        return None


def _build_context_from_database(db_data: dict) -> dict[str, Any]:
    """Build template context from database models."""
    config = db_data["config"]
    locations = db_data["locations"]
    social_accounts = db_data["social_accounts"]
    site_meta = db_data["site_meta"]

    # Build site context
    site = {
        "name": config.name_short,
        "name_long": config.name_long,
        "name_legal": config.name_legal,
        "abbr": config.name_abbr,
        "summary": config.description,
        "keywords": config.get_keywords_list(),
    }

    # Build site_contact context
    primary_location = next(
        (loc for loc in locations if loc.is_primary),
        locations[0] if locations else None
    )

    site_contact = {
        "url": config.website_url,
        "site_url": config.website_url,
        "site_email": config.email_main,
        "email": config.email_support or config.email_main,
        "phone": config.phone_main,
        "locations": [loc.to_dict() for loc in locations],
    }

    if primary_location:
        site_contact["primary_location"] = primary_location.to_dict()

    # Build social context
    social = [
        {
            "service": acc.get_service_name(),
            "profile": acc.profile_url,
            "username": acc.username,
        }
        for acc in social_accounts
    ]

    # Build meta context
    meta = {
        "site": {
            "language": site_meta.language,
            "standards": site_meta.get_standards_list(),
            "components": site_meta.get_components_list(),
            "software": site_meta.get_software_list(),
        },
        "tags": {
            "google_analytics": site_meta.google_analytics_id,
            "google_search_console": site_meta.google_search_console_token,
        },
        "ads": {
            "google_adsense_id": site_meta.google_adsense_id,
            "ads_txt_content": site_meta.ads_txt_content,
        },
    }

    return {
        "site": site,
        "site_contact": site_contact,
        "social": social,
        "meta": meta,
        "current_year": datetime.now().year,
        "developer": config.name_long,
        "site_name": config.name_long,
    }


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


# =============================================================================
# Classes
# =============================================================================

class TextView(TemplateView):
    """
    Text Template View Class.

    Loads configuration from database when available,
    with automatic fallback to JSON files.
    """

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """
        Returns context with data loaded from database or JSON files.

        Priority:
        1. Database (if models exist and have data)
        2. JSON files (fallback)
        """
        context = super().get_context_data(**kwargs)

        # Try database first
        db_data = _load_from_database()

        if db_data:
            # Load from database
            data_context = _build_context_from_database(db_data)
        else:
            # Fallback to JSON files
            data_context = _build_context_from_json()

        context.update(data_context)
        return context


# =============================================================================
# Variables | Export
# =============================================================================

text_view = TextView.as_view


# =============================================================================
# Export
# =============================================================================

__all__: list[str] = ["text_view",]
