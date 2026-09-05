# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Admin for social accounts."""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from ..models import SocialAccount


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    """Admin for social accounts."""

    list_display = [
        "get_service_display",
        "username",
        "profile_url_link",
        "is_active",
        "order",
    ]
    list_editable = ["is_active", "order"]
    list_filter = ["service", "is_active"]
    search_fields = ["username", "profile_url", "service_custom"]
    ordering = ["order", "service"]

    fieldsets = (
        (None, {
            "fields": ("service", "service_custom"),
        }),
        (_("Profile"), {
            "fields": ("profile_url", "username"),
        }),
        (_("Settings"), {
            "fields": ("is_active", "order"),
        }),
    )

    @admin.display(description=_("Service"))
    def get_service_display(self, obj):
        """Display service name."""
        return obj.get_service_name()

    @admin.display(description=_("Profile URL"))
    def profile_url_link(self, obj):
        """Display profile URL as link."""
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">{}</a>',
            obj.profile_url,
            obj.profile_url[:50] + "..." if len(obj.profile_url) > 50 else obj.profile_url
        )
