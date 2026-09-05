# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Singleton model base class."""

# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from typing import Any, ClassVar, TypeVar, cast

# Import | Django
from django.core.cache import cache
from django.db import models

T = TypeVar("T", bound="SingletonModel")


# =============================================================================
# Classes
# =============================================================================


class SingletonModel(models.Model):
    """
    Abstract base class for singleton models.
    Ensures only one instance exists.
    """

    # Declared explicitly so mypy/django-stubs can see a manager on this
    # abstract base (the plugin does not synthesize `objects` for abstract
    # models). Concrete subclasses get their own manager as usual.
    objects: ClassVar[models.Manager[SingletonModel]] = models.Manager()

    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.pk = 1
        super().save(*args, **kwargs)
        self.clear_cache()

    def delete(self, *args: Any, **kwargs: Any) -> tuple[int, dict[str, int]]:
        # Prevent deletion; report "nothing deleted" using the same
        # (count, {label: count}) shape as Model.delete().
        return (0, {})

    @classmethod
    def load(cls: type[T]) -> T:
        """Load the singleton instance, creating if necessary."""
        obj, _ = cls.objects.get_or_create(pk=1)
        # `objects` is declared on this abstract base as `Manager[SingletonModel]`,
        # but at runtime each concrete subclass has its own manager bound to
        # that subclass, so the returned instance is actually a `T`.
        return cast(T, obj)

    def clear_cache(self) -> None:
        """Clear cached data when model changes."""
        cache.delete(f"wellknown_{self.__class__.__name__.lower()}")
