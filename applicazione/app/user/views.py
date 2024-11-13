from django.contrib import messages
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render, redirect

import logging

from .models import CustomUser
from .signup_form import SignUpForm


logger = logging.getLogger(__name__)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(
            request.POST or None, 
            request.FILES or None
        )
        
        if form.is_valid():
            user = form.save()
            
            if user:
                messages.success(
                    request, 
                    'Registration completed'
                )
                
                login(request, user)
                
                messages.success(
                    request, 
                    f"Welcome {user.nickname}!"
                )
                
                return redirect('home')
            else:
                messages.error(
                    request, 
                    'Error during registration'
                )
        else:
            messages.error(
                request, 
                'Error during registration'
            )
    else:
        form = SignUpForm()
    
    return render(
        request, 
        "user/create_user.html", 
        {'form': form}
    )


def check_nickname(request):
    if request.method == "POST":
        nickname = request.POST.get('nickname', None)
        data = {
            'is_taken': CustomUser.objects\
                .filter(nickname__iexact=nickname)\
                .exists()
        }
        
        return JsonResponse(data)
    
    return JsonResponse(
        {'error': 'Invalid request method'}, 
        status=405
    )


def check_email(request):
    if request.method == "POST":
        email = request.POST.get('email', None)
        data = {
            'is_taken': CustomUser.objects\
                .filter(email__iexact=email)\
                .exists()
        }
        
        return JsonResponse(data)
    
    return JsonResponse(
        {'error': 'Invalid request method'}, 
        status=405
    )
