"""

The **profiles.admin.py** file involves settings and configurations for the administration page, specific for the Profiles (Settings) models.

"""
from django.contrib import admin

from profiles.models import (
    Settings,
)

admin.site.register(Settings)