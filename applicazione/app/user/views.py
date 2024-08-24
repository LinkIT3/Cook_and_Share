from django.shortcuts import render, redirect
from app.user.singup_form import SignUpForm
from django.contrib import messages
from django.http import JsonResponse
from .models import CustomUser

import logging

logger = logging.getLogger(__name__)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            if user:
                messages.success(request, 'Registration compeated')
                return redirect('home')
            
            else:
                messages.error(request, 'Error during registrtion')
        
        else:
            messages.error(request, 'Error during registrtion')
    
    else:
        form = SignUpForm()
    
    return render(request, "user/create_user.html", {'form': form})
    
    
    # context = {"form": SignUpForm()}
    # return render(request, "user/create_user.html", context)
    
    

def check_username(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        data = {
            'is_taken': CustomUser.objects.filter(username__iexact=username).exists()
        }
        return JsonResponse(data)

def check_email(request):
    if request.method == "POST":
        email = request.POST.get('email', None)
        data = {
            'is_taken': CustomUser.objects.filter(email__iexact=email).exists()
        }
        return JsonResponse(data)