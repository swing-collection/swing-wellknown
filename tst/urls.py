"""Minimal URLConf for test Django project."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("swing_text.urls.urls_texts")),
]
