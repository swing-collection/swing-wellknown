# -*- coding: utf-8 -*-

"""Admin for well-known templates with code editor."""

from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from ..models import WellKnownTemplate


@admin.register(WellKnownTemplate)
class WellKnownTemplateAdmin(admin.ModelAdmin):
    """
    Admin for editable templates with code editor.
    Allows live editing of wellknown templates.
    """

    list_display = [
        "name",
        "is_active",
        "updated_at",
        "preview_link",
    ]
    list_filter = ["is_active"]
    search_fields = ["name", "content", "description"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["name"]

    fieldsets = (
        (None, {
            "fields": ("name", "is_active"),
        }),
        (_("Template Content"), {
            "fields": ("content",),
            "description": _(
                "Edit the Jinja2 template. Available variables: "
                "site, site_contact, social, meta, current_year, developer, etc."
            ),
        }),
        (_("Information"), {
            "fields": ("description", "created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(attrs={
                "rows": 30,
                "cols": 100,
                "style": "font-family: monospace; font-size: 13px;",
            })
        },
    }

    def preview_link(self, obj):
        """Link to preview the template."""
        # Map template names to URLs
        url_map = {
            "robots.txt.jinja": "/robots.txt",
            "humans.txt.jinja": "/humans.txt",
            "security.txt.jinja": "/security.txt",
            "ads.txt.jinja": "/ads.txt",
            "business.txt.jinja": "/business.txt",
            "copyright.txt.jinja": "/copyright.txt",
            "license.txt.jinja": "/license.txt",
            "hackers.txt.jinja": "/hackers.txt",
            "pgp-key.txt.jinja": "/pgp-key.txt",
            "trust.txt.jinja": "/trust.txt",
            "earth.txt.jinja": "/earth.txt",
            "llms.txt.jinja": "/llms.txt",
            "ai.txt.jinja": "/ai.txt",
            "privacy.txt.jinja": "/privacy.txt",
            "dnt-policy.txt.jinja": "/.well-known/dnt-policy.txt",
            "acknowledgments.txt.jinja": "/acknowledgments.txt",
            "contact.vcard.jinja": "/contact.vcard",
            "contact.ldif.jinja": "/contact.ldif",
            "manifest.webmanifest": "/manifest.webmanifest",
            "browserconfig.xml": "/browserconfig.xml",
            "gpc.json.jinja": "/.well-known/gpc.json",
            "funding.json.jinja": "/.well-known/funding.json",
            "apple-app-site-association.jinja": "/.well-known/apple-app-site-association",
            "assetlinks.json.jinja": "/.well-known/assetlinks.json",
        }
        url = url_map.get(obj.name, "#")
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">Preview →</a>',
            url
        )
    preview_link.short_description = _("Preview")

    class Media:
        css = {
            "all": [
                "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/theme/monokai.min.css",
            ]
        }
        js = [
            "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/jinja2/jinja2.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/xml/xml.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/javascript/javascript.min.js",
        ]
