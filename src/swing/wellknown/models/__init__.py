# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Django models for wellknown configuration.

Provides database-backed configuration for site settings,
locations, social accounts, and editable templates.
"""

from .singleton import SingletonModel
from .site_configuration import SiteConfiguration
from .location import Location
from .social_account import SocialAccount
from .site_meta import SiteMeta
from .wellknown_template import WellKnownTemplate
from .security_policy import SecurityPolicy
from .robots_rule import RobotsRule
from .sitemap import Sitemap

__all__ = [
    "SingletonModel",
    "SiteConfiguration",
    "Location",
    "SocialAccount",
    "SiteMeta",
    "WellKnownTemplate",
    "SecurityPolicy",
    "RobotsRule",
    "Sitemap",
]
