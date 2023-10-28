# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, BanIp


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'avatar', 'bio', 'password', 'groups', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'avatar', 'bio', 'password1', 'password2', 'is_staff')}
         ),
    )


admin.site.register(CustomUser, CustomUserAdmin)


class BanIpAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'status', 'time_unblock')
    search_fields = ('ip_address',)


admin.site.register(BanIp, BanIpAdmin)
