from django.contrib import admin
# Register your models here.
from .models import User, UserProfile


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name',
                    'is_active', 'is_staff', 'date_joined']
    list_display_links = ('id', 'email')
    list_filter = ['first_name', 'last_name', 'email']
    search_fields = ['first_name', 'last_name', 'email']
    date_hierarchy = 'date_joined'
    ordering = ['first_name', 'last_name', 'is_active']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'gender', 'region', 'age', 'phone')


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, ProfileAdmin)
