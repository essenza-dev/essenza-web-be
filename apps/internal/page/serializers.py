from rest_framework import serializers

from core.models import Page

# Constants
TEXTAREA_TEMPLATE = "textarea.html"


class PageModelSerializer(serializers.ModelSerializer):
    """Serializer for Page model."""

    class Meta:
        model = Page
        fields = "__all__"


class PostCreatePageRequest(serializers.Serializer):
    """Serializer for creating a new page."""

    slug = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text="URL slug for the page. If empty, will be generated from title.",
    )
    title = serializers.CharField(
        max_length=255,
        required=True,
        help_text="Title of the page.",
    )
    content = serializers.CharField(
        required=True,
        help_text="HTML content of the page.",
        style={"base_template": TEXTAREA_TEMPLATE, "rows": 10},
    )
    meta_title = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text="Meta title for SEO purposes.",
    )
    meta_description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Meta description for SEO purposes.",
        style={"base_template": TEXTAREA_TEMPLATE, "rows": 3},
    )
    meta_keywords = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Meta keywords for SEO purposes.",
        style={"base_template": TEXTAREA_TEMPLATE, "rows": 2},
    )
    template = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text="Template name to use for rendering this page.",
    )
    is_active = serializers.BooleanField(
        required=False,
        help_text="Whether the page is active and visible to public.",
    )


class PutUpdatePageRequest(serializers.Serializer):
    """Serializer for updating an existing page."""

    slug = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text="URL slug for the page. If empty, will be generated from title.",
    )
    title = serializers.CharField(
        max_length=255,
        required=False,
        help_text="Title of the page.",
    )
    content = serializers.CharField(
        required=False,
        help_text="HTML content of the page.",
        style={"base_template": TEXTAREA_TEMPLATE, "rows": 10},
    )
    meta_title = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text="Meta title for SEO purposes.",
    )
    meta_description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Meta description for SEO purposes.",
        style={"base_template": TEXTAREA_TEMPLATE, "rows": 3},
    )
    meta_keywords = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Meta keywords for SEO purposes.",
        style={"base_template": TEXTAREA_TEMPLATE, "rows": 2},
    )
    template = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text="Template name to use for rendering this page.",
    )
    is_active = serializers.BooleanField(
        required=False,
        help_text="Whether the page is active and visible to public.",
    )


class PatchTogglePageStatusRequest(serializers.Serializer):
    """Serializer for toggling page active status."""

    is_active = serializers.BooleanField(
        required=True,
        help_text="Whether the page should be active or inactive.",
    )
