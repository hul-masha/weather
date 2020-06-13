from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.index.models import Weather


@admin.register(Weather)
class UserInfoAdminModel(ModelAdmin):
    ...
