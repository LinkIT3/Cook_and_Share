from django.shortcuts import render, redirect
from .signup_form import SignUpForm
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
                messages.success(request, 'Registration compleated')
                # login(request, user)
                return redirect('home')
            
            else:
                messages.error(request, 'Error during registration')
        
        else:
            messages.error(request, 'Error during registration')
    
    else:
        form = SignUpForm()
    
    return render(request, "user/create_user.html", {'form': form})
    
    
    # context = {"form": SignUpForm()}
    # return render(request, "user/create_user.html", context)
    
    

def check_nickname(request):
    if request.method == "POST":
        nickname = request.POST.get('nickname', None)
        data = {
            'is_taken': CustomUser.objects.filter(nickname__iexact=nickname).exists()
        }
        return JsonResponse(data)
    
    return JsonResponse(None)

def check_email(request):
    if request.method == "POST":
        email = request.POST.get('email', None)
        data = {
            'is_taken': CustomUser.objects.filter(email__iexact=email).exists()
        }
        return JsonResponse(data)
    
    return JsonResponse(None)
