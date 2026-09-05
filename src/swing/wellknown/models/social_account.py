# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Social account model for social media profiles."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class SocialAccount(models.Model):
    """
    Model for social media accounts.
    """

    SERVICE_CHOICES = [
        ("500px", "500px"),
        ("angellist", "AngelList"),
        ("archinect", "Archinect"),
        ("behance", "Behance"),
        ("bluesky", "Bluesky"),
        ("crunchbase", "Crunchbase"),
        ("discord", "Discord"),
        ("dribbble", "Dribbble"),
        ("facebook", "Facebook"),
        ("figma", "Figma"),
        ("github", "GitHub"),
        ("gitlab", "GitLab"),
        ("instagram", "Instagram"),
        ("issuu", "Issuu"),
        ("linkedin", "LinkedIn"),
        ("mastodon", "Mastodon"),
        ("medium", "Medium"),
        ("pinterest", "Pinterest"),
        ("reddit", "Reddit"),
        ("slack", "Slack"),
        ("snapchat", "Snapchat"),
        ("spotify", "Spotify"),
        ("stackoverflow", "Stack Overflow"),
        ("telegram", "Telegram"),
        ("threads", "Threads"),
        ("tiktok", "TikTok"),
        ("tumblr", "Tumblr"),
        ("twitch", "Twitch"),
        ("twitter", "Twitter/X"),
        ("vimeo", "Vimeo"),
        ("whatsapp", "WhatsApp"),
        ("youtube", "YouTube"),
        ("other", "Other"),
    ]

    service = models.CharField(
        _("Service"),
        max_length=50,
        choices=SERVICE_CHOICES,
        help_text=_("Social media platform")
    )
    service_custom = models.CharField(
        _("Custom Service Name"),
        max_length=100,
        blank=True,
        help_text=_("If 'Other' selected, specify the service name")
    )
    profile_url = models.URLField(
        _("Profile URL"),
        help_text=_("Full URL to your profile")
    )
    username = models.CharField(
        _("Username"),
        max_length=100,
        blank=True,
        help_text=_("Your username/handle on this platform")
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Show this account in templates")
    )
    order = models.PositiveIntegerField(
        _("Display Order"),
        default=0
    )

    class Meta:
        verbose_name = _("Social Account")
        verbose_name_plural = _("Social Accounts")
        ordering = ["order", "service"]

    def __str__(self):
        service_name = self.get_service_name()
        return f"{service_name}: {self.username or self.profile_url}"

    def get_service_name(self):
        """Return the display name for the service."""
        if self.service == "other" and self.service_custom:
            return self.service_custom
        return self.get_service_display()
