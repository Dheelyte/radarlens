from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, IpUser, SavedProduct
admin.site.site_header = "RadarLens Admin"
admin.site.site_title = "RadarLens Admin"
admin.site.index_title = "Welcome to the RadarLens Admin"



class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('name', 'email', 'is_active')
    list_filter = ('email', 'name', 'is_active')
    fieldsets = (
        (None, {'fields': ( 'name', 'email', 'password', 'image')}),
        ('Permissions', {'fields': ('email_is_verified', 'is_staff', 'is_active', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
        ('Groups and Permissions', {'fields': ('groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('name', 'email',)
    ordering = ('name', 'email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(IpUser)
admin.site.register(SavedProduct)
