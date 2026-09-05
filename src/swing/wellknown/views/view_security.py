# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Swing Well-Known - Security.txt View
======================================

Class-based view for serving security.txt files per RFC 9116.
Provides security researchers with vulnerability disclosure information.

Usage::

    # In urls.py
    from swing.wellknown.views import SecurityView

    urlpatterns = [
        path(".well-known/security.txt", SecurityView.as_view(), name="security"),
        path("security.txt", SecurityView.as_view(), name="security_root"),
    ]

Configuration via settings.py::

    WELLKNOWN_CONFIG = {
        "security": {
            "contact": ["mailto:security@example.com"],
            "expires": "2027-12-31T23:59:59.000Z",
            "preferred_languages": ["en", "nl"],
            "canonical": ["https://example.com/.well-known/security.txt"],
            "encryption": "https://example.com/.well-known/pgp-key.txt",
            "acknowledgments": "https://example.com/security/hall-of-fame/",
            "policy": "https://example.com/security/policy/",
            "hiring": "https://example.com/careers/security/",
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


class SecurityView(BaseWellKnownView):
    """
    Security.txt View
    ==================

    Serves a security.txt file per RFC 9116 to help security researchers
    report vulnerabilities.

    Required fields (per RFC 9116):
    - Contact: How to report vulnerabilities
    - Expires: When this file should be considered stale

    Recommended fields:
    - Canonical: The canonical URI for this file
    - Preferred-Languages: Languages for security reports

    Optional fields:
    - Encryption: PGP key for encrypted communications
    - Acknowledgments: Page recognizing security researchers
    - Policy: Link to security policy
    - Hiring: Security job openings
    - CSAF: Security advisories

    """

    file_type: str = "security"
    template_name: str = "swing_wellknown/security.txt"
    content_type: str = "text/plain; charset=utf-8"

    def get_context_data(self, request: HttpRequest) -> dict[str, Any]:
        """Build context for security.txt template."""
        context = super().get_context_data(request)
        site_url = context["site_url"]

        # Get configuration with defaults
        contact = self.get_config("contact", [])
        expires = self.get_config(
            "expires",
            f"{context['current_year'] + 1}-12-31T23:59:59.000Z",
        )
        preferred_languages = self.get_config("preferred_languages", ["en"])
        canonical = self.get_config("canonical", [])
        encryption = self.get_config("encryption")
        acknowledgments = self.get_config("acknowledgments")
        policy = self.get_config("policy")
        hiring = self.get_config("hiring")
        csaf = self.get_config("csaf")

        # Default contact from site config
        if not contact:
            site_config = self.get_site_config()
            email = site_config.get("security_email") or site_config.get("email")
            if email:
                contact = [f"mailto:{email}"]

        # Default canonical URLs
        if not canonical:
            canonical = [
                f"{site_url}/.well-known/security.txt",
                f"{site_url}/security.txt",
            ]

        context.update({
            "contact": contact,
            "expires": expires,
            "preferred_languages": preferred_languages,
            "canonical": canonical,
            "encryption": encryption,
            "acknowledgments": acknowledgments,
            "policy": policy,
            "hiring": hiring,
            "csaf": csaf,
        })

        return context

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Generate security.txt content.

        Falls back to programmatic generation if template not found.
        """
        try:
            return super().get(request)
        except Exception:
            return self._generate_security_txt(request)

    def _generate_security_txt(self, request: HttpRequest) -> HttpResponse:
        """Generate security.txt content programmatically."""
        context = self.get_context_data(request)
        lines: list[str] = [
            "# security.txt",
            "# See https://securitytxt.org/ for specification",
            "# RFC 9116 - A File Format to Aid in Security Vulnerability Disclosure",
            "",
        ]

        # Required: Contact
        for contact_method in context["contact"]:
            lines.append(f"Contact: {contact_method}")

        # Required: Expires
        lines.append(f"Expires: {context['expires']}")
        lines.append("")

        # Recommended: Canonical
        for uri in context["canonical"]:
            lines.append(f"Canonical: {uri}")

        # Recommended: Preferred-Languages
        if context["preferred_languages"]:
            languages = ", ".join(context["preferred_languages"])
            lines.append(f"Preferred-Languages: {languages}")

        lines.append("")

        # Optional fields
        if context["encryption"]:
            lines.append(f"Encryption: {context['encryption']}")

        if context["acknowledgments"]:
            lines.append(f"Acknowledgments: {context['acknowledgments']}")

        if context["policy"]:
            lines.append(f"Policy: {context['policy']}")

        if context["hiring"]:
            lines.append(f"Hiring: {context['hiring']}")

        if context["csaf"]:
            lines.append(f"CSAF: {context['csaf']}")

        content = "\n".join(lines)
        return HttpResponse(content, content_type=self.content_type)


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = ["SecurityView"]
