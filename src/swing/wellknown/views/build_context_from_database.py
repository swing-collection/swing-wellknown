# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Build context data from database models."""

from datetime import datetime
from typing import Any


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
