"""
Brochure API Serializers
Contains all serializers for brochure-related API operations
"""

from rest_framework import serializers

from core.models import Brochure

# Constants
BROCHURE_FILE_HELP = "Brochure PDF file"
BROCHURE_TITLE_HELP = "Brochure title"
PDF_FILE_ERROR = "Only PDF files are allowed."
FILE_SIZE_ERROR = "File size must be less than 50MB."
TITLE_EMPTY_ERROR = "Title cannot be empty."
TITLE_LENGTH_ERROR = "Title must be at least 3 characters long."


class BrochureModelSerializer(serializers.ModelSerializer):
    """Serializer for Brochure model with file URL."""

    class Meta:
        model = Brochure
        read_only_fields = ["id", "created_at", "updated_at"]
        fields = ["id", "title", "file_url", "created_at", "updated_at"]


class PostCreateBrochureRequest(serializers.Serializer):
    """Serializer for creating a new brochure."""

    title = serializers.CharField(
        max_length=255,
        help_text=BROCHURE_TITLE_HELP,
    )
    file = serializers.FileField(
        required=False,
        allow_empty_file=False,
        use_url=False,
        help_text=BROCHURE_FILE_HELP,
    )

    def validate_title(self, value: str) -> str:
        """Validate brochure title format and basic requirements."""
        if not value or not value.strip():
            raise serializers.ValidationError(TITLE_EMPTY_ERROR)

        # Check for minimum length
        if len(value.strip()) < 3:
            raise serializers.ValidationError(TITLE_LENGTH_ERROR)

        return value.strip()

    def validate_file(self, value) -> serializers.FileField:
        """Validate brochure file."""
        if value:
            # Check file extension
            if not value.name.lower().endswith(".pdf"):
                raise serializers.ValidationError("Only PDF files are allowed.")

            # Check file size (50MB limit)
            max_size = 50 * 1024 * 1024  # 50MB in bytes
            if value.size > max_size:
                raise serializers.ValidationError("File size must be less than 50MB.")

        return value


class PutUpdateBrochureRequest(serializers.Serializer):
    """Serializer for updating an existing brochure."""

    title = serializers.CharField(
        max_length=255,
        required=False,
        help_text=BROCHURE_TITLE_HELP,
    )
    file = serializers.FileField(
        required=False,
        allow_empty_file=False,
        use_url=False,
        help_text=BROCHURE_FILE_HELP,
    )

    def validate_title(self, value: str) -> str:
        """Validate brochure title format and basic requirements."""
        if value is not None:
            if not value or not value.strip():
                raise serializers.ValidationError(TITLE_EMPTY_ERROR)

            # Check for minimum length
            if len(value.strip()) < 3:
                raise serializers.ValidationError(TITLE_LENGTH_ERROR)

            return value.strip()
        return value

    def validate_file(self, value) -> serializers.FileField:
        """Validate brochure file."""
        if value:
            # Check file extension
            if not value.name.lower().endswith(".pdf"):
                raise serializers.ValidationError(PDF_FILE_ERROR)

            # Check file size (50MB limit)
            max_size = 50 * 1024 * 1024  # 50MB in bytes
            if value.size > max_size:
                raise serializers.ValidationError(FILE_SIZE_ERROR)

        return value


class PostUploadBrochureFileRequest(serializers.Serializer):
    """Serializer for uploading a brochure file."""

    file = serializers.FileField(
        required=True,
        allow_empty_file=False,
        use_url=False,
        help_text=BROCHURE_FILE_HELP,
    )

    def validate_file(self, value) -> serializers.FileField:
        """Validate brochure file."""
        # Check file extension
        if not value.name.lower().endswith(".pdf"):
            raise serializers.ValidationError(PDF_FILE_ERROR)

        # Check file size (50MB limit)
        max_size = 50 * 1024 * 1024  # 50MB in bytes
        if value.size > max_size:
            raise serializers.ValidationError(FILE_SIZE_ERROR)

        return value


class BrochureFilterSerializer(serializers.Serializer):
    """Serializer for brochure filtering query parameters."""

    search = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Search term for filtering brochures by title",
    )
    page = serializers.IntegerField(
        required=False,
        min_value=1,
        help_text="Page number for pagination",
    )
    page_size = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=100,
        help_text="Number of items per page (max: 100)",
    )
