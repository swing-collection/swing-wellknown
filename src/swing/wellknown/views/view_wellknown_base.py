# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Swing Well-Known - Base View
==============================

Base class for all well-known file views. Provides common functionality
for template rendering, context building, and settings-based configuration.

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from datetime import datetime
from typing import TYPE_CHECKING, Any

# Import | Django
from django.conf import settings
from django.http import HttpResponse
from django.template import engines
from django.views import View

if TYPE_CHECKING:
    from django.http import HttpRequest


# =============================================================================
# Classes
# =============================================================================


class BaseWellKnownView(View):
    """
    Base Well-Known View
    =====================

    Abstract base class for all well-known file views (robots.txt,
    humans.txt, security.txt, llms.txt, etc.).

    Subclasses should define:
    - `file_type`: The type identifier (e.g., "robots", "security")
    - `template_name`: The template to render
    - `content_type`: The MIME type (defaults to "text/plain")

    Configuration is loaded from Django settings using the
    `WELLKNOWN_CONFIG` namespace.

    Example settings::

        WELLKNOWN_CONFIG = {
            "robots": {
                "allow_all": True,
                "disallow_paths": ["/admin/", "/api/"],
                "crawl_delay": 1,
            },
            "security": {
                "contact": ["mailto:security@example.com"],
                "expires": "2027-12-31T23:59:59.000Z",
            },
        }

    """

    # NOTE: Not annotated as ClassVar - django-stubs types `View.http_method_names`
    # as a plain instance attribute, so overriding it as a ClassVar here would be
    # a mypy [misc] "Cannot override instance variable with class variable" error.
    http_method_names: list[str] = ["get", "head", "options"]

    # Override in subclasses
    file_type: str = "base"
    template_name: str = ""
    content_type: str = "text/plain; charset=utf-8"

    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value for this file type.

        Args:
            key: Configuration key to look up.
            default: Default value if not found.

        Returns:
            Configuration value or default.

        """
        wellknown_config = getattr(settings, "WELLKNOWN_CONFIG", {})
        file_config = wellknown_config.get(self.file_type, {})
        return file_config.get(key, default)

    def get_site_config(self) -> dict[str, Any]:
        """
        Get site-wide configuration.

        Returns:
            Site configuration dictionary.

        """
        wellknown_config = getattr(settings, "WELLKNOWN_CONFIG", {})
        return wellknown_config.get("site", {})

    def get_context_data(self, request: HttpRequest) -> dict[str, Any]:
        """
        Build context data for template rendering.

        Args:
            request: The HTTP request.

        Returns:
            Context dictionary for template rendering.

        """
        site_config = self.get_site_config()
        now = datetime.now()

        # Build base context
        context: dict[str, Any] = {
            "request": request,
            "site": site_config,
            "site_url": request.build_absolute_uri("/").rstrip("/"),
            "current_year": now.year,
            "current_month": now.month,
            "current_day": now.day,
        }

        # Add file-specific configuration
        wellknown_config = getattr(settings, "WELLKNOWN_CONFIG", {})
        file_config = wellknown_config.get(self.file_type, {})
        context[self.file_type] = file_config

        return context

    def render_template(self, request: HttpRequest) -> str:
        """
        Render the template with context.

        Args:
            request: The HTTP request.

        Returns:
            Rendered template content.

        """
        context = self.get_context_data(request)

        # Try Jinja2 engine first, fall back to Django
        try:
            jinja_engine = engines["jinja2"]
            template = jinja_engine.get_template(self.template_name)
        except (KeyError, Exception):
            django_engine = engines["django"]
            template = django_engine.get_template(self.template_name)

        return template.render(context)

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handle GET request.

        Args:
            request: The HTTP request.

        Returns:
            HTTP response with rendered content.

        """
        content = self.render_template(request)
        return HttpResponse(content, content_type=self.content_type)


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = ["BaseWellKnownView"]
