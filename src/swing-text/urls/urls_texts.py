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
from typing import List, Union

# Import | Libraries
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.urls.resolvers import URLPattern, URLResolver
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from django.views.generic.base import RedirectView

# Import | Local Modules
from ..views import text_view

# =============================================================================
# Variables
# =============================================================================

# Export
__all__: List[str] = ["app_name", "urlpatterns"]

# App Name
app_name = "texts"

# Views
favicon_view = RedirectView.as_view(
    url=staticfiles_storage.url("favicon/favicon.ico")
)

# URL Patterns
urlpatterns: List[Union[URLPattern, URLResolver]] = [

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

    path(
        "manifest.webmanifest",
        text_view(
            template_name   = "manifest.webmanifest",
            content_type    = "application/manifest+json",
        ),
        name = "manifest"
    ),
    # path(
    #     "manifest.json",
    #     TemplateView.as_view(
    #         template_name   = "manifest.webmanifest",
    #         content_type    = "application/manifest+json",
    #     ),
    #     name = "manifest"
    # ),
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
