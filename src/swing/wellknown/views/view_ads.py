# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Swing Well-Known - Ads.txt View
=================================

Class-based view for serving ads.txt files for authorized digital sellers.

Usage::

    # In urls.py
    from swing.wellknown.views import AdsView

    urlpatterns = [
        path("ads.txt", AdsView.as_view(), name="ads"),
    ]

Configuration via settings.py::

    WELLKNOWN_CONFIG = {
        "ads": {
            "sellers": [
                {
                    "domain": "google.com",
                    "account_id": "pub-1234567890",
                    "account_type": "DIRECT",
                    "certification_id": "f08c47fec0942fa0",
                },
            ],
            "contact": "mailto:ads@example.com",
            "subdomain": "example.com",
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


class AdsView(BaseWellKnownView):
    """
    Ads.txt View
    =============

    Serves an ads.txt file that lists authorized digital sellers
    per the IAB Tech Lab specification.

    """

    file_type: str = "ads"
    template_name: str = "swing_wellknown/ads.txt"
    content_type: str = "text/plain; charset=utf-8"

    def get_context_data(self, request: HttpRequest) -> dict[str, Any]:
        """Build context for ads.txt template."""
        context = super().get_context_data(request)

        sellers = self.get_config("sellers", [])
        contact = self.get_config("contact")
        subdomain = self.get_config("subdomain")

        context.update({
            "sellers": sellers,
            "contact": contact,
            "subdomain": subdomain,
        })

        return context

    def get(self, request: HttpRequest) -> HttpResponse:
        """Generate ads.txt content."""
        try:
            return super().get(request)
        except Exception:
            return self._generate_ads_txt(request)

    def _generate_ads_txt(self, request: HttpRequest) -> HttpResponse:
        """Generate ads.txt content programmatically."""
        context = self.get_context_data(request)
        lines: list[str] = [
            "# ads.txt",
            "# Authorized Digital Sellers",
            "",
        ]

        # Contact
        if context["contact"]:
            lines.append(f"CONTACT={context['contact']}")
            lines.append("")

        # Subdomain
        if context["subdomain"]:
            lines.append(f"SUBDOMAIN={context['subdomain']}")
            lines.append("")

        # Sellers
        for seller in context["sellers"]:
            domain = seller.get("domain", "")
            account_id = seller.get("account_id", "")
            account_type = seller.get("account_type", "DIRECT")
            cert_id = seller.get("certification_id", "")

            if domain and account_id:
                line = f"{domain}, {account_id}, {account_type}"
                if cert_id:
                    line += f", {cert_id}"
                lines.append(line)

        content = "\n".join(lines)
        return HttpResponse(content, content_type=self.content_type)


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = ["AdsView"]
