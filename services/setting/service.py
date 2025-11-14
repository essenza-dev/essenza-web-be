from typing import Tuple
from django.db.models.manager import BaseManager
from django.utils.text import slugify

from core.service import BaseService
from core.models import Setting


class SettingService(BaseService):
    """
    Service class for managing application settings
    """

    def create_setting(self, **setting_data) -> Tuple[Setting, Exception | None]:
        """
        Create a new application settings
        """
        slug = setting_data.get("slug") or slugify(setting_data.get("label", ""))
        setting_data["slug"] = slug

        if Setting.objects.filter(slug=slug).exists():
            return Setting(), Exception(f"Setting with slug '{slug}' already exists.")

        return Setting.objects.create(**setting_data), None

    def get_all_settings(self) -> BaseManager[Setting]:
        """
        Retrieve all application settings
        """
        return Setting.objects.all()

    def get_setting_by_slug(self, slug: str) -> Setting | None:
        """
        Retrieve a specific setting by its slug
        """
        try:
            return Setting.objects.get(slug=slug)
        except Setting.DoesNotExist:
            return None