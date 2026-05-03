# -*- coding: utf-8 -*-

"""Admin for robots.txt rules."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models import RobotsRule


@admin.register(RobotsRule)
class RobotsRuleAdmin(admin.ModelAdmin):
    """Admin for robots.txt rules."""

    list_display = [
        "user_agent",
        "rule_type",
        "path",
        "crawl_delay",
        "is_active",
        "order",
    ]
    list_editable = ["rule_type", "path", "is_active", "order"]
    list_filter = ["rule_type", "is_active", "user_agent"]
    search_fields = ["user_agent", "path"]
    ordering = ["order", "user_agent"]

    fieldsets = (
        (None, {
            "fields": ("user_agent", "rule_type", "path"),
        }),
        (_("Options"), {
            "fields": ("crawl_delay", "is_active", "order"),
        }),
    )
