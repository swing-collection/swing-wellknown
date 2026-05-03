# -*- coding: utf-8 -*-

"""Singleton model base class."""

from django.db import models
from django.core.cache import cache


class SingletonModel(models.Model):
    """
    Abstract base class for singleton models.
    Ensures only one instance exists.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        self.clear_cache()

    def delete(self, *args, **kwargs):
        pass  # Prevent deletion

    @classmethod
    def load(cls):
        """Load the singleton instance, creating if necessary."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def clear_cache(self):
        """Clear cached data when model changes."""
        cache.delete(f"wellknown_{self.__class__.__name__.lower()}")
