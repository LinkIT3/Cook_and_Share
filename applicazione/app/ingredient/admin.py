from django.contrib import admin

from .models import Ingredient

class IngredientAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Ingredient fields', {'fields': ('name',)}),
    )
    
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name']
    ordering = ['id', 'name']
    
admin.site.register(Ingredient, IngredientAdmin)