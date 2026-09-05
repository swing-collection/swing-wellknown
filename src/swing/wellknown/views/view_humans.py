# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Swing Well-Known - Humans.txt View
====================================

Class-based view for serving humans.txt files that credit the team
behind the website per humanstxt.org specification.

Usage::

    # In urls.py
    from swing.wellknown.views import HumansView

    urlpatterns = [
        path("humans.txt", HumansView.as_view(), name="humans"),
    ]

Configuration via settings.py::

    WELLKNOWN_CONFIG = {
        "humans": {
            "team": [
                {
                    "role": "Developer",
                    "name": "Jane Doe",
                    "site": "https://janedoe.com",
                    "twitter": "@janedoe",
                    "location": "Amsterdam, Netherlands",
                },
            ],
            "thanks": [
                {"name": "Open Source Community"},
            ],
            "standards": ["HTML5", "CSS3", "Python", "Django"],
            "software": ["VS Code", "Git", "Docker"],
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


class HumansView(BaseWellKnownView):
    """
    Humans.txt View
    ================

    Serves a humans.txt file that credits the people behind the website.
    Follows the humanstxt.org specification.

    Sections:
    - TEAM: People who worked on the site
    - THANKS: People/organizations to thank
    - SITE: Technical information about the site

    """

    file_type: str = "humans"
    template_name: str = "swing_wellknown/humans.txt"
    content_type: str = "text/plain; charset=utf-8"

    def get_context_data(self, request: HttpRequest) -> dict[str, Any]:
        """Build context for humans.txt template."""
        context = super().get_context_data(request)

        # Get configuration
        team = self.get_config("team", [])
        thanks = self.get_config("thanks", [])
        standards = self.get_config("standards", ["HTML5", "CSS3", "JavaScript"])
        software = self.get_config("software", [])
        language = self.get_config("language", "English")

        # Get site info from global config
        site_config = self.get_site_config()
        site_name = site_config.get("name", "")
        site_url = site_config.get("url", context["site_url"])

        context.update({
            "team": team,
            "thanks": thanks,
            "standards": standards,
            "software": software,
            "language": language,
            "site_name": site_name,
            "site_url": site_url,
        })

        return context

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Generate humans.txt content.

        Falls back to programmatic generation if template not found.
        """
        try:
            return super().get(request)
        except Exception:
            return self._generate_humans_txt(request)

    def _generate_humans_txt(self, request: HttpRequest) -> HttpResponse:
        """Generate humans.txt content programmatically."""
        context = self.get_context_data(request)
        lines: list[str] = [
            "# humanstxt.org/",
            "# The humans responsible for this site",
            "",
            "/* TEAM */",
            "",
        ]

        # Team members
        if context["team"]:
            for member in context["team"]:
                role = member.get("role", "Team Member")
                name = member.get("name", "")
                lines.append(f"    {role}: {name}")
                if member.get("site"):
                    lines.append(f"    Site: {member['site']}")
                if member.get("email"):
                    lines.append(f"    Email: {member['email']}")
                if member.get("twitter"):
                    lines.append(f"    Twitter: {member['twitter']}")
                if member.get("location"):
                    lines.append(f"    Location: {member['location']}")
                lines.append("")
        else:
            lines.append(f"    Site: {context['site_url']}")
            lines.append("")

        # Thanks section
        lines.append("/* THANKS */")
        lines.append("")
        if context["thanks"]:
            for person in context["thanks"]:
                name = person.get("name", person) if isinstance(person, dict) else person
                note = person.get("note", "") if isinstance(person, dict) else ""
                if note:
                    lines.append(f"    {name} - {note}")
                else:
                    lines.append(f"    {name}")
            lines.append("")
        else:
            lines.append("    Our users and community")
            lines.append("    Open source contributors")
            lines.append("")

        # Site section
        lines.append("/* SITE */")
        lines.append("")
        lines.append(f"    Last Update: {context['current_year']}/{context['current_month']:02d}/{context['current_day']:02d}")
        lines.append(f"    Language: {context['language']}")
        if context["standards"]:
            lines.append(f"    Standards: {', '.join(context['standards'])}")
        if context["software"]:
            lines.append(f"    Software: {', '.join(context['software'])}")

        content = "\n".join(lines)
        return HttpResponse(content, content_type=self.content_type)


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = ["HumansView"]
