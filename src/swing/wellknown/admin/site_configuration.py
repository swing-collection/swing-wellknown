# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Admin for site configuration."""

from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _

from ..models import SiteConfiguration


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    """Admin for site configuration singleton."""

    fieldsets = (
        (_("Brand Names"), {
            "fields": ("name_short", "name_long", "name_legal", "name_abbr"),
            "description": _("Configure your brand/company names"),
        }),
        (_("Contact Information"), {
            "fields": ("website_url", "email_main", "email_support", "phone_main"),
        }),
        (_("Description & SEO"), {
            "fields": ("description", "keywords"),
            "description": _("Used in templates and SEO"),
        }),
    )

    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 4, "cols": 80})},
    }

    def has_add_permission(self, request):
        """Only allow one instance."""
        return not SiteConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of singleton."""
        return False

    def changelist_view(self, request, extra_context=None):
        """Redirect to change view if instance exists."""
        obj = SiteConfiguration.objects.first()
        if obj is not None:
            from django.shortcuts import redirect
            return redirect("admin:wellknown_siteconfiguration_change", obj.pk)
        return super().changelist_view(request, extra_context)
