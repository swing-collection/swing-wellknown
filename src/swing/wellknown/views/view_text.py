# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Text Template View Class.

Loads configuration from database when available, with fallback to JSON files.
"""


# =============================================================================
# Import
# =============================================================================

# Import | Standard Library
from typing import Any

# Import | Libraries
from django.views.generic.base import TemplateView

# Import | Local Modules
from .load_from_database import _load_from_database
from .build_context_from_database import _build_context_from_database
from .build_context_from_json import _build_context_from_json


# =============================================================================
# Classes
# =============================================================================

class TextView(TemplateView):
    """
    Text Template View Class.

    Loads configuration from database when available,
    with automatic fallback to JSON files.
    """

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """
        Returns context with data loaded from database or JSON files.

        Priority:
        1. Database (if models exist and have data)
        2. JSON files (fallback)
        """
        context = super().get_context_data(**kwargs)

        # Try database first
        db_data = _load_from_database()

        if db_data:
            # Load from database
            data_context = _build_context_from_database(db_data)
        else:
            # Fallback to JSON files
            data_context = _build_context_from_json()

        context.update(data_context)
        return context


# =============================================================================
# Variables | Export
# =============================================================================

text_view = TextView.as_view
# Export
# =============================================================================

__all__: list[str] = ["text_view",]
