# -*- coding: utf-8 -*-

"""
Django models for wellknown configuration.

Provides database-backed configuration for site settings,
locations, social accounts, and editable templates.
"""

from django.db import models
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _


# =============================================================================
# Abstract Models
# =============================================================================

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


# =============================================================================
# Configuration Models
# =============================================================================

class SiteConfiguration(SingletonModel):
    """
    Singleton model for site-wide configuration.
    Replaces _brand.json for brand/site settings.
    """

    # Brand names
    name_short = models.CharField(
        _("Short Name"),
        max_length=100,
        blank=True,
        help_text=_("Short brand name (e.g., 'Acme')")
    )
    name_long = models.CharField(
        _("Long Name"),
        max_length=255,
        blank=True,
        help_text=_("Full brand name (e.g., 'Acme Corporation')")
    )
    name_legal = models.CharField(
        _("Legal Name"),
        max_length=255,
        blank=True,
        help_text=_("Legal entity name (e.g., 'Acme Corp. Inc.')")
    )
    name_abbr = models.CharField(
        _("Abbreviation"),
        max_length=20,
        blank=True,
        help_text=_("Brand abbreviation (e.g., 'AC')")
    )

    # Contact info
    website_url = models.URLField(
        _("Website URL"),
        blank=True,
        help_text=_("Primary website URL")
    )
    email_main = models.EmailField(
        _("Main Email"),
        blank=True,
        help_text=_("Primary contact email")
    )
    email_support = models.EmailField(
        _("Support Email"),
        blank=True,
        help_text=_("Support/people email")
    )
    phone_main = models.CharField(
        _("Main Phone"),
        max_length=50,
        blank=True,
        help_text=_("Primary phone number")
    )

    # Description
    description = models.TextField(
        _("Description"),
        blank=True,
        help_text=_("Brief site/brand description")
    )
    keywords = models.TextField(
        _("Keywords"),
        blank=True,
        help_text=_("Comma-separated keywords for SEO")
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Site Configuration")
        verbose_name_plural = _("Site Configuration")

    def __str__(self):
        return self.name_long or self.name_short or "Site Configuration"

    def get_keywords_list(self):
        """Return keywords as a list."""
        if not self.keywords:
            return []
        return [k.strip() for k in self.keywords.split(",") if k.strip()]


class Location(models.Model):
    """
    Model for office/business locations.
    """

    name = models.CharField(
        _("Location Name"),
        max_length=255,
        help_text=_("e.g., 'Headquarters', 'Amsterdam Office'")
    )
    building = models.CharField(
        _("Building"),
        max_length=255,
        blank=True
    )
    street = models.CharField(
        _("Street"),
        max_length=255,
        blank=True
    )
    street_number = models.CharField(
        _("Street Number"),
        max_length=20,
        blank=True
    )
    postal_code = models.CharField(
        _("Postal Code"),
        max_length=20,
        blank=True
    )
    city = models.CharField(
        _("City"),
        max_length=100,
        blank=True
    )
    province = models.CharField(
        _("Province/State"),
        max_length=100,
        blank=True
    )
    country = models.CharField(
        _("Country"),
        max_length=100,
        blank=True
    )
    phone = models.CharField(
        _("Phone"),
        max_length=50,
        blank=True
    )
    email = models.EmailField(
        _("Email"),
        blank=True
    )
    google_map_url = models.URLField(
        _("Google Map URL"),
        blank=True,
        help_text=_("Embed URL for Google Maps")
    )
    is_primary = models.BooleanField(
        _("Primary Location"),
        default=False,
        help_text=_("Mark as primary/headquarters location")
    )
    order = models.PositiveIntegerField(
        _("Display Order"),
        default=0
    )

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def to_dict(self):
        """Convert to dictionary for template context."""
        return {
            "name": self.name,
            "building": self.building,
            "street": self.street,
            "street_number": self.street_number,
            "postal_code": self.postal_code,
            "city": self.city,
            "province": self.province,
            "country": self.country,
            "phone": self.phone,
            "email": self.email,
            "google_map": self.google_map_url,
        }


class SocialAccount(models.Model):
    """
    Model for social media accounts.
    """

    SERVICE_CHOICES = [
        ("500px", "500px"),
        ("angellist", "AngelList"),
        ("archinect", "Archinect"),
        ("behance", "Behance"),
        ("bluesky", "Bluesky"),
        ("crunchbase", "Crunchbase"),
        ("discord", "Discord"),
        ("dribbble", "Dribbble"),
        ("facebook", "Facebook"),
        ("figma", "Figma"),
        ("github", "GitHub"),
        ("gitlab", "GitLab"),
        ("instagram", "Instagram"),
        ("issuu", "Issuu"),
        ("linkedin", "LinkedIn"),
        ("mastodon", "Mastodon"),
        ("medium", "Medium"),
        ("pinterest", "Pinterest"),
        ("reddit", "Reddit"),
        ("slack", "Slack"),
        ("snapchat", "Snapchat"),
        ("spotify", "Spotify"),
        ("stackoverflow", "Stack Overflow"),
        ("telegram", "Telegram"),
        ("threads", "Threads"),
        ("tiktok", "TikTok"),
        ("tumblr", "Tumblr"),
        ("twitch", "Twitch"),
        ("twitter", "Twitter/X"),
        ("vimeo", "Vimeo"),
        ("whatsapp", "WhatsApp"),
        ("youtube", "YouTube"),
        ("other", "Other"),
    ]

    service = models.CharField(
        _("Service"),
        max_length=50,
        choices=SERVICE_CHOICES,
        help_text=_("Social media platform")
    )
    service_custom = models.CharField(
        _("Custom Service Name"),
        max_length=100,
        blank=True,
        help_text=_("If 'Other' selected, specify the service name")
    )
    profile_url = models.URLField(
        _("Profile URL"),
        help_text=_("Full URL to your profile")
    )
    username = models.CharField(
        _("Username"),
        max_length=100,
        blank=True,
        help_text=_("Your username/handle on this platform")
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Show this account in templates")
    )
    order = models.PositiveIntegerField(
        _("Display Order"),
        default=0
    )

    class Meta:
        verbose_name = _("Social Account")
        verbose_name_plural = _("Social Accounts")
        ordering = ["order", "service"]

    def __str__(self):
        service_name = self.get_service_name()
        return f"{service_name}: {self.username or self.profile_url}"

    def get_service_name(self):
        """Return the display name for the service."""
        if self.service == "other" and self.service_custom:
            return self.service_custom
        return self.get_service_display()


class SiteMeta(SingletonModel):
    """
    Singleton model for site metadata.
    Replaces _meta.json for standards, tags, etc.
    """

    # Site standards
    language = models.CharField(
        _("Language"),
        max_length=50,
        default="English"
    )
    standards = models.TextField(
        _("Web Standards"),
        blank=True,
        default="HTML5, CSS3, JavaScript",
        help_text=_("Comma-separated list of standards used")
    )
    components = models.TextField(
        _("Components/Frameworks"),
        blank=True,
        help_text=_("Comma-separated list of frameworks/libraries")
    )
    software = models.TextField(
        _("Software"),
        blank=True,
        help_text=_("Comma-separated list of software used")
    )

    # Analytics tags
    google_analytics_id = models.CharField(
        _("Google Analytics ID"),
        max_length=50,
        blank=True,
        help_text=_("e.g., UA-XXXXXXXX-X or G-XXXXXXXXXX")
    )
    google_search_console_token = models.CharField(
        _("Google Search Console Token"),
        max_length=100,
        blank=True
    )

    # Ads configuration
    google_adsense_id = models.CharField(
        _("Google AdSense Publisher ID"),
        max_length=50,
        blank=True,
        help_text=_("pub-XXXXXXXXXXXXXXXX")
    )
    ads_txt_content = models.TextField(
        _("ads.txt Content"),
        blank=True,
        help_text=_("Custom ads.txt entries")
    )

    class Meta:
        verbose_name = _("Site Metadata")
        verbose_name_plural = _("Site Metadata")

    def __str__(self):
        return "Site Metadata"

    def get_standards_list(self):
        """Return standards as a list."""
        if not self.standards:
            return []
        return [s.strip() for s in self.standards.split(",") if s.strip()]

    def get_components_list(self):
        """Return components as a list."""
        if not self.components:
            return []
        return [c.strip() for c in self.components.split(",") if c.strip()]

    def get_software_list(self):
        """Return software as a list."""
        if not self.software:
            return []
        return [s.strip() for s in self.software.split(",") if s.strip()]


# =============================================================================
# Template Models
# =============================================================================

class WellKnownTemplate(models.Model):
    """
    Model for editable wellknown templates.
    Allows live editing of template files via admin.
    """

    TEMPLATE_CHOICES = [
        ("robots.txt.jinja", "robots.txt"),
        ("humans.txt.jinja", "humans.txt"),
        ("security.txt.jinja", "security.txt"),
        ("ads.txt.jinja", "ads.txt"),
        ("business.txt.jinja", "business.txt"),
        ("copyright.txt.jinja", "copyright.txt"),
        ("license.txt.jinja", "license.txt"),
        ("hackers.txt.jinja", "hackers.txt"),
        ("pgp-key.txt.jinja", "pgp-key.txt"),
        ("trust.txt.jinja", "trust.txt"),
        ("earth.txt.jinja", "earth.txt"),
        ("llms.txt.jinja", "llms.txt"),
        ("ai.txt.jinja", "ai.txt"),
        ("privacy.txt.jinja", "privacy.txt"),
        ("dnt-policy.txt.jinja", "dnt-policy.txt"),
        ("acknowledgments.txt.jinja", "acknowledgments.txt"),
        ("contact.vcard.jinja", "contact.vcard"),
        ("contact.ldif.jinja", "contact.ldif"),
        ("manifest.webmanifest", "manifest.webmanifest"),
        ("browserconfig.xml", "browserconfig.xml"),
        ("gpc.json.jinja", "gpc.json"),
        ("funding.json.jinja", "funding.json"),
        ("apple-app-site-association.jinja", "apple-app-site-association"),
        ("assetlinks.json.jinja", "assetlinks.json"),
    ]

    name = models.CharField(
        _("Template Name"),
        max_length=100,
        unique=True,
        choices=TEMPLATE_CHOICES,
        help_text=_("Select the template to customize")
    )
    content = models.TextField(
        _("Template Content"),
        help_text=_("Jinja2 template content. Use {{ variable }} for dynamic content.")
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Use this custom template instead of the default")
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        help_text=_("Notes about this template")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Well-Known Template")
        verbose_name_plural = _("Well-Known Templates")
        ordering = ["name"]

    def __str__(self):
        return self.get_name_display()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f"wellknown_template_{self.name}")


# =============================================================================
# Security Models
# =============================================================================

class SecurityPolicy(SingletonModel):
    """
    Model for security.txt specific settings.
    """

    contact_email = models.EmailField(
        _("Security Contact Email"),
        blank=True
    )
    contact_url = models.URLField(
        _("Security Contact URL"),
        blank=True,
        help_text=_("URL for security reporting page")
    )
    encryption_key_url = models.URLField(
        _("PGP Key URL"),
        blank=True,
        help_text=_("URL to PGP public key")
    )
    acknowledgments_url = models.URLField(
        _("Acknowledgments URL"),
        blank=True,
        help_text=_("URL to security researcher acknowledgments")
    )
    policy_url = models.URLField(
        _("Security Policy URL"),
        blank=True
    )
    hiring_url = models.URLField(
        _("Security Hiring URL"),
        blank=True,
        help_text=_("URL to security job openings")
    )
    preferred_languages = models.CharField(
        _("Preferred Languages"),
        max_length=100,
        default="en",
        help_text=_("Comma-separated language codes")
    )
    expires_date = models.DateField(
        _("Expires Date"),
        blank=True,
        null=True,
        help_text=_("When this security.txt expires")
    )

    class Meta:
        verbose_name = _("Security Policy")
        verbose_name_plural = _("Security Policy")

    def __str__(self):
        return "Security Policy"

    def get_languages_list(self):
        """Return languages as a list."""
        if not self.preferred_languages:
            return ["en"]
        return [lang.strip() for lang in self.preferred_languages.split(",") if lang.strip()]


class RobotsRule(models.Model):
    """
    Model for robots.txt rules.
    """

    user_agent = models.CharField(
        _("User Agent"),
        max_length=100,
        default="*",
        help_text=_("User agent pattern (e.g., '*', 'Googlebot', 'GPTBot')")
    )
    rule_type = models.CharField(
        _("Rule Type"),
        max_length=10,
        choices=[
            ("allow", "Allow"),
            ("disallow", "Disallow"),
        ],
        default="disallow"
    )
    path = models.CharField(
        _("Path"),
        max_length=500,
        default="/",
        help_text=_("Path pattern to allow/disallow")
    )
    crawl_delay = models.PositiveIntegerField(
        _("Crawl Delay"),
        blank=True,
        null=True,
        help_text=_("Seconds between requests (optional)")
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True
    )
    order = models.PositiveIntegerField(
        _("Order"),
        default=0
    )

    class Meta:
        verbose_name = _("Robots Rule")
        verbose_name_plural = _("Robots Rules")
        ordering = ["order", "user_agent"]

    def __str__(self):
        return f"{self.user_agent}: {self.rule_type} {self.path}"


class Sitemap(models.Model):
    """
    Model for sitemap URLs in robots.txt.
    """

    url = models.URLField(
        _("Sitemap URL"),
        help_text=_("Full URL to sitemap")
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True
    )

    class Meta:
        verbose_name = _("Sitemap")
        verbose_name_plural = _("Sitemaps")

    def __str__(self):
        return self.url
