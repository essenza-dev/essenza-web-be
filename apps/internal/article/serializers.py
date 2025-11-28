from rest_framework import serializers

from core.models import Article

# Constants
TEXTAREA_TEMPLATE = "textarea.html"


class ArticleModelSerializer(serializers.ModelSerializer):
    """Serializer for Article model."""

    class Meta:
        model = Article
        fields = "__all__"


class PostCreateArticleRequest(serializers.Serializer):
    """Serializer for creating a new article."""

    slug = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text="URL slug for the article. If empty, will be generated from title.",
    )
    title = serializers.CharField(
        max_length=255,
        required=True,
        help_text="Title of the article.",
    )
    content = serializers.CharField(
        required=True,
        help_text="HTML content of the article.",
        style={"base_template": TEXTAREA_TEMPLATE, "rows": 15},
    )
    thumbnail = serializers.ImageField(
        required=False,
        allow_empty_file=True,
        use_url=False,
        help_text="Thumbnail image for the article.",
    )
    author = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text="Author name of the article. If empty, will be set from current user's name.",
    )
    tags = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text="Tags/categories separated by commas.",
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
    is_active = serializers.BooleanField(
        required=False,
        help_text="Whether the article is active and visible to public. When true, published_at is automatically set to current time.",
    )


class PutUpdateArticleRequest(serializers.Serializer):
    """Serializer for updating an existing article."""

    slug = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text="URL slug for the article. If empty, will be generated from title.",
    )
    title = serializers.CharField(
        max_length=255,
        required=False,
        help_text="Title of the article.",
    )
    content = serializers.CharField(
        required=False,
        help_text="HTML content of the article.",
        style={"base_template": TEXTAREA_TEMPLATE, "rows": 15},
    )
    thumbnail = serializers.ImageField(
        required=False,
        allow_empty_file=True,
        use_url=False,
        help_text="Thumbnail image for the article.",
    )
    author = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text="Author name of the article.",
    )
    tags = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text="Tags/categories separated by commas.",
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
    published_at = serializers.DateTimeField(
        required=False,
        allow_null=True,
        help_text="Publication date and time.",
    )
    is_active = serializers.BooleanField(
        required=False,
        help_text="Whether the article is active and visible to public. When true, published_at is automatically managed.",
    )


class PatchToggleArticleStatusRequest(serializers.Serializer):
    """Serializer for toggling article active status."""

    is_active = serializers.BooleanField(
        required=True,
        help_text="Whether the article should be active or inactive. This also manages the published_at field automatically.",
    )


class PatchPublishArticleRequest(serializers.Serializer):
    """Serializer for publishing/unpublishing an article."""

    published_at = serializers.DateTimeField(
        required=False,
        allow_null=True,
        help_text="Publication date and time. Use current time to publish, null to unpublish.",
    )
