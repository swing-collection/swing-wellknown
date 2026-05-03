# -*- coding: utf-8 -*-

"""Inline admin for social accounts."""

from django.contrib import admin

from ..models import SocialAccount


class SocialAccountInline(admin.TabularInline):
    """Inline admin for social accounts."""

    model = SocialAccount
    extra = 0
    fields = ["service", "username", "profile_url", "is_active", "order"]
    ordering = ["order", "service"]
