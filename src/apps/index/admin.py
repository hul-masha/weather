from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.index.models import Weather
from project.utils.xforms import gen_textinput_admin_form


@admin.register(Weather)
class UserInfoAdminModel(ModelAdmin):
    ...
