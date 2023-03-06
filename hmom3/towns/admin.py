from django.contrib import admin
from . import models


class FractionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'bonus', 'description', 'image')


class ResourcesAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'gold_amount',
        'wood_amount',
        'stone_amount',
        'updated_time'
    )


class BuildingsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'fraction',
        'image',
        'top',
        'left'
    )


class BuildingsCostAdmin(admin.ModelAdmin):
    list_display = (
        'building',
        'gold',
        'wood',
        'stone',
    )


class BuildingsCompletedAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'building',
        'level',
    )


admin.site.register(models.Fractions, FractionAdmin)
admin.site.register(models.Resources, ResourcesAdmin)
admin.site.register(models.Buildings, BuildingsAdmin)
admin.site.register(models.BuildingsCost, BuildingsCostAdmin)
admin.site.register(models.BuildingsCompleted, BuildingsCompletedAdmin)
