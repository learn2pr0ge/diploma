from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'client_name', 'service_organization', 'management')


# Register your models here.
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('client_name', 'service_organization', 'management')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('client_name', 'service_organization', 'management')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)