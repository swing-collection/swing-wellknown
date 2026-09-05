# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for the URL pattern helper functions (swing.wellknown.urls.helpers).
"""

from swing.wellknown.urls.helpers import (
    ads_urlpatterns,
    ai_urlpatterns,
    humans_urlpatterns,
    llms_urlpatterns,
    robots_urlpatterns,
    security_urlpatterns,
    wellknown_urlpatterns,
)


def _names(patterns: list) -> list[str]:
    return [pattern.name for pattern in patterns]


class TestIndividualHelpers:
    """Tests for the single-file URL pattern helpers."""

    def test_robots_urlpatterns(self) -> None:
        """robots_urlpatterns() returns a single robots.txt pattern."""
        assert _names(robots_urlpatterns()) == ["robots"]

    def test_humans_urlpatterns(self) -> None:
        """humans_urlpatterns() returns a single humans.txt pattern."""
        assert _names(humans_urlpatterns()) == ["humans"]

    def test_security_urlpatterns(self) -> None:
        """security_urlpatterns() returns both security.txt locations."""
        assert _names(security_urlpatterns()) == [
            "security_wellknown",
            "security",
        ]

    def test_llms_urlpatterns(self) -> None:
        """llms_urlpatterns() returns a single llms.txt pattern."""
        assert _names(llms_urlpatterns()) == ["llms"]

    def test_ads_urlpatterns(self) -> None:
        """ads_urlpatterns() returns a single ads.txt pattern."""
        assert _names(ads_urlpatterns()) == ["ads"]

    def test_ai_urlpatterns(self) -> None:
        """ai_urlpatterns() returns both ai.txt locations."""
        assert _names(ai_urlpatterns()) == ["ai", "ai_wellknown"]


class TestWellknownUrlpatterns:
    """Tests for the combined wellknown_urlpatterns() helper."""

    def test_default_selection(self) -> None:
        """By default: robots, humans, security and llms are included."""
        names = _names(wellknown_urlpatterns())
        assert "robots" in names
        assert "humans" in names
        assert "security" in names
        assert "security_wellknown" in names
        assert "llms" in names
        # ads/ai are opt-in.
        assert "ads" not in names
        assert "ai" not in names

    def test_all_disabled(self) -> None:
        """Every pattern can be excluded."""
        patterns = wellknown_urlpatterns(
            include_robots=False,
            include_humans=False,
            include_security=False,
            include_llms=False,
            include_ads=False,
            include_ai=False,
        )
        assert patterns == []

    def test_ads_and_ai_are_opt_in(self) -> None:
        """ads.txt and ai.txt are only included when explicitly requested."""
        names = _names(
            wellknown_urlpatterns(
                include_robots=False,
                include_humans=False,
                include_security=False,
                include_llms=False,
                include_ads=True,
                include_ai=True,
            )
        )
        assert names == ["ads", "ai", "ai_wellknown"]
