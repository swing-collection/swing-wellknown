# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Site configuration model."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from .singleton import SingletonModel


class SiteConfiguration(SingletonModel):
    """
    Singleton model for site-wide configuration.
    Replaces _brand.json for brand/site settings.
    """

    # Brand names
    name_short = models.CharField(
        _("Short Name"),
        max_length=100,
        blank=True,
        help_text=_("Short brand name (e.g., 'Acme')")
    )
    name_long = models.CharField(
        _("Long Name"),
        max_length=255,
        blank=True,
        help_text=_("Full brand name (e.g., 'Acme Corporation')")
    )
    name_legal = models.CharField(
        _("Legal Name"),
        max_length=255,
        blank=True,
        help_text=_("Legal entity name (e.g., 'Acme Corp. Inc.')")
    )
    name_abbr = models.CharField(
        _("Abbreviation"),
        max_length=20,
        blank=True,
        help_text=_("Brand abbreviation (e.g., 'AC')")
    )

    # Contact info
    website_url = models.URLField(
        _("Website URL"),
        blank=True,
        help_text=_("Primary website URL")
    )
    email_main = models.EmailField(
        _("Main Email"),
        blank=True,
        help_text=_("Primary contact email")
    )
    email_support = models.EmailField(
        _("Support Email"),
        blank=True,
        help_text=_("Support/people email")
    )
    phone_main = models.CharField(
        _("Main Phone"),
        max_length=50,
        blank=True,
        help_text=_("Primary phone number")
    )

    # Description
    description = models.TextField(
        _("Description"),
        blank=True,
        help_text=_("Brief site/brand description")
    )
    keywords = models.TextField(
        _("Keywords"),
        blank=True,
        help_text=_("Comma-separated keywords for SEO")
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Site Configuration")
        verbose_name_plural = _("Site Configuration")

    def __str__(self):
        return self.name_long or self.name_short or "Site Configuration"

    def get_keywords_list(self):
        """Return keywords as a list."""
        if not self.keywords:
            return []
        return [k.strip() for k in self.keywords.split(",") if k.strip()]
