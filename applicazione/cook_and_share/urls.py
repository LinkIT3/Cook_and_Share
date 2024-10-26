from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from .views import *
from app.user.views import *

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls, name="admin_page"),
    path('', load_page, name="index"),
    path('#home', load_page, name="home"),
    path('#profile', load_page, name="profile"),
    path('#new-recipe', load_page, name="new_recipe"),
    path('get_ingredients/', get_ingredients, name="get_ingredients"),
    path('<path:extra_path>/get_ingredients/', get_ingredients, name="get_ingredients_extra_path"),

    path('signup/', include("app.user.urls")),
    path('logout/', log_out, name='logout'),
    path('reload/', reload, name='reload'),

    # path('settings/', settings_page, name='settings'),
    # re_path(r"^$|^/$|^home/$", home_page, name="homepage")    
    path('set_admin/', set_admin, name='set_admin'),
    path('select2/', include('django_select2.urls')),
    path('new_ingredient/', new_ingredient, name='new_ingredient'),
    
    path('get-recipes/', getRecipes, name='get-recipes'),
    path('<path:extra_path>/get-recipes/', getRecipes, name='get-recipes_exta_path'),
    
    path('load-recipe-card/', load_recipe_card, name='load_recipe_card'),
    path('<path:extra_path>/load-recipe-card/', load_recipe_card, name='load_recipe_card_extra_path'),
    path('toggle_liked/', update_liked, name='toggle_liked'),
    path('toggle_saved/', update_saved, name='toggle_saved'),
    path('remix_edit_recipe/<int:recipe_id>/', load_page, name="remix-edit-recipe"),
    
    path('recipe/<int:recipe_id>/', load_recipe_page, name="recipe_page"),
    path('recipe/<int:recipe_id>/<path:extra_path>', load_recipe_page, name="recipe_page_extra_path"),

    path('user/<str:nickname>/', user_page, name="user_page"),
    path('<path:extra_path>/user/<str:nickname>/', user_page, name="user_page_extra_path"),
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)