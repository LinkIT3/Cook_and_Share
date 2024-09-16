from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):    
    fieldsets = (
        ('Login credentials', {'fields': ('email', 'password')}),
        ('User info', {'fields': ('nickname', 'first_name', 'last_name', 'food_critic')}),
        ('Permission', {'fields': ('is_staff', 'is_superuser')}),
    )
    
    list_display = ['id', 'nickname', 'email', 'first_name', 'last_name', 'food_critic', 'is_staff']
    search_fields = ['id', 'nickname', 'email', 'first_name', 'last_name']
    list_filter = ['food_critic', 'is_staff']
    ordering = ['id', 'nickname'] 

admin.site.register(CustomUser, CustomUserAdmin)