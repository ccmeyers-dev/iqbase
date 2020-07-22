from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Account
from .forms import RegistrationForm


class UserAdmin(BaseUserAdmin):
    add_form = RegistrationForm
    list_display = ('email','first_name','last_name','referrer','date_joined')
    list_filter = ('is_active','is_staff','is_admin','is_verified',)

    add_fieldsets = (
        ('Authenticate', {'fields': ('first_name','last_name','email','password1','passworld',)}),
        ('Permissions', {'fields': ('is_active','is_staff','is_admin','is_verified','is_setup')}),
    )

    fieldsets = (
        ('User Information', {'fields': ('first_name','last_name','email','referrer','password','passworld')}),
        ('Time Stamps', {'fields': ('last_login','date_joined')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_admin','is_verified','is_setup')}),
    )
    search_fields = ('first_name','last_name','email')
    ordering = ('-date_joined',)
    readonly_fields = ('last_login','date_joined')

    filter_horizontal = ()

admin.site.register(Account, UserAdmin)
admin.site.unregister(Group)