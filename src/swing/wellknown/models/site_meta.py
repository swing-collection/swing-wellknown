# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Site metadata model."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from .singleton import SingletonModel


class SiteMeta(SingletonModel):
    """
    Singleton model for site metadata.
    Replaces _meta.json for standards, tags, etc.
    """

    # Site standards
    language = models.CharField(
        _("Language"),
        max_length=50,
        default="English"
    )
    standards = models.TextField(
        _("Web Standards"),
        blank=True,
        default="HTML5, CSS3, JavaScript",
        help_text=_("Comma-separated list of standards used")
    )
    components = models.TextField(
        _("Components/Frameworks"),
        blank=True,
        help_text=_("Comma-separated list of frameworks/libraries")
    )
    software = models.TextField(
        _("Software"),
        blank=True,
        help_text=_("Comma-separated list of software used")
    )

    # Analytics tags
    google_analytics_id = models.CharField(
        _("Google Analytics ID"),
        max_length=50,
        blank=True,
        help_text=_("e.g., UA-XXXXXXXX-X or G-XXXXXXXXXX")
    )
    google_search_console_token = models.CharField(
        _("Google Search Console Token"),
        max_length=100,
        blank=True
    )

    # Ads configuration
    google_adsense_id = models.CharField(
        _("Google AdSense Publisher ID"),
        max_length=50,
        blank=True,
        help_text=_("pub-XXXXXXXXXXXXXXXX")
    )
    ads_txt_content = models.TextField(
        _("ads.txt Content"),
        blank=True,
        help_text=_("Custom ads.txt entries")
    )

    class Meta:
        verbose_name = _("Site Metadata")
        verbose_name_plural = _("Site Metadata")

    def __str__(self):
        return "Site Metadata"

    def get_standards_list(self):
        """Return standards as a list."""
        if not self.standards:
            return []
        return [s.strip() for s in self.standards.split(",") if s.strip()]

    def get_components_list(self):
        """Return components as a list."""
        if not self.components:
            return []
        return [c.strip() for c in self.components.split(",") if c.strip()]

    def get_software_list(self):
        """Return software as a list."""
        if not self.software:
            return []
        return [s.strip() for s in self.software.split(",") if s.strip()]
