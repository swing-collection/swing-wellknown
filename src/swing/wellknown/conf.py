# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Swing Well-Known - Configuration
==================================

Default settings and configuration helpers for the swing.wellknown app.

Configuration is read from Django settings using the `WELLKNOWN_CONFIG`
namespace.

Example settings::

    WELLKNOWN_CONFIG = {
        "site": {
            "name": "My Website",
            "url": "https://example.com",
            "email": "info@example.com",
            "security_email": "security@example.com",
        },
        "robots": {
            "allow_all": True,
            "disallow_paths": ["/admin/", "/api/"],
            "crawl_delay": 1,
            "ai_crawlers": {
                "GPTBot": False,
                "anthropic-ai": False,
            },
        },
        "security": {
            "contact": ["mailto:security@example.com"],
            "expires": "2027-12-31T23:59:59.000Z",
            "preferred_languages": ["en"],
        },
        "humans": {
            "team": [{"role": "Developer", "name": "Jane Doe"}],
            "standards": ["HTML5", "CSS3", "Python"],
        },
        "llms": {
            "title": "My Website",
            "summary": "A brief description.",
            "permissions": ["Summarize content"],
            "restrictions": ["Do not use for training"],
        },
    }

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from typing import Any

# Import | Django
from django.conf import settings


# =============================================================================
# Default Settings
# =============================================================================

DEFAULT_WELLKNOWN_CONFIG: dict[str, dict[str, Any]] = {
    "site": {
        "name": "",
        "url": "",
        "email": "",
        "security_email": "",
    },
    "robots": {
        "allow_all": True,
        "disallow_paths": [
            "/admin/",
            "/api/",
            "/auth/",
            "/accounts/",
            "/dashboard/",
            "/settings/",
            "/internal/",
        ],
        "allow_paths": ["/"],
        "crawl_delay": 1,
        "sitemaps": [],
        "ai_crawlers": {
            "GPTBot": False,
            "ChatGPT-User": False,
            "anthropic-ai": False,
            "Claude-Web": False,
            "CCBot": False,
            "Google-Extended": False,
            "FacebookBot": False,
            "cohere-ai": False,
            "Bytespider": False,
            "Applebot-Extended": False,
        },
    },
    "security": {
        "contact": [],
        "expires": "",  # Will be computed dynamically
        "preferred_languages": ["en"],
        "canonical": [],
        "encryption": None,
        "acknowledgments": None,
        "policy": None,
        "hiring": None,
        "csaf": None,
    },
    "humans": {
        "team": [],
        "thanks": [],
        "standards": ["HTML5", "CSS3", "JavaScript"],
        "software": [],
        "language": "English",
    },
    "llms": {
        "title": "",
        "summary": "",
        "about": "",
        "api_endpoints": [],
        "capabilities": [],
        "usage_guidelines": "",
        "permissions": [],
        "restrictions": [],
        "contact": "",
        "social": [],
    },
    "ads": {
        "sellers": [],
        "contact": None,
        "subdomain": None,
    },
    "ai": {
        "allow_training": False,
        "allow_summarization": True,
        "allow_indexing": True,
        "attribution_required": True,
        "contact": None,
        "rules": [],
    },
}


# =============================================================================
# Configuration Functions
# =============================================================================


def get_wellknown_config() -> dict[str, dict[str, Any]]:
    """
    Get the complete well-known configuration.

    Merges user settings with defaults.

    Returns:
        Complete configuration dictionary.

    """
    user_config = getattr(settings, "WELLKNOWN_CONFIG", {})
    merged_config: dict[str, dict[str, Any]] = {}

    # Merge each section
    for section, defaults in DEFAULT_WELLKNOWN_CONFIG.items():
        section_config = user_config.get(section, {})
        merged_config[section] = {**defaults, **section_config}

    return merged_config


def get_config(
    file_type: str,
    key: str | None = None,
    default: Any = None,
) -> Any:
    """
    Get configuration for a specific file type.

    Args:
        file_type: The file type (e.g., "robots", "security").
        key: Optional specific key to retrieve.
        default: Default value if not found.

    Returns:
        Configuration value or section dictionary.

    """
    config = get_wellknown_config()
    section = config.get(file_type, {})

    if key is None:
        return section

    return section.get(key, default)


def get_site_config(key: str | None = None, default: Any = None) -> Any:
    """
    Get site-wide configuration.

    Args:
        key: Optional specific key to retrieve.
        default: Default value if not found.

    Returns:
        Site configuration value or dictionary.

    """
    return get_config("site", key, default)


# =============================================================================
# Exports
# =============================================================================

__all__: list[str] = [
    "DEFAULT_WELLKNOWN_CONFIG",
    "get_wellknown_config",
    "get_config",
    "get_site_config",
]
