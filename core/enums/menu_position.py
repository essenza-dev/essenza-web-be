from django.db import models


class MenuPosition(models.TextChoices):
    HEADER = "header", "Header"
    FOOTER = "footer", "Footer"
    SIDEBAR = "sidebar", "Sidebar"
