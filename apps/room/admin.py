from django.contrib import admin
from django.contrib.admin import (
    ModelAdmin,
    TabularInline
)
from apps.room.models import (
    Room,
    Order
)


class OrderInline(TabularInline):
    model = Order


@admin.register(Order)
class OrderModelAdmin(ModelAdmin):
    list_display = ('room', 'is_active')


@admin.register(Room)
class RoomModelAdmin(ModelAdmin):
    inlines = (OrderInline,)
    list_display = ('name', 'type')
