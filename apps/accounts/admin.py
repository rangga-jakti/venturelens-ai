from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'full_name', 'plan', 'total_analyses', 'created_at', 'is_active']
    list_filter = ['plan', 'is_active', 'created_at']
    search_fields = ['email', 'full_name', 'username']
    ordering = ['-created_at']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('VentureLens', {
            'fields': ('full_name', 'plan', 'language', 'total_analyses', 'analyses_today')
        }),
    )
