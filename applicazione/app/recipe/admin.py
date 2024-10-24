from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Recipe

class RecipeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Recipe fields', {'fields': ('title', 'description', 'text', 'ingredient', 'ingredient_quantity', 'dish_pic')}),
        ('Info', {'fields': ('author_link', 'original_recipe',)}),
    )

    def author_link(self, obj):
        author = obj.author.all()[0]
        if author:
            url = reverse('admin:user_customuser_change', args=[author.id]) 
            return format_html('<a href="{}">{}</a>', url, author.nickname)
        return "-"
    
    def author_name(self, obj):
        author = obj.author.all()[0]
        if author:
            return author.nickname
        return "-"
    
    author_link.short_description = 'Author'
    
    readonly_fields = ('author_link',)
    list_display = ['id', 'title', 'author_link', 'creation_date', 'last_edit_date']
    list_display_links = ('id', 'author_link',)
    ordering = ['id', 'title', 'creation_date', 'last_edit_date']
    
    
admin.site.register(Recipe, RecipeAdmin)
