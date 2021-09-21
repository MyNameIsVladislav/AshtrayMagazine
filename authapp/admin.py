from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User, UserProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name',
                    'is_active', 'is_staff', 'date_joined']
    list_display_links = ('id', 'email')
    list_filter = ['first_name', 'last_name', 'email']
    search_fields = ['first_name', 'last_name', 'email']
    date_hierarchy = 'date_joined'
    ordering = ['first_name', 'last_name', 'is_active']


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'user', 'full_name', 'gender', 'region', 'age', 'phone')
    list_display_links = ('user', 'full_name')
    readonly_fields = ('user', 'get_image')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.avatar.url} width="60">')

    get_image.short_description = 'avatar'


admin.site.site_title = 'Ashtray Magazine'
admin.site.site_header = 'Ashtray Magazine'
