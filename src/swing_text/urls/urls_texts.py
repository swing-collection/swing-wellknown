# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Texts URL Config
========================

...

Todo:
-----

Links:
------

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library


# Import | Libraries
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.urls.resolvers import URLPattern, URLResolver
from django.utils.translation import gettext as _
from django.views.generic.base import RedirectView

# Import | Local Modules
from ..views import text_view

# =============================================================================
# Variables
# =============================================================================

# Export
__all__: list[str] = ["app_name", "urlpatterns"]

# App Name
app_name = "texts"

# Views
favicon_view = RedirectView.as_view(
    url=staticfiles_storage.url("favicon/favicon.ico")
)

# URL Patterns
urlpatterns: list[URLPattern | URLResolver] = [

    path(
        "business.txt",
        text_view(
            template_name   = "business.txt.jinja",
            content_type    = "text/plain",
        ),
        name = "business"
    ),

    path(
        "copyright.txt",
        text_view(
            template_name   = "copyright.txt.jinja",
            content_type    = "text/plain",
        ),
        name = "copyright"
    ),


    path(
        "robots.txt",
        text_view(
            template_name   = "robots.txt.jinja",
            content_type    = "text/plain",
        ),
        name = "robots"
    ),
    path(
        "humans.txt",
        text_view(
            template_name   = "humans.txt.jinja",
            content_type    = "text/plain",
        ),
        name = "humans"
    ),
    path(
        "hackers.txt",
        text_view(
            template_name   = "hackers.txt.jinja",
            content_type    = "text/plain",
        ),
        name = "hackers"
    ),
    # path(
    #     "security.txt",
    #     text_view(
    #         template_name   = "security.txt",
    #         content_type    = "text/plain",
    #     ),
    #     name = "security"
    # ),
    path(
        ".well-known/security.txt",
        text_view(
            template_name   = "security.txt.jinja",
            content_type    = "text/plain",
        ),
        name = "security"  # check
    ),
    path(
        "pgp-key.txt",
        text_view(
            template_name   = "pgp-key.txt.jinja",
            content_type    = "text/plain",
        ),
        name = "pgp-key"
    ),
    path(
        "license.txt",
        text_view(
            template_name   = "license.txt.jinja",
            content_type    = "text/plain",
        ),
        name = "license"
    ),

    # Ads & Trust
    path(
        "ads.txt",
        text_view(
            template_name   = "ads.txt.jinja",
            content_type    = "text/plain",
        ),
        name = "ads"
    ),
    path(
        "trust.txt",
        text_view(
            template_name   = "trust.txt.jinja",
            content_type    = "text/plain",
        ),
        name = "trust"
    ),
    path(
        "earth.txt",
        text_view(
            template_name   = "earth.txt.jinja",
            content_type    = "text/plain",
        ),
        name = "earth"
    ),

    # Contact formats
    path(
        "contact.vcard",
        text_view(
            template_name   = "contact.vcard.jinja",
            content_type    = "text/vcard",
        ),
        name = "contact-vcard"
    ),
    path(
        "contact.ldif",
        text_view(
            template_name   = "contact.ldif.jinja",
            content_type    = "text/plain",
        ),
        name = "contact-ldif"
    ),

    # Web manifests
    path(
        "manifest.webmanifest",
        text_view(
            template_name   = "manifest.webmanifest",
            content_type    = "application/manifest+json",
        ),
        name = "manifest"
    ),
    path(
        "manifest.json",
        text_view(
            template_name   = "manifest.webmanifest",
            content_type    = "application/manifest+json",
        ),
        name = "manifest-json"
    ),
    path(
        "browserconfig.xml",
        text_view(
            template_name   = "browserconfig.xml",
            content_type    = "application/xml",
        ),
        name = "browserconfig"
    ),
    path(
        "favicon.ico",
        favicon_view,
        name = "favicon")
]
