from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import *
from app.user.views import *

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls, name="admin"),
    path('', load_page, name="home"),
    path('#profile', load_page, name="profile"),
    path('signup/', include("app.user.urls")),
    path('logout/', log_out, name='logout'),
    path('reload/', reload, name='reload'),

    # path('settings/', settings_page, name='settings'),
    # re_path(r"^$|^/$|^home/$", home_page, name="homepage")    
    path('set_admin/', set_admin, name='set_admin'),
    path('select2/', include('django_select2.urls')),
    path('new_ingredient/', new_ingredient, name='new_ingredient'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)