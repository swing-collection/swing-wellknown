# -*- coding: utf-8 -*-

"""
Provides Jinja2 environment configuration.
"""

from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment


def environment(**options):
    """
    Create Jinja2 environment with Django integrations.
    """
    env = Environment(**options)
    env.globals.update({
        "static": static,
        "url": reverse,
    })
    return env
