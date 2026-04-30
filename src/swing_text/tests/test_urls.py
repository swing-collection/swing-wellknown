# -*- coding: utf-8 -*-

"""
Tests for URL configuration.
"""

from django.urls import resolve, reverse


class TestURLPatterns:
    """Tests for URL patterns resolution."""

    def test_robots_url_resolves(self) -> None:
        """Test robots.txt URL resolves correctly."""
        resolver = resolve("/robots.txt")
        assert resolver.url_name == "robots"

    def test_humans_url_resolves(self) -> None:
        """Test humans.txt URL resolves correctly."""
        resolver = resolve("/humans.txt")
        assert resolver.url_name == "humans"

    def test_security_url_resolves(self) -> None:
        """Test security.txt URL resolves correctly."""
        resolver = resolve("/.well-known/security.txt")
        assert resolver.url_name == "security"

    def test_business_url_resolves(self) -> None:
        """Test business.txt URL resolves correctly."""
        resolver = resolve("/business.txt")
        assert resolver.url_name == "business"

    def test_copyright_url_resolves(self) -> None:
        """Test copyright.txt URL resolves correctly."""
        resolver = resolve("/copyright.txt")
        assert resolver.url_name == "copyright"

    def test_license_url_resolves(self) -> None:
        """Test license.txt URL resolves correctly."""
        resolver = resolve("/license.txt")
        assert resolver.url_name == "license"

    def test_pgp_key_url_resolves(self) -> None:
        """Test pgp-key.txt URL resolves correctly."""
        resolver = resolve("/pgp-key.txt")
        assert resolver.url_name == "pgp-key"

    def test_hackers_url_resolves(self) -> None:
        """Test hackers.txt URL resolves correctly."""
        resolver = resolve("/hackers.txt")
        assert resolver.url_name == "hackers"

    def test_ads_url_resolves(self) -> None:
        """Test ads.txt URL resolves correctly."""
        resolver = resolve("/ads.txt")
        assert resolver.url_name == "ads"

    def test_trust_url_resolves(self) -> None:
        """Test trust.txt URL resolves correctly."""
        resolver = resolve("/trust.txt")
        assert resolver.url_name == "trust"

    def test_earth_url_resolves(self) -> None:
        """Test earth.txt URL resolves correctly."""
        resolver = resolve("/earth.txt")
        assert resolver.url_name == "earth"

    def test_manifest_url_resolves(self) -> None:
        """Test manifest.webmanifest URL resolves correctly."""
        resolver = resolve("/manifest.webmanifest")
        assert resolver.url_name == "manifest"

    def test_manifest_json_url_resolves(self) -> None:
        """Test manifest.json URL resolves correctly."""
        resolver = resolve("/manifest.json")
        assert resolver.url_name == "manifest-json"

    def test_browserconfig_url_resolves(self) -> None:
        """Test browserconfig.xml URL resolves correctly."""
        resolver = resolve("/browserconfig.xml")
        assert resolver.url_name == "browserconfig"

    def test_contact_vcard_url_resolves(self) -> None:
        """Test contact.vcard URL resolves correctly."""
        resolver = resolve("/contact.vcard")
        assert resolver.url_name == "contact-vcard"

    def test_contact_ldif_url_resolves(self) -> None:
        """Test contact.ldif URL resolves correctly."""
        resolver = resolve("/contact.ldif")
        assert resolver.url_name == "contact-ldif"

    def test_favicon_url_resolves(self) -> None:
        """Test favicon.ico URL resolves correctly."""
        resolver = resolve("/favicon.ico")
        assert resolver.url_name == "favicon"


class TestReverseURLs:
    """Tests for reverse URL lookups."""

    def test_reverse_robots(self) -> None:
        """Test reverse lookup for robots URL."""
        url = reverse("texts:robots")
        assert url == "/robots.txt"

    def test_reverse_humans(self) -> None:
        """Test reverse lookup for humans URL."""
        url = reverse("texts:humans")
        assert url == "/humans.txt"

    def test_reverse_security(self) -> None:
        """Test reverse lookup for security URL."""
        url = reverse("texts:security")
        assert url == "/.well-known/security.txt"

    def test_reverse_manifest(self) -> None:
        """Test reverse lookup for manifest URL."""
        url = reverse("texts:manifest")
        assert url == "/manifest.webmanifest"

    def test_reverse_browserconfig(self) -> None:
        """Test reverse lookup for browserconfig URL."""
        url = reverse("texts:browserconfig")
        assert url == "/browserconfig.xml"

    def test_reverse_contact_vcard(self) -> None:
        """Test reverse lookup for contact-vcard URL."""
        url = reverse("texts:contact-vcard")
        assert url == "/contact.vcard"

    def test_reverse_contact_ldif(self) -> None:
        """Test reverse lookup for contact-ldif URL."""
        url = reverse("texts:contact-ldif")
        assert url == "/contact.ldif"

    def test_reverse_ads(self) -> None:
        """Test reverse lookup for ads URL."""
        url = reverse("texts:ads")
        assert url == "/ads.txt"

    def test_reverse_trust(self) -> None:
        """Test reverse lookup for trust URL."""
        url = reverse("texts:trust")
        assert url == "/trust.txt"

    def test_reverse_earth(self) -> None:
        """Test reverse lookup for earth URL."""
        url = reverse("texts:earth")
        assert url == "/earth.txt"


class TestURLNamespacing:
    """Tests for URL namespacing."""

    def test_app_namespace_is_texts(self) -> None:
        """Test that the app namespace is 'texts'."""
        resolver = resolve("/robots.txt")
        assert resolver.app_name == "texts"
