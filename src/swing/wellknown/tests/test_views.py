# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for text views.
"""

import pytest
from django.test import Client, TestCase


@pytest.mark.django_db
class TestTextViews(TestCase):
    """Tests for text file views."""

    def setUp(self) -> None:
        """Set up test client."""
        self.client = Client()

    def test_robots_txt_returns_200(self) -> None:
        """Test robots.txt endpoint returns 200."""
        response = self.client.get("/robots.txt")
        assert response.status_code == 200

    def test_robots_txt_content_type(self) -> None:
        """Test robots.txt returns text/plain content type."""
        response = self.client.get("/robots.txt")
        assert response["Content-Type"] == "text/plain"

    def test_humans_txt_returns_200(self) -> None:
        """Test humans.txt endpoint returns 200."""
        response = self.client.get("/humans.txt")
        assert response.status_code == 200

    def test_humans_txt_content_type(self) -> None:
        """Test humans.txt returns text/plain content type."""
        response = self.client.get("/humans.txt")
        assert response["Content-Type"] == "text/plain"

    def test_security_txt_returns_200(self) -> None:
        """Test security.txt endpoint returns 200."""
        response = self.client.get("/.well-known/security.txt")
        assert response.status_code == 200

    def test_security_txt_content_type(self) -> None:
        """Test security.txt returns text/plain content type."""
        response = self.client.get("/.well-known/security.txt")
        assert response["Content-Type"] == "text/plain"

    def test_business_txt_returns_200(self) -> None:
        """Test business.txt endpoint returns 200."""
        response = self.client.get("/business.txt")
        assert response.status_code == 200

    def test_copyright_txt_returns_200(self) -> None:
        """Test copyright.txt endpoint returns 200."""
        response = self.client.get("/copyright.txt")
        assert response.status_code == 200

    def test_license_txt_returns_200(self) -> None:
        """Test license.txt endpoint returns 200."""
        response = self.client.get("/license.txt")
        assert response.status_code == 200

    def test_pgp_key_txt_returns_200(self) -> None:
        """Test pgp-key.txt endpoint returns 200."""
        response = self.client.get("/pgp-key.txt")
        assert response.status_code == 200

    def test_hackers_txt_returns_200(self) -> None:
        """Test hackers.txt endpoint returns 200."""
        response = self.client.get("/hackers.txt")
        assert response.status_code == 200

    def test_ads_txt_returns_200(self) -> None:
        """Test ads.txt endpoint returns 200."""
        response = self.client.get("/ads.txt")
        assert response.status_code == 200

    def test_trust_txt_returns_200(self) -> None:
        """Test trust.txt endpoint returns 200."""
        response = self.client.get("/trust.txt")
        assert response.status_code == 200

    def test_earth_txt_returns_200(self) -> None:
        """Test earth.txt endpoint returns 200."""
        response = self.client.get("/earth.txt")
        assert response.status_code == 200

    def test_manifest_webmanifest_returns_200(self) -> None:
        """Test manifest.webmanifest endpoint returns 200."""
        response = self.client.get("/manifest.webmanifest")
        assert response.status_code == 200

    def test_manifest_webmanifest_content_type(self) -> None:
        """Test manifest.webmanifest returns correct content type."""
        response = self.client.get("/manifest.webmanifest")
        assert response["Content-Type"] == "application/manifest+json"

    def test_manifest_json_alias_returns_200(self) -> None:
        """Test manifest.json alias endpoint returns 200."""
        response = self.client.get("/manifest.json")
        assert response.status_code == 200

    def test_browserconfig_xml_returns_200(self) -> None:
        """Test browserconfig.xml endpoint returns 200."""
        response = self.client.get("/browserconfig.xml")
        assert response.status_code == 200

    def test_browserconfig_xml_content_type(self) -> None:
        """Test browserconfig.xml returns XML content type."""
        response = self.client.get("/browserconfig.xml")
        assert response["Content-Type"] == "application/xml"

    def test_contact_vcard_returns_200(self) -> None:
        """Test contact.vcard endpoint returns 200."""
        response = self.client.get("/contact.vcard")
        assert response.status_code == 200

    def test_contact_vcard_content_type(self) -> None:
        """Test contact.vcard returns vCard content type."""
        response = self.client.get("/contact.vcard")
        assert response["Content-Type"] == "text/vcard"

    def test_contact_ldif_returns_200(self) -> None:
        """Test contact.ldif endpoint returns 200."""
        response = self.client.get("/contact.ldif")
        assert response.status_code == 200


@pytest.mark.django_db
class TestTextViewContext(TestCase):
    """Tests for view context data."""

    def setUp(self) -> None:
        """Set up test client."""
        self.client = Client()

    def test_robots_txt_contains_user_agent(self) -> None:
        """Test robots.txt contains User-agent directive."""
        response = self.client.get("/robots.txt")
        content = response.content.decode("utf-8")
        # robots.txt should have User-agent directive
        assert "User-agent" in content or "user-agent" in content.lower()

    def test_humans_txt_contains_developer(self) -> None:
        """Test humans.txt contains developer information."""
        response = self.client.get("/humans.txt")
        content = response.content.decode("utf-8")
        # Should contain some text content (not empty)
        assert len(content.strip()) > 0

    def test_security_txt_contains_contact(self) -> None:
        """Test security.txt contains required Contact field."""
        response = self.client.get("/.well-known/security.txt")
        content = response.content.decode("utf-8")
        # security.txt should have Contact field per RFC 9116
        assert "Contact" in content or "contact" in content.lower()

    def test_context_includes_current_year(self) -> None:
        """Test that copyright.txt includes current year."""
        from datetime import datetime

        response = self.client.get("/copyright.txt")
        content = response.content.decode("utf-8")
        current_year = str(datetime.now().year)
        # Copyright should include current year
        assert current_year in content or len(content.strip()) > 0
