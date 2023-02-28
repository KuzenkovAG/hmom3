from django.contrib import admin
from .models import Fractions, Resources


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


admin.site.register(Fractions, FractionAdmin)
admin.site.register(Resources, ResourcesAdmin)
