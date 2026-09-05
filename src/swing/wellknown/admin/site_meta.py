# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Admin for site metadata."""

from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _

from ..models import SiteMeta


@admin.register(SiteMeta)
class SiteMetaAdmin(admin.ModelAdmin):
    """Admin for site metadata singleton."""

    fieldsets = (
        (_("Technical Information"), {
            "fields": ("language", "standards", "components", "software"),
            "description": _("Used in humans.txt and other technical files"),
        }),
        (_("Analytics"), {
            "fields": ("google_analytics_id", "google_search_console_token"),
            "classes": ("collapse",),
        }),
        (_("Advertising"), {
            "fields": ("google_adsense_id", "ads_txt_content"),
            "classes": ("collapse",),
        }),
    )

    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 3, "cols": 80})},
    }

    def has_add_permission(self, request):
        """Only allow one instance."""
        return not SiteMeta.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of singleton."""
        return False

    def changelist_view(self, request, extra_context=None):
        """Redirect to change view if instance exists."""
        obj = SiteMeta.objects.first()
        if obj is not None:
            from django.shortcuts import redirect
            return redirect("admin:wellknown_sitemeta_change", obj.pk)
        return super().changelist_view(request, extra_context)
