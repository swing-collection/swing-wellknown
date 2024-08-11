# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Text Template View Class.

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
import json
from typing import Any, Dict, List

# Import | Libraries
from django.shortcuts import render
from django.views.generic.base import TemplateView

# Import | Local Modules
# from ..helpers import read_json


# =============================================================================
# Export
# =============================================================================

__all__: List[str] = ["text_view",]


# =============================================================================
# Classes
# =============================================================================

class TextView(TemplateView):
    """
    Text Template View Class
    """

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """
        Returns context.
        """
        context             = super().get_context_data(**kwargs)
        # context =         read_json()
        context["developer"]    = "Starling Associates"
        context["title"]    = "Hello!"
        context["content"]  = "Lorem ipsum dolor sit amet"
        return context


# =============================================================================
# Variables | Export
# =============================================================================

text_view = TextView.as_view
