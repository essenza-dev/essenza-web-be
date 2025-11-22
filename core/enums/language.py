from django.db import models


class Language(models.TextChoices):
    EN = "en", "English"
    ID = "id", "Indonesian"
