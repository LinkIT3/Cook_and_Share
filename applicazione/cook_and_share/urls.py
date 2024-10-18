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
    path('signup/', include("app.user.urls")),
    path('logout/', log_out, name='logout'),
    path('reload/', reload, name='reload'),

    # path('settings/', settings_page, name='settings'),
    # re_path(r"^$|^/$|^home/$", home_page, name="homepage")    
    path('set_admin/', set_admin, name='set_admin'),
    path('select2/', include('django_select2.urls')),
    path('new_ingredient/', new_ingredient, name='new_ingredient'),
    
    path("recipes-page/", getRecipes, name='recipes_page'),
    path("<path:extra_path>/recipes-page/", getRecipes, name='recipes_page_exta_path'),
    path('load-recipe-template/', load_recipe_template, name='load_recipe_template'),
    path('<path:extra_path>/load-recipe-template/', load_recipe_template, name='load_recipe_template_extra_path'),
    path('toggle_liked/', update_liked, name='toggle_liked'),
    path('toggle_saved/', update_saved, name='toggle_saved'),
    path('remix_recipe/<int:remix_id>/', load_page, name="remix-recipe"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)