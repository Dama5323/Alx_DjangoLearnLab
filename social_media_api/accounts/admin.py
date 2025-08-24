from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'bio', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'profile_picture', 'followers')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)