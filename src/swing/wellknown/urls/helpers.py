# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Swing Well-Known - URL Helpers
================================

Helper functions for configuring well-known file URL patterns in
Django projects.

Usage::

    # In urls.py
    from swing.wellknown.urls import wellknown_urlpatterns

    urlpatterns = [
        ...
    ] + wellknown_urlpatterns()

Or selectively include specific patterns::

    from swing.wellknown.urls import (
        robots_urlpatterns,
        security_urlpatterns,
    )

    urlpatterns = [
        ...
    ] + robots_urlpatterns() + security_urlpatterns()

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from typing import TYPE_CHECKING

# Import | Django
from django.urls import path

# Import | Local
from swing.wellknown.views import (
    AdsView,
    AiView,
    HumansView,
    LlmsView,
    RobotsView,
    SecurityView,
)

if TYPE_CHECKING:
    from django.urls.resolvers import URLPattern


# =============================================================================
# URL Pattern Generators
# =============================================================================


def robots_urlpatterns() -> list[URLPattern]:
    """
    Return URL patterns for robots.txt.

    Returns:
        List with robots.txt URL pattern.

    """
    return [
        path("robots.txt", RobotsView.as_view(), name="robots"),
    ]


def humans_urlpatterns() -> list[URLPattern]:
    """
    Return URL patterns for humans.txt.

    Returns:
        List with humans.txt URL pattern.

    """
    return [
        path("humans.txt", HumansView.as_view(), name="humans"),
    ]


def security_urlpatterns() -> list[URLPattern]:
    """
    Return URL patterns for security.txt.

    Includes both RFC 9116 standard path (.well-known/security.txt)
    and common root path (security.txt).

    Returns:
        List with security.txt URL patterns.

    """
    return [
        path(
            ".well-known/security.txt",
            SecurityView.as_view(),
            name="security_wellknown",
        ),
        path("security.txt", SecurityView.as_view(), name="security"),
    ]


def llms_urlpatterns() -> list[URLPattern]:
    """
    Return URL patterns for llms.txt.

    Returns:
        List with llms.txt URL pattern.

    """
    return [
        path("llms.txt", LlmsView.as_view(), name="llms"),
    ]


def ads_urlpatterns() -> list[URLPattern]:
    """
    Return URL patterns for ads.txt.

    Returns:
        List with ads.txt URL pattern.

    """
    return [
        path("ads.txt", AdsView.as_view(), name="ads"),
    ]


def ai_urlpatterns() -> list[URLPattern]:
    """
    Return URL patterns for ai.txt.

    Returns:
        List with ai.txt URL pattern.

    """
    return [
        path("ai.txt", AiView.as_view(), name="ai"),
        path(".well-known/ai.txt", AiView.as_view(), name="ai_wellknown"),
    ]


def wellknown_urlpatterns(
    include_robots: bool = True,
    include_humans: bool = True,
    include_security: bool = True,
    include_llms: bool = True,
    include_ads: bool = False,
    include_ai: bool = False,
) -> list[URLPattern]:
    """
    Return combined URL patterns for well-known files.

    Args:
        include_robots: Include robots.txt pattern.
        include_humans: Include humans.txt pattern.
        include_security: Include security.txt patterns.
        include_llms: Include llms.txt pattern.
        include_ads: Include ads.txt pattern.
        include_ai: Include ai.txt patterns.

    Returns:
        Combined list of URL patterns.

    Example::

        # Include all standard patterns
        urlpatterns += wellknown_urlpatterns()

        # Include only specific patterns
        urlpatterns += wellknown_urlpatterns(
            include_robots=True,
            include_security=True,
            include_humans=False,
            include_llms=False,
        )

    """
    patterns: list[URLPattern] = []

    if include_robots:
        patterns.extend(robots_urlpatterns())

    if include_humans:
        patterns.extend(humans_urlpatterns())

    if include_security:
        patterns.extend(security_urlpatterns())

    if include_llms:
        patterns.extend(llms_urlpatterns())

    if include_ads:
        patterns.extend(ads_urlpatterns())

    if include_ai:
        patterns.extend(ai_urlpatterns())

    return patterns


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "robots_urlpatterns",
    "humans_urlpatterns",
    "security_urlpatterns",
    "llms_urlpatterns",
    "ads_urlpatterns",
    "ai_urlpatterns",
    "wellknown_urlpatterns",
]
