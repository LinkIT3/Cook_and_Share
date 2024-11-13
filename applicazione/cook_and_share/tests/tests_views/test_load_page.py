from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from cook_and_share.forms.login_form import LoginForm
from cook_and_share.forms.settings_forms import *
from app.recipe.forms.new_recipe import NewRecipeForm

from app.user.models import CustomUser

import os

class TestLoadPage(TestCase):
    def test_user_not_authenticated(self):
        response = self.client.get(reverse('home'))
        
        self.assertEqual(
            response.status_code, 
            200
        )
        self.assertTemplateUsed(
            response, 
            'index.html'
        )
        
        self.assertIsInstance(
            response.context['login_form'], 
            LoginForm
        )
    
    
    def test_user_authenticated(self):
        user = CustomUser.objects.create_user(
            nickname='test_user',
            email='testuser@testuser.com',
            password='test_user'
        )
        user.save()
        
        self.client.login(
            username='testuser@testuser.com', 
            password='test_user'
        )
        
        response = self.client.get(reverse('home'))
        
        self.assertEqual(
            response.status_code, 
            200
        )
        self.assertTemplateUsed(
            response, 
            'index.html'
        )
        
        self.assertIsInstance(
            response.context['new_recipe_form'], 
            NewRecipeForm
        )
        
        self.assertIsInstance(
            response.context['profile_pic_form'], 
            ProfilePicForm
        )
        
        self.assertIsInstance(
            response.context['name_form'], 
            NameForm
        )
        
        self.assertIsInstance(
            response.context['password_form'], 
            PasswordForm
        )
    
    
    def test_login_form(self):
        user = CustomUser.objects.create_user(
            nickname='test_user',
            email='testuser@testuser.com',
            password='test_user'
        )
        
        response = self.client.post(
            reverse('home'),
            data={
                'username': 'testuser@testuser.com',
                'password': 'test_user'
            }
        )
        
        self.assertRedirects(
            response,
            reverse('home')
        )
        
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(
            str(messages[0]),
            f"Welcome {user.nickname}!"
        )
    
    
    def test_login_staff(self):
        user = CustomUser.objects.create_user(
            nickname='test_user',
            email='testuser@testuser.com',
            password='test_user',
            is_staff=True
        )
        user.save()
        
        response = self.client.post(
            reverse('home'),
            data={
                'username': 'testuser@testuser.com',
                'password': 'test_user'
            }
        )
        
        self.assertRedirects(
            response,
            reverse('admin:index')
        )