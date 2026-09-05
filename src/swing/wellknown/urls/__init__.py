# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Swing Well-Known - URL Configuration
======================================

URL patterns and helpers for well-known files (robots.txt, humans.txt,
security.txt, llms.txt, etc.).

Usage - Helper functions (recommended)::

    # In urls.py
    from swing.wellknown.urls import wellknown_urlpatterns

    urlpatterns = [
        path("admin/", admin.site.urls),
        ...
    ] + wellknown_urlpatterns()

Usage - Direct include::

    from django.urls import include, path

    urlpatterns = [
        path("", include("swing.wellknown.urls")),
    ]

Usage - Selective patterns::

    from swing.wellknown.urls import (
        robots_urlpatterns,
        security_urlpatterns,
    )

    urlpatterns += robots_urlpatterns() + security_urlpatterns()

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Django
from django.urls import path
from django.urls.resolvers import URLPattern, URLResolver

# Import | Local
from swing.wellknown.urls.helpers import (
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
    HumansView,
    LlmsView,
    RobotsView,
    SecurityView,
)

# =============================================================================
# URL Patterns
# =============================================================================

app_name: str = "wellknown"

# Default URL patterns when using include("swing.wellknown.urls")
urlpatterns: list[URLPattern | URLResolver] = [
    # Robots.txt
    path("robots.txt", RobotsView.as_view(), name="robots"),
    # Humans.txt
    path("humans.txt", HumansView.as_view(), name="humans"),
    # Security.txt (RFC 9116)
    path(
        ".well-known/security.txt",
        SecurityView.as_view(),
        name="security_wellknown",
    ),
    path("security.txt", SecurityView.as_view(), name="security"),
    # LLMs.txt
    path("llms.txt", LlmsView.as_view(), name="llms"),
    # AI.txt
    path("ai.txt", AiView.as_view(), name="ai"),
    # Ads.txt
    path("ads.txt", AdsView.as_view(), name="ads"),
]


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    # App name and patterns
    "app_name",
    "urlpatterns",
    # Helper functions
    "robots_urlpatterns",
    "humans_urlpatterns",
    "security_urlpatterns",
    "llms_urlpatterns",
    "ads_urlpatterns",
    "ai_urlpatterns",
    "wellknown_urlpatterns",
]
