from django.contrib import admin

from . import models


class FractionAdmin(admin.ModelAdmin):
    """Edit Fractions."""
    list_display = ('pk', 'name', 'slug', 'bonus', 'description')


class ResourcesAdmin(admin.ModelAdmin):
    """Edit Resources what user have."""
    list_display = (
        'user',
        'gold_amount',
        'wood_amount',
        'stone_amount',
        'updated_time'
    )
    list_filter = ("user__username",)
    search_fields = ("user__username",)
    list_editable = ('gold_amount', 'wood_amount', 'stone_amount')


class BuildingsAdmin(admin.ModelAdmin):
    """Edit valuables buildings."""
    list_display = ('id', 'name', 'type', 'fraction', 'description',)


class BuildingsTypeAdmin(admin.ModelAdmin):
    """Edit type of buildings."""
    list_display = (
        'id',
        'name',
        'order',
        'base_time',
        'base_gold',
        'base_wood',
        'base_stone'
    )


class UserBuildAdmin(admin.ModelAdmin):
    """Edit buildings wat user made."""
    list_display = (
        'user',
        'building',
        'level',
        'building_time',
        'gold',
        'wood',
        'stone',
        'slug'
    )
    list_filter = ("user__username",)
    search_fields = ("user__username",)
    list_editable = ('level', 'slug')


class BuildingInProcessAdmin(admin.ModelAdmin):
    """Edit buildings wat user made."""
    list_display = ('user', 'building', 'finish_date')
    search_fields = ("user__username",)


admin.site.register(models.Fraction, FractionAdmin)
admin.site.register(models.Resource, ResourcesAdmin)
admin.site.register(models.Building, BuildingsAdmin)
admin.site.register(models.BuildingType, BuildingsTypeAdmin)
admin.site.register(models.UserBuilding, UserBuildAdmin)
admin.site.register(models.BuildingRequirement)
admin.site.register(models.BuildingInProcess, BuildingInProcessAdmin)
