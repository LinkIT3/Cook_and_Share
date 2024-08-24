from django.urls import path
from .views import *

urlpatterns = [
    path("", signup, name="signup"),
    path('check_nickname/', check_nickname, name='check_nickname'),
    path("check_email/", check_email, name="check_email"),
]