# -*- coding: utf-8 -*-

# =============================================================================
# Docstring
# =============================================================================

"""
Provides Texts Config Class
==========================
...

Todo:
-----

Links:
------

"""


# =============================================================================
# Import
# =============================================================================

# Import | Standard Library
from typing import Dict, List, Union


# Import | Libraries
from django.apps import AppConfig
# from django.core.signals import request_finished
from django.utils.translation import gettext_lazy as _

# Import | Local Modules


# =============================================================================
# Classes
# =============================================================================

class TextsConfig(AppConfig):
    """
    Texts Config Class
    =================
    """



    # Full Python path to the application
    name = "website.texts"

    # Short name for the application
    label = "texts"

    # Human-readable name for the application
    verbose_name = _("Texts")

    # Filesystem path to the application directory,
    # path = "/usr/lib/pythonX.Y/dist-packages/django/contrib/admin"

    # default = True

    # The implicit primary key type to add to models within this app.
    default_auto_field = "django.db.models.BigAutoField"

    # def ready(self):
    #     """
    #     Apps Config Ready Function
    #     """
        
        # Implicitly connect signal handlers decorated with @receiver.
        # from .. import signals

        # Explicitly connect a signal handler.
        # request_finished.connect(signals.my_callback)
