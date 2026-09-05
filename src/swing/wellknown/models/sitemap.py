# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Sitemap model for robots.txt sitemap entries."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Sitemap(models.Model):
    """
    Model for sitemap URLs in robots.txt.
    """

    url = models.URLField(
        _("Sitemap URL"),
        help_text=_("Full URL to sitemap")
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True
    )

    class Meta:
        verbose_name = _("Sitemap")
        verbose_name_plural = _("Sitemaps")

    def __str__(self):
        return self.url
