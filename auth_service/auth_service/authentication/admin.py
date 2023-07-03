from django.contrib import admin
from . models import CustomUser
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_manager')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff')

admin.site.register(CustomUser, CustomUserAdmin)