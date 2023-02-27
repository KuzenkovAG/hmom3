from django.contrib import admin
from .models import Fractions


class FractionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'bonus', 'description', 'image')


admin.site.register(Fractions, FractionAdmin)
