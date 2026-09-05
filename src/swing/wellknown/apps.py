# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Swing Well-Known - App Configuration
======================================

Django app configuration for the swing.wellknown reusable app.

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# =============================================================================
# Classes
# =============================================================================


class SwingWellKnownConfig(AppConfig):
    """
    Swing Well-Known App Configuration
    ====================================

    Django app configuration for serving well-known files
    (robots.txt, humans.txt, security.txt, llms.txt, etc.).

    """

    # Full Python path to the application
    name = "swing.wellknown"

    # Short name for the application
    label = "swing_wellknown"

    # Human-readable name for the application
    verbose_name = _("Well-Known Files")

    # The implicit primary key type to add to models within this app.
    default_auto_field = "django.db.models.BigAutoField"
