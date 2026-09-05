# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Swing Well-Known - AI.txt View
================================

Class-based view for serving ai.txt files that provide AI-specific
guidelines and permissions for the website.

Usage::

    # In urls.py
    from swing.wellknown.views import AiView

    urlpatterns = [
        path("ai.txt", AiView.as_view(), name="ai"),
        path(".well-known/ai.txt", AiView.as_view(), name="ai_wellknown"),
    ]

Configuration via settings.py::

    WELLKNOWN_CONFIG = {
        "ai": {
            "allow_training": False,
            "allow_summarization": True,
            "allow_indexing": True,
            "attribution_required": True,
            "contact": "ai@example.com",
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


class AiView(BaseWellKnownView):
    """
    AI.txt View
    ============

    Serves an ai.txt file that provides guidelines for AI systems
    interacting with the website.

    """

    file_type: str = "ai"
    template_name: str = "swing_wellknown/ai.txt"
    content_type: str = "text/plain; charset=utf-8"

    def get_context_data(self, request: HttpRequest) -> dict[str, Any]:
        """Build context for ai.txt template."""
        context = super().get_context_data(request)

        allow_training = self.get_config("allow_training", False)
        allow_summarization = self.get_config("allow_summarization", True)
        allow_indexing = self.get_config("allow_indexing", True)
        attribution_required = self.get_config("attribution_required", True)
        contact = self.get_config("contact")
        custom_rules = self.get_config("rules", [])

        context.update({
            "allow_training": allow_training,
            "allow_summarization": allow_summarization,
            "allow_indexing": allow_indexing,
            "attribution_required": attribution_required,
            "contact": contact,
            "rules": custom_rules,
        })

        return context

    def get(self, request: HttpRequest) -> HttpResponse:
        """Generate ai.txt content."""
        try:
            return super().get(request)
        except Exception:
            return self._generate_ai_txt(request)

    def _generate_ai_txt(self, request: HttpRequest) -> HttpResponse:
        """Generate ai.txt content programmatically."""
        context = self.get_context_data(request)
        lines: list[str] = [
            "# ai.txt",
            "# AI usage guidelines for this website",
            "",
        ]

        # Training permission
        if context["allow_training"]:
            lines.append("Allow-Training: yes")
        else:
            lines.append("Allow-Training: no")

        # Summarization permission
        if context["allow_summarization"]:
            lines.append("Allow-Summarization: yes")
        else:
            lines.append("Allow-Summarization: no")

        # Indexing permission
        if context["allow_indexing"]:
            lines.append("Allow-Indexing: yes")
        else:
            lines.append("Allow-Indexing: no")

        # Attribution
        if context["attribution_required"]:
            lines.append("Attribution-Required: yes")
        else:
            lines.append("Attribution-Required: no")

        lines.append("")

        # Contact
        if context["contact"]:
            lines.append(f"Contact: {context['contact']}")
            lines.append("")

        # Custom rules
        if context["rules"]:
            lines.append("# Custom Rules")
            for rule in context["rules"]:
                lines.append(f"# {rule}")

        content = "\n".join(lines)
        return HttpResponse(content, content_type=self.content_type)


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = ["AiView"]
