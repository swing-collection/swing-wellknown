# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Swing Well-Known - Robots.txt View
====================================

Class-based view for serving robots.txt files with configurable rules
for search engine crawlers and AI bots.

Usage::

    # In urls.py
    from swing.wellknown.views import RobotsView

    urlpatterns = [
        path("robots.txt", RobotsView.as_view(), name="robots"),
    ]

Configuration via settings.py::

    WELLKNOWN_CONFIG = {
        "robots": {
            "allow_all": True,
            "disallow_paths": ["/admin/", "/api/"],
            "allow_paths": ["/"],
            "crawl_delay": 1,
            "sitemaps": ["https://example.com/sitemap.xml"],
            "ai_crawlers": {
                "GPTBot": False,
                "ChatGPT-User": False,
                "anthropic-ai": False,
            },
        },
    }

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from typing import TYPE_CHECKING, Any

# Import | Django
from django.conf import settings
from django.http import HttpResponse

# Import | Local
from swing.wellknown.views.view_wellknown_base import BaseWellKnownView

if TYPE_CHECKING:
    from django.http import HttpRequest


# =============================================================================
# Classes
# =============================================================================


class RobotsView(BaseWellKnownView):
    """
    Robots.txt View
    ================

    Serves a dynamic robots.txt file for controlling search engine
    and AI crawler access.

    Supports:
    - Allow/disallow rules per user-agent
    - AI crawler blocking (GPTBot, ChatGPT, Claude, etc.)
    - Crawl delay specification
    - Sitemap references

    """

    file_type: str = "robots"
    template_name: str = "swing_wellknown/robots.txt"
    content_type: str = "text/plain; charset=utf-8"

    # Default settings
    DEFAULT_DISALLOW_PATHS: list[str] = [
        "/admin/",
        "/api/",
        "/auth/",
        "/accounts/",
        "/dashboard/",
        "/settings/",
        "/internal/",
    ]

    DEFAULT_AI_CRAWLERS: dict[str, bool] = {
        "GPTBot": False,
        "ChatGPT-User": False,
        "anthropic-ai": False,
        "Claude-Web": False,
        "CCBot": False,
        "Google-Extended": False,
        "FacebookBot": False,
        "cohere-ai": False,
        "Bytespider": False,
        "Applebot-Extended": False,
    }

    def get_context_data(self, request: HttpRequest) -> dict[str, Any]:
        """Build context for robots.txt template."""
        context = super().get_context_data(request)

        # Get configuration with defaults
        allow_all = self.get_config(
            "allow_all",
            not getattr(settings, "DEBUG", False),
        )
        disallow_paths = self.get_config(
            "disallow_paths",
            self.DEFAULT_DISALLOW_PATHS,
        )
        allow_paths = self.get_config("allow_paths", ["/"])
        crawl_delay = self.get_config("crawl_delay", 1)
        sitemaps = self.get_config("sitemaps", [])
        ai_crawlers = self.get_config("ai_crawlers", self.DEFAULT_AI_CRAWLERS)

        # Build sitemap URLs if not specified
        if not sitemaps:
            site_url = context["site_url"]
            sitemaps = [f"{site_url}/sitemap.xml"]

        context.update({
            "allow_all": allow_all,
            "disallow_paths": disallow_paths,
            "allow_paths": allow_paths,
            "crawl_delay": crawl_delay,
            "sitemaps": sitemaps,
            "ai_crawlers": ai_crawlers,
        })

        return context

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Generate robots.txt content.

        Falls back to programmatic generation if template not found.
        """
        try:
            return super().get(request)
        except Exception:
            # Fallback: generate programmatically
            return self._generate_robots_txt(request)

    def _generate_robots_txt(self, request: HttpRequest) -> HttpResponse:
        """Generate robots.txt content programmatically."""
        context = self.get_context_data(request)
        lines: list[str] = [
            "# robots.txt",
            "# https://www.robotstxt.org/",
            "",
            "User-agent: *",
        ]

        if context["allow_all"]:
            lines.append("Allow: /")
            for path in context["disallow_paths"]:
                lines.append(f"Disallow: {path}")
        else:
            lines.append("Disallow: /")
            for path in context["allow_paths"]:
                lines.append(f"Allow: {path}")

        # AI crawlers
        lines.append("")
        lines.append("# AI Crawlers")
        for crawler, allowed in context["ai_crawlers"].items():
            lines.append(f"User-agent: {crawler}")
            if allowed:
                lines.append("Allow: /")
            else:
                lines.append("Disallow: /")
            lines.append("")

        # Sitemaps
        for sitemap in context["sitemaps"]:
            lines.append(f"Sitemap: {sitemap}")

        # Crawl delay
        if context["crawl_delay"]:
            lines.append(f"Crawl-delay: {context['crawl_delay']}")

        content = "\n".join(lines)
        return HttpResponse(content, content_type=self.content_type)


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = ["RobotsView"]
