from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from eBirth_auth.models import User
from django import forms


# Register your User model with the custom UserAdmin


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'nin', 'pic', 'is_hospital', 'is_staff',
                    'is_superuser', 'date_joined', 'last_login', 'is_active')
    # You can search by both email and nin
    search_fields = ('email', 'nin')
    ordering = ()
    readonly_fields = ('date_joined', 'last_login',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('nin', 'pic')}),
        ('Permissions', {'fields': (
            'is_hospital', 'is_staff', 'is_superuser', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nin', 'password1', 'password2'),
        }),
    )


# Register your models here.
admin.site.register(User, UserAdmin)
