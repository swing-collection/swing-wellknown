# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Admin for sitemaps."""

from django.contrib import admin

from ..models import Sitemap


@admin.register(Sitemap)
class SitemapAdmin(admin.ModelAdmin):
    """Admin for sitemap URLs."""

    list_display = ["url", "is_active"]
    list_editable = ["is_active"]
    search_fields = ["url"]
