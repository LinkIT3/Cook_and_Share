from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from app.user.models import CustomUser

from app.user.signup_form import SignUpForm

class TestSignUp(TestCase):
    def test_post_request_valid(self):
        data = {
            'nickname': 'test',
            'email': 'test@test.com',
            'password': 'test',
            'password_confirm': 'test',
        }
        
        response = self.client.post(
            reverse('signup'), 
            data
        )
        
        self.assertRedirects(
            response, 
            reverse('home')
        )
        
        self.assertTrue(
            CustomUser.objects\
                .filter(nickname=data['nickname'])\
                .exists()
        )
        
        user = CustomUser.objects.get(nickname=data['nickname'])
        self.assertEqual(
            int(self.client.session['_auth_user_id']), 
            user.id
        )
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 
            'Registration completed'
        )
        self.assertEqual(
            str(messages[1]), 
            f"Welcome {user.nickname}!"
        )
    
    
    def test_post_request_invalid(self):
        data = {
            'nickname': 'test',
            'email': 'test@test.com',
            'password': 'test',
            'password_confirm': 'test1',
        }
        
        response = self.client.post(
            reverse('signup'), 
            data
        )
        
        self.assertEqual(
            response.status_code, 
            200
        )
        
        self.assertFalse(
            CustomUser.objects\
                .filter(nickname=data['nickname'])\
                .exists())
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]), 
            'Error during registration'
        )
    
    
    def test_get_request(self):
        response = self.client.get(reverse('signup'))
        
        self.assertEqual(
            response.status_code, 
            200
        )
        self.assertTemplateUsed(
            response, 
            'user/create_user.html'
        )
        
        self.assertIsInstance(
            response.context['form'], 
            SignUpForm
        )


class TestCheckNickname(TestCase):
    def test_nickname_not_exists(self):
        response = self.client.post(
            reverse('check_nickname'), 
            {'nickname': 'test',}
        )
        
        self.assertEqual(
            response.status_code, 
            200
        )
        self.assertEqual(
            response.content, 
            b'{"is_taken": false}'
        )
    
    
    def test_nickname_exists(self):
        user = CustomUser.objects.create_user(
            nickname='test',
            email='test@test.com',
            password='test'
        )
        user.save()
        
        response = self.client.post(
            reverse('check_nickname'), 
            {'nickname': 'test',}
        )
        
        self.assertEqual(
            response.status_code, 
            200
        )
        self.assertEqual(
            response.content, 
            b'{"is_taken": true}'
        )
    
    
    def test_nickname_get_request(self):
        response = self.client.get(
            reverse('check_nickname'), 
            {'nickname': 'test',}
        )
        
        self.assertEqual(
            response.status_code, 
            405
        )


class TestCheckEmail(TestCase):
    def test_email_not_exists(self):
        response = self.client.post(
            reverse('check_email'), 
            {'email': 'test@test.com',}
        )
        
        self.assertEqual(
            response.status_code, 
            200
        )
        self.assertEqual(
            response.content, 
            b'{"is_taken": false}'
        )
    
    
    def test_email_exists(self):
        user = CustomUser.objects.create_user(
            nickname='test',
            email='test@test.com',
            password='test'
        )
        user.save()
        
        response = self.client.post(
            reverse('check_email'), 
            {'email': 'test@test.com',}
        )
        
        self.assertEqual(
            response.status_code, 
            200
        )
        self.assertEqual(
            response.content, 
            b'{"is_taken": true}'
        )
    
    def test_email_get_request(self):
        response = self.client.get(
            reverse('check_email'),
            {'email': 'test@test.com',}
        )
        
        self.assertEqual(
            response.status_code, 
            405
        )