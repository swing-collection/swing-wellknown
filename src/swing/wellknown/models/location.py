# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Location model for office/business addresses."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Location(models.Model):
    """
    Model for office/business locations.
    """

    name = models.CharField(
        _("Location Name"),
        max_length=255,
        help_text=_("e.g., 'Headquarters', 'Amsterdam Office'")
    )
    building = models.CharField(
        _("Building"),
        max_length=255,
        blank=True
    )
    street = models.CharField(
        _("Street"),
        max_length=255,
        blank=True
    )
    street_number = models.CharField(
        _("Street Number"),
        max_length=20,
        blank=True
    )
    postal_code = models.CharField(
        _("Postal Code"),
        max_length=20,
        blank=True
    )
    city = models.CharField(
        _("City"),
        max_length=100,
        blank=True
    )
    province = models.CharField(
        _("Province/State"),
        max_length=100,
        blank=True
    )
    country = models.CharField(
        _("Country"),
        max_length=100,
        blank=True
    )
    phone = models.CharField(
        _("Phone"),
        max_length=50,
        blank=True
    )
    email = models.EmailField(
        _("Email"),
        blank=True
    )
    google_map_url = models.URLField(
        _("Google Map URL"),
        blank=True,
        help_text=_("Embed URL for Google Maps")
    )
    is_primary = models.BooleanField(
        _("Primary Location"),
        default=False,
        help_text=_("Mark as primary/headquarters location")
    )
    order = models.PositiveIntegerField(
        _("Display Order"),
        default=0
    )

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def to_dict(self):
        """Convert to dictionary for template context."""
        return {
            "name": self.name,
            "building": self.building,
            "street": self.street,
            "street_number": self.street_number,
            "postal_code": self.postal_code,
            "city": self.city,
            "province": self.province,
            "country": self.country,
            "phone": self.phone,
            "email": self.email,
            "google_map": self.google_map_url,
        }
