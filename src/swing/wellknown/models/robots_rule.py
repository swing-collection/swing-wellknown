# -*- coding: utf-8 -*-

"""Robots rule model for robots.txt configuration."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class RobotsRule(models.Model):
    """
    Model for robots.txt rules.
    """

    user_agent = models.CharField(
        _("User Agent"),
        max_length=100,
        default="*",
        help_text=_("User agent pattern (e.g., '*', 'Googlebot', 'GPTBot')")
    )
    rule_type = models.CharField(
        _("Rule Type"),
        max_length=10,
        choices=[
            ("allow", "Allow"),
            ("disallow", "Disallow"),
        ],
        default="disallow"
    )
    path = models.CharField(
        _("Path"),
        max_length=500,
        default="/",
        help_text=_("Path pattern to allow/disallow")
    )
    crawl_delay = models.PositiveIntegerField(
        _("Crawl Delay"),
        blank=True,
        null=True,
        help_text=_("Seconds between requests (optional)")
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True
    )
    order = models.PositiveIntegerField(
        _("Order"),
        default=0
    )

    class Meta:
        verbose_name = _("Robots Rule")
        verbose_name_plural = _("Robots Rules")
        ordering = ["order", "user_agent"]

    def __str__(self):
        return f"{self.user_agent}: {self.rule_type} {self.path}"
