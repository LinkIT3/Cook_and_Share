from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect

import logging

from app.user.models import CustomUser

from .forms.login_form import LoginForm
from .forms.settings_forms import *


logger = logging.getLogger(__name__)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {user.nickname}!") # type: ignore
                return redirect('home')
            else:
                messages.error(request, "Incorrect username or password")
        else:
            messages.error(request, "Incorrect username or password")
    else:
        form = LoginForm()
    
    return form


def load_page(request):
    homepage = "last"
    form = login_view(request)
    cont = {}
    pic_setted = False
    pic_path = "/media/default_profile_pic/default-profile-pic.webp"
    
    if request.user.is_authenticated:
        homepage = "home"   
        number_of_recipes_created = CustomUser.objects.filter(pk=request.user.id).annotate(number_of_recipes=Count('recipes_created')).first()
        
        if request.user.profile_pic != None:
            pic_setted = True
            pic_path = request.user.profile_pic.url
        
        cont = {
            "nickname": request.user.nickname,
            "number_of_recipes": number_of_recipes_created.number_of_recipes, # type: ignore
        }
    
    context = {
        "homepage": homepage,
        "login_form": form,
        "profile_pic_setted": pic_setted,
        "profile_pic_path": pic_path,
    }  
    context.update(cont)
    
    return render(request, 'index.html', context)


def log_out(request):
    logout(request)
    return redirect('home')


def profile_pic_form(request):
    if request.method == 'POST':
        if "profile-pic-form" in request.POST:
            form = ProfilePicForm(request.POST, instance=request.user)
            
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile picture is updated!')
            
            return form
    
    return ProfilePicForm(instance=request.user)


def name_form(request):
    if request.method == 'POST':
        if "name-form" in request.POST:
            form = NameForm(request.POST, instance=request.user)
            
            if form.is_valid():
                form.save()
                messages.success(request, 'Your name is updated!')
            
            return form
    
    return NameForm(instance=request.user)


@login_required
def settings_page(request):
    if request.method == 'POST':
        profile_pic_form = ProfilePicForm(request.POST, request.FILES, instance=request.user)
        name_form = NameForm(request.POST, instance=request.user)
        password_form = PasswordForm(data=request.POST, user=request.user)
        
        if "profile-pic-form" in request.POST and profile_pic_form.is_valid():
            profile_pic_form.save()
            messages.success(request, 'Your profile picture is updated!')
        
        if "name-form" in request.POST and name_form.is_valid():
            name_form.save()
            messages.success(request, 'Your name is updated!')
        
        if "password-form" in request.POST and password_form.is_valid():
            password_form.save()
            messages.success(request, 'Your password is updated!')
            return redirect("profile")
        
    else:
        profile_pic_form = ProfilePicForm()
        name_form = NameForm()
        password_form = PasswordForm(user=request.user)
    
    
    context = {
        "profile_pic_form": profile_pic_form,
        "name_form": name_form,
        "password_form": password_form,
    }
    
    return render(request, 'settings-page/settings.html', context)


def set_admin(request):
    request.user.is_staff = True
    request.user.save()
    
    return redirect("home")