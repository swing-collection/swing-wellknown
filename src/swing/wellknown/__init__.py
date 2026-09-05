# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Swing Well-Known - Reusable Django App
========================================

A fully-featured reusable Django app for serving well-known files
(robots.txt, humans.txt, security.txt, llms.txt, etc.) with
class-based views and settings-driven configuration.

Features
--------
- Class-based views for all common well-known files
- Settings-driven configuration via `WELLKNOWN_CONFIG`
- Template-based or programmatic content generation
- URL helpers for easy integration
- AI crawler control in robots.txt
- RFC 9116 compliant security.txt
- llmstxt.org compliant llms.txt

Quick Start
-----------
1. Add to INSTALLED_APPS::

    INSTALLED_APPS = [
        ...
        "swing.wellknown",
    ]

2. Include URL patterns::

    # Option A: Include all patterns
    from swing.wellknown.urls import wellknown_urlpatterns

    urlpatterns = [
        ...
    ] + wellknown_urlpatterns()

    # Option B: Include as Django URLs
    urlpatterns = [
        path("", include("swing.wellknown.urls")),
    ]

3. Configure in settings (optional)::

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
        },
    }

Views
-----
- `RobotsView`: robots.txt for search engines and AI crawlers
- `HumansView`: humans.txt crediting the team
- `SecurityView`: security.txt per RFC 9116
- `LlmsView`: llms.txt for LLM guidance
- `AdsView`: ads.txt for authorized digital sellers
- `AiView`: ai.txt for AI usage guidelines

URL Helpers
-----------
- `wellknown_urlpatterns()`: All patterns combined
- `robots_urlpatterns()`: robots.txt only
- `security_urlpatterns()`: security.txt only
- And more...

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import importlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from swing.wellknown.conf import (
        DEFAULT_WELLKNOWN_CONFIG,
        get_config,
        get_site_config,
        get_wellknown_config,
    )
    from swing.wellknown.urls import (
        ads_urlpatterns,
        ai_urlpatterns,
        humans_urlpatterns,
        llms_urlpatterns,
        robots_urlpatterns,
        security_urlpatterns,
        wellknown_urlpatterns,
    )
    from swing.wellknown.views import (
        AdsView,
        AiView,
        BaseWellKnownView,
        HumansView,
        LlmsView,
        RobotsView,
        SecurityView,
        TextView,
    )


# =============================================================================
# Module Metadata
# =============================================================================

__author__ = "Lars van Vianen"
__copyright__ = "Copyright (c) 2024 Scape Press"
__credits__ = ["Lars van Vianen"]
__license__ = "Proprietary"
__version__ = "1.1.0"
__maintainer__ = "Lars van Vianen"
__email__ = "lars@scape.press"
__status__ = "Alpha"

default_app_config = "swing.wellknown.apps.SwingWellKnownConfig"


# =============================================================================
# Lazy-loaded Public API
# =============================================================================

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    # Views
    "BaseWellKnownView": (
        "swing.wellknown.views.view_wellknown_base",
        "BaseWellKnownView",
    ),
    "RobotsView": (
        "swing.wellknown.views.view_robots",
        "RobotsView",
    ),
    "HumansView": (
        "swing.wellknown.views.view_humans",
        "HumansView",
    ),
    "SecurityView": (
        "swing.wellknown.views.view_security",
        "SecurityView",
    ),
    "LlmsView": (
        "swing.wellknown.views.view_llms",
        "LlmsView",
    ),
    "AdsView": (
        "swing.wellknown.views.view_ads",
        "AdsView",
    ),
    "AiView": (
        "swing.wellknown.views.view_ai",
        "AiView",
    ),
    "TextView": (
        "swing.wellknown.views.view_text",
        "TextView",
    ),
    # URL helpers
    "wellknown_urlpatterns": (
        "swing.wellknown.urls.helpers",
        "wellknown_urlpatterns",
    ),
    "robots_urlpatterns": (
        "swing.wellknown.urls.helpers",
        "robots_urlpatterns",
    ),
    "humans_urlpatterns": (
        "swing.wellknown.urls.helpers",
        "humans_urlpatterns",
    ),
    "security_urlpatterns": (
        "swing.wellknown.urls.helpers",
        "security_urlpatterns",
    ),
    "llms_urlpatterns": (
        "swing.wellknown.urls.helpers",
        "llms_urlpatterns",
    ),
    "ads_urlpatterns": (
        "swing.wellknown.urls.helpers",
        "ads_urlpatterns",
    ),
    "ai_urlpatterns": (
        "swing.wellknown.urls.helpers",
        "ai_urlpatterns",
    ),
    # Configuration
    "get_wellknown_config": (
        "swing.wellknown.conf",
        "get_wellknown_config",
    ),
    "get_config": (
        "swing.wellknown.conf",
        "get_config",
    ),
    "get_site_config": (
        "swing.wellknown.conf",
        "get_site_config",
    ),
    "DEFAULT_WELLKNOWN_CONFIG": (
        "swing.wellknown.conf",
        "DEFAULT_WELLKNOWN_CONFIG",
    ),
}


def __getattr__(name: str) -> Any:
    """Lazy-load public API symbols on first access."""
    if name in _LAZY_IMPORTS:
        module_name, attr_name = _LAZY_IMPORTS[name]
        module = importlib.import_module(module_name)
        return getattr(module, attr_name)
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)


def __dir__() -> list[str]:
    """List available public API symbols."""
    return list(_LAZY_IMPORTS.keys()) + [
        "__version__",
        "__author__",
        "__email__",
        "default_app_config",
    ]


__all__: list[str] = list(_LAZY_IMPORTS.keys())
