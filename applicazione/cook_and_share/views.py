from heapq import merge
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from app.user.models import CustomUser
from django.db.models import Count

import logging

from .login_form import LoginForm

logger = logging.getLogger(__name__)

def load_page(request):
    template = loader.get_template("index.html")
    homepage = "last"
    form = login_view(request)
    cont = {}
    if request.user.is_authenticated:
        homepage = "home"   
        number_of_recipes_created = CustomUser.objects.filter(pk=request.user.id).annotate(number_of_recipes=Count('recipes_created')).first()

        cont = {
            "nickname": request.user.nickname,
            "number_of_recipes": number_of_recipes_created.number_of_recipes, # type: ignore
        }
    
    context = {
        "homepage": homepage,
        "login_form": form,
        "profile_pic_setted": False,
        "profile_pic_path": "",
    }  
    context.update(cont)
    
    return render(request, 'index.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Benvenuto {user.get_username}!")
                return redirect('home')  # Modifica 'home' con il nome della tua vista
            else:
                messages.error(request, "Username o password non validi.")
        else:
            messages.error(request, "Username o password non validi.")
    else:
        form = LoginForm()
        
    return form

def log_out(request):
    logout(request)
    return redirect('home')