# -*- coding: utf-8 -*-

"""
Django admin configuration for wellknown app.

Provides admin interfaces for managing site configuration,
locations, social accounts, and editable templates.
"""

from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (
    SiteConfiguration,
    Location,
    SocialAccount,
    SiteMeta,
    WellKnownTemplate,
    SecurityPolicy,
    RobotsRule,
    Sitemap,
)


# =============================================================================
# Inline Admin Classes
# =============================================================================

class LocationInline(admin.TabularInline):
    """Inline admin for locations in site configuration."""

    model = Location
    extra = 0
    fields = ["name", "city", "country", "phone", "is_primary", "order"]
    ordering = ["order", "name"]


class SocialAccountInline(admin.TabularInline):
    """Inline admin for social accounts."""

    model = SocialAccount
    extra = 0
    fields = ["service", "username", "profile_url", "is_active", "order"]
    ordering = ["order", "service"]


# =============================================================================
# Admin Classes
# =============================================================================

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
        if SiteConfiguration.objects.exists():
            obj = SiteConfiguration.objects.first()
            from django.shortcuts import redirect
            return redirect("admin:wellknown_siteconfiguration_change", obj.pk)
        return super().changelist_view(request, extra_context)


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

    def get_service_display(self, obj):
        """Display service name."""
        return obj.get_service_name()
    get_service_display.short_description = _("Service")

    def profile_url_link(self, obj):
        """Display profile URL as link."""
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">{}</a>',
            obj.profile_url,
            obj.profile_url[:50] + "..." if len(obj.profile_url) > 50 else obj.profile_url
        )
    profile_url_link.short_description = _("Profile URL")


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
        if SiteMeta.objects.exists():
            obj = SiteMeta.objects.first()
            from django.shortcuts import redirect
            return redirect("admin:wellknown_sitemeta_change", obj.pk)
        return super().changelist_view(request, extra_context)


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


@admin.register(SecurityPolicy)
class SecurityPolicyAdmin(admin.ModelAdmin):
    """Admin for security policy singleton."""

    fieldsets = (
        (_("Contact"), {
            "fields": ("contact_email", "contact_url"),
            "description": _("How to report security vulnerabilities"),
        }),
        (_("Security Information"), {
            "fields": (
                "encryption_key_url",
                "policy_url",
                "acknowledgments_url",
                "hiring_url",
            ),
        }),
        (_("Settings"), {
            "fields": ("preferred_languages", "expires_date"),
        }),
    )

    def has_add_permission(self, request):
        """Only allow one instance."""
        return not SecurityPolicy.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of singleton."""
        return False

    def changelist_view(self, request, extra_context=None):
        """Redirect to change view if instance exists."""
        if SecurityPolicy.objects.exists():
            obj = SecurityPolicy.objects.first()
            from django.shortcuts import redirect
            return redirect("admin:wellknown_securitypolicy_change", obj.pk)
        return super().changelist_view(request, extra_context)


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

@admin.register(Sitemap)
class SitemapAdmin(admin.ModelAdmin):
    """Admin for sitemap URLs."""

    list_display = ["url", "is_active"]
    list_editable = ["is_active"]
    search_fields = ["url"]
