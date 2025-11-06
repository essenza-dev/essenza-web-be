from django.db import models
from core.enums import MenuPosition
from core.models._base import TimeStampedModel


class Menu(TimeStampedModel):
    id = models.AutoField(primary_key=True, editable=False)
    name: models.CharField = models.CharField(max_length=100)
    position: models.CharField = models.CharField(
        max_length=20,
        choices=MenuPosition.choices,
        default=MenuPosition.HEADER
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        db_table: str = "menus"

    def __str__(self) -> str:
        return f"{self.id}: {self.name}"


class MenuItem(TimeStampedModel):
    id = models.AutoField(primary_key=True, editable=False)
    menu: models.ForeignKey = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='items'
    )
    lang: models.CharField = models.CharField(max_length=10, default='en')
    label: models.CharField = models.CharField(max_length=255)
    link: models.CharField = models.CharField(max_length=255)
    parent: models.ForeignKey = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    order_no: models.IntegerField = models.IntegerField(default=0)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: list[str] = ["order_no", "-created_at"]
        db_table: str = "menu_items"

    def __str__(self) -> str:
        return f"{self.id}: {self.label}"