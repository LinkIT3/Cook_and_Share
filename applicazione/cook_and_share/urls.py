from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    
    path('admin/', admin.site.urls, name="admin_page"),
    
    path('', load_page, name="index"),
    
    path('#home', load_page, name="home"),
    path('#profile', load_page, name="profile"),
    path('#new-recipe', load_page, name="new_recipe"),
    
    re_path(r'^(?:.*/)?get_ingredients/$', get_ingredients, name="get_ingredients"),
    
    path('signup/', include("app.user.urls")),
    path('logout/', log_out, name='logout'),
    path('reload/', reload, name='reload'),

    path('select2/', include('django_select2.urls')),
    
    re_path(r'^(?:.*/)?get-recipes/$', getRecipes, name='get_recipes'),

    re_path(r'^(?:.*/)?load-recipe-card/$', load_recipe_card, name='load_recipe_card'),
    re_path(r'^(?:.*/)?load-user-card/$', load_user_card, name='load_user_card'),
    
    re_path(r'^(?:.*/)?toggle_liked/$', update_liked, name='toggle_liked'),
    re_path(r'^(?:.*/)?toggle_saved/$', update_saved, name='toggle_saved'),
    re_path(r'^(?:.*/)?toggle_follow/$', update_follow, name='toggle_follow'),
    
    path('remix_edit_recipe/<int:recipe_id>/', load_page, name="remix-edit-recipe"),
    
    re_path(r'^recipe/(?P<recipe_id>\d+)/.*$', load_recipe_page, name="recipe_page"),    
    
    re_path(r'^(?:.*/)?user/(?P<nickname>\w+)/.*$', user_page, name="user_page"),
]   

if settings.DEBUG:
        urlpatterns.append(path('set_admin/', set_admin, name='set_admin'))
        urlpatterns.append(path('new_ingredient/', new_ingredient, name='new_ingredient'))
        
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
