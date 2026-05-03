# -*- coding: utf-8 -*-

"""Inline admin classes for locations and social accounts."""

from django.contrib import admin

from ..models import Location, SocialAccount


class LocationInline(admin.TabularInline):
    """Inline admin for locations in site configuration."""

    model = Location
    extra = 0
    fields = ["name", "city", "country", "phone", "is_primary", "order"]
    ordering = ["order", "name"]
