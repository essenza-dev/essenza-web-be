from django.db import models
from core.models._base import TimeStampedModel, FileUploadModel, upload_to


class Brochure(TimeStampedModel, FileUploadModel):
    id = models.AutoField(primary_key=True, editable=False)
    title: models.CharField = models.CharField(max_length=255)
    file: models.FileField = models.FileField(
        upload_to=upload_to("brochure"), blank=True
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        db_table: str = "brochures"

    def __str__(self) -> str:
        return f"{self.id}: {self.title}"

    @property
    def file_url(self) -> str | None:
        """Get the file URL for accessing the brochure file."""
        return self.file.url if self.file else None
