# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Tests for the WELLKNOWN_CONFIG settings helpers (swing.wellknown.conf).
"""

from django.test import TestCase, override_settings

from swing.wellknown.conf import (
    DEFAULT_WELLKNOWN_CONFIG,
    get_config,
    get_site_config,
    get_wellknown_config,
)


class TestGetWellknownConfig(TestCase):
    """Tests for get_wellknown_config()."""

    def test_returns_defaults_when_unconfigured(self) -> None:
        """Without WELLKNOWN_CONFIG in settings, defaults are returned."""
        config = get_wellknown_config()
        assert config["robots"]["allow_all"] == DEFAULT_WELLKNOWN_CONFIG["robots"]["allow_all"]
        assert config["security"]["preferred_languages"] == ["en"]

    def test_includes_all_default_sections(self) -> None:
        """All default sections are present even when unconfigured."""
        config = get_wellknown_config()
        for section in DEFAULT_WELLKNOWN_CONFIG:
            assert section in config

    @override_settings(
        WELLKNOWN_CONFIG={
            "site": {"name": "Acme Example Company"},
            "robots": {"crawl_delay": 5},
        }
    )
    def test_merges_user_settings_over_defaults(self) -> None:
        """User settings override defaults per-key, per-section."""
        config = get_wellknown_config()
        assert config["site"]["name"] == "Acme Example Company"
        assert config["robots"]["crawl_delay"] == 5
        # Untouched keys in a partially-overridden section keep their default.
        assert config["robots"]["allow_all"] == DEFAULT_WELLKNOWN_CONFIG["robots"]["allow_all"]
        # Untouched sections keep their full default.
        assert config["llms"] == DEFAULT_WELLKNOWN_CONFIG["llms"]


class TestGetConfig(TestCase):
    """Tests for get_config()."""

    def test_returns_section_when_no_key(self) -> None:
        """Without a key, the whole section dict is returned."""
        section = get_config("security")
        assert section == get_wellknown_config()["security"]

    def test_returns_key_value(self) -> None:
        """A specific key within a section is returned."""
        assert get_config("robots", "crawl_delay") == 1

    def test_returns_default_for_missing_key(self) -> None:
        """Missing keys fall back to the provided default."""
        assert get_config("robots", "does-not-exist", "fallback") == "fallback"

    def test_returns_empty_dict_for_unknown_file_type(self) -> None:
        """An unknown file type yields an empty section."""
        assert get_config("does-not-exist") == {}


class TestGetSiteConfig(TestCase):
    """Tests for get_site_config()."""

    def test_returns_site_section(self) -> None:
        """Without a key, the whole site section is returned."""
        assert get_site_config() == get_wellknown_config()["site"]

    @override_settings(WELLKNOWN_CONFIG={"site": {"name": "Acme"}})
    def test_returns_specific_key(self) -> None:
        """A specific site key is returned."""
        assert get_site_config("name") == "Acme"

    def test_returns_default_for_missing_key(self) -> None:
        """Missing site keys fall back to the provided default."""
        assert get_site_config("does-not-exist", "fallback") == "fallback"
