# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Load context data from database models."""

import logging

logger = logging.getLogger(__name__)


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
