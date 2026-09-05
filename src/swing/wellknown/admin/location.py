# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Admin for locations."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Admin for locations."""

    list_display = [
        "name",
        "city",
        "country",
        "phone",
        "is_primary",
        "order",
    ]
    list_editable = ["order", "is_primary"]
    list_filter = ["country", "is_primary"]
    search_fields = ["name", "city", "country", "building"]
    ordering = ["order", "name"]

    fieldsets = (
        (None, {
            "fields": ("name", "is_primary", "order"),
        }),
        (_("Address"), {
            "fields": (
                "building",
                ("street", "street_number"),
                ("postal_code", "city"),
                ("province", "country"),
            ),
        }),
        (_("Contact"), {
            "fields": ("phone", "email"),
        }),
        (_("Map"), {
            "fields": ("google_map_url",),
            "classes": ("collapse",),
        }),
    )
