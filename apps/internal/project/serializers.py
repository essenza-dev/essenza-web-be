from typing import List
from rest_framework import serializers
from django.conf import settings

from core.models import Project


class ProjectModelSerializer(serializers.ModelSerializer):
    """Serializer for Project model with gallery handling."""

    gallery = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"

    def get_gallery(self, obj: Project) -> List[str]:
        """Get gallery images with proper media URL prefix."""
        if obj.gallery and isinstance(obj.gallery, list):
            media_base = settings.FILE_UPLOAD_BASE_DIR.rstrip("/")
            return [
                f"/{path}" if path.startswith(media_base) else f"/{media_base}/{path}"
                for path in obj.gallery
            ]
        return []


class PostCreateProjectRequest(serializers.Serializer):
    """Serializer for creating a new project."""

    title = serializers.CharField(max_length=255)
    slug = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255, allow_blank=True, required=False)
    description = serializers.CharField(allow_blank=True, required=False)
    image = serializers.ImageField(required=False, allow_empty_file=True, use_url=False)
    gallery = serializers.ListField(
        child=serializers.ImageField(use_url=False), required=False, allow_empty=True
    )
    meta_title = serializers.CharField(max_length=255, allow_blank=True, required=False)
    meta_description = serializers.CharField(allow_blank=True, required=False)
    meta_keywords = serializers.CharField(allow_blank=True, required=False)
    is_active = serializers.BooleanField()


class PutUpdateProjectRequest(serializers.Serializer):
    """Serializer for updating an existing project."""

    title = serializers.CharField(max_length=255, required=False)
    slug = serializers.CharField(max_length=255, required=False)
    location = serializers.CharField(max_length=255, allow_blank=True, required=False)
    description = serializers.CharField(allow_blank=True, required=False)
    image = serializers.ImageField(required=False, allow_empty_file=True, use_url=False)
    gallery = serializers.ListField(
        child=serializers.ImageField(use_url=False), required=False, allow_empty=True
    )
    meta_title = serializers.CharField(max_length=255, allow_blank=True, required=False)
    meta_description = serializers.CharField(allow_blank=True, required=False)
    meta_keywords = serializers.CharField(allow_blank=True, required=False)
    is_active = serializers.BooleanField(required=False)


class PatchToggleProjectStatusRequest(serializers.Serializer):
    """Serializer for toggling project active status."""

    is_active = serializers.BooleanField()


class PostUploadProjectImageRequest(serializers.Serializer):
    """Serializer for uploading project main image."""

    image = serializers.ImageField(required=True, allow_empty_file=False, use_url=False)


class PostUploadProjectGalleryRequest(serializers.Serializer):
    """Serializer for uploading project gallery images."""

    gallery = serializers.ListField(
        child=serializers.ImageField(use_url=False), required=True, allow_empty=False
    )
