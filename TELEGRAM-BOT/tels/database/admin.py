from django.contrib import admin

from .models import (RobotsInfo, RobotsData)

# Register your models here.
@admin.register(RobotsInfo)
class RobotsInfoAdmin(admin.ModelAdmin):
    list_display = [
        'bot_id', 'latitude', 'longitude',
        'yaw', 'pitch',
        'movement_direction',
        'task',
        'battery_capacity', 'battery_durability',
        'light_state',
        'status'
    ]

@admin.register(RobotsData)
class RobotsDataAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']