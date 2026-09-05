# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for the class-based well-known views added in swing.wellknown.views
(RobotsView, HumansView, SecurityView, LlmsView, AdsView, AiView) and their
shared BaseWellKnownView.

These views are not wired into `tst.urls` (which exercises the legacy
`urls_texts` module instead), so they are exercised directly here via
Django's RequestFactory rather than through URL resolution.
"""

from typing import cast

from django.http import HttpResponse
from django.test import RequestFactory, TestCase, override_settings
from django.views import View

from swing.wellknown.views import (
    AdsView,
    AiView,
    HumansView,
    LlmsView,
    RobotsView,
    SecurityView,
)


def _get(view_cls: type[View], path: str) -> HttpResponse:
    """GET `path` through `view_cls` and return it typed as `HttpResponse`.

    `View.as_view()` is typed to return the broader `HttpResponseBase`
    (which has no `.content`); every well-known view always returns a
    concrete `HttpResponse`, so this cast reflects that at the type level.
    """
    request = RequestFactory().get(path)
    return cast(HttpResponse, view_cls.as_view()(request))


class TestRobotsView(TestCase):
    """Tests for RobotsView."""

    def test_returns_200_and_text_plain(self) -> None:
        response = _get(RobotsView, "/robots.txt")
        assert response.status_code == 200
        assert response["Content-Type"] == "text/plain; charset=utf-8"

    def test_default_disallows_when_debug(self) -> None:
        """DEBUG=True in the test settings and no explicit config: default
        `allow_all` is `not DEBUG`, so crawling should be disallowed."""
        response = _get(RobotsView, "/robots.txt")
        content = response.content.decode("utf-8")
        assert "Disallow: /" in content

    @override_settings(
        WELLKNOWN_CONFIG={
            "robots": {
                "allow_all": True,
                "disallow_paths": ["/private/"],
                "sitemaps": ["https://example.com/custom-sitemap.xml"],
            }
        }
    )
    def test_respects_config_overrides(self) -> None:
        response = _get(RobotsView, "/robots.txt")
        content = response.content.decode("utf-8")
        assert "Allow: /" in content
        assert "Disallow: /private/" in content
        assert "Sitemap: https://example.com/custom-sitemap.xml" in content

    def test_ai_crawlers_listed(self) -> None:
        response = _get(RobotsView, "/robots.txt")
        content = response.content.decode("utf-8")
        assert "GPTBot" in content
        assert "anthropic-ai" in content


class TestHumansView(TestCase):
    """Tests for HumansView."""

    def test_returns_200_and_text_plain(self) -> None:
        response = _get(HumansView, "/humans.txt")
        assert response.status_code == 200
        assert response["Content-Type"] == "text/plain; charset=utf-8"
        assert len(response.content.strip()) > 0

    @override_settings(
        WELLKNOWN_CONFIG={
            "humans": {
                "team": [{"role": "Developer", "name": "Jane Doe"}],
                "standards": ["HTML5", "Django"],
            }
        }
    )
    def test_team_appears_in_content(self) -> None:
        response = _get(HumansView, "/humans.txt")
        content = response.content.decode("utf-8")
        assert "Jane Doe" in content


class TestSecurityView(TestCase):
    """Tests for SecurityView."""

    def test_returns_200_and_text_plain(self) -> None:
        response = _get(SecurityView, "/.well-known/security.txt")
        assert response.status_code == 200
        assert response["Content-Type"] == "text/plain; charset=utf-8"

    def test_contains_required_rfc9116_fields(self) -> None:
        response = _get(SecurityView, "/.well-known/security.txt")
        content = response.content.decode("utf-8")
        assert "Expires:" in content

    @override_settings(
        WELLKNOWN_CONFIG={
            "security": {"contact": ["mailto:security@example.com"]},
        }
    )
    def test_respects_explicit_contact(self) -> None:
        response = _get(SecurityView, "/.well-known/security.txt")
        content = response.content.decode("utf-8")
        assert "Contact: mailto:security@example.com" in content

    @override_settings(WELLKNOWN_CONFIG={"site": {"security_email": "sec@example.com"}})
    def test_falls_back_to_site_security_email(self) -> None:
        response = _get(SecurityView, "/.well-known/security.txt")
        content = response.content.decode("utf-8")
        assert "Contact: mailto:sec@example.com" in content


class TestLlmsView(TestCase):
    """Tests for LlmsView."""

    def test_returns_200_and_text_plain(self) -> None:
        response = _get(LlmsView, "/llms.txt")
        assert response.status_code == 200
        assert response["Content-Type"] == "text/plain; charset=utf-8"

    @override_settings(
        WELLKNOWN_CONFIG={
            "llms": {
                "title": "Acme Docs",
                "summary": "A brief description.",
                "permissions": ["Summarize content"],
            }
        }
    )
    def test_respects_config(self) -> None:
        response = _get(LlmsView, "/llms.txt")
        content = response.content.decode("utf-8")
        assert "Acme Docs" in content
        assert "A brief description." in content


class TestAdsView(TestCase):
    """Tests for AdsView (its template does not exist, so this also
    exercises the programmatic fallback generator used by every view)."""

    def test_returns_200_and_text_plain(self) -> None:
        response = _get(AdsView, "/ads.txt")
        assert response.status_code == 200
        assert response["Content-Type"] == "text/plain; charset=utf-8"

    @override_settings(
        WELLKNOWN_CONFIG={
            "ads": {
                "sellers": [
                    {
                        "domain": "example-exchange.com",
                        "account_id": "pub-0000000000",
                        "account_type": "DIRECT",
                    }
                ],
                "contact": "mailto:ads@example.com",
            }
        }
    )
    def test_lists_sellers_and_contact(self) -> None:
        response = _get(AdsView, "/ads.txt")
        content = response.content.decode("utf-8")
        assert "example-exchange.com, pub-0000000000, DIRECT" in content
        assert "CONTACT=mailto:ads@example.com" in content


class TestAiView(TestCase):
    """Tests for AiView (its template does not exist, so this also
    exercises the programmatic fallback generator used by every view)."""

    def test_returns_200_and_text_plain(self) -> None:
        response = _get(AiView, "/ai.txt")
        assert response.status_code == 200
        assert response["Content-Type"] == "text/plain; charset=utf-8"
        content = response.content.decode("utf-8")
        assert "Allow-Training: no" in content  # default is False

    @override_settings(WELLKNOWN_CONFIG={"ai": {"allow_training": True}})
    def test_respects_config(self) -> None:
        response = _get(AiView, "/ai.txt")
        content = response.content.decode("utf-8")
        assert "Allow-Training: yes" in content
