from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

User = get_user_model()
admin.site.unregister(Group)

ADDITIONAL_USER_FIELDS = (
    ('Игровой уровень', {'fields': ('fraction',)}),
)


@admin.register(User)
class MyUserAdmin(UserAdmin):

    list_display = ('pk', 'email', 'username', 'last_login', 'fraction')
    add_fieldsets = UserAdmin.add_fieldsets + ADDITIONAL_USER_FIELDS
    fieldsets = UserAdmin.fieldsets + ADDITIONAL_USER_FIELDS
