# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Security policy model for security.txt settings."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from .singleton import SingletonModel


class SecurityPolicy(SingletonModel):
    """
    Model for security.txt specific settings.
    """

    contact_email = models.EmailField(
        _("Security Contact Email"),
        blank=True
    )
    contact_url = models.URLField(
        _("Security Contact URL"),
        blank=True,
        help_text=_("URL for security reporting page")
    )
    encryption_key_url = models.URLField(
        _("PGP Key URL"),
        blank=True,
        help_text=_("URL to PGP public key")
    )
    acknowledgments_url = models.URLField(
        _("Acknowledgments URL"),
        blank=True,
        help_text=_("URL to security researcher acknowledgments")
    )
    policy_url = models.URLField(
        _("Security Policy URL"),
        blank=True
    )
    hiring_url = models.URLField(
        _("Security Hiring URL"),
        blank=True,
        help_text=_("URL to security job openings")
    )
    preferred_languages = models.CharField(
        _("Preferred Languages"),
        max_length=100,
        default="en",
        help_text=_("Comma-separated language codes")
    )
    expires_date = models.DateField(
        _("Expires Date"),
        blank=True,
        null=True,
        help_text=_("When this security.txt expires")
    )

    class Meta:
        verbose_name = _("Security Policy")
        verbose_name_plural = _("Security Policy")

    def __str__(self):
        return "Security Policy"

    def get_languages_list(self):
        """Return languages as a list."""
        if not self.preferred_languages:
            return ["en"]
        return [lang.strip() for lang in self.preferred_languages.split(",") if lang.strip()]
