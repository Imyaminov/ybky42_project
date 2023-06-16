from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.common.models import User


@admin.register(User)
class UserModelAdmin(ModelAdmin):
    list_display = ('username', 'id')
    exclude = ('last_login', 'first_name', 'last_name')