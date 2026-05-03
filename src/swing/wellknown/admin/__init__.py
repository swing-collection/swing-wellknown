# -*- coding: utf-8 -*-

"""
Django admin configuration for wellknown app.

Provides admin interfaces for managing site configuration,
locations, social accounts, and editable templates.
"""

# Import all admin classes to register them
from .location_inline import LocationInline
from .social_account_inline import SocialAccountInline
from .site_configuration import SiteConfigurationAdmin
from .location import LocationAdmin
from .social_account import SocialAccountAdmin
from .site_meta import SiteMetaAdmin
from .wellknown_template import WellKnownTemplateAdmin
from .security_policy import SecurityPolicyAdmin
from .robots_rule import RobotsRuleAdmin
from .sitemap import SitemapAdmin

__all__ = [
    "LocationInline",
    "SocialAccountInline",
    "SiteConfigurationAdmin",
    "LocationAdmin",
    "SocialAccountAdmin",
    "SiteMetaAdmin",
    "WellKnownTemplateAdmin",
    "SecurityPolicyAdmin",
    "RobotsRuleAdmin",
    "SitemapAdmin",
]
