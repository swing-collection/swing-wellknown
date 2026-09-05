# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Well-known template model for editable templates."""

from django.db import models
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _


class WellKnownTemplate(models.Model):
    """
    Model for editable wellknown templates.
    Allows live editing of template files via admin.
    """

    TEMPLATE_CHOICES = [
        ("robots.txt.jinja", "robots.txt"),
        ("humans.txt.jinja", "humans.txt"),
        ("security.txt.jinja", "security.txt"),
        ("ads.txt.jinja", "ads.txt"),
        ("business.txt.jinja", "business.txt"),
        ("copyright.txt.jinja", "copyright.txt"),
        ("license.txt.jinja", "license.txt"),
        ("hackers.txt.jinja", "hackers.txt"),
        ("pgp-key.txt.jinja", "pgp-key.txt"),
        ("trust.txt.jinja", "trust.txt"),
        ("earth.txt.jinja", "earth.txt"),
        ("llms.txt.jinja", "llms.txt"),
        ("ai.txt.jinja", "ai.txt"),
        ("privacy.txt.jinja", "privacy.txt"),
        ("dnt-policy.txt.jinja", "dnt-policy.txt"),
        ("acknowledgments.txt.jinja", "acknowledgments.txt"),
        ("contact.vcard.jinja", "contact.vcard"),
        ("contact.ldif.jinja", "contact.ldif"),
        ("manifest.webmanifest", "manifest.webmanifest"),
        ("browserconfig.xml", "browserconfig.xml"),
        ("gpc.json.jinja", "gpc.json"),
        ("funding.json.jinja", "funding.json"),
        ("apple-app-site-association.jinja", "apple-app-site-association"),
        ("assetlinks.json.jinja", "assetlinks.json"),
    ]

    name = models.CharField(
        _("Template Name"),
        max_length=100,
        unique=True,
        choices=TEMPLATE_CHOICES,
        help_text=_("Select the template to customize")
    )
    content = models.TextField(
        _("Template Content"),
        help_text=_("Jinja2 template content. Use {{ variable }} for dynamic content.")
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Use this custom template instead of the default")
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        help_text=_("Notes about this template")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Well-Known Template")
        verbose_name_plural = _("Well-Known Templates")
        ordering = ["name"]

    def __str__(self):
        return self.get_name_display()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f"wellknown_template_{self.name}")
