# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Swing Well-Known - Views Package
==================================

Class-based views for serving well-known files (robots.txt, humans.txt,
security.txt, llms.txt, etc.).

Each view follows the single-symbol-per-file pattern and can be
configured via Django settings using the `WELLKNOWN_CONFIG` namespace.

Usage::

    # In urls.py
    from swing.wellknown.views import RobotsView, HumansView, SecurityView

    urlpatterns = [
        path("robots.txt", RobotsView.as_view(), name="robots"),
        path("humans.txt", HumansView.as_view(), name="humans"),
        path(".well-known/security.txt", SecurityView.as_view(), name="security"),
    ]

Configuration::

    # In settings.py
    WELLKNOWN_CONFIG = {
        "site": {
            "name": "My Website",
            "url": "https://example.com",
            "email": "info@example.com",
        },
        "robots": {
            "allow_all": True,
            "disallow_paths": ["/admin/"],
        },
        "security": {
            "contact": ["mailto:security@example.com"],
            "expires": "2027-12-31T23:59:59.000Z",
        },
    }

"""

# =============================================================================
# Imports
# =============================================================================

from swing.wellknown.views.view_wellknown_base import BaseWellKnownView
from swing.wellknown.views.view_robots import RobotsView
from swing.wellknown.views.view_humans import HumansView
from swing.wellknown.views.view_security import SecurityView
from swing.wellknown.views.view_llms import LlmsView
from swing.wellknown.views.view_ads import AdsView
from swing.wellknown.views.view_ai import AiView
from swing.wellknown.views.view_text import TextView, text_view


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    # Base class
    "BaseWellKnownView",
    # Specific views
    "RobotsView",
    "HumansView",
    "SecurityView",
    "LlmsView",
    "AdsView",
    "AiView",
    # Legacy / generic
    "TextView",
    "text_view",
]
