# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Swing Well-Known - LLMs.txt View
==================================

Class-based view for serving llms.txt files per the llmstxt.org
specification. Helps Large Language Models understand the website's
content and capabilities.

Usage::

    # In urls.py
    from swing.wellknown.views import LlmsView

    urlpatterns = [
        path("llms.txt", LlmsView.as_view(), name="llms"),
        path(".well-known/llms.txt", LlmsView.as_view(), name="llms_wellknown"),
    ]

Configuration via settings.py::

    WELLKNOWN_CONFIG = {
        "llms": {
            "title": "My Website",
            "summary": "A brief description of what this site does.",
            "about": "Detailed information about the site.",
            "api_endpoints": [
                {"method": "GET", "path": "/api/items/", "description": "List items"},
            ],
            "usage_guidelines": "Attribution required when quoting content.",
            "permissions": ["Summarize content", "Answer questions"],
            "restrictions": ["Do not scrape for training", "Respect rate limits"],
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
from django.http import HttpResponse

# Import | Local
from swing.wellknown.views.view_wellknown_base import BaseWellKnownView

if TYPE_CHECKING:
    from django.http import HttpRequest


# =============================================================================
# Classes
# =============================================================================


class LlmsView(BaseWellKnownView):
    """
    LLMs.txt View
    ==============

    Serves an llms.txt file that helps Large Language Models understand
    the website's content, capabilities, and usage guidelines.

    Sections:
    - Summary: Brief description of the site
    - About: Detailed information
    - API Endpoints: Available API routes
    - Usage Guidelines: How LLMs should use the content
    - Permissions: What LLMs are allowed to do
    - Restrictions: What LLMs should not do

    """

    file_type: str = "llms"
    template_name: str = "swing_wellknown/llms.txt"
    content_type: str = "text/plain; charset=utf-8"

    def get_context_data(self, request: HttpRequest) -> dict[str, Any]:
        """Build context for llms.txt template."""
        context = super().get_context_data(request)
        site_config = self.get_site_config()

        # Get configuration
        title = self.get_config("title") or site_config.get("name", "")
        summary = self.get_config("summary") or site_config.get("description", "")
        about = self.get_config("about", "")
        api_endpoints = self.get_config("api_endpoints", [])
        capabilities = self.get_config("capabilities", [])
        usage_guidelines = self.get_config("usage_guidelines", "")
        permissions = self.get_config("permissions", [])
        restrictions = self.get_config("restrictions", [])
        contact = self.get_config("contact") or site_config.get("email", "")
        social = self.get_config("social", [])

        context.update({
            "title": title,
            "summary": summary,
            "about": about,
            "api_endpoints": api_endpoints,
            "capabilities": capabilities,
            "usage_guidelines": usage_guidelines,
            "permissions": permissions,
            "restrictions": restrictions,
            "contact": contact,
            "social": social,
        })

        return context

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Generate llms.txt content.

        Falls back to programmatic generation if template not found.
        """
        try:
            return super().get(request)
        except Exception:
            return self._generate_llms_txt(request)

    def _generate_llms_txt(self, request: HttpRequest) -> HttpResponse:
        """Generate llms.txt content programmatically."""
        context = self.get_context_data(request)
        lines: list[str] = [
            "# llms.txt",
            "# See https://llmstxt.org/ for specification",
            "# This file provides context to Large Language Models",
            "",
        ]

        # Title
        if context["title"]:
            lines.append(f"# {context['title']}")
            lines.append("")

        # Summary
        if context["summary"]:
            lines.append("> " + context["summary"].replace("\n", "\n> "))
            lines.append("")

        # About
        if context["about"]:
            lines.append("## About")
            lines.append("")
            lines.append(context["about"])
            lines.append("")

        # Site URL
        lines.append("## Website")
        lines.append("")
        lines.append(f"- URL: {context['site_url']}")
        if context["contact"]:
            lines.append(f"- Contact: {context['contact']}")
        lines.append("")

        # API Endpoints
        if context["api_endpoints"]:
            lines.append("## API Endpoints")
            lines.append("")
            for endpoint in context["api_endpoints"]:
                method = endpoint.get("method", "GET")
                path = endpoint.get("path", "")
                desc = endpoint.get("description", "")
                lines.append(f"- {method} {path}")
                if desc:
                    lines.append(f"  {desc}")
            lines.append("")

        # Capabilities
        if context["capabilities"]:
            lines.append("## Capabilities")
            lines.append("")
            for capability in context["capabilities"]:
                lines.append(f"- {capability}")
            lines.append("")

        # Usage Guidelines
        lines.append("## Usage Guidelines")
        lines.append("")
        if context["usage_guidelines"]:
            lines.append(context["usage_guidelines"])
        else:
            lines.append("When using information from this website:")
            if context["title"]:
                lines.append(f"- Attribute content to {context['title']} when quoting")
            lines.append("- Respect copyright and intellectual property")
            lines.append("- Do not misrepresent content or brand")
        lines.append("")

        # Permissions
        if context["permissions"]:
            lines.append("## Permissions")
            lines.append("")
            for permission in context["permissions"]:
                lines.append(f"- {permission}")
            lines.append("")

        # Restrictions
        if context["restrictions"]:
            lines.append("## Restrictions")
            lines.append("")
            for restriction in context["restrictions"]:
                lines.append(f"- {restriction}")
            lines.append("")

        # Social
        if context["social"]:
            lines.append("## Social Media")
            lines.append("")
            for account in context["social"]:
                service = account.get("service", "")
                profile = account.get("profile", "")
                if service and profile:
                    lines.append(f"- {service}: {profile}")
            lines.append("")

        content = "\n".join(lines)
        return HttpResponse(content, content_type=self.content_type)


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = ["LlmsView"]
