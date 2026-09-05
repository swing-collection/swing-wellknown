# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""Admin for security policy."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models import SecurityPolicy


@admin.register(SecurityPolicy)
class SecurityPolicyAdmin(admin.ModelAdmin):
    """Admin for security policy singleton."""

    fieldsets = (
        (_("Contact"), {
            "fields": ("contact_email", "contact_url"),
            "description": _("How to report security vulnerabilities"),
        }),
        (_("Security Information"), {
            "fields": (
                "encryption_key_url",
                "policy_url",
                "acknowledgments_url",
                "hiring_url",
            ),
        }),
        (_("Settings"), {
            "fields": ("preferred_languages", "expires_date"),
        }),
    )

    def has_add_permission(self, request):
        """Only allow one instance."""
        return not SecurityPolicy.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of singleton."""
        return False

    def changelist_view(self, request, extra_context=None):
        """Redirect to change view if instance exists."""
        obj = SecurityPolicy.objects.first()
        if obj is not None:
            from django.shortcuts import redirect
            return redirect("admin:wellknown_securitypolicy_change", obj.pk)
        return super().changelist_view(request, extra_context)
